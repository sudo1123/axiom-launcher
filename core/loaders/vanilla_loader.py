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

from core.loaders.loader import Loader
class VanillaLoader(Loader):
    loader_name = "vanilla"

    def install_metadata(self, instance_id, minecraft_version, loader_version):
        """
        确保版本json就位，返回 launch_version
        """
        return                 #原版安装逻辑完全由安装器完成

    def get_launch_version(self, minecraft_version, loader_version):
        return minecraft_version       #原版名称

    def install_libraries(self, instance_id, minecraft_version, loader_version):
        """原版没有追加库，此为策略模式的空实现占位"""
        return

    def get_client_jar_version(self, minecraft_version, launch_version):
        return minecraft_version       #原版使用原版客户端 jar

    def get_available_versions(self, minecraft_version):
        return                       #原版没有加载器版本
   
