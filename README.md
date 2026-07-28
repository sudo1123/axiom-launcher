```markdown README.md
# Axiom Launcher

一个用 Python 编写的第三方 Minecraft: Java Edition 启动器（离线模式）。
> A third-party Minecraft: Java Edition launcher (offline mode).

> ⚠️ **免责声明**：本项目与 Mojang、Microsoft、Xbox 或 Minecraft 无任何官方关联，不隶属于、不受其赞助或认可。Minecraft 及相关名称、素材均为其各自所有者的财产。使用本启动器前，请自行确保你合法拥有 Minecraft: Java Edition，并遵守 [Minecraft 使用指南](https://www.minecraft.net/en-us/usage-guidelines)、EULA 及 Microsoft 服务协议等相关条款。

## 功能

- **多实例管理** — 创建、查看、删除多个独立实例，每个实例拥有隔离的 `.minecraft` 目录
- **自动安装 Minecraft** — 从 Mojang 服务器下载版本 json、客户端 jar、依赖库及 assets 资源文件
- **Mod 加载器支持** — 支持 vanilla、Fabric、Forge 三种实例类型
- **智能库过滤** — 解析版本 json 中的依赖库，根据操作系统、架构等规则自动过滤并下载匹配的库
- **资产（Assets）管理** — 下载并管理资源索引与资源对象
- **离线账号系统** — 基于用户名生成确定性的离线 UUID（与官方启动器算法一致，兼容存档/皮肤缓存）
- **启动游戏** — 拼接 classpath、处理启动参数，启动 Minecraft 游戏进程

## 环境要求

- Python 3.x
- 对应版本所需的 Java 运行时（需自行安装）

> 💡 无需预先安装 Minecraft 或手动下载任何游戏文件，启动器会自动完成安装。

## 快速开始

1. 克隆本仓库
   ```bash
   git clone <your-repo-url>
   cd <repo-name>
   ```

2. 首次运行会自动在 `configs/` 目录下生成默认配置文件。你也可以参考 `configs/` 下的 `.example.json` 模板手动配置：
   - `configs/config.json` — 通用配置（Java 路径等）
   - `configs/accounts.json` — 离线账号配置
   - `configs/launch_context.json` — 启动参数上下文（JVM 参数、内存等）

3. 运行启动器
   ```bash
   python main.py
   ```

4. 在交互式菜单中，先进入「实例管理」创建一个实例（选择 Minecraft 版本和类型），再选择「启动游戏」即可自动完成安装并启动。

## 项目结构

```
.
├── main.py                  # 入口文件
├── cli/                     # 命令行交互界面
├── core/                    # 核心逻辑
│   ├── launcher.py          # 游戏启动器
│   ├── instance_manager.py  # 实例管理（创建/删除/查询）
│   ├── version_manager.py   # 版本元数据管理
│   ├── version_parser.py    # 版本 json 解析
│   ├── library_manager.py   # 依赖库过滤与管理
│   ├── asset_manager.py     # 资源索引与对象管理
│   ├── minecraft_installer.py # Minecraft 自动安装
│   ├── downloader.py        # 文件下载器
│   ├── config_manager.py    # 配置管理
│   ├── rule_checker.py      # 平台规则过滤
│   └── runtime_context.py   # 运行时上下文
├── accounts/                # 账号系统（离线/正版）
├── configs/                 # 配置文件目录
├── instances/               # 实例存储目录
├── test/                    # 测试代码
└── setup/                   # 安装相关脚本
```

## 项目状态

目前支持离线模式的完整游戏启动流程：实例管理 → 自动下载安装 → 启动游戏。支持 vanilla、Fabric、Forge 实例类型。暂未支持 Microsoft 正版登录及更复杂的 Mod 加载器功能（如自动安装 Mod 加载器）。

## 协议

本项目基于 [GNU General Public License v3.0](./LICENSE) 开源。这意味着：

- 任何人都可以自由使用、复制、修改、分发本项目
- 但基于本项目二次开发的衍生作品，同样必须以 GPLv3 开源（即"传染性"/copyleft）
- 分发时必须保留版权声明和协议全文
