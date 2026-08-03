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
class MojangSource(DownloadSource):
    source_name = "Mojang 官方源"

    def __init__(self):
        pass

    def get_source_notice(self):
        return "下载来源: Mojang 官方源 (https://www.minecraft.net)"

    def get_asset_base_url(self):
        asset_url_prefix="https://resources.download.minecraft.net"
        return asset_url_prefix

    def get_manifest_url(self):
        mojang_manifest="https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"
        return mojang_manifest