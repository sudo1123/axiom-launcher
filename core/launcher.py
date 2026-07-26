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
import json
import subprocess
import platform
import os

'''== 配置加载 =='''

def config_load(config_file_path):
    path = Path(config_file_path)
    # 文件不存在，抛出错误
    if not path.exists():

        raise EnvironmentError("config加载失败，请检查配置文件")
    
    with open (path,"r", encoding="utf-8") as cf:
        return json.load(cf)

def launch_context_load(path):

    path = Path(path)

    # 文件不存在，抛出错误
    if not path.exists():

        raise EnvironmentError("launch_context加载失败，请检查配置文件")


    # 文件存在，读取
    with open(path, "r", encoding="utf-8") as f:
        context = json.load(f)

    return context

def account_load(path):

    path = Path(path)

    # 文件不存在，抛出错误
    if not path.exists():

        raise EnvironmentError("account加载失败，请检查配置文件")

    # 文件存在，读取
    with open(path, "r", encoding="utf-8") as f:
        context = json.load(f)

    return context

'''== JAVA环境检查 =='''

def java_validity_check(config):
    java_path=config["java"]["path"]
    if isinstance(java_path,str):
        try:
            result=subprocess.run ([java_path,"--version"],capture_output=True,text=True)
            if result.returncode == 0:
                print("Java is available")
                print(f"当前Java版本:{result.stdout}")
                return True
            else:
                        return False
        except FileNotFoundError:
             return False

    else:
        return False

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
def get_platform():
    os_type=platform.system()
    if os_type == "Windows":
        return "windows"
    if os_type == "Darwin":
        return "osx"
    if os_type == "Linux":
        return "linux"

def get_arch():

    arch=platform.machine().lower()

    if arch in ("amd64","x86_64"):
        return "x86_64"

    if arch in ("x86","i386","i686"):
        return "x86"

    if arch in ("arm64","aarch64"):
        return "arm64"

def runtime_context_load():

    return {
        "name":get_platform(),
        "arch":get_arch()
    }

'''=== libraries解析 ==='''
def library_paths_load(config,libraries,os_type):
    paths=[]
    minecraft_directory_path = Path(config["minecraft"]["directory"])
    prefix=minecraft_directory_path / "libraries"
    for element in libraries:
        rule=element.get("rules")
        if rule != None:
            if rule[0].get("action") == "allow" :
                if rule[0].get("os").get("name") == os_type:
                    paths.append(prefix / Path(element["downloads"]["artifact"]["path"]))
                else:
                    pass
            if rule[0].get("action") == "disallow" :
                if rule[0].get("os").get("name") != os_type:
                    paths.append(prefix / Path(element["downloads"]["artifact"]["path"]))
                else:
                    pass
        else:
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

def game_rules_check(element,launch_context):
    if element.get("rules")[0].get("action") == "allow":
        feature=element.get("rules")[0].get("features")
        for local_lc_key in launch_context:
            if local_lc_key in feature:

                if feature.get(local_lc_key) == launch_context.get(local_lc_key):
                    return True

    return False

def jvm_rules_check(element, runtime_context):

    rules = element.get("rules")

    # 没有 rules，默认允许
    if not rules:
        return True

    for rule in rules:

        if rule.get("action") != "allow":
            continue

        os_rule = rule.get("os")

        # allow，但没有 os 限制
        if not os_rule:
            return True

        # 检查系统
        if "name" in os_rule:
            if os_rule["name"] != runtime_context["name"]:
                continue

        # 检查架构
        if "arch" in os_rule:
            if os_rule["arch"] != runtime_context["arch"]:
                continue

        # 所有条件通过
        return True

    return False

    

def arguments_parse(arguments,launch_context,runtime_context,check_mode):
    result_list=[]
    for element in arguments:
        if isinstance(element,str):
            result_list.append(element)
        if isinstance(element,dict):
            if check_mode=="game":
                check_result=game_rules_check(element,launch_context)
            if check_mode=="jvm":
                check_result=jvm_rules_check(element,runtime_context)
            if check_result:
                value=element.get("value")
                if isinstance(value,str):
                    result_list.append(value)
                if isinstance(value,list):
                    result_list.extend(value)
            else:
                pass

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

    process=subprocess.Popen(
        command
    )

    return process



class Launcher:

    def __init__(self):
        self.instance_manager = InstanceManager()

    def start(self):
        #配置文件加载
        self.PROGRAM_DIR = Path(__file__).resolve().parent.parent
        self.CONFIG_DIR = self.PROGRAM_DIR / "configs"
        self.config_file_path = self.CONFIG_DIR / "config.json"
        self.config = config_load(self.config_file_path)
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
        if not java_validity_check(self.config):
            return
        if not minecraft_validity_check(self.config):
            return

        #启动准备
        version_json = version_json_load(self.config)
        mainclass=version_json["mainClass"]
        mc_jar_path=get_minecraft_jar_path(self.config)
        libraries = version_json["libraries"]
        os_type=get_platform()
        libraries_paths=library_paths_load(self.config,libraries,os_type)
        result,missing_paths=check_libraries_exist(libraries_paths)
        if result:
            classpath_list=classpath_build(libraries_paths,mc_jar_path)
            classpath_string=classpath_list_to_string(classpath_list)
            game_arguments = arguments_load(version_json,"game")
            jvm_arguments = arguments_load(version_json,"jvm")
            filtered_game_arguments=arguments_parse(game_arguments,self.launch_context,self.runtime_context,"game")
            filtered_jvm_arguments=arguments_parse(jvm_arguments,self.launch_context,self.runtime_context,"jvm")

            account_object = accounts.manager.AccountManager(self.account_config)
            account=account_object.get_selected_account()
            auth_context=account.get_auth_context()

            argument_context=argument_context_load(self.config,version_json,classpath_string,auth_context)
            filtered_game_arguments=arguments_replace(filtered_game_arguments,argument_context)
            filtered_jvm_arguments=arguments_replace(filtered_jvm_arguments,argument_context)
            command = build_launch_command(self.config["java"]["path"],filtered_jvm_arguments,mainclass,filtered_game_arguments)

        #启动Minecraft
            launch_minecraft(command)