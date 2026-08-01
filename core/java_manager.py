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
from pathlib import Path
import subprocess
import re
program_path=Path(__file__).resolve().parent.parent
class JavaManager:
    def __init__(self):
        self.instance_manager=InstanceManager()
        self.version_parser=VersionParser()

    def find_java(self,instance_id):
        instance_java_path=self.instance_manager.get_instance_java_path(instance_id)
        if instance_java_path != None:
            return instance_java_path
        else:
            return None


    def check_java(self,instance_id,java_path):
        #检查java版本是否符合实例启动要求
        instance_path=self.instance_manager.get_instance_path(instance_id)
        instance_version=self.instance_manager.load_instance(instance_id)["version"]
        instance_version_json_path=instance_path /".minecraft" /"versions"/f"{instance_version}"/f"{instance_version}.json"
        major_java_version=self.version_parser.get_major_version(instance_version_json_path)
        java_version=self.get_java_version(java_path)
        if int(java_version) == int(major_java_version): #传入的java路径对应的java版本和mojang官方要求一致
            return True , None
        else:
            return False , major_java_version 

        

    def get_java_version(self,java_path):
        result=subprocess.run ([java_path,"--version"],capture_output=True,text=True)
        if result.returncode == 0:
            version_info = result.stdout
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