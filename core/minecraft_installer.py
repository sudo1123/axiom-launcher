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


class MinecraftInstaller:

    def __init__(self):
        self.instance_manager = InstanceManager()
        self.version_manager = VersionManager()
        self.downloader = Downloader()
        self.version_parser= VersionParser()


    def install(self, instance_id, version):
        print(f"开始安装 Minecraft {version}")
        print(f"目标实例: {instance_id}")
        # == 下载版本json ==
        version_dic=self.version_manager.get_version(version)
        version_url=version_dic["url"]
        instance_path=self.instance_manager.get_instance_path(instance_id)
        download_path=instance_path / ".minecraft" / "versions" / str(version) / f"{version}.json" 
        self.downloader.download(version_url,download_path)
        # == 下载客户端 ==
        client_url=self.version_parser.get_client_url(download_path)
        download_path=instance_path / ".minecraft" / "versions" / str(version) / f"{version}.jar"
        self.downloader.download(client_url,download_path)
        print("安装完毕")