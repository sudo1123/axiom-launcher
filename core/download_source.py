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

#注意，这只是一个抽象类，用于定义此后接入的下载源应提供的方法和属性，请勿调用此类
class DownloadSource:
    # 下载源显示名（供界面/CLI 展示）
    source_name = "未知下载源"
    def get_source_notice(self):
        raise NotImplementedError
    
    def get_asset_base_url(self):
        raise NotImplementedError