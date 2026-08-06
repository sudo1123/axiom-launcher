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

import json
from pathlib import Path
from accounts.offline import OfflineAccount 
from accounts.microsoft import MicrosoftAccount

class AccountManager:

    def __init__(self, account_config, accounts_file=None):
        self.account_config = account_config
        self.accounts_file = accounts_file   # accounts.json 路径，用于保存



    def get_selected_account(self):

        selected_account_id = self.account_config["selected"]

        for account in self.account_config["accounts"]:

            if account["id"] == selected_account_id:

                if account["type"] == "offline":

                    return OfflineAccount(
                        account
                    )
                elif account["type"] == "microsoft":

                    return MicrosoftAccount(
                        account
                    )

        return None

    def save(self):
        """把当前 account_config 写回 accounts.json"""
        if not self.accounts_file:
            raise ValueError("未指定 accounts_file 路径，无法保存")
        with open(self.accounts_file, "w", encoding="utf-8") as f:
            json.dump(self.account_config, f, ensure_ascii=False, indent=4)

    def list_accounts(self):
        """返回所有账号条目列表"""
        return self.account_config["accounts"]

    def get_account(self, account_id):
        """按 id 查找账号条目，找不到返回 None"""
        for account in self.account_config["accounts"]:
            if account["id"] == account_id:
                return account
        return None

    def add_account(self, account_data):
        """新增账号条目并保存"""
        if self.get_account(account_data["id"]) is not None:
            raise ValueError(f"账号 id 已存在: {account_data['id']}")
        self.account_config["accounts"].append(account_data)
        self.save()

    def set_selected(self, account_id):
        """切换选中账号并保存"""
        if self.get_account(account_id) is None:
            raise ValueError(f"账号不存在: {account_id}")
        self.account_config["selected"] = account_id
        self.save()

    def remove_account(self, account_id):
        """删除账号条目并保存"""
        original_len = len(self.account_config["accounts"])
        self.account_config["accounts"] = [
            acc for acc in self.account_config["accounts"]
            if acc["id"] != account_id
        ]
        if len(self.account_config["accounts"]) == original_len:
            raise ValueError(f"账号不存在: {account_id}")
        # 若删除的是当前选中账号，重置 selected 为空
        if self.account_config["selected"] == account_id:
            self.account_config["selected"] = ""
        self.save()

