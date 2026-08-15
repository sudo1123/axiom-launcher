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

import sys
from pathlib import Path


def get_program_dir() -> Path:
    """返回启动器可写的"程序目录"。

    - 编译模式（Nuitka/PyInstaller，sys.frozen 为真）：
      `__file__` 指向只读的临时/打包目录，不可持久化数据。
      这里返回 exe 所在目录（Path(sys.executable).parent），
      用于存放 configs/instances/data/runtime/launcher_logs 等运行时数据。
    - 源码模式：返回项目根目录（保持原有行为）。
    """
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent.parent
