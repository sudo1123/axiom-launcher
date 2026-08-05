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
import zipfile
from core.instance_manager import InstanceManager 
from core.downloader import Downloader
class NativeManager:
    def __init__(self):
        self.instance_manager=InstanceManager()
        self.downloader=Downloader()

    def install_extraction_natives(self,filtered_natives_list,instance_id):#注：过滤后的natives_list可以由library_manager内的get_native_libraries提供
        #总入口函数
        downloaded_native_libraries,native_dir_path=self.install_natives(filtered_natives_list,instance_id)
        self.extract_natives(native_dir_path,downloaded_native_libraries)
        #清理jar文件
        for file in native_dir_path.glob("*.jar"):   # 找出目录下所有 .jar 文件
            file.unlink()                            # 逐个删除


    def install_natives(self,filtered_natives_list,instance_id):
        version=self.instance_manager.load_instance(instance_id)["minecraft_version"]
        native_dir_path=Path(self.instance_manager.get_instance_path(instance_id)) /".minecraft" /"versions"/ str(version) / f"{version}-natives"
        (native_dir_path).mkdir(parents=True,exist_ok=True)#创建本地库文件夹
        downloaded_native_libraries=[]
        for natives in filtered_natives_list:   #循环提取每一个本地类项
            url=natives["url"]
            local_path= native_dir_path / Path(natives["url"]).name 
            self.downloader.download(url,local_path,silent_success=True,expected_sha1=natives.get("sha1"))
            downloaded_native_libraries.append(
                {
                "file_name":str(Path(natives["url"]).name),
                "local_path":local_path,
                "extract":natives.get("extract",{})
                }
                                                )
        return downloaded_native_libraries,native_dir_path
        

    def extract_natives(self,native_dir_path,downloaded_native_libraries):
        for native in downloaded_native_libraries:
            has_extract=False
            local_path=native["local_path"]
            if native.get("extract",{}) != {}:
                excludes=native["extract"]["exclude"]
                has_extract=True
            with zipfile.ZipFile(local_path) as zf:
                names=zf.namelist()
                for name in names:
                    not_excluded=True
                    if has_extract:                       #仅针对具有extract字段的库做解压检查
                        for exclude in excludes:
                            if name.startswith(exclude):   #条目名以exclude列表中列出的字符开头
                                not_excluded=False
                    if not_excluded:
                        zf.extract(name,native_dir_path)
                        