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

from pathlib import Path
import json
class VersionManager():
    def __init__(self):
        self.program_dir=Path(__file__).resolve().parent.parent
        self.manifest_path=self.program_dir / "data" / "manifests" / "version_manifest.json"

    def check_manifest(self):
        if self.manifest_path.is_file():
            return True
        return False

    def load_manifest(self):
        with open (self.manifest_path,"r",encoding="utf-8") as mp:
            self.manifest=json.load(mp)
        
    def get_version(self,version):
        if self.check_manifest():
            self.load_manifest()
        else:
            raise FileNotFoundError("未找到manifest文件")
        for dic in self.manifest["versions"]:
            if dic["id"] == version:
                return dic
