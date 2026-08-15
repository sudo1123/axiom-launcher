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
from accounts.microsoft import MicrosoftAuthenticator
from core.instance_manager import InstanceManager
from core.launcher import Launcher
from core.config_manager import ConfigManager
from core.minecraft_installer import MinecraftInstaller
from core.source_manager import SourceManager
from core.loaders.loader_manager import LoaderManager

class CLI():
    def __init__(self):
        self.instance_manager = InstanceManager()
        self.config_manager = ConfigManager()
        self.launcher = Launcher()
        self.minecraft_installer = MinecraftInstaller()
        self.accounts_file = Path(__file__).resolve().parent.parent / "configs" / "accounts.json"
        with open(self.accounts_file, "r", encoding="utf-8") as f:
            self.account_config = json.load(f)
        self.account_manager = AccountManager(self.account_config, str(self.accounts_file))


    def main_menu(self):
        print(
        """
====================
Axiom Launcher
====================

1. 启动游戏
2. 实例管理
3. 设置
4. 账号管理
5. 退出

请输入:
""")
    def instance_menu(self):
        print("""
====================
实例管理
====================

1. 查看实例
2. 创建实例
3. 安装实例
4. 删除实例
5. 返回

请输入:
        """)

    def create_instance(self):
        print("""
====================
创建实例
====================
""")

        instance_id = input("请输入实例ID:\n>")

        version = input("请输入Minecraft版本:\n>")

        instance_type = input("请输入实例类型(vanilla/fabric):\n>")
        try:

            self.instance_manager.create_instance(
            instance_id,
            version,
            instance_type
            )
            if instance_type in ("vanilla", "fabric"):
                choice = input(
                    "是否安装Minecraft? (y/n)\n>"
                )

                if choice.lower() == "y":
                    try:
                        if instance_type == "fabric":
                            self.install_fabric(instance_id, version)
                        else:
                            self.minecraft_installer.install(
                                instance_id,
                                version
                            )
                    except Exception as e:
                        print(f"安装遇到问题: {e}")
                        return

            print(f'''
====================
实例创建成功
====================

ID:
{instance_id}

版本:
{version}

类型:
{instance_type}

            ''' )
            input("按ENTER返回")
        except FileExistsError as e:
            print(f"创建失败: {e}")
            input("按ENTER返回")


    def instance_menu_loop(self):
        while True:
            self.instance_menu()

            choice = input(">")

            if choice == "5":
                break

            elif choice == "1":
                result = self.instance_manager.list_instances()

                print(
    """
====================
实例管理 : 实例列表
====================
"""
                )

                if not result:
                    print("暂无实例")
                    input("按ENTER返回")
                    continue


                instance_name_dic = {}

                index = 1

                for item in result:
                    print(f"{index}. {item.name}")
                    instance_name_dic[str(index)] = item.name
                    index += 1


                choice = input("请选择实例:\n>")


                if choice in instance_name_dic:
                    self.show_instance(
                        instance_name_dic[choice]
                    )

            elif choice == "2":
                self.create_instance()

            elif choice == "3":
                self.install_instance()

            elif choice == "4":
                self.delete_instance()

    def install_instance(self):
        print("""
====================
安装实例
====================
        """)

        result = self.instance_manager.list_instances()

        if not result:
            print("暂无实例")
            input("按ENTER返回")
            return

        instance_name_dic = {}

        index = 1

        for item in result:
            print(f"{index}. {item.name}")
            instance_name_dic[str(index)] = item.name
            index += 1

        choice = input("请选择安装的实例:\n>")

        if choice not in instance_name_dic:
            print("选择无效")
            input("按ENTER返回")
            return

        instance_id = instance_name_dic[choice]

        instance_config = self.instance_manager.load_instance(instance_id)

        instance_type = instance_config["loader"]["type"]
        version = instance_config["minecraft_version"]

        if instance_type not in ("vanilla", "fabric"):
            print(
                f"暂不支持安装类型: {instance_type}"
            )
            input("按ENTER返回")
            return

        print(
    f"""
====================
开始安装
====================

实例:
{instance_id}

版本:
{version}

    """
        )

        try:
            if instance_type == "fabric":
                self.install_fabric(instance_id, version)
            else:
                self.minecraft_installer.install(
                    instance_id,
                    version
                )

            print(
    """
====================
安装完成
====================
    """
            )

        except Exception as e:
            print(
    f"""
====================
安装失败
====================

错误:
{e}

    """
            )

        input("按ENTER返回")

    def install_fabric(self, instance_id, version):
        """选择 Fabric loader 版本并安装（选版本→写回→统一install）"""
        loader = LoaderManager().get_loader("fabric")
        try:
            available = loader.get_available_versions(version)
        except Exception as e:
            print(f"获取 Fabric 版本列表失败: {e}")
            input("按ENTER返回")
            return

        if not available:
            print(f"未找到 {version} 可用的 Fabric loader 稳定版")
            input("按ENTER返回")
            return

        print("可用的 Fabric loader 版本:")
        for idx, lv in enumerate(available, 1):
            print(f"  {idx}. {lv}")

        choice = input("请选择 loader 版本:\n>")
        try:
            loader_version = available[int(choice) - 1]
        except (ValueError, IndexError):
            print("选择无效")
            input("按ENTER返回")
            return

        self.instance_manager.set_loader_version(instance_id, loader_version)
        self.minecraft_installer.install(instance_id, version)


    def show_instance(self, instance_id):
        instance_config = self.instance_manager.load_instance(instance_id)

        print(
f"""
====================
实例信息
====================

ID:
{instance_config["id"]}

Minecraft版本:
{instance_config["minecraft_version"]}

类型:
{instance_config["loader"]["type"]}

路径:
{self.instance_manager.instances_path / instance_id}

"""
        )

        input("按ENTER返回")

    def delete_instance(self):
        print("""
====================
删除实例
====================
    """)

        result = self.instance_manager.list_instances()

        if not result:
            print("暂无实例")
            input("按ENTER返回")
            return

        instance_name_dic = {}

        index = 1

        for item in result:
            print(f"{index}. {item.name}")
            instance_name_dic[str(index)] = item.name
            index += 1

        choice = input("请选择删除的实例:\n>")

        if choice not in instance_name_dic:
            print("选择无效")
            input("按ENTER返回")
            return

        instance_id = instance_name_dic[choice]

        confirm = input(
            f"确认删除 {instance_id} ? (y/n)\n>"
        )

        if confirm.lower() == "y":
            try:
                self.instance_manager.delete_instance(instance_id)
                print("删除成功")
            except FileNotFoundError as e:
                print(e)

        input("按ENTER返回")
    def settings_menu_loop(self):
        while True:
            print("""
====================
设置
====================

1. 查看当前下载源
2. 切换下载源
3. 切换"下载源变更时自动刷新版本列表"
4. 调整下载并发数
5. 返回

请输入:
            """)
            choice = input(">")

            if choice == "5":
                break
            elif choice == "1":
                self.show_download_source()
            elif choice == "2":
                self.change_download_source()
            elif choice == "3":
                self.toggle_manifest_refresh()
            elif choice == "4":
                self.adjust_threads()
    def adjust_threads(self):
        """调整依赖库/资源文件的下载并发数"""
        while True:
            lib = self.config_manager.get_library_threads()
            asset = self.config_manager.get_asset_threads()
            print(f"""
====================
调整下载并发数
====================

1. 依赖库并发: {lib}
2. 资源文件并发: {asset}
3. 返回

请输入:
            """)
            choice = input(">")
            if choice == "3":
                break
            elif choice in ("1", "2"):
                try:
                    value = int(input("请输入新的并发数:\n>"))
                except ValueError:
                    print("请输入数字")
                    continue
                if value <= 0:
                    print("并发数必须为正整数")
                    continue
                if choice == "1":
                    self.config_manager.set_library_threads(value)
                else:
                    self.config_manager.set_asset_threads(value)
                print("已保存")


    def show_download_source(self):
        selected = self.config_manager.get_selected_download_source()
        display_name = SourceManager.SUPPORTED_SOURCES.get(selected, selected)
        print(f"""
====================
当前下载源
====================

配置值: {selected}
显示名: {display_name}
""")
        input("按ENTER返回")

    def change_download_source(self):
        print("""
====================
切换下载源
====================
""")
        index = 1
        source_map = {}
        for key, display_name in SourceManager.SUPPORTED_SOURCES.items():
            print(f"{index}. {key} ({display_name})")
            source_map[str(index)] = key
            index += 1

        choice = input("请选择下载源:\n>")

        if choice in source_map:
            self.config_manager.set_selected_download_source(source_map[choice])
            print("下载源已切换")
        else:
            print("选择无效")

        input("按ENTER返回")

    def toggle_manifest_refresh(self):
        current = self.config_manager.get_manifest_refresh_on_source_change()
        status = "开启" if current else "关闭"
        print(f"""
====================
下载源变更时自动刷新版本列表
====================

当前状态: {status}
""")
        choice = input("切换状态? (y/n)\n>")
        if choice.lower() == "y":
            self.config_manager.set_manifest_refresh_on_source_change(not current)
            print("已切换")
        else:
            print("未修改")

        input("按ENTER返回")

    def launch_menu_loop(self):
        while True:
            result=self.instance_manager.list_instances()
            if not result:
                print("没有可用的实例，请先前往「实例管理」创建实例")
                input("按ENTER返回主菜单")
                return
            print("""
====================
启动游戏 : 实例列表
====================
                    """)
            print()
            index=1
            instance_name_dic={}
            for item in result:
                print(f"{str(index)}. {item.name}")
                instance_name_dic[str(index)]=item.name
                index+=1
            print("")
            print("请输入要启动的实例")
            print("0. 返回主菜单")
            choice=input(">")
            if choice == "0":
                break
            if choice in instance_name_dic.keys():
                self.config_manager.set_selected_instance(instance_name_dic[choice])
                print(
"""
====================
正在启动
====================
"""
)
                self.launcher.start()
                input("Minecraft已退出，按ENTER返回主菜单")
                break
                
            else:
                print("输入无效，请重新输入数字或按 0 返回")

    def account_menu_loop(self):
        while True:
            print("""
====================
账号管理
====================

1. 添加微软账号
2. 添加离线账号
3. 查看账号
4. 切换账号
5. 删除账号
6. 返回

请输入:
            """)
            choice = input(">")
            if choice == "6":
                break
            elif choice == "1":
                self.add_microsoft_account()
            elif choice == "2":
                self.add_offline_account()
            elif choice == "3":
                self.show_accounts()
            elif choice == "4":
                self.switch_account()
            elif choice == "5":
                self.delete_account()

    def add_microsoft_account(self):
        print("""
====================
添加微软账号
====================
""")
        authenticator = MicrosoftAuthenticator()
        try:
            init_info = authenticator.authenticate_1()
        except Exception as e:
            print(f"发起授权失败: {e}")
            input("按ENTER返回")
            return

        print(f"请访问: {init_info['verification_uri']}")
        print(f"并在页面输入代码: {init_info['user_code']}")
        print("等待授权...")

        try:
            account_data = authenticator.authenticate_2(
                init_info["device_code"], init_info["interval"]
            )
        except Exception as e:
            print(f"授权失败: {e}")
            input("按ENTER返回")
            return

        account_data["id"] = "ms_" + account_data["uuid"][:8]
        account_data["type"] = "microsoft"

        try:
            self.account_manager.add_account(account_data)
            self.account_manager.set_selected(account_data["id"])
            print(f"微软账号添加成功: {account_data['player_name']}")
        except Exception as e:
            print(f"保存账号失败: {e}")

        input("按ENTER返回")

    def add_offline_account(self):
        print("""
====================
添加离线账号
====================
""")
        username = input("请输入离线用户名:\n>")
        if not username.strip():
            print("用户名不能为空")
            input("按ENTER返回")
            return

        account_data = {
            "id": "offline_" + username,
            "type": "offline",
            "username": username,
        }
        try:
            self.account_manager.add_account(account_data)
            self.account_manager.set_selected(account_data["id"])
            print(f"离线账号添加成功: {username}")
        except Exception as e:
            print(f"保存账号失败: {e}")

        input("按ENTER返回")

    def show_accounts(self):
        print("""
====================
账号列表
====================
""")
        accounts = self.account_manager.list_accounts()
        if not accounts:
            print("暂无账号")
            input("按ENTER返回")
            return

        for acc in accounts:
            if acc["type"] == "microsoft":
                name = acc.get("player_name", "未知")
            else:
                name = acc.get("username", "未知")
            selected = " [当前]" if acc["id"] == self.account_config["selected"] else ""
            print(f"- {acc['id']} ({acc['type']}) {name}{selected}")

        input("按ENTER返回")

    def switch_account(self):
        print("""
====================
切换账号
====================
""")
        accounts = self.account_manager.list_accounts()
        if not accounts:
            print("暂无账号")
            input("按ENTER返回")
            return

        acc_map = {}
        for i, acc in enumerate(accounts, 1):
            if acc["type"] == "microsoft":
                name = acc.get("player_name", "未知")
            else:
                name = acc.get("username", "未知")
            print(f"{i}. {acc['id']} ({acc['type']}) {name}")
            acc_map[str(i)] = acc["id"]

        choice = input("请选择账号:\n>")
        if choice in acc_map:
            try:
                self.account_manager.set_selected(acc_map[choice])
                print("切换成功")
            except Exception as e:
                print(f"切换失败: {e}")
        else:
            print("选择无效")
        input("按ENTER返回")

    def delete_account(self):
        print("""
====================
删除账号
====================
""")
        accounts = self.account_manager.list_accounts()
        if not accounts:
            print("暂无账号")
            input("按ENTER返回")
            return

        acc_map = {}
        for i, acc in enumerate(accounts, 1):
            if acc["type"] == "microsoft":
                name = acc.get("player_name", "未知")
            else:
                name = acc.get("username", "未知")
            print(f"{i}. {acc['id']} ({acc['type']}) {name}")
            acc_map[str(i)] = acc["id"]

        choice = input("请选择要删除的账号:\n>")
        if choice not in acc_map:
            print("选择无效")
            input("按ENTER返回")
            return

        confirm = input(f"确认删除 {acc_map[choice]} ? (y/n)\n>")
        if confirm.lower() == "y":
            try:
                self.account_manager.remove_account(acc_map[choice])
                print("删除成功")
            except Exception as e:
                print(f"删除失败: {e}")
        input("按ENTER返回")



    def run(self):
        while True:
            self.main_menu()

            choice = input(">")

            if choice == "5":
                break

            elif choice == "1":
                self.launch_menu_loop()

            elif choice == "2":
                self.instance_menu_loop()
            elif choice == "3":
                self.settings_menu_loop()

            elif choice == "4":
                self.account_menu_loop()