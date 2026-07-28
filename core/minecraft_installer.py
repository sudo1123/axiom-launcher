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

from core.downloader import Downloader
from core.version_manager import VersionManager
from core.instance_manager import InstanceManager
from core.version_parser import VersionParser
from core.runtime_context import RuntimeContext
from core.library_manager import LibraryManager
from core.asset_manager import AssetManager


class MinecraftInstaller:

    def __init__(self):
        self.instance_manager = InstanceManager()
        self.version_manager = VersionManager()
        self.downloader = Downloader()
        self.version_parser = VersionParser()
        runtime_context = RuntimeContext().to_dict()
        self.library_manager = LibraryManager(runtime_context)
        self.asset_manager= AssetManager()

    def download_libraries(self, artifacts, instance_path):

        for artifact in artifacts:

            target_path = (
                instance_path
                / ".minecraft"
                / "libraries"
                / artifact["path"]
            )

            self.downloader.download(
                artifact["url"],
                target_path
            )

    def download_asset_objects(self,asset_index_path):
        objects_list=self.asset_manager.get_objects_list(asset_index_path,self.instance_path)
        for asset_object in objects_list:
            self.downloader.download(asset_object["url"],asset_object["path"])


    def install(self, instance_id, version):
        print(f"开始安装 Minecraft {version}")
        print(f"目标实例: {instance_id}")
        self.instance_manager.set_installation_status(instance_id,"installing") #修改实例安装状态

        # == 下载版本json ==
        print("开始下载版本json")
        version_dic=self.version_manager.get_version(version)
        version_url=version_dic["url"]
        self.instance_path=self.instance_manager.get_instance_path(instance_id)
        download_path=self.instance_path / ".minecraft" / "versions" / str(version) / f"{version}.json" 
        self.downloader.download(version_url,download_path)
        print("下载版本json完毕")
        # == 下载客户端 ==
        print("开始下载客户端")
        client_url=self.version_parser.get_client_url(download_path)
        download_path=self.instance_path / ".minecraft" / "versions" / str(version) / f"{version}.jar"
        self.downloader.download(client_url,download_path)
        print("下载客户端完毕")
        # == 下载普通库 ==
        print("开始下载普通库")
        self.version_json_path = self.instance_path / ".minecraft" / "versions" / str(version) / f"{version}.json"
        libraries=self.version_parser.get_libraries(self.version_json_path)       
        filtered_libraries=self.library_manager.filter_libraries(libraries)
        artifacts_list=self.library_manager.get_artifacts(filtered_libraries)
        self.download_libraries(
            artifacts_list,
            self.instance_path
        )
        print("普通库下载完毕")
        # == 从版本json提取assetIndex ==
        asset_index_info=self.version_parser.get_asset_index(self.version_json_path)
        asset_index_url=asset_index_info["url"]
        asset_index_id=asset_index_info["id"]
        asset_index_path=self.instance_path / ".minecraft" / "assets" / "indexes" / f"{asset_index_id}.json"
        # == 下载assetIndex文件 ==
        self.downloader.download(
            asset_index_url,
            asset_index_path)
        # == 下载asset objects ==
        print("开始下载资产（“用时可能会比较久，请耐心等待”）")
        self.download_asset_objects(asset_index_path)
        print("资产下载完毕")

        self.instance_manager.set_installation_status(instance_id,"installed") #修改实例安装状态
        print("安装完毕")