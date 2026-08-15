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
from accounts.manager import AccountManager
from core.instance_manager import InstanceManager
from core.launcher import Launcher
from core.config_manager import ConfigManager
from core.minecraft_installer import MinecraftInstaller
from core.loaders.loader_manager import LoaderManager
from core.runtime_paths import get_program_dir


class Commands:
    def __init__(self):
        self.instance_manager = InstanceManager()
        self.config_manager = ConfigManager()
        self.launcher = Launcher()
        self.minecraft_installer = MinecraftInstaller()
        self.loader_manager = LoaderManager()
        self.accounts_file = get_program_dir() / "configs" / "accounts.json"
        with open(self.accounts_file, "r", encoding="utf-8") as f:
            self.account_config = json.load(f)
        self.account_manager = AccountManager(self.account_config, str(self.accounts_file))

    # ---- 实例 ----
    def list_instances(self):
        result = self.instance_manager.list_instances()
        if not result:
            print("暂无实例")
            return
        header = f"{'ID':<20}{'版本':<12}{'类型':<10}{'安装状态':<14}Java路径"
        print(header)
        print("-" * 80)
        for item in result:
            cfg = self.instance_manager.load_instance(item.name)
            print(f"{cfg['id']:<20}{cfg['minecraft_version']:<12}"
                  f"{cfg['loader']['type']:<10}{cfg['installation_status']:<14}"
                  f"{cfg.get('java_path') or '-'}")

    def launch(self, instance_id, auto_download_java=False):
        try:
            self.instance_manager.load_instance(instance_id)
        except FileNotFoundError as e:
            print(f"启动失败: {e}")
            return
        self.config_manager.set_selected_instance(instance_id)
        self.launcher.start(auto_download_java=auto_download_java)

    def create_instance(self, instance_id, mc_version, instance_type, with_install=False):
        if not mc_version:
            print("错误：--create-instance 需要配合 --mc-version 指定版本")
            return
        try:
            self.instance_manager.create_instance(instance_id, mc_version, instance_type)
            print(f"实例创建成功: {instance_id}")
            if with_install:
                self.install(instance_id)
        except FileExistsError as e:
            print(f"创建失败: {e}")

    def install(self, instance_id):
        try:
            cfg = self.instance_manager.load_instance(instance_id)
        except FileNotFoundError as e:
            print(f"安装失败: {e}")
            return
        version = cfg["minecraft_version"]
        instance_type = cfg["loader"]["type"]
        if instance_type not in ("vanilla", "fabric"):
            print(f"暂不支持安装类型: {instance_type}")
            return
        try:
            if instance_type == "fabric":
                self._install_fabric_latest(instance_id, version)
            else:
                self.minecraft_installer.install(instance_id, version)
            print(f"实例安装完成: {instance_id}")
        except Exception as e:
            print(f"安装失败: {e}")

    def _install_fabric_latest(self, instance_id, version):
        """命令行模式：自动选用最新稳定版 loader，无交互"""
        loader = self.loader_manager.get_loader("fabric")
        available = loader.get_available_versions(version)
        if not available:
            print(f"未找到 {version} 可用的 Fabric loader 稳定版")
            return
        loader_version = available[0]   # 假定列表最新在前；如需最旧改用 available[-1]
        self.instance_manager.set_loader_version(instance_id, loader_version)
        self.minecraft_installer.install(instance_id, version)

    def delete_instance(self, instance_id):
        try:
            self.instance_manager.delete_instance(instance_id)
            print(f"实例已删除: {instance_id}")
        except FileNotFoundError as e:
            print(f"删除失败: {e}")

    # ---- 账号 ----
    def list_accounts(self):
        accounts = self.account_manager.list_accounts()
        if not accounts:
            print("暂无账号")
            return
        for acc in accounts:
            name = acc.get("player_name") if acc["type"] == "microsoft" else acc.get("username")
            selected = " [当前]" if acc["id"] == self.account_config["selected"] else ""
            print(f"- {acc['id']} ({acc['type']}) {name}{selected}")

    def add_offline_account(self, username):
        if not username.strip():
            print("用户名不能为空")
            return
        account_data = {"id": "offline_" + username, "type": "offline", "username": username}
        try:
            self.account_manager.add_account(account_data)
            self.account_manager.set_selected(account_data["id"])
            print(f"离线账号添加成功: {username}")
        except Exception as e:
            print(f"添加失败: {e}")

    def switch_account(self, account_id):
        try:
            self.account_manager.set_selected(account_id)
            print(f"切换成功: {account_id}")
        except Exception as e:
            print(f"切换失败: {e}")

    def delete_account(self, account_id):
        try:
            self.account_manager.remove_account(account_id)
            print(f"账号已删除: {account_id}")
        except Exception as e:
            print(f"删除失败: {e}")

    # ---- 设置 ----
    def set_download_source(self, source):
        self.config_manager.set_selected_download_source(source)
        print(f"下载源已切换: {source}")

    def set_library_threads(self, n):
        if n <= 0:
            print("并发数必须为正整数")
            return
        self.config_manager.set_library_threads(n)
        print(f"依赖库并发数已设置为: {n}")

    def set_asset_threads(self, n):
        if n <= 0:
            print("并发数必须为正整数")
            return
        self.config_manager.set_asset_threads(n)
        print(f"资源文件并发数已设置为: {n}")

    def set_manifest_refresh(self, val):
        self.config_manager.set_manifest_refresh_on_source_change(val == "on")
        print(f"下载源变更自动刷新已{'开启' if val == 'on' else '关闭'}")

    def set_java_source(self, source):
        self.config_manager.set_java_source(source)
        print(f"Java下载源已切换: {source}")

