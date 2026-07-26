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

class CLI():
    def __init__(self):
        self.instance_manager = InstanceManager()
        self.config_manager = ConfigManager()
        self.launcher = Launcher()

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
3. 返回

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

            if choice == "3":
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
                index = 1

                for item in result:
                    print(f"{index}. {item.name}")
                    index += 1

                print("")
                input("按ENTER回到上级菜单")

            elif choice == "2":
                self.create_instance()

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
                        return
                        
                    else:
                        continue

            elif choice == "2":
                self.instance_menu_loop()
