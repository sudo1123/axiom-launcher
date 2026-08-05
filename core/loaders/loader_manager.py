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

from core.loaders.fabric_loader import FabricLoader
from core.loaders.vanilla_loader import VanillaLoader
class LoaderManager:
    def __init__(self):
        pass

    def get_loader(self,loader_type):
        if loader_type == "vanilla":
            return VanillaLoader()

        if loader_type == "fabric":
            return FabricLoader()

        raise ValueError("未知加载器类型")