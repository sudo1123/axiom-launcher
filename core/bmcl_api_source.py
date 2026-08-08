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

    def get_manifest_url(self):
        bmcl_api_manifest="https://bmclapi2.bangbang93.com/mc/game/version_manifest_v2.json"
        return bmcl_api_manifest


    def rewrite_url(self, official_url):
        #官方CDN域名 → 镜像根，路径保留（版本json/客户端jar/assets index）
        mirror_root="https://bmclapi2.bangbang93.com"
        for official_prefix in (
            "https://piston-meta.mojang.com/",
            "https://piston-data.mojang.com/",
            "https://launchermeta.mojang.com/",
            "https://launcher.mojang.com/",
        ):
            if official_url.startswith(official_prefix):
                return mirror_root + "/" + official_url[len(official_prefix):]

        #依赖库 / fabric maven 库 → 镜像 /maven
        for official_prefix in ("https://libraries.minecraft.net/", "https://maven.fabricmc.net/"):
            if official_url.startswith(official_prefix):
                return mirror_root + "/maven/" + official_url[len(official_prefix):]

        #fabric meta → 镜像 /fabric-meta
        meta_prefix="https://meta.fabricmc.net/"
        if official_url.startswith(meta_prefix):
            return mirror_root + "/fabric-meta/" + official_url[len(meta_prefix):]

        return official_url
