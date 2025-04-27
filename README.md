# Auto Sync

An automatic synchronization tool that uses the rsync command to synchronize source directories to target directories in real-time.

## Features

- Read project information from YAML configuration files, including source paths, target paths, and ignored files
- Real-time monitoring of source directory file changes, automatically triggering synchronization
- Efficient synchronization using rsync command
- Complete logging
- Support for monitoring and synchronizing multiple projects simultaneously
- Modular design for easy extension

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd auto_sync

# Install dependencies
pip install -e .
```

## Configuration

Configure your synchronization projects in `config/sync_config.yml`:

```yaml
projects:
  - name: project1  # Project name
    src: /path/to/source/dir/  # Source directory
    dst: server:/path/to/dest/dir/    # Target directory
    watch: true  # Whether to monitor file changes, if true, will automatically monitor
    exclude:  # File patterns to exclude
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

## Usage

### Start Monitoring

```bash
auto_sync -c config/sync_config.yml
```

### Command Line Arguments

- `-c, --config`: Specify configuration file path (default: `config/sync_config.yml`)
- `-l, --log`: Specify log file path (default: `stdout`)
- `-o, --once`: Synchronize only once, do not continuously monitor file changes

### Examples

```bash

# Use a custom configuration file
auto_sync -c /path/to/custom_config.yml

# Synchronize only once
auto_sync -c /path/to/custom_config.yml --once
```

## Dependencies

- Python 3.6+
- pyyaml
- watchdog
- rsync (system command)

## Project Structure

```
auto_sync/
├── config/
│   └── sync_config.yml  # Configuration file
├── logs/                # Log directory
├── src/
│   ├── main.py          # Main entry file
│   └── auto_sync/       # Core package
│       ├── __init__.py
│       ├── config_loader.py  # Configuration loader
│       ├── logger.py         # Logging module
│       ├── synchronizer.py   # Synchronization module
│       └── watcher.py        # File monitoring module
└── setup.py             # Installation script
```