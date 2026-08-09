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
from core.native_manager import NativeManager
from core.source_manager import SourceManager
from core.loaders.loader_manager import LoaderManager
from core.config_manager import ConfigManager


class MinecraftInstaller:

    def __init__(self):
        self.instance_manager = InstanceManager()
        self.version_manager = VersionManager()
        self.downloader = Downloader()
        self.version_parser = VersionParser()
        self.runtime_context = RuntimeContext().to_dict()
        self.library_manager = LibraryManager(self.runtime_context)
        self.asset_manager= AssetManager()
        self.native_manager = NativeManager()

    def download_libraries(self, artifacts, instance_path):
        download_source = SourceManager().get_download_source()
        threads = ConfigManager().get_library_threads()
        tasks = []
        for artifact in artifacts:
            target_path = instance_path / ".minecraft" / "libraries" / artifact["path"]
            tasks.append({
                "url": download_source.rewrite_url(artifact["url"]),
                "target_path": str(target_path),
                "sha1": artifact.get("sha1"),
            })
        result = self.downloader.download_many(tasks, sha1_enabled=True, show_progress=True,threads=threads)
        if result["failed"]:
            raise Exception(f"库文件下载失败，共 {len(result['failed'])} 个文件失败")

    def download_asset_objects(self, asset_index_path):
        objects_list = self.asset_manager.get_objects_list(
            asset_index_path, self.instance_path
        )
        threads = ConfigManager().get_asset_threads()
        tasks = [{
            "url": obj["url"],
            "target_path": str(obj["path"]),
            "sha1": obj["hash"],          # 注意字段名是 hash
        } for obj in objects_list]
        result = self.downloader.download_many(tasks, sha1_enabled=True, show_progress=True,threads=threads)
        if result["failed"]:
            raise Exception(f"资源文件下载失败，共 {len(result['failed'])} 个文件失败")

    def install(self, instance_id, version):
        download_source = SourceManager().get_download_source()
        print(f"开始安装 Minecraft {version}")
        print(f"目标实例: {instance_id}")
        print(download_source.get_source_notice())
        self.instance_manager.set_installation_status(instance_id,"installing") #修改实例安装状态

        # == 下载版本json ==
        print("[1/6] 下载版本json...")
        version_dic=self.version_manager.get_version(version)
        version_url=download_source.rewrite_url(version_dic["url"])
        self.instance_path=self.instance_manager.get_instance_path(instance_id)
        download_path=self.instance_path / ".minecraft" / "versions" / str(version) / f"{version}.json" 
        self.downloader.download(
            version_url, download_path,
            show_progress=True, silent_success=True,
            expected_sha1=version_dic.get("sha1")
        )
        print("下载版本json完毕")

        # == 下载客户端 ==
        print("[2/6] 下载客户端jar...")
        client_info=self.version_parser.get_client_info(download_path)
        client_url=download_source.rewrite_url(client_info["url"])
        download_path=self.instance_path / ".minecraft" / "versions" / str(version) / f"{version}.jar"
        self.downloader.download(
            client_url, download_path,
            show_progress=True, silent_success=True,
            expected_sha1=client_info.get("sha1")
        )
        print("下载客户端完毕")

        # == 下载普通库 ==
        print("[3/6] 下载依赖库...")
        self.version_json_path = self.instance_path / ".minecraft" / "versions" / str(version) / f"{version}.json"
        libraries=self.version_parser.get_libraries(self.version_json_path)       
        filtered_libraries=self.library_manager.filter_libraries(libraries)
        artifacts_list=self.library_manager.get_artifacts(filtered_libraries)
        self.download_libraries(
            artifacts_list,
            self.instance_path
        )
        print("依赖库下载完毕")
        # == 下载原生库 ==
        print("[4/6] 下载原生库...")
        native_libraries_list=self.library_manager.get_native_libraries(filtered_libraries, self.runtime_context["os_name"])
        if native_libraries_list != []:
            #覆盖url为镜像源
            for native in native_libraries_list:
                native["url"] = download_source.rewrite_url(native["url"])
            self.native_manager.install_extraction_natives(native_libraries_list, instance_id)
            print("原生库下载并解压完毕")
        else:
            print("已跳过下载原生库")
        # == 从版本json提取assetIndex ==
        asset_index_info=self.version_parser.get_asset_index(self.version_json_path)
        asset_index_url=download_source.rewrite_url(asset_index_info["url"])
        asset_index_id=asset_index_info["id"]
        asset_index_path=self.instance_path / ".minecraft" / "assets" / "indexes" / f"{asset_index_id}.json"
        # == 下载assetIndex文件 ==
        print("[5/6] 下载资源索引...")
        self.downloader.download(
            asset_index_url, asset_index_path,
            show_progress=True, silent_success=True,
            expected_sha1=asset_index_info.get("sha1")
        )
        print("资源索引下载完毕")
        # == 下载asset objects ==
        print("[6/6] 下载资源文件...")
        self.download_asset_objects(asset_index_path)
        print("\n资产下载完毕")
        print()

        # == 追加加载器专属步骤 ==
        print("追加加载器安装...")
        instance_config = self.instance_manager.load_instance(instance_id)
        loader_type = instance_config["loader"]["type"]
        loader_version = instance_config["loader"]["version"]

        loader = LoaderManager().get_loader(loader_type)
        loader.install_metadata(instance_id, version, loader_version)
        loader.install_libraries(instance_id, version, loader_version)
        print("加载器追加安装完毕")

        self.instance_manager.set_installation_status(instance_id,"installed") #修改实例安装状态
        print("安装完毕")