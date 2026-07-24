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
import json
import subprocess
import platform
import os
import zipfile
'''== 配置文件默认内容 == '''

DEFAULT_CONFIG={
    "config_version": 1,

    "launcher": {
        "name": "Axiom Launcher",
        "version": "0.2_build2"
    },

    "minecraft": {
        "directory": r"C:\path\to\.minecraft",
        "selected_version": "1.20.1"
    },

    "java": {
        "path": r"C:\path\to\java.exe",
        "memory": {
            "min": 1024,
            "max": 4096
        }
    },

    "game": {
        "resolution": {
            "width": 854,
            "height": 480
        },
        "fullscreen": "false"
    }
}

DEFAULT_LAUNCH_CONTEXT = {
    "is_demo_user": False,

    "has_custom_resolution": False,

    "has_quick_plays_support": False,

    "is_quick_play_singleplayer": False,

    "is_quick_play_multiplayer": False,

    "is_quick_play_realms": False
}

DEFAULT_ACCOUNTS={
    "accounts": [
        {
            "id": "offline_default",
            "type": "offline",
            "username": "Steve"
        }
    ],

    "selected": "offline_default"
}


'''== 配置加载函数 =='''
def config_init ():
    current_script_path = Path(__file__).resolve()                #获取当前脚本文件的绝对路径
    program_dir = current_script_path.parent   #跳转至程序主目录               
    config_dir = program_dir / "configs"
    config_dir.mkdir(parents=True, exist_ok=True)                 #确保configs目录存在
    config_file_path = config_dir / "config.json"
    if not config_file_path.exists():                             #如果config 文件不存在,创建之
        with open ( config_file_path ,"w" ) as c: 
            json.dump(
            DEFAULT_CONFIG,
            c,
            indent=4
            )
    return config_file_path                                       #返回配置文件路径

def config_load(config_file_path):
    with open (config_file_path,"r") as cf:
        return json.load(cf)

def launch_context_load(path):

    path = Path(path)

    # 文件不存在，创建默认配置
    if not path.exists():

        path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(path, "w", encoding="utf-8") as f:
            json.dump(
                DEFAULT_LAUNCH_CONTEXT,
                f,
                indent=4
            )

        return DEFAULT_LAUNCH_CONTEXT.copy()


    # 文件存在，读取
    with open(path, "r", encoding="utf-8") as f:
        context = json.load(f)


    # 补充新增字段
    changed = False

    for key,value in DEFAULT_LAUNCH_CONTEXT.items():

        if key not in context:
            context[key] = value
            changed = True


    if changed:

        with open(path,"w",encoding="utf-8") as f:
            json.dump(
                context,
                f,
                indent=4
            )


    return context

def account_load(path):

    path = Path(path)

    # 文件不存在，创建默认配置
    if not path.exists():

        path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(path, "w", encoding="utf-8") as f:
            json.dump(
                DEFAULT_ACCOUNTS,
                f,
                indent=4
            )

        return DEFAULT_ACCOUNTS.copy()


    # 文件存在，读取
    with open(path, "r", encoding="utf-8") as f:
        context = json.load(f)


    # 补充新增字段
    changed = False

    for key,value in DEFAULT_ACCOUNTS.items():

        if key not in context:
            context[key] = value
            changed = True


    if changed:

        with open(path,"w",encoding="utf-8") as f:
            json.dump(
                context,
                f,
                indent=4
            )


    return context

'''== 启动功能函数 =='''

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
                        print("Java failed")
                        return False
        except FileNotFoundError:
             return False

    else:
        return False

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
                    print("Minecraft files are valid")
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
        return False

def version_json_load(config):
    minecraft_directory_path = config["minecraft"]["directory"]
    dicpath = Path(minecraft_directory_path)
    version_path= dicpath / "versions" / config["minecraft"]["selected_version"]
    file_path = version_path / f'{config["minecraft"]["selected_version"]}.json'
    with open(file_path,"r") as vj:
        version_json=json.load(vj)
    return version_json

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
            
def main():
    PROGRAM_DIR = Path(__file__).resolve().parent
    CONFIG_DIR = PROGRAM_DIR / "configs"
    config_file_path=config_init()
    config=config_load(config_file_path)
    runtime_context=runtime_context_load()
    launch_context=launch_context_load(CONFIG_DIR/"launch_context.json")
    account_config=account_load(CONFIG_DIR/"accounts.json")
    if java_validity_check(config) and minecraft_validity_check(config):
        version_json = version_json_load(config)
        mainclass=version_json["mainClass"]
        mc_jar_path=get_minecraft_jar_path(config)
        libraries = version_json["libraries"]
        os_type=get_platform()
        libraries_paths=library_paths_load(config,libraries,os_type)
        result,missing_paths=check_libraries_exist(libraries_paths)
        if result:
            classpath_list=classpath_build(libraries_paths,mc_jar_path)
            classpath_string=classpath_list_to_string(classpath_list)
            game_arguments = arguments_load(version_json,"game")
            jvm_arguments = arguments_load(version_json,"jvm")
            filtered_game_arguments=arguments_parse(game_arguments,launch_context,runtime_context,"game")
            filtered_jvm_arguments=arguments_parse(jvm_arguments,launch_context,runtime_context,"jvm")

            account_object = accounts.manager.AccountManager(account_config)
            account=account_object.get_selected_account()
            auth_context=account.get_auth_context()

            argument_context=argument_context_load(config,version_json,classpath_string,auth_context)
            filtered_game_arguments=arguments_replace(filtered_game_arguments,argument_context)
            filtered_jvm_arguments=arguments_replace(filtered_jvm_arguments,argument_context)
            command = build_launch_command(config["java"]["path"],filtered_jvm_arguments,mainclass,filtered_game_arguments)
            launch_minecraft(command)
        else:
            print("library missing")
    
main()