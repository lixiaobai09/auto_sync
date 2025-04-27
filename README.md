# Auto Sync

自动同步工具，使用 rsync 命令将源目录实时同步到目标目录。

## 功能特点

- 从 YAML 配置文件中读取项目信息，包括源路径、目标路径和忽略文件
- 实时监控源目录的文件变化，自动触发同步
- 使用 rsync 命令进行高效同步
- 完整的日志记录
- 支持多个项目同时监控和同步
- 模块化设计，便于扩展

## 安装

```bash
# 克隆代码库
git clone <repository-url>
cd auto_sync

# 安装依赖
pip install -e .
```

## 配置

在 `config/sync_config.yml` 中配置你的同步项目：

```yaml
projects:
  - name: project1  # 项目名称
    src: /path/to/source/dir/  # 源目录
    dst: server:/path/to/dest/dir/    # 目标目录
    watch: true  # 是否监控文件变化，若有则自动监控
    exclude:  # 需要排除的文件模式
      - "*.pyc"
      - "__pycache__"
      - ".git"
      - ".DS_Store"
  
  - name: project2
    src: /path/to/another/source/
    dst: /path/to/another/dest/
    exclude:
      - "*.log"
      - "*.tmp"
      - "node_modules"
```

## 使用方法

### 启动监控

```bash
python src/main.py
```

### 命令行参数

- `-c, --config`: 指定配置文件路径 (默认: `config/sync_config.yml`)
- `-l, --log`: 指定日志文件路径 (默认: `logs/auto_sync.log`)
- `-o, --once`: 只同步一次，不持续监控文件变化

### 例子

```bash
# 使用默认配置文件启动
python src/main.py

# 使用自定义配置文件
python src/main.py -c /path/to/custom_config.yml

# 只同步一次
python src/main.py --once
```

## 依赖

- Python 3.6+
- pyyaml
- watchdog
- rsync (系统命令)

## 项目结构

```
auto_sync/
├── config/
│   └── sync_config.yml  # 配置文件
├── logs/                # 日志目录
├── src/
│   ├── main.py          # 主入口文件
│   └── auto_sync/       # 核心包
│       ├── __init__.py
│       ├── config_loader.py  # 配置加载器
│       ├── logger.py         # 日志模块
│       ├── synchronizer.py   # 同步模块
│       └── watcher.py        # 文件监控模块
└── setup.py             # 安装脚本
```