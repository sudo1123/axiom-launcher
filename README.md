# Axiom Launcher

一个用 Python 编写的第三方 Minecraft: Java Edition 启动器（离线模式）。
> A third-party Minecraft: Java Edition launcher (offline mode).

> ⚠️ **免责声明**：本项目与 Mojang、Microsoft、Xbox 或 Minecraft 无任何官方关联，不隶属于、不受其赞助或认可。Minecraft 及相关名称、素材均为其各自所有者的财产。使用本启动器前，请自行确保你合法拥有 Minecraft: Java Edition，并遵守 [Minecraft 使用指南](https://www.minecraft.net/en-us/usage-guidelines)、EULA 及 Microsoft 服务协议等相关条款。本项目不打包、不分发任何 Minecraft 游戏资源。

## 功能

- **多实例管理** — 创建、查看、删除多个独立实例，每个实例拥有隔离的 `.minecraft` 目录
- **离线账号系统** — 基于用户名生成确定性的离线 UUID（与官方启动器算法一致，兼容存档 / 皮肤缓存）
- **版本完整性检查** — 启动前校验目标版本的 json、jar 及依赖库是否齐全
- **启动参数解析** — 解析版本 json 中的游戏参数与 JVM 参数，根据操作系统和平台规则自动过滤
- **classpath 拼接与游戏启动** — 自动拼接依赖库路径并启动游戏进程
- **Minecraft 自动安装**（🧪 开发中）— `core/minecraft_installer.py` 已实现从 Mojang 服务器下载版本 json、客户端 jar、依赖库及资源文件的功能，目前尚未接入 CLI 菜单，可通过脚本手动调用

## 环境要求

- Python 3.x
- 对应版本所需的 Java 运行时（需自行安装）
- 目标 Minecraft 版本的 jar 文件及依赖库（需用户自行放入对应实例的 `.minecraft` 目录）

## 快速开始

1. 克隆本仓库
   ```bash
   git clone <your-repo-url>
   cd <repo-name>
   ```

2. 首次使用前，运行初始化脚本自动生成所需目录和默认配置文件：
   ```bash
   python -c "from setup.initializer import initialize; initialize()"
   ```
   这会在项目目录下创建 `configs/`、`instances/`、`launcher_logs/`、`data/` 文件夹，并生成三个带默认值的配置文件：
   - `configs/config.json` — 通用配置（Java 路径、内存、分辨率等）
   - `configs/accounts.json` — 离线账号配置
   - `configs/launch_context.json` — 启动参数上下文

3. 编辑 `configs/config.json`，将 `java.path` 修改为你的 Java 可执行文件路径。

4. 运行启动器并通过 CLI 菜单创建实例：
   ```bash
   python main.py
   ```
   - 选择「实例管理」→「创建实例」，输入实例 ID、Minecraft 版本号和实例类型（vanilla/fabric/forge）
   - 将对应版本的 `{version}.json` 和 `{version}.jar` 放入 `instances/{实例ID}/.minecraft/versions/{版本号}/` 目录
   - 将依赖库放入 `instances/{实例ID}/.minecraft/libraries/` 对应路径

5. 在主菜单中选择「启动游戏」，选择实例即可启动

## 配置文件说明

| 文件 | 用途 | 关键字段 |
|------|------|----------|
| `config.json` | 启动器主配置 | `java.path`、`java.memory`、`minecraft.selected_instance`、`game.resolution` |
| `accounts.json` | 离线账号 | `accounts[].username`、`selected` |
| `launch_context.json` | 启动参数过滤 | `is_demo_user`、`has_custom_resolution` 等 features 开关 |

所有配置文件均可使用 `setup.initializer.initialize()` 生成带默认值的版本。

## 实例类型说明

实例类型字段目前作为标识存储，不影响下载和启动行为。三种类型选项均已预留：
- **vanilla** — 原版 Minecraft
- **fabric** — Fabric（加载器自动安装尚未实现）
- **forge** — Forge（加载器自动安装尚未实现）

> 使用 fabric 或 forge 类型时，需用户自行将对应加载器的 jar 及依赖库放入实例的 `.minecraft` 目录。

## 项目结构

```
.
├── main.py                  # 入口文件
├── cli/
│   └── cli.py               # 命令行交互界面
├── core/                    # 核心逻辑
│   ├── launcher.py          # 游戏启动器（版本检查、参数解析、classpath 构建、进程启动）
│   ├── instance_manager.py  # 多实例管理（创建/删除/查询）
│   ├── config_manager.py    # 配置文件加载与保存
│   ├── version_manager.py   # 版本元数据管理（读取 manifest 获取版本信息）
│   ├── version_parser.py    # 版本 json 解析（提取参数、库、资源索引等）
│   ├── library_manager.py   # 依赖库的规则过滤与路径管理
│   ├── asset_manager.py     # 资源索引与资源对象管理
│   ├── minecraft_installer.py # Minecraft 自动安装（开发中，暂未接入 CLI）
│   ├── downloader.py        # 通用文件下载器
│   ├── rule_checker.py      # 平台规则过滤（OS/arch）
│   └── runtime_context.py   # 运行时上下文（平台信息等）
├── accounts/                # 账号系统
│   ├── account.py           # 账号基类
│   ├── offline.py           # 离线账号（UUID 生成）
│   └── manager.py           # 账号管理器
├── setup/                   # 初始化脚本
│   ├── initializer.py       # 目录创建与配置文件初始化
│   └── templates.py         # 配置文件默认模板
├── configs/                 # 配置文件目录
├── instances/               # 实例存储目录（每个实例一个子目录）
├── data/                    # 元数据（如版本 manifest）
├── test/                    # 测试代码
└── launcher_logs/           # 启动器日志
```

## 项目状态

目前为早期开发阶段：

- ✅ 离线模式完整启动流程（实例管理 → 版本检查 → 参数解析 → 启动游戏）
- ✅ 多实例管理（创建、查看、删除）
- ✅ 初始化脚本（自动生成目录和默认配置文件）
- 🧪 Minecraft 自动下载安装（代码已实现，CLI 接入开发中）
- ❌ Fabric / Forge 加载器自动安装
- ❌ Microsoft 正版登录

## 协议

本项目基于 [GNU General Public License v3.0](./LICENSE) 开源。这意味着：

- 任何人都可以自由使用、复制、修改、分发本项目
- 但基于本项目二次开发的衍生作品，同样必须以 GPLv3 开源（即"传染性"/copyleft）
- 分发时必须保留版权声明和协议全文
