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

from pathlib import Path 
import requests
import time

class Downloader():
    def __init__(self):
        self.headers = {
            "User-Agent": "Axiom Launcher/Launcher"
        }

    def ensure_target_path(self,target_path):
        folder_path=Path(target_path).parent
        if folder_path.is_dir():
            return
        folder_path.mkdir(parents=True)

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

         
    
    def download(self, url, target_path, max_retry=10, show_progress=False,silent_success=False):
        target_path = Path(target_path)

        if target_path.is_file(): #跳过重复文件
            return

        self.ensure_target_path(target_path)
        """将下载文件路径转换成临时路径（给文件加上临时文件后缀名）"""
        temp_path = target_path.parent / (
                    target_path.name + ".axiom_download_temp"
                )

        for attempt in range(max_retry): #重试机制

            try:
                response = requests.get(
                    url,
                    timeout=30,
                    headers=self.headers,
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

                temp_path.replace(target_path) #恢复正常文件名
                if show_progress:   #恢复自动换行
                    print()
                if not silent_success:
                    print("已成功下载")                           


                return

            except requests.RequestException as e:
                print(
                    f"\n下载失败 {attempt + 1}/{max_retry}: {url}\n 错误: {e},请耐心等待程序自动重试"
                )
                time.sleep(min(2 ** attempt, 30))                #失败后等待一定时间再重试(指数退避，最大30秒)

                if temp_path.exists():   #删除临时文件
                    temp_path.unlink()

                print("开始重试")

        raise Exception(
            f"下载失败，超过最大重试次数: {url}"
        )