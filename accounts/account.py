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

class Account:
    def __init__ (self):
        self.auth_player_name=None
        self.auth_uuid=None
        self.auth_access_token=None
        self.user_type=None
        self.auth_xuid = ""
        self.clientid = ""

        
    def get_auth_context(self):
        context={
    "auth_player_name": self.auth_player_name,
    "auth_uuid": str(self.auth_uuid),
    "auth_access_token": self.auth_access_token,
    "user_type": self.user_type,
    "auth_xuid": self.auth_xuid,
    "clientid": self.clientid

    }
        return context