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

from core.config_manager import ConfigManager
from core.mojang_source import MojangSource
from core.bmcl_api_source import BMCLAPISource
class SourceManager:
    # 受支持的下载源: key 为配置文件取值, value 为显示名
    SUPPORTED_SOURCES = {
        "mojang": "Mojang 官方源",
        "bmclapi": "BMCLAPI"
    }
    def __init__(self):
        self.config_manager=ConfigManager()
    def get_download_source(self):
        selected_download_source=self.config_manager.get_selected_download_source()
        if selected_download_source == "mojang":
            return MojangSource()
        if selected_download_source == "bmclapi":
            return BMCLAPISource()

        raise ValueError("未知的下载源")