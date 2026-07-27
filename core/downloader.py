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
from urllib.request import urlopen
class Downloader():
    def __init__(self):
        pass
    def ensure_target_path(self,target_path):
        folder_path=Path(target_path).parent
        if folder_path.is_dir():
            return
        folder_path.mkdir(parents=True)
    
    def download(self,url,target_path):
        if Path(target_path).is_file(): #跳过重复下载
            return
        self.ensure_target_path(target_path)

        with urlopen(url) as response:
            data = response.read()

        with open(target_path, "wb") as file:
            file.write(data)
