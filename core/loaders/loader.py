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

# 注意，这只是一个抽象类，用于定义此后接入的加载器应提供的方法和属性，请勿调用此类

class Loader:

    # 加载器显示名称（供CLI/日志展示）
    loader_name = "未知加载器"


    def install_metadata(self,instance_id, minecraft_version, loader_version):
        """
        确保版本json就位，返回 launch_version
        """

        raise NotImplementedError


    def get_launch_version(self, minecraft_version, loader_version):
        """
        获取加载器对应的启动版本名称

        参数:
            minecraft_version:
                Minecraft版本

            loader_version:
                加载器版本

        返回:
            启动版本名称
        """
        raise NotImplementedError

    def install_libraries(self, instance_id, minecraft_version, loader_version):
        """下载加载器所用的追加库（不包含原版库）"""
        raise NotImplementedError

    def get_client_jar_version(self, minecraft_version, launch_version):
        """返回客户端 jar 的文件名（不含 .jar 后缀，如 1.20.1 或 forge-1.20.1-47.x）。

        原版/Fabric 没有独立客户端 jar，返回原版版本；
        Forge 等修改过客户端 jar 的加载器，返回自己的启动版本。
        """
        raise NotImplementedError

    def get_available_versions(self, minecraft_version):
        """获取指定 Minecraft 版本可用的 loader 稳定版列表"""
        raise NotImplementedError
        