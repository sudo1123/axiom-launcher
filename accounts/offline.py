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

from accounts.account import Account
import hashlib
import uuid
class OfflineAccount(Account):
    def __init__ (self,username):
        super().__init__()
        self.auth_player_name = username
        self.auth_uuid = self.generate_offline_uuid(username)
        self.auth_access_token ="offline"
        self.user_type = "legacy"

    def generate_offline_uuid(self, username):
        offline_account_prefix="OfflinePlayer:"
        offline_username=offline_account_prefix+username
        username_md5=hashlib.md5(offline_username.encode())
        username_md5_bytes=username_md5.digest()
        username_md5_bytearray=bytearray(username_md5_bytes)
        #写入version字段
        username_md5_bytearray[6]=username_md5_bytearray[6]  & 0b00001111   #将第六索引字节高四位清空
        username_md5_bytearray[6]= username_md5_bytearray[6] | 0b00110000   #将uuid版本号3写入高四位
        #写入variant字段 （RFC 4122）
        username_md5_bytearray[8]=username_md5_bytearray[8]  & 0b00111111   #清空第8索引字节最高两位
        username_md5_bytearray[8]=username_md5_bytearray[8]  | 0b10000000   #将10写入第8索引字节最高两位
        username_final_bytes=bytes(username_md5_bytearray)
        uuid_result=uuid.UUID(bytes=username_final_bytes)
        return uuid_result