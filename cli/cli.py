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


from core.instance_manager import InstanceManager
from core.launcher import Launcher
from core.config_manager import ConfigManager
from core.minecraft_installer import MinecraftInstaller

class CLI():
    def __init__(self):
        self.instance_manager = InstanceManager()
        self.config_manager = ConfigManager()
        self.launcher = Launcher()
        self.minecraft_installer = MinecraftInstaller()

    def main_menu(self):
        print(
        """
====================
Axiom Launcher
====================

1. 启动游戏
2. 实例管理
3. 设置
4. 退出

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

        instance_type = input("请输入实例类型(vanilla/fabric/forge):\n>")
        try:

            self.instance_manager.create_instance(
            instance_id,
            version,
            instance_type
            )
            if instance_type == "vanilla":
                choice = input(
                    "是否安装Minecraft? (y/n)\n>"
                )

                if choice.lower() == "y":
                    try:
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

        instance_type = instance_config["type"]
        version = instance_config["version"]

        if instance_type != "vanilla":
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
{instance_config["version"]}

类型:
{instance_config["type"]}

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

    def run(self):
        while True:
            self.main_menu()

            choice = input(">")

            if choice == "4":
                break

            elif choice == "1":
                while True:
                    result=self.instance_manager.list_instances()
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
                    choice=input(">")
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
                        continue

            elif choice == "2":
                self.instance_menu_loop()
