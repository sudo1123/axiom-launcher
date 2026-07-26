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
from pathlib import Path
import json
import shutil

class InstanceManager():
    def __init__(self):
        program_path=Path(__file__).resolve().parent.parent
        self.instances_path=program_path / "instances"  #定位实例文件夹

    def check_validity_instance(self,instance_path):
        instance=Path(instance_path)
        if instance.is_dir():
            count=0
            for item in instance.iterdir(): 
                if item.name == "instance.json" and item.is_file():
                    count += 1

                if item.name == ".minecraft" and item.is_dir():
                    count += 1
                
            if count==2:
                return True
            else:
                return False
        else:
            return False


    def list_instances(self):
        instances=[]
        for item in self.instances_path.iterdir():
            if self.check_validity_instance(item):
                instances.append(item)

        return instances

    def load_instance(self,instance_id):
        result=self.list_instances()
        instance_exist=False
        current_instance_folder_path=None
        for item in result:
            if instance_id == item.name:
                instance_exist=True
                current_instance_folder_path=item
                break
        if instance_exist:
            instance_json_path=Path(current_instance_folder_path) / "instance.json"
            with open(instance_json_path,"r",encoding="utf-8") as ij :
                instance_json=json.load(ij)

            return instance_json
        raise FileNotFoundError("实例不存在")

    def create_instance(self,id,version,instance_type):
        result=self.list_instances()
        instance_exist=False
        for item in result:
            if id == item.name:
                instance_exist=True
                break
        if instance_exist:
            raise FileExistsError("同名实例已存在")
        instance_path=Path(self.instances_path) / id
        if instance_path.exists():
            raise FileExistsError("实例目录已存在")
        (instance_path).mkdir(parents=True)
        with open(instance_path / "instance.json","w",encoding="utf-8") as ij :
            content={"id":id,
                     "version":version,
                     "type":instance_type}
            json.dump(content,
                      ij,
                      ensure_ascii=False,
                      indent=4)
        minecraft_path = instance_path / ".minecraft"
        minecraft_path.mkdir()
        
    def delete_instance(self, instance_id):
        result = self.list_instances()

        instance_exist = False
        instance_path = None

        for item in result:
            if instance_id == item.name:
                instance_exist = True
                instance_path = item
                break

        if not instance_exist:
            raise FileNotFoundError("实例不存在")

        shutil.rmtree(instance_path)
