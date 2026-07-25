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

# == 文件默认内容 ==
'''== 配置文件默认内容 == '''

DEFAULT_CONFIG={
    "config_version": 1,

    "launcher": {
        "name": "Axiom Launcher",
        "version": "0.2.2"
    },

    "minecraft": {
        "directory": r"C:\path\to\.minecraft",
        "selected_version": "version_number"
    },

    "java": {
        "path": r"C:\path\to\java.exe",
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
    }
}

DEFAULT_LAUNCH_CONTEXT = {
    "is_demo_user": False,

    "has_custom_resolution": False,

    "has_quick_plays_support": False,

    "is_quick_play_singleplayer": False,

    "is_quick_play_multiplayer": False,

    "is_quick_play_realms": False
}

DEFAULT_ACCOUNTS={
    "accounts": [
        {
            "id": "offline_default",
            "type": "offline",
            "username": "Steve"
        }
    ],

    "selected": "offline_default"
}