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
program_dir=Path(__file__).resolve().parent.parent
import json

class VersionParser():
    def __init__(self):
        pass

    def get_client_url(self,json_path):
        with open (json_path,"r",encoding="utf-8") as jp:
            version_json=json.load(jp)
        url = version_json["downloads"]["client"]["url"]
        return url
