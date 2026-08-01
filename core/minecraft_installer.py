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
        total = len(artifacts)
        skipped = 0
        for idx, artifact in enumerate(artifacts, 1):
            target_path = (
                instance_path
                / ".minecraft"
                / "libraries"
                / artifact["path"]
            )

            # 跳过已存在的文件
            if target_path.is_file():
                skipped += 1
                continue

            # 同一行刷新整体进度（\r 回到行首，不换行）
            print(f"\r  库文件进度: [{idx}/{total}]", end="")

            self.downloader.download(
                artifact["url"],
                target_path,
                show_progress=False,      # 不显示单文件进度，避免覆盖计数器
                silent_success=True       # 不打印"已成功下载"，避免刷屏
            )

        actual_downloaded = total - skipped
        print(f"\r  库文件下载完成! ({actual_downloaded} 个新文件, {skipped} 个已存在)")

    def download_asset_objects(self, asset_index_path):
        objects_list = self.asset_manager.get_objects_list(
            asset_index_path, self.instance_path
        )
        total = len(objects_list)
        skipped = 0

        for idx, asset_object in enumerate(objects_list, 1):
            if asset_object["path"].is_file():
                skipped += 1
                continue

            # 每3个文件刷新一次计数器
            if idx % 3 == 0 or idx == total:
                print(f"\r  资源文件进度: [{idx}/{total}]", end="")

            self.downloader.download(
                asset_object["url"],
                asset_object["path"],
                show_progress=False,
                silent_success=True
            )

        actual_downloaded = total - skipped
        print(f"\r  资源文件下载完成! ({actual_downloaded} 个新文件, {skipped} 个已存在)")


    def install(self, instance_id, version):
        print(f"开始安装 Minecraft {version}")
        print(f"目标实例: {instance_id}")
        print(self.asset_manager.download_source.get_source_notice())
        self.instance_manager.set_installation_status(instance_id,"installing") #修改实例安装状态

        # == 下载版本json ==
        print("[1/5] 下载版本json...")
        version_dic=self.version_manager.get_version(version)
        version_url=version_dic["url"]
        self.instance_path=self.instance_manager.get_instance_path(instance_id)
        download_path=self.instance_path / ".minecraft" / "versions" / str(version) / f"{version}.json" 
        self.downloader.download(
            version_url, download_path,
            show_progress=True, silent_success=True
        )
        print("下载版本json完毕")

        # == 下载客户端 ==
        print("[2/5] 下载客户端jar...")
        client_url=self.version_parser.get_client_url(download_path)
        download_path=self.instance_path / ".minecraft" / "versions" / str(version) / f"{version}.jar"
        self.downloader.download(
            client_url, download_path,
            show_progress=True, silent_success=True
        )
        print("下载客户端完毕")

        # == 下载普通库 ==
        print("[3/5] 下载依赖库...")
        self.version_json_path = self.instance_path / ".minecraft" / "versions" / str(version) / f"{version}.json"
        libraries=self.version_parser.get_libraries(self.version_json_path)       
        filtered_libraries=self.library_manager.filter_libraries(libraries)
        artifacts_list=self.library_manager.get_artifacts(filtered_libraries)
        self.download_libraries(
            artifacts_list,
            self.instance_path
        )
        print("依赖库下载完毕")
        # == 从版本json提取assetIndex ==
        asset_index_info=self.version_parser.get_asset_index(self.version_json_path)
        asset_index_url=asset_index_info["url"]
        asset_index_id=asset_index_info["id"]
        asset_index_path=self.instance_path / ".minecraft" / "assets" / "indexes" / f"{asset_index_id}.json"
        # == 下载assetIndex文件 ==
        print("[4/5] 下载资源索引...")
        self.downloader.download(
            asset_index_url, asset_index_path,
            show_progress=True, silent_success=True
        )
        print("资源索引下载完毕")
        # == 下载asset objects ==
        print("[5/5] 下载资源文件...")
        self.download_asset_objects(asset_index_path)
        print("\n资产下载完毕")
        print()
        self.instance_manager.set_installation_status(instance_id,"installed") #修改实例安装状态
        print("安装完毕")