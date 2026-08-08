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
from core.config_manager import ConfigManager
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
        self._write_source_marker()       # 记录manifest来自哪个下载源

    def _ensure_manifest(self):
        if not self.manifest_path.is_file():                 # 缺失 → 自动下载
            self.update_manifest()
            return
        if self._should_refresh_on_source_change():          # 切源后 → 自动刷新（受设置控制）
            self.update_manifest(force=True)
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
            
    def _source_marker_path(self):
        marker_path = self.manifest_path.with_suffix(self.manifest_path.suffix + ".source")
        return marker_path

    def _write_source_marker(self):
        source_key = ConfigManager().get_selected_download_source()
        self._source_marker_path().write_text(source_key, encoding="utf-8")

    def _read_source_marker(self):
        path = self._source_marker_path()
        if not path.exists():
            return None
        source_key = path.read_text(encoding="utf-8").strip()
        return source_key

    def _should_refresh_on_source_change(self):
        refresh_enabled = ConfigManager().get_manifest_refresh_on_source_change()
        if not refresh_enabled:             # 设置项关闭时不刷新
            return False
        current_source = ConfigManager().get_selected_download_source()
        marker_source = self._read_source_marker()
        if marker_source is None:           # 旧缓存无标记：补写当前源标记，避免无谓下载
            self._write_source_marker()
            return False
        return marker_source != current_source
