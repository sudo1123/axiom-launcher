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
                while True:
                    self.instance_menu()
                    choice = input(">")
                    if choice == "3":
                        break
                    if choice == "1":
                        result=self.instance_manager.list_instances()
                        print("""
====================
实例管理 : 实例列表
====================
                                """)
                        print()
                        index=1
                        for item in result:
                            print(f"{str(index)}. {item.name}")
                            index+=1
                        print("")
                        input("按ENTER回到上级菜单")


test=CLI()
test.run()