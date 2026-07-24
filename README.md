# Axiom Launcher

一个用 Python 编写的第三方 Minecraft: Java Edition 启动器（离线模式）。

> ⚠️ **免责声明**：本项目与 Mojang、Microsoft、Xbox 或 Minecraft 无任何官方关联，不隶属于、不受其赞助或认可。Minecraft 及相关名称、素材均为其各自所有者的财产。使用本启动器前，请自行确保你合法拥有 Minecraft: Java Edition，并遵守 [Minecraft 使用指南](https://www.minecraft.net/en-us/usage-guidelines)、EULA 及 Microsoft 服务协议等相关条款。本项目不打包、不分发任何 Minecraft 游戏资源（jar / assets / libraries），只在本地读取你已安装的 Minecraft 目录。

## 功能

- 读取本地 `.minecraft` 目录，校验指定版本的完整性（版本 json / jar / 依赖库是否齐全）
- 解析版本 json 中的 launch arguments（游戏参数与 JVM 参数），并根据规则（操作系统 / 架构 / features）过滤
- 离线账号系统，基于用户名生成确定性的离线 UUID（与官方启动器算法一致，兼容存档 / 皮肤缓存）
- 拼接 classpath 并启动游戏进程

## 环境要求

- Python 3.x
- 本地已安装 Minecraft: Java Edition（含对应版本的 libraries / assets）
- 对应版本所需的 Java 运行时

## 快速开始

1. 克隆本仓库
   ```bash
   git clone <your-repo-url>
   cd <repo-name>
   ```
2. 首次运行会自动在 `configs/` 目录下生成默认 `config.json`（如果不存在的话）。你也可以参考 `configs/config.example.json`，手动复制一份改名为 `configs/config.json`，并填入你自己的：
   - `minecraft.directory`：你的 `.minecraft` 目录路径
   - `minecraft.selected_version`：要启动的版本号
   - `java.path`：对应版本的 java.exe 路径
3. 运行：
   ```bash
   python main.py
   ```

`configs/accounts.json`、`configs/launch_context.json` 同理，可参考对应的 `.example.json` 模板，也会在首次运行时自动生成默认值。

## 项目状态

目前是最小可行原型（MVP），仅支持离线模式登录，尚未支持正版（Microsoft）登录、Mod 加载器（Forge / Fabric）等。

## 协议

本项目基于 [GNU General Public License v3.0](./LICENSE) 开源。这意味着：

- 任何人都可以自由使用、复制、修改、分发本项目
- 但基于本项目二次开发的衍生作品，同样必须以 GPLv3 开源（即"传染性"/copyleft）
- 分发时必须保留版权声明和协议全文