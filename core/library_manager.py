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
import os
from core.rule_checker import RuleChecker
class LibraryManager:

    def __init__(self, runtime_context):
        self.rule_checker = RuleChecker(runtime_context)


    def filter_libraries(self, libraries):
        result=[]

        for library in libraries:

            if "rules" in library:
                if not self.rule_checker.check_rules(library["rules"]):
                    continue

            result.append(library)

        return result


    def get_artifacts(self, filtered_libraries):
        artifacts = []

        for library in filtered_libraries:
            if "downloads" in library:       #mojang格式
                downloads = library["downloads"]

                if "artifact" in downloads:
                    artifacts.append(downloads["artifact"])

            elif "name" in library and "url" in library: #fabric追加库(Maven格式)
                parse_result=self.parse_maven_library(library)
                artifacts.append(parse_result)

        return artifacts

    def get_native_libraries(self, filtered_libraries, os_name):
        result = []
        for library in filtered_libraries:
            downloads = library.get("downloads", {})
            classifiers = downloads.get("classifiers", {})
            if not classifiers:          # 新版本：natives jar 已是独立 artifact，跳过
                continue

            # 旧版本：classifiers 键名形如 natives-windows / natives-linux / natives-osx
            # 按当前 OS 映射到目标键名
            target_key = f"natives-{os_name}"   # os_name 为 windows/linux/osx
            if target_key in classifiers:
                obj = classifiers[target_key]
                result.append({
                    "url": obj["url"],
                    "name": library.get("name"),
                    "extract": library.get("extract",{}),   # 解压排除规则(部分库有)
                    "sha1" : obj.get("sha1")
                })
        return result

    def parse_maven_library(self, library):  #fabric追加库解析
        name=library["name"]
        url=library["url"]
        split_name=name.split(":")   #根据:符号将名称拆成三个部分group:artifact:version
        if len(split_name) != 3:
            raise ValueError("非法Maven坐标")
        group=split_name[0]
        file_name=f"{split_name[1]}-{split_name[2]}.jar"
        transferred_maven_head=group.replace(".","/")
        artifact_path=f"{transferred_maven_head}/{split_name[1]}/{split_name[2]}/{file_name}"
        artifact_url = url.rstrip("/") + "/" + artifact_path
        return {
            "path": artifact_path,
            "url": artifact_url,
            "sha1": library.get("sha1")
        }

