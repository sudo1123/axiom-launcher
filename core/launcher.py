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

import accounts.offline
import accounts.manager
from pathlib import Path
from core.instance_manager import InstanceManager
from core.runtime_context import RuntimeContext
from core.config_manager import ConfigManager
from core.library_manager import LibraryManager
from core.rule_checker import RuleChecker
from core.java_manager import JavaManager
import json
import subprocess
import os

'''== 配置加载 =='''

def _safe_json_load(path, file_label=""):
    """通用 JSON 文件读取，文件不存在时抛出异常"""
    path = Path(path)
    if not path.exists():
        raise EnvironmentError(f"{file_label}加载失败，请检查配置文件：{path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def launch_context_load(path):
    return _safe_json_load(path, "launch_context")

def account_load(path):
    return _safe_json_load(path, "account")

'''== JAVA环境检查 == 已迁移至 core.java_manager.JavaManager =='''

'''== Minecraft完整性检查 =='''

def minecraft_validity_check(config):
    minecraft_directory_path = config["minecraft"]["directory"]
    dicpath = Path(minecraft_directory_path)

    if dicpath.is_dir():
        versions_dir = dicpath / "versions"

        if versions_dir.is_dir():
            version_dic = versions_dir / config["minecraft"]["selected_version"]

            if version_dic.is_dir():
                version_json_file = version_dic / f'{config["minecraft"]["selected_version"]}.json'
                version_jar_file = version_dic / f'{config["minecraft"]["selected_version"]}.jar'

                if version_json_file.is_file() and version_jar_file.is_file():
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
        return False

'''==  version读取  =='''
def version_json_load(config):
    minecraft_directory_path = config["minecraft"]["directory"]
    dicpath = Path(minecraft_directory_path)
    version_path= dicpath / "versions" / config["minecraft"]["selected_version"]
    file_path = version_path / f'{config["minecraft"]["selected_version"]}.json'
    with open(file_path,"r") as vj:
        version_json=json.load(vj)
    return version_json

'''==  系统环境 =='''
# 系统环境检测已迁移至 core.runtime_context.RuntimeContext，当前函数为封装，用于兼容旧代码
def get_platform():
    return RuntimeContext().os_name

def get_arch():
    return RuntimeContext().arch

def runtime_context_load():
    """返回与 RuleChecker 兼容的运行时上下文字典"""
    rt = RuntimeContext()
    return rt.to_dict()
    # 现在返回: {"os_name": ..., "os_version": ..., "arch": ..., "features": {}}

'''=== libraries解析 ==='''
def library_paths_load(config, libraries):
    """根据已过滤的 libraries 列表构建库文件路径"""
    paths = []
    prefix = Path(config["minecraft"]["directory"]) / "libraries"
    for element in libraries:
        if "downloads" in element and "artifact" in element["downloads"]:
            paths.append(prefix / Path(element["downloads"]["artifact"]["path"]))
    return paths

def check_libraries_exist(libraries_paths):
    missing_paths=[]
    for path in libraries_paths:
        if path.is_file():
            pass
        else:
            missing_paths.append(path)
    if len(missing_paths) != 0:
        return False, missing_paths
    else:
        return True, None

def get_minecraft_jar_path(config):
    prefix=Path(config["minecraft"]["directory"])
    mc_version=config["minecraft"]["selected_version"]
    tail=Path(f"versions/{mc_version}/{mc_version}.jar")
    full_path= prefix / tail
    return full_path

def classpath_build(libraries_paths,mc_jar_path):
    path_list=libraries_paths.copy()
    path_list.append(mc_jar_path)    
    return path_list
def classpath_list_to_string(classpath_list):
    classpath_string=""
    for path in classpath_list:
        classpath_string += str(path)
        classpath_string += os.pathsep
    return classpath_string

'''==  arguments解析 =='''
def arguments_load(version_json,key:str):
    return version_json["arguments"][key]

# game_rules_check 已迁移至 core.rule_checker.RuleChecker
# jvm_rules_check 已迁移至 core.rule_checker.RuleChecker
    

def arguments_parse(arguments, rule_checker):
    result_list=[]
    for element in arguments:
        if isinstance(element,str):
            result_list.append(element)
        elif isinstance(element,dict):
            rules=element.get("rules")
            if not rules or rule_checker.check_rules(rules):
                value=element.get("value")
                if isinstance(value,str):
                    result_list.append(value)
                elif isinstance(value,list):
                    result_list.extend(value)
    return result_list

def argument_context_load(config, version_json, classpath_string ,auth_context):

    template= {

        "auth_player_name":"",

        "version_name":config["minecraft"]["selected_version"],

        "game_directory":config["minecraft"]["directory"],

        "assets_root":str(
            Path(config["minecraft"]["directory"])
            /
            "assets"
        ),

        "assets_index_name":
            version_json["assetIndex"]["id"],


        "auth_uuid":"",
        "auth_access_token":"",
        "clientid":"",
        "auth_xuid":"",

        "user_type":"legacy",

        "version_type":"release",

        "classpath":classpath_string,


        "launcher_name":
            config["launcher"]["name"],

        "launcher_version":
            config["launcher"]["version"]
    }
    template.update(auth_context) #使用账号系统生成的信息更新模板字典的值
    return template

def arguments_replace(arguments, context):

    result=[]

    for argument in arguments:

        if isinstance(argument,str):

            for key,value in context.items():

                argument=argument.replace(
                    "${"+key+"}",
                    str(value)
                )

            result.append(argument)

    return result


'''=== 启动参数构建和最终启动 ==='''
def build_launch_command(
    java_path,
    jvm_arguments,
    mainclass,
    game_arguments
):

    command=[]

    command.append(java_path)

    command.extend(jvm_arguments)

    command.append(mainclass)

    command.extend(game_arguments)

    return command

def launch_minecraft(command):

    process=subprocess.run(
        command
    )

    return process



class Launcher:

    def __init__(self):
        self.instance_manager = InstanceManager()
        self.config_manager = ConfigManager()
        self.java_manager = JavaManager()

    def start(self):
        #配置文件加载
        self.PROGRAM_DIR = Path(__file__).resolve().parent.parent
        self.CONFIG_DIR = self.PROGRAM_DIR / "configs"
        self.config = self.config_manager.load_config()
        self.runtime_context=runtime_context_load()
        self.launch_context=launch_context_load(self.CONFIG_DIR/"launch_context.json")
        self.account_config=account_load(self.CONFIG_DIR/"accounts.json")
        self.instance_id = self.config["minecraft"]["selected_instance"]
        instance_config = self.instance_manager.load_instance(self.instance_id)

        #兼容旧函数（使用实例管理类动态加载实例信息）
        self.config["minecraft"]["selected_version"] = instance_config["version"]
        self.config["minecraft"]["directory"] = (
                self.instance_manager.instances_path
                / self.instance_id
                / ".minecraft"
            )
        self.instance_type = instance_config["type"]
        
        #启动前检查
        java_path = self.java_manager.find_java(self.instance_id)
        if java_path is None:
            print("实例未配置 Java 路径，无法启动")
            return
        ok, required = self.java_manager.check_java(self.instance_id, java_path)
        if not ok:
            print(f"Java 版本不匹配：需要 Java {required}，无法启动")
            return
        if not minecraft_validity_check(self.config):
            return

        #启动准备
        version_json = version_json_load(self.config)
        mainclass=version_json["mainClass"]
        mc_jar_path=get_minecraft_jar_path(self.config)

        # ---- Libraries 解析 ----
        library_mgr = LibraryManager(self.runtime_context)
        libraries = version_json["libraries"]
        filtered_libraries = library_mgr.filter_libraries(libraries)
        libraries_paths = library_paths_load(self.config, filtered_libraries)

        result,missing_paths=check_libraries_exist(libraries_paths)
        if result:
            classpath_list=classpath_build(libraries_paths,mc_jar_path)
            classpath_string=classpath_list_to_string(classpath_list)

            # ---- Arguments 解析 ----
            game_arguments = arguments_load(version_json, "game")
            jvm_arguments = arguments_load(version_json, "jvm")

            # 构建合并上下文（JVM 参数需要 os/arch，游戏参数需要 features）
            full_context = {
                **self.runtime_context,
                "features": self.launch_context,
            }
            rule_checker = RuleChecker(full_context)

            filtered_game_arguments = arguments_parse(game_arguments, rule_checker)
            filtered_jvm_arguments = arguments_parse(jvm_arguments, rule_checker)


            account_object = accounts.manager.AccountManager(self.account_config)
            account=account_object.get_selected_account()
            auth_context=account.get_auth_context()

            argument_context=argument_context_load(self.config,version_json,classpath_string,auth_context)
            filtered_game_arguments=arguments_replace(filtered_game_arguments,argument_context)
            filtered_jvm_arguments=arguments_replace(filtered_jvm_arguments,argument_context)
            command = build_launch_command(java_path,filtered_jvm_arguments,mainclass,filtered_game_arguments)

        #启动Minecraft
            launch_minecraft(command)
        else:
            print(f"以下库文件缺失，无法启动：")
            for p in missing_paths:
                print(f"  - {p}")