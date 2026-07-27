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

import platform


'''== 运行环境检测 =='''


class RuntimeContext:

    def __init__(self):

        self.os_name = self._get_platform()
        self.os_version = self._get_os_version()
        self.arch = self._get_arch()
        self.features = {}

    def _get_platform(self):

        system = platform.system()

        if system == "Windows":
            return "windows"

        if system == "Darwin":
            return "osx"

        if system == "Linux":
            return "linux"

        # 未知系统直接返回原值
        return system.lower()

    def _get_os_version(self):

        system = platform.system()

        if system == "Windows":
            return platform.version()

        if system == "Darwin":
            mac_ver = platform.mac_ver()[0]
            if mac_ver:
                return mac_ver
            return platform.release()

        # Linux / 其他
        return platform.release()

    def _get_arch(self):

        machine = platform.machine().lower()

        if machine in ("amd64", "x86_64", "x64"):
            return "x86_64"

        if machine in ("i386", "i486", "i586", "i686", "x86"):
            return "x86"

        if machine in ("arm64", "aarch64"):
            return "arm64"

        if machine in ("armv7l", "armv6l", "arm"):
            return "arm"

        # 兜底返回
        return machine

    def to_dict(self):

        return {
            "os_name": self.os_name,
            "os_version": self.os_version,
            "arch": self.arch,
            "features": self.features,
        }