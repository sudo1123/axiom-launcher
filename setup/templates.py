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

import tomllib
from pathlib import Path
from core.runtime_paths import get_program_dir

def get_launcher_version():
    try:
        pyproject_path = get_program_dir() / "pyproject.toml"
        with open(pyproject_path, "rb") as f:
            return tomllib.load(f)["project"]["version"]
    except Exception:
        return "0.0.0"

VERSION=get_launcher_version()

'''== 配置文件默认内容 == '''
TEMPLATES={
"config.json":{
    "config_version": 6,

    "launcher": {
        "name": "Axiom Launcher",
        "version": VERSION
    },

    "minecraft": {
        "selected_instance": ""
    },

    "java": {
        "memory": {
            "min": 1024,
            "max": 4096
        }
    },

    "game": {
        "resolution": {
            "width": 854,
            "height": 480
        },
        "fullscreen": "false"
            },

    "download":{
        "selected_source":"mojang",
        "manifest_refresh_on_source_change": True,
        "library_threads": 12,
        "asset_threads": 32
        }

    }
,

"launch_context.json":{
    "is_demo_user": False,

    "has_custom_resolution": False,

    "has_quick_plays_support": False,

    "is_quick_play_singleplayer": False,

    "is_quick_play_multiplayer": False,

    "is_quick_play_realms": False
},

"accounts.json":{
    "accounts": [
        {
            "id": "offline_default",
            "type": "offline",
            "username": "Steve"
        }
    ],

    "selected": "offline_default"
}
}