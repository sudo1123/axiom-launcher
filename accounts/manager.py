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

from accounts.offline import OfflineAccount 

class AccountManager:

    def __init__(self, account_config):
        self.account_config = account_config


    def get_selected_account(self):

        selected_account_id = self.account_config["selected"]

        for account in self.account_config["accounts"]:

            if account["id"] == selected_account_id:

                if account["type"] == "offline":

                    return OfflineAccount(
                        account["username"]
                    )

        return None
