# Axiom Launcher

一个用 Python 编写的第三方 Minecraft: Java Edition 启动器。
> A third-party Minecraft: Java Edition launcher written in Python.

> ⚠️ **免责声明**：本项目与 Mojang、Microsoft、Xbox 或 Minecraft 无任何官方关联，不隶属于、不受其赞助或认可。Minecraft 及相关名称、素材均为其各自所有者的财产。使用本启动器前，请自行确保你合法拥有 Minecraft: Java Edition，并遵守 [Minecraft 使用指南](https://www.minecraft.net/en-us/usage-guidelines)、EULA 及 Microsoft 服务协议等相关条款。本项目不打包、不分发任何 Minecraft 游戏资源。正版登录功能仅面向合法拥有 Minecraft: Java Edition 的用户，登录过程由微软官方 OAuth 完成，本项目不接触用户密码。


## 功能

- **多实例管理** — 创建、查看、安装、删除多个独立实例，每个实例拥有隔离的 `.minecraft` 目录，并独立记录安装状态与 Java 路径
- **Minecraft 自动安装** — 一键从所选下载源下载版本 json、客户端 jar、依赖库、原生库、资源索引及资源文件，无需手动放置任何游戏文件
- **多下载源** — 内置 Mojang 官方源与 BMCLAPI 镜像源，可在「设置」菜单中随时切换，适应不同网络环境
- **Java 自动管理** — 自动在 PATH 与系统常见安装位置查找 Java 并校验版本；缺失时可从 Adoptium API 自动下载对应版本 JDK
- **原生库处理** — 自动下载并解压原生库（natives），正确应用解压排除规则
- **离线账号系统** — 基于用户名生成确定性的离线 UUID（与官方启动器算法一致，兼容存档 / 皮肤缓存）
- **Microsoft 正版登录** — 通过微软设备码流程（Device Code Flow）登录 Microsoft 账户，自动完成微软 → Xbox Live → XSTS → Minecraft 完整鉴权链，获取真实玩家名与 UUID；支持 refresh token 自动续期，token 过期时启动前自动刷新，可进入正版（online-mode）服务器
- **启动前完整性检查** — 校验 Java 运行时、版本 json、jar 及依赖库是否齐全
- **智能参数解析** — 解析版本 json 中的 JVM 参数与游戏参数，按操作系统、平台与 features 规则自动过滤
- **classpath 自动拼接** — 自动构建依赖库 classpath 并启动游戏进程
- **版本清单缓存** — 自动缓存版本 manifest，超过 24 小时自动刷新
- **Fabric 加载器自动安装** — 自动下载 Fabric 专属版本 json 与追加依赖库，安装时可选 loader 稳定版，一键启动
- **并发下载** — 依赖库与资源文件的下载并发数可独立调整（默认 12 / 40），加快大体积文件下载
- **下载源自动刷新** — 切换下载源时自动刷新版本清单缓存，确保版本列表与所选源一致

## Client ID 警告

⚠️ 本项目代码中包含的 Azure **Client ID 属于 Axiom Launcher 官方所有，仅供本项目官方版本使用**，未授权不得用于任何其他第三方应用。

请勿直接复用本项目中的 Client ID。**自建部署、Fork 或任何衍生版本，必须使用你自己注册的 Client ID**，并自行承担相应的申请与审核责任。

Axiom Launcher 项目保留管理、更新或撤销该 Client ID 的权利。

## 环境要求

- Python 3.8+
- `requests` 依赖（`pip install requests`）
- 网络连接（用于下载 Minecraft 游戏文件与 Java 运行时）
- Java：非必需——启动器会自动查找系统 Java，缺失时可在启动流程中选择自动下载

## 快速开始

1. 克隆本仓库并安装依赖
   ```bash
   git clone https://github.com/sudo1123/axiom-launcher
   cd axiom-launcher
   pip install requests
   ```

2. 运行初始化脚本，自动生成所需目录和默认配置文件：
   ```bash
   python setup.py
   ```
   这会在项目目录下创建 `configs/`、`instances/`、`launcher_logs/`、`data/` 文件夹，并生成三个带默认值的配置文件：
   - `configs/config.json` — 通用配置（启动器信息、内存、分辨率、下载源等）
   - `configs/accounts.json` — 离线账号配置（默认账号 "Steve"）
   - `configs/launch_context.json` — 启动参数上下文（features 开关）

3. 运行启动器并通过 CLI 菜单创建实例：
   ```bash
   python main.py
   ```
   - 选择「**实例管理**」→「**创建实例**」
      - 输入实例 ID、Minecraft 版本号（如 `1.21.4`）、实例类型（`vanilla` / `fabric`）
   - 若选择 `fabric`，安装时会提示从可用稳定版中选择 loader 版本
   - 提示「是否安装 Minecraft?」时选择 **y**
   - 等待自动下载完成即可

4. 返回主菜单，选择「**启动游戏**」→ 选择实例即可启动
   - 若系统缺少实例所需的 Java 版本，程序会提示并询问是否自动下载

## CLI 菜单

主菜单：

| 选项 | 说明 |
|------|------|
| `1. 启动游戏` | 选择实例并启动 |
| `2. 实例管理` | 查看 / 创建 / 安装 / 删除实例 |
| `3. 设置` | 查看 / 切换下载源 |
| `4. 账号管理` | 添加微软/离线账号、查看、切换、删除 |
| `5. 退出` | 退出程序 |


实例管理：

| 选项 | 说明 |
|------|------|
| `1. 查看实例` | 查看实例详细信息（ID、版本、类型、路径） |
| `2. 创建实例` | 创建新实例，可附带安装 Minecraft |
| `3. 安装实例` | 为已创建但未安装的实例安装 Minecraft |
| `4. 删除实例` | 删除指定实例（含其 `.minecraft` 目录） |

设置：

| 选项 | 说明 |
|------|------|
| `1. 查看当前下载源` | 显示当前配置值与下载源名称 |
| `2. 切换下载源` | 在 Mojang 官方源 / BMCLAPI 之间切换 |
| `3. 切换"下载源变更时自动刷新版本列表"` | 开启/关闭切换下载源时自动刷新版本清单 |
| `4. 调整下载并发数` | 分别调整依赖库 / 资源文件的下载并发数 |

账号管理：

| 选项 | 说明 |
|------|------|
| `1. 添加微软账号` | 设备码流程登录微软账户（需浏览器访问 microsoft.com/link 输入代码） |
| `2. 添加离线账号` | 输入用户名创建离线账号 |
| `3. 查看账号` | 列出所有账号及当前选中项 |
| `4. 切换账号` | 切换当前启动使用的账号 |
| `5. 删除账号` | 删除指定账号 |


## 实例类型说明

| 类型 | 自动安装 | 说明 |
|------|----------|------|
| **vanilla** | ✅ 支持 | 原版 Minecraft，可从所选下载源自动下载全部游戏文件 |
| **fabric** | ✅ 支持 | Fabric 加载器：自动下载专属版本 json 与追加依赖库，安装时选择 loader 稳定版 |
| **forge** | ❌ 预留 | Forge 加载器自动安装尚未实现 |


## 下载源说明

| 配置值 | 显示名 | 说明 |
|--------|--------|------|
| `mojang` | Mojang 官方源 | 从 Mojang 官方服务器下载（默认） |
| `bmclapi` | BMCLAPI | BangBang93 提供的镜像源，中国大陆网络环境下通常更快 |

下载源在 `configs/config.json` 的 `download.selected_source` 字段配置，也可通过 CLI 的「设置」菜单切换。

## 配置文件说明

| 文件 | 用途 | 关键字段 |
|------|------|----------|
| `config.json` | 启动器主配置 | `launcher.name` / `launcher.version`、`minecraft.selected_instance`、`java.memory.min/max`、`game.resolution.width/height`、`game.fullscreen`、`download.selected_source` / `manifest_refresh_on_source_change` / `library_threads` / `asset_threads` |
| `accounts.json` | 账号配置 | `accounts[].id` / `type`（`offline` / `microsoft`）/ `username` / `player_name` / `uuid` / `access_token` / `refresh_token` / `microsoft_token` / `xuid` / `client_id`、`selected` |
| `launch_context.json` | 启动参数 features 开关 | `is_demo_user`、`has_custom_resolution`、`has_quick_plays_support`、`is_quick_play_*` 等 |

微软账号条目包含 OAuth 凭证（`access_token` / `refresh_token` / `microsoft_token`）与玩家档案（`player_name` / `uuid` / `xuid`）。这些 token 为明文存储，请注意保护 `configs/accounts.json` 的访问权限。token 过期后启动器会在启动前自动用 `refresh_token` 刷新。
所有配置文件均可使用 `python setup.py` 生成带默认值的版本（已存在则跳过）。
`configs/config.json` 使用 `config_version` 字段（当前为 6）标识配置结构版本。`download.manifest_refresh_on_source_change` 控制切换下载源时是否自动刷新版本清单；`download.library_threads` 与 `download.asset_threads` 分别控制依赖库与资源文件的下载并发数。

每个实例对应 `instances/<id>/instance.json`，记录：

- `id` — 实例 ID
- `minecraft_version` — 原版 Minecraft 版本
- `loader` — 加载器配置：`type`（vanilla / fabric / forge）与 `version`（加载器版本，安装后写入）
- `installation_status` — 安装状态（`not_installed` / `installing` / `installed`）
- `java_path` — 该实例实际使用的 Java 可执行文件路径


## 项目结构

```
.
├── main.py                    # 入口文件
├── setup.py                   # 初始化脚本
├── cli/
│   └── cli.py                 # 命令行交互界面
├── core/                      # 核心逻辑
│   ├── launcher.py            # 游戏启动器（版本检查、参数解析、classpath 构建、进程启动）
│   ├── instance_manager.py    # 多实例管理（创建/删除/查询、安装状态、Java 路径记录）
│   ├── config_manager.py      # 配置文件加载与保存
│   ├── version_manager.py     # 版本 manifest 管理（缓存与 24h 自动刷新）
│   ├── version_parser.py      # 版本 json 解析（提取参数、库、资源索引、Java 版本等）
│   ├── library_manager.py     # 依赖库的规则过滤与路径管理
│   ├── asset_manager.py       # 资源索引与资源对象管理（下载 URL 生成）
│   ├── native_manager.py      # 原生库下载与解压
│   ├── java_manager.py        # Java 查找、版本校验、缺失时自动下载
│   ├── java_downloader.py     # 通过 Adoptium API 下载并解压对应版本 JDK
│   ├── minecraft_installer.py # Minecraft 自动安装（6 步：json、jar、依赖库、原生库、资源索引、资源文件）
│   ├── downloader.py          # 通用文件下载器（断点续传、重试、进度显示）
│   ├── rule_checker.py        # 平台/features 规则过滤
│   ├── runtime_context.py     # 运行时上下文（OS、架构、系统版本检测）
│   ├── download_source.py     # 下载源抽象基类
│   ├── mojang_source.py       # Mojang 官方下载源实现
│   ├── bmcl_api_source.py     # BMCLAPI 镜像下载源实现
│   ├── source_manager.py      # 下载源管理器（按配置选择下载源）
│   └── loaders/               # 加载器策略模块
│   │   ├── loader.py          # Loader 抽象基类（统一安装/启动接口）
│   │   ├── loader_manager.py  # LoaderManager 策略工厂（按类型获取加载器）
│   │   ├── vanilla_loader.py  # 原版加载器（空实现占位）
│   │   └── fabric_loader.py   # Fabric 加载器（版本列表、专属 json、追加库）
├── accounts/                  # 账号系统
│   ├── account.py             # 账号基类（auth_player_name / uuid / access_token / user_type / xuid / clientid）
│   ├── offline.py             # 离线账号（UUID 生成，接收字典构造）
│   ├── microsoft.py           # 微软 OAuth 认证 + 正版账号（设备码申请、token 轮询/刷新、Xbox→XSTS→Minecraft 鉴权链）
│   └── manager.py             # 账号管理器（类型分发 + 增删/保存/切换）
├── setup/                     # 初始化模块
│   ├── initializer.py         # 目录创建与配置文件初始化
│   └── templates.py           # 配置文件默认模板
├── configs/                   # 配置文件目录（运行时生成）
├── instances/                 # 实例存储目录（每个实例一个子目录）
├── data/                      # 元数据（版本 manifest 缓存等）
├── runtime/                   # 自动下载的 Java 运行时（JavaDownloader 生成）
├── test/                      # 测试代码
└── launcher_logs/             # 启动器日志
```

## 项目状态

当前版本：**v0.14.1**

- ✅ 离线模式完整启动流程（实例管理 → 版本检查 → 参数解析 → 启动游戏）
- ✅ 多实例管理（创建、查看、安装、删除，含安装状态追踪）
- ✅ 初始化脚本（自动生成目录和默认配置文件）
- ✅ Minecraft 自动下载安装（版本 json、客户端 jar、依赖库、原生库、资源索引、资源文件）
- ✅ 多下载源支持（Mojang 官方源 / BMCLAPI 镜像，可切换）
- ✅ Java 自动查找与缺失时自动下载（Adoptium）
- ✅ 原生库自动下载与解压
- ✅ Fabric 加载器自动安装（版本选择、专属版本 json、追加依赖库）
- ❌ Forge 加载器自动安装
- ✅ Microsoft 正版登录（设备码 OAuth + Xbox→XSTS→Minecraft 鉴权链 + refresh token 自动刷新）

## 协议

本项目基于 [GNU General Public License v3.0](./LICENSE) 开源。这意味着：

- 任何人都可以自由使用、复制、修改、分发本项目
- 但基于本项目二次开发的衍生作品，同样必须以 GPLv3 开源（即"传染性"/copyleft）
- 分发时必须保留版权声明和协议全文
