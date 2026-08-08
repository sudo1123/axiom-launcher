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

import json
import requests
from core.loaders.loader import Loader
from core.downloader import Downloader
from core.instance_manager import InstanceManager
from core.library_manager import LibraryManager
from core.runtime_context import RuntimeContext
from core.source_manager import SourceManager

class FabricLoader(Loader):
    loader_name = "fabric"
    FABRIC_META_BASE = "https://meta.fabricmc.net/v2/versions/loader"
    def __init__(self):
        self.downloader = Downloader()
        self.instance_manager = InstanceManager()
        self.runtime_context = RuntimeContext().to_dict()
        self.library_manager = LibraryManager(self.runtime_context)


    def get_available_versions(self, minecraft_version):
        """获取指定 Minecraft 版本可用的 Fabric loader 稳定版列表"""
        url = f"{self.FABRIC_META_BASE}/{minecraft_version}"
        response = requests.get(url, timeout=30, headers=self.downloader.headers)
        response.raise_for_status()
        versions = []
        for entry in response.json():
            loader_info = entry.get("loader", {})
            version = loader_info.get("version")
            stable = loader_info.get("stable", False)
            if version and stable:
                versions.append(version)
        return versions



    def install_metadata(self, instance_id, minecraft_version, loader_version):
        """
        下载loader对应的version json，返回launch_version
        """

        launch_version = self.get_launch_version(
            minecraft_version,
            loader_version
        )

        instance_path = self.instance_manager.get_instance_path(instance_id)

        version_path = (
            instance_path
            / ".minecraft"
            / "versions"
            / launch_version
        )

        json_path = version_path / f"{launch_version}.json"

        fabric_metadata_url = (
            f"https://meta.fabricmc.net/v2/versions/loader/"
            f"{minecraft_version}/{loader_version}/profile/json"
        )

        self.downloader.download(
            fabric_metadata_url,
            json_path,
            show_progress=True,
            silent_success=True
        )

        return launch_version

    def install_libraries(self, instance_id, minecraft_version, loader_version):
        """下载 Fabric 追加库（Maven 格式）到实例 libraries 目录"""
        launch_version = self.get_launch_version(minecraft_version, loader_version)
        instance_path = self.instance_manager.get_instance_path(instance_id)

        version_json_path = (
            instance_path
            / ".minecraft"
            / "versions"
            / launch_version
            / f"{launch_version}.json"
        )
        with open(version_json_path, "r", encoding="utf-8") as f:
            version_json = json.load(f)

        libraries = version_json.get("libraries", [])
        filtered_libraries = self.library_manager.filter_libraries(libraries)
        artifacts = self.library_manager.get_artifacts(filtered_libraries)

        total = len(artifacts)
        download_source = SourceManager().get_download_source()
        for idx, artifact in enumerate(artifacts, 1):
            target_path = instance_path / ".minecraft" / "libraries" / artifact["path"]
            print(f"\r  Fabric库进度: [{idx}/{total}]", end="")
            self.downloader.download(
                download_source.rewrite_url(artifact["url"]),
                target_path,
                silent_success=True,
                expected_sha1=artifact.get("sha1")
            )
        print(f"\r  Fabric 库下载完成! 共 {total} 个文件")

            
            

    def get_launch_version(self, minecraft_version, loader_version):
        launch_version=f"fabric-loader-{loader_version}-{minecraft_version}"
        return launch_version

    def get_client_jar_version(self, minecraft_version, launch_version):
        return minecraft_version       #Fabric 无独立 jar，使用原版客户端 jar

