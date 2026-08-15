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
from core.runtime_paths import get_program_dir
program_dir=get_program_dir()
import json

class VersionParser():
    def __init__(self):
        pass

    def get_client_url(self,json_path):
        with open (json_path,"r",encoding="utf-8") as jp:
            version_json=json.load(jp)
        url = version_json["downloads"]["client"]["url"]
        return url

    def get_client_info(self,json_path):
        with open (json_path,"r",encoding="utf-8") as jp:
            version_json=json.load(jp)
        client = version_json["downloads"]["client"]
        return client

    def get_libraries(self,json_path):
        with open (json_path,"r",encoding="utf-8") as jp:
            version_json=json.load(jp)
        libraries=version_json["libraries"]
        return libraries

    def get_asset_index(self,json_path):
        with open (json_path,"r",encoding="utf-8") as jp:
            version_json=json.load(jp)
        asset_index=version_json["assetIndex"]
        return asset_index
    
    def get_major_version(self,json_path):
        with open (json_path,"r",encoding="utf-8") as jp:
            version_json=json.load(jp)
        major_version=version_json.get("javaVersion", {}).get("majorVersion", 8)#如果版本json缺失javaVersion字段，自动使用Java8，修复1.6.1启动失败
        return  major_version