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
from core.download_source import DownloadSource
class BMCLAPISource(DownloadSource):
    source_name = "BMCLAPI"
    def __init__(self):
        pass

    def get_source_notice(self):
        return "下载来源: BMCLAPI 镜像源 (https://bmclapi2.bangbang93.com)"

    def get_asset_base_url(self):
        asset_url_prefix="https://bmclapi2.bangbang93.com/assets"
        return asset_url_prefix