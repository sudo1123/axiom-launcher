# Axiom Launcher - a third-party Minecraft: Java Edition launcher
# Copyright (C) 2026  Felix Qu
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
from pathlib import Path 
import hashlib
import requests
import requests.adapters
import time

class SHAMismatchError(Exception):  #自定义SHA1校验失败异常
    pass

class Downloader():
    def __init__(self):
        self.session=requests.Session()
        self.session.headers.update({
            "User-Agent": "Axiom Launcher/Launcher"
        })
        adapter=requests.adapters.HTTPAdapter(pool_connections=128,   #缓存的"不同主机"连接池数量
                                            pool_maxsize=128,       #单个主机的连接池最大连接数
                                            max_retries=0)
        self.session.mount("https://",adapter)
        self.session.mount("http://",adapter)

    def ensure_target_path(self,target_path):
        folder_path=Path(target_path).parent
        if folder_path.is_dir():
            return
        folder_path.mkdir(parents=True,exist_ok=True)

    def calculate_sha1(self,path):
        path=Path(path)
        with open(path,"rb") as p:
            hasher = hashlib.sha1()
            while True:
                chunk = p.read(65536)
                if not chunk:  #chunk是空字节（文件已完全读完）
                    break
                hasher.update(chunk)

        result = hasher.hexdigest()
        return result

    def show_progress(self,downloaded_size,total_size,last_refresh,refresh_interval):
        if time.time() - last_refresh >= refresh_interval:
            if total_size == 0: #服务器没有返回文件总大小
                print(f"{downloaded_size} bytes")
                return time.time()
            percentage= round((downloaded_size / total_size)*100 ,2)
            # end=""参数使终端打印完不换行，\r回车符使光标回到开头，两者结合实现反复刷新同一行避免刷屏 
            print(f"\r{downloaded_size} bytes / {total_size} bytes ({percentage} %)",end="")
            return time.time()
        else:  #没到刷新间隔
            return last_refresh

         
    
    def download(self, url, target_path, max_retry=10, show_progress=False,silent_success=False,expected_sha1=None,show_retry_message=True):
        target_path = Path(target_path)

        if target_path.is_file(): #跳过重复文件
            if expected_sha1:  #启用了SHA1校验
                if self.calculate_sha1(target_path) == expected_sha1:
                    return
                else:   #存在此文件但是SHA1校验不通过
                    target_path.unlink(missing_ok=True)   #强制删除损坏文件,继续下载
            else:              #未启用校验，存在即跳过
                return

        self.ensure_target_path(target_path)
        """将下载文件路径转换成临时路径（给文件加上临时文件后缀名）"""
        temp_path = target_path.parent / (
                    target_path.name + ".axiom_download_temp"
                )

        for attempt in range(max_retry): #重试机制

            try:
                response = self.session.get(
                    url,
                    timeout=30,
                    stream=True             #启用流式传输
                )

                response.raise_for_status() #抛出网络错误
                total_size = int(
                        response.headers.get("content-length", 0)
                    )
                if show_progress:
                    last_refresh=0
                
                with open(temp_path, "wb") as file:
                    #流式下载并写入文件
                    downloaded_size=0
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:            #返回的不是空数据
                            file.write(chunk)
                        downloaded_size += len(chunk)
                        if show_progress:
                            last_refresh=self.show_progress(downloaded_size,total_size,last_refresh,0.5) #间隔500ms刷新

                if expected_sha1:            #启用了sha1校验
                    local_sha1=self.calculate_sha1(temp_path)
                    if local_sha1 != expected_sha1:    #校验不通过
                        raise SHAMismatchError(f"SHA1校验失败,url: {url},期望SHA1: {expected_sha1}, 实际SHA1: {local_sha1}")
                        #抛出异常中断替换，开始重试

                temp_path.replace(target_path) #恢复正常文件名
                if show_progress:   #恢复自动换行
                    print()
                if not silent_success:
                    print("已成功下载")                           


                return

            except SHAMismatchError as e:         #捕获匹配失败异常
                if show_retry_message:
                    print(
                        f"\n下载失败 {attempt + 1}/{max_retry}: {url}\n 错误: {e},请耐心等待程序自动重试"
                    )
                time.sleep(min(2 ** attempt, 30))                #失败后等待一定时间再重试(指数退避，最大30秒)
                temp_path.unlink(missing_ok=True)#删除临时文件
                if show_retry_message:
                    print("开始重试")  

            except requests.RequestException as e:
                if show_retry_message:
                    print(
                        f"\n下载失败 {attempt + 1}/{max_retry}: {url}\n 错误: {e},请耐心等待程序自动重试"
                    )
                time.sleep(min(2 ** attempt, 30))                #失败后等待一定时间再重试(指数退避，最大30秒)

                temp_path.unlink(missing_ok=True)                                           #删除临时文件
                if show_retry_message:
                    print("开始重试")


        raise Exception(
            f"下载失败，超过最大重试次数: {url}"
        )

    def download_many(self,tasks:list,sha1_enabled:bool,max_retry:int=10,threads:int=8,show_progress=False):
        """
        多线程下载器
        tasks:存储所有要下载对象信息的list，结构
        [{"url":str ,"target_path":str,sha1:str},{...},{...}]
        max_retry:单个下载任务的最大重试次数(默认为10)
        threads: 线程并发数(默认为8)
        sha1_enabled:是否全局启用sha1校验，设置为false则全局禁用，设置为true则将校验所有有sha1字段的对象，如没有或者为空则自动跳过校验
        返回: {"failed": [异常对象, ...]}
        """
        completed=0
        total=len(tasks)
        failed=0
        failures=[]
        with ThreadPoolExecutor(max_workers=threads) as executor:
            last_refresh=None
            futures=[]
            for task in tasks:
                #关闭单线程的所有输出，避免引发IO冲突
                future=executor.submit(self.download,
                                url=task["url"],
                                target_path=task["target_path"],
                                expected_sha1=task.get("sha1",None) if sha1_enabled else None,
                                max_retry=max_retry,
                                show_progress=False,
                                silent_success=True,
                                show_retry_message=False)
                futures.append(future)

            for future in as_completed(futures):
                completed+=1
                try:
                    result=future.result()
                except Exception as e:
                    failures.append(e)
                    failed+=1
                if show_progress:
                    if last_refresh==None or time.time() - last_refresh >= 0.5:
                        print(f"\r 当前下载任务共{total}个，已完成{completed}(失败:{failed})",end="")
                        last_refresh=time.time()
        print()
        return {"failed":failures}
                