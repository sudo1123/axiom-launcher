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

from core.instance_manager import InstanceManager
from core.version_parser import VersionParser
from core.runtime_context import RuntimeContext
from core.java_downloader import JavaDownloader

import os
from pathlib import Path
import subprocess
import re
class JavaManager:
    def __init__(self):
        self.instance_manager=InstanceManager()
        self.version_parser=VersionParser()
        self.java_downloader=JavaDownloader()
        
    def get_instance_java_version(self,instance_id):
        instance_path=self.instance_manager.get_instance_path(instance_id)
        instance_version=self.instance_manager.load_instance(instance_id)["minecraft_version"]

        version_json=(
            instance_path
            / ".minecraft"
            / "versions"
            / instance_version
            / f"{instance_version}.json"
        )

        return self.version_parser.get_major_version(version_json)

    def find_java(self,instance_id):
        instance_java_path=self.instance_manager.get_instance_java_path(instance_id)
        #优先使用实例中记录的Java
        if instance_java_path != None:
            ok,version=self.check_java(instance_id,instance_java_path)
            if ok:
                return instance_java_path              #使用实例java
            
        #搜索系统Java
        javas=[]
        javas.extend(self.find_path_java())
        javas.extend(self.find_system_java())
        javas=list(set(javas))  #去重

        #检查候选Java
        for java_path in javas:       #注：如果javas == []（为空），循环将直接跳过
            ok,version=self.check_java(instance_id,java_path)
            if ok:
                self.instance_manager.update_instance_java_path(instance_id,java_path)
                return java_path
        #失败
        required_java_version=self.get_instance_java_version(instance_id)  
        print(f"当前实例需要使用Java {required_java_version},请先下载Java")
        raise ValueError(f"未找到符合要求的Java")


    def check_java(self,instance_id,java_path):
        #检查java版本是否符合实例启动要求
        major_java_version=self.get_instance_java_version(instance_id)
        try:
            java_version=self.get_java_version(java_path)
        except (ValueError,FileNotFoundError):           #捕获版本获取模块的异常和系统的文件异常
            return False, major_java_version
        if int(java_version) == int(major_java_version): #传入的java路径对应的java版本和mojang官方要求一致
            return True , None
        else:
            return False , major_java_version 

        

    def get_java_version(self,java_path):
        result=subprocess.run ([java_path,"-version"],  #注意：这里不使用--version是为了兼容java8
                               capture_output=True,
                               text=True,
                               timeout=5)
        if result.returncode == 0:
            version_info = result.stdout + result.stderr
            match = re.search(r"\d+\.\d+", version_info)   #正则匹配数字.数字的字段
            if match:
                if match.group() != "1.8":                      
                    java_version=int(match.group().split(".")[0])    #取出主版本号

                else:                                        #Java8特殊格式特殊处理
                    java_version=8
                return java_version
            else:
                raise ValueError("Java版本信息异常")
        else:
            raise ValueError("Java版本查询失败")

    def find_path_java(self):  #在PATH环境变量查找Java
        java_paths_in_path=[]
        paths = os.environ["PATH"].split(os.pathsep)
        paths=set(paths)  #去重
        for p in paths:
            path=Path(p)
            if not path.exists():
                continue
            try:
                files_and_dirs=Path(p).iterdir()
            except PermissionError:
                continue
            for item in files_and_dirs:
                if item.is_file():
                    if item.name == "java.exe" or item.name == "java":
                        java_paths_in_path.append(item)
        return java_paths_in_path

    def find_system_java(self): #在系统常见安装位置查找Java
        java_paths=[]

        search_dirs=[
            Path(r"C:\Program Files\Common Files\Oracle\Java\javapath"),
            Path(r"C:\Program Files\Java"),
            Path(r"C:\Program Files\Eclipse Adoptium"),
            Path(r"C:\Program Files\Microsoft"),
        ]

        for directory in search_dirs:
            if not directory.exists():
                continue

            for item in directory.rglob("java.exe"):
                java_paths.append(item)

        return java_paths

    def download_java_for_instance(self,instance_id):
            feature_version = self.get_instance_java_version(instance_id)
    
            rt = RuntimeContext()
            program_dir = Path(__file__).resolve().parent.parent  
            target_dir = program_dir / "runtime" / "java" / f"{feature_version}-{rt.os_name}-{rt.arch}"
    
            # 下载并解压，得到 java 可执行文件路径
            java_exe = self.java_downloader.install(feature_version, target_dir)
    
            # 将路径写回实例
            self.instance_manager.update_instance_java_path(instance_id, java_exe)
            return java_exe