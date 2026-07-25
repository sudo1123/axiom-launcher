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
from .templates import TEMPLATES  #注意：！！templates前面有点代表在当前文件所在目录下搜索！！
program_path=Path(__file__).resolve().parent.parent

def create_dir():

    directories = [
        "configs",
        "instances",
        "launcher_logs",
        "data"
    ]

    for directory in directories:
        (program_path / directory).mkdir(
            parents=True,
            exist_ok=True
        )

def create_configs_files():
    files=[
          "accounts.json",
           "config.json",
           "launch_context.json"
        ]
    for file in files:
        file_path=(program_path / "configs" / file)
        if file_path.exists():            #文件已存在
            continue        
        else:                             #文件不存在
            with file_path.open("w", encoding="utf-8") as f:
                json.dump(
                    TEMPLATES[file],
                    f,
                    indent=4,
                    ensure_ascii=False
                )

def initialize():
    print("Initializing Axiom Launcher...")
    create_dir()
    print("[OK] Directories created")
    create_configs_files()
    print("[OK] Config files created")

    print("Setup complete.")