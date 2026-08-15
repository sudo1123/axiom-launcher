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
import requests
import zipfile
import tarfile
import glob
from pathlib import Path
from core.config_manager import ConfigManager
from core.runtime_context import RuntimeContext
from core.downloader import Downloader
class JavaDownloader:
    def __init__(self, runtime_context=None, downloader=None):
        # 缺省自行加载
        self.runtime_context = runtime_context or RuntimeContext()
        self.downloader = downloader or Downloader()
        #映射Adoptium API所需的系统和架构方言
        self.os_map = {"windows": "windows", "linux": "linux", "osx": "mac"}
        self.arch_map = {"x86_64": "x64", "x86": "x86", "arm64": "aarch64", "arm": "arm"}
        self.java_source = ConfigManager().get_java_source()

    def install(self, feature_version, target_dir):
        #入口方法
        package_link = self.resolve_java_url(feature_version)
        return self.download_java(feature_version, package_link, target_dir)

    def resolve_java_url(self,feature_version,local_image_type="jdk"):
        os_name = self.os_map[self.runtime_context.os_name]
        local_arch = self.arch_map[self.runtime_context.arch]
        adoptium_api_meta_request=(
        f"https://api.adoptium.net/v3/assets/latest/"
        f"{feature_version}/hotspot?os={os_name}&architecture={local_arch}&"
        f"image_type={local_image_type}&vendor=eclipse&jvm_impl=hotspot"
        )
                                            
        headers={'User-Agent':"Axiom Launcher/Launcher"}

        response=requests.get(adoptium_api_meta_request,
                              headers=headers,
                              timeout=30)
        response.raise_for_status()
        assets=response.json()
        for asset in assets:
            try:
                major=asset["version"]["major"]
                os=asset["binary"]["os"]
                arch=asset["binary"]["architecture"]
                image_type=asset["binary"]["image_type"]
            except Exception as e:
                print(f"获取的元数据列表异常: {e}")
                continue
            if (major==feature_version and
                os == os_name            and
                arch == local_arch       and
                image_type == local_image_type):
                if self.java_source == "tuna":
                    # 清华 TUNA 镜像：按镜像目录结构拼接（字段与 API 返回一致）
                    package_name = asset["binary"]["package"]["name"]
                    mirror_root = "https://mirrors.tuna.tsinghua.edu.cn/Adoptium"
                    return f"{mirror_root}/{major}/{image_type}/{arch}/{os}/{package_name}"
                #adoptium官方源路径
                package_link=asset["binary"]["package"]["link"]
                return package_link

        raise ValueError(f"未找到 Java {feature_version} 的 {local_image_type} 下载地址")

    def download_java(self,feature_version, package_link, target_dir):
        existing = self._find_java_executable(target_dir)
        if existing is not None:  #已存在java可执行文件
            return existing
        zip_path=target_dir / f"java-{feature_version}.zip"
        self.downloader.download(package_link, zip_path, show_progress=True, silent_success=True)
        self.extract_java(zip_path,target_dir)
        return self._find_java_executable(target_dir)

    def extract_java(self,archive_path,target_dir):
        if self.runtime_context.os_name == "windows":
            with zipfile.ZipFile(archive_path) as zf:
                zf.extractall(target_dir)

        else:
            with tarfile.open(archive_path) as tf:
                tf.extractall(target_dir)      

    def _find_java_executable(self, target_dir):
        name = "java.exe" if self.runtime_context.os_name == "windows" else "java"
        matches = glob.glob(str(target_dir / "**" / "bin" / name), recursive=True)
        if not matches:
            return None          # 找不到返回 None
        return Path(matches[0]) 