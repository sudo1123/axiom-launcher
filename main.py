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

import tomllib
import argparse
from pathlib import Path
from cli.cli import CLI
from cli.commands import Commands

def get_version():
    try:
        pyproject_path = Path(__file__).resolve().parent / "pyproject.toml"
        with open(pyproject_path, "rb") as f:
            return tomllib.load(f)["project"]["version"]
    except Exception:
        return "0.0.0"

def build_parser():
    p = argparse.ArgumentParser(prog="axiom-launcher",
                                description="Axiom Launcher - 第三方 Minecraft: Java Edition 启动器")
    p.add_argument("-V", "--version", action="store_true", help="显示版本号")

    # 实例类
    p.add_argument("--list-instances", action="store_true", help="列出所有实例")
    p.add_argument("--launch", metavar="INSTANCE_ID", help="直接启动指定实例")
    p.add_argument("--auto-download-java", action="store_true",
                   help="Java 缺失时自动下载（配合 --launch）")
    p.add_argument("--create-instance", metavar="INSTANCE_ID", help="创建新实例")
    p.add_argument("--mc-version", metavar="VERSION", help="Minecraft 版本号（配合 --create-instance）")
    p.add_argument("--type", choices=["vanilla", "fabric", "forge"], default="vanilla",
                   help="实例类型（配合 --create-instance，默认 vanilla）")
    p.add_argument("--with-install", action="store_true", help="创建实例后立即安装（配合 --create-instance）")
    p.add_argument("--install", metavar="INSTANCE_ID", help="安装已有实例")
    p.add_argument("--delete-instance", metavar="INSTANCE_ID", help="删除实例")

    # 账号类
    p.add_argument("--list-accounts", action="store_true", help="列出所有账号")
    p.add_argument("--add-offline-account", metavar="USERNAME", help="添加离线账号")
    p.add_argument("--switch-account", metavar="ACCOUNT_ID", help="切换当前账号")
    p.add_argument("--delete-account", metavar="ACCOUNT_ID", help="删除账号")

    # 设置类
    p.add_argument("--set-download-source", choices=["mojang", "bmclapi"], help="切换下载源")
    p.add_argument("--set-library-threads", type=int, help="设置依赖库下载并发数")
    p.add_argument("--set-asset-threads", type=int, help="设置资源文件下载并发数")
    p.add_argument("--set-manifest-refresh", choices=["on", "off"],
                   help="设置下载源变更时自动刷新版本清单开关")
    return p

def main():
    args = build_parser().parse_args()

    if args.version:
        print(f"Axiom Launcher {get_version()}")
        return

    cmd = Commands()

    if args.list_instances:
        cmd.list_instances(); return
    if args.launch:
        cmd.launch(args.launch, args.auto_download_java); return
    if args.create_instance:
        cmd.create_instance(args.create_instance, args.mc_version, args.type, args.with_install); return
    if args.install:
        cmd.install(args.install); return
    if args.delete_instance:
        cmd.delete_instance(args.delete_instance); return
    if args.list_accounts:
        cmd.list_accounts(); return
    if args.add_offline_account:
        cmd.add_offline_account(args.add_offline_account); return
    if args.switch_account:
        cmd.switch_account(args.switch_account); return
    if args.delete_account:
        cmd.delete_account(args.delete_account); return
    if args.set_download_source:
        cmd.set_download_source(args.set_download_source); return
    if args.set_library_threads is not None:
        cmd.set_library_threads(args.set_library_threads); return
    if args.set_asset_threads is not None:
        cmd.set_asset_threads(args.set_asset_threads); return
    if args.set_manifest_refresh is not None:
        cmd.set_manifest_refresh(args.set_manifest_refresh); return

    # 无参数：保持原有交互式菜单
    CLI().run()

if __name__ == "__main__":
    main()

