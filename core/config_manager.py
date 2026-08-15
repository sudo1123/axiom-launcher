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
from core.runtime_paths import get_program_dir
class ConfigManager():
    def __init__(self):
        self.PROGRAM_DIR = get_program_dir()
        self.config_file = self.PROGRAM_DIR / "configs" / "config.json"

    def load_config(self):
        path = Path(self.config_file)
        # 文件不存在，抛出错误
        if not path.exists():

            raise EnvironmentError("config加载失败，请检查配置文件")
        
        with open (path,"r", encoding="utf-8") as cf:
            return json.load(cf)

    
    def save_config(self, config):
        """
        保存config.json
        """

        with open(
            self.config_file,
            "w",
            encoding="utf-8"
        ) as cf:

            json.dump(
                config,
                cf,
                ensure_ascii=False,
                indent=4
            )

  


    def get_selected_instance(self):
        """
        获取当前选择的实例
        """
        config = self.load_config()
        selected_instance=config["minecraft"]["selected_instance"]

        return selected_instance



    def set_selected_instance(self, instance_id: str):
        """
        修改当前选择的实例
        """

        config = self.load_config()

        config["minecraft"]["selected_instance"] = instance_id

        self.save_config(config)

    def get_selected_download_source(self):
        """
        获取当前选择的下载源
        """
        config = self.load_config()
        selected_source=config["download"]["selected_source"]

        return selected_source
    
    
    
    def set_selected_download_source(self, source_name: str):
        """
        修改当前选择的下载源
        """

        config = self.load_config()

        config["download"]["selected_source"] = source_name

        self.save_config(config)

    def get_manifest_refresh_on_source_change(self):
        """
        获取"下载源变更时自动刷新版本清单"开关（默认开启）
        """
        config = self.load_config()
        download = config.setdefault("download", {})

        return download.get("manifest_refresh_on_source_change", True)

    def set_manifest_refresh_on_source_change(self, enabled: bool):
        """
        设置"下载源变更时自动刷新版本清单"开关
        """
        config = self.load_config()
        download = config.setdefault("download", {})

        download["manifest_refresh_on_source_change"] = bool(enabled)

        self.save_config(config)

    def get_library_threads(self):
        """获取依赖库下载并发数"""
        config = self.load_config()
        return config["download"]["library_threads"]

    def set_library_threads(self, threads: int):
        config = self.load_config()
        config["download"]["library_threads"] = int(threads)
        self.save_config(config)

    def get_asset_threads(self):
        """获取资源文件下载并发数"""
        config = self.load_config()
        return config["download"]["asset_threads"]

    def set_asset_threads(self, threads: int):
        config = self.load_config()
        config["download"]["asset_threads"] = int(threads)
        self.save_config(config)

    def get_java_source(self):
        """
        获取当前 Java 下载源（adoptium 官方 / tuna 清华镜像）
        """
        config = self.load_config()
        download = config.setdefault("download", {})

        return download.get("java_source", "adoptium")

    def set_java_source(self, source_name: str):
        """
        修改当前 Java 下载源
        """
        config = self.load_config()
        download = config.setdefault("download", {})

        download["java_source"] = source_name

        self.save_config(config)


