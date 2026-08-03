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
import time
from core.downloader import Downloader
from core.source_manager import SourceManager
from pathlib import Path
import json
class VersionManager():
    def __init__(self):
        self.downloader = Downloader()
        self.program_dir=Path(__file__).resolve().parent.parent
        self.manifest_path=self.program_dir / "data" / "manifests" / "version_manifest.json"

    REFRESH_INTERVAL_SECONDS = 86400   # 24 小时后自动刷新manifests文件

    def update_manifest(self, force=False):
        url = SourceManager().get_download_source().get_manifest_url()
        if force and self.manifest_path.exists():
            self.manifest_path.unlink()   # 强制刷新前删旧文件，绕过 downloader 的"已存在即跳过"逻辑
        self.downloader.download(url, self.manifest_path, show_progress=True, silent_success=True)

    def _ensure_manifest(self):
        if not self.manifest_path.is_file():                 # 缺失 → 自动下载
            self.update_manifest()
            return
        age = time.time() - self.manifest_path.stat().st_mtime
        if age > self.REFRESH_INTERVAL_SECONDS:              # 过期 → 自动刷新
            self.update_manifest(force=True)

    def check_manifest(self):
        if self.manifest_path.is_file():
            return True
        return False

    def load_manifest(self):
        with open (self.manifest_path,"r",encoding="utf-8") as mp:
            self.manifest=json.load(mp)
        
    def get_version(self,version):
        self._ensure_manifest()
        self.load_manifest()
        for dic in self.manifest["versions"]:
            if dic["id"] == version:
                return dic
