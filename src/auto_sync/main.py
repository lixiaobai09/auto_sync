#!/usr/bin/env python3
import os
import sys
import time
import signal
import argparse
from auto_sync.config_loader import ConfigLoader
from auto_sync.watcher import DirectoryWatcher
from auto_sync.logger import Logger


def parse_arguments():
    """Parse command line arguments.

    Returns:
        argparse.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="Auto Sync - Directory synchronization tool"
    )
    parser.add_argument(
        "-c",
        "--config",
        default="config/sync_config.yml",
        help="Path to configuration file (default: config/sync_config.yml)",
    )
    parser.add_argument(
        "-l",
        "--log",
        default=None,
        help="Path to log file (if not specified, logs will only be sent to stdout)",
    )
    parser.add_argument(
        "-o",
        "--once",
        action="store_true",
        help="Sync once and exit without watching for changes",
    )

    return parser.parse_args()


def signal_handler(sig, frame):
    """Handle interrupt signals.

    Args:
        sig: Signal number
        frame: Current stack frame
    """
    logger.info("Received interrupt signal, shutting down...")
    if watcher:
        watcher.stop_watching()
    sys.exit(0)


def main():
    """Main function to start the auto sync process."""
    args = parse_arguments()

    # Setup logger
    global logger
    logger_instance = Logger("main", args.log)
    logger = logger_instance.get_logger()

    # Set up signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        # Load configuration
        config_path = os.path.abspath(args.config)
        logger.info(f"Loading configuration from {config_path}")

        config_loader = ConfigLoader(config_path)
        projects = config_loader.get_projects()

        if not projects:
            logger.error("No projects found in configuration file")
            sys.exit(1)

        logger.info(f"Loaded {len(projects)} project(s)")

        # Set up and start directory watcher
        global watcher
        watcher = DirectoryWatcher(projects, args.log)

        # If once flag is set, sync all projects once and exit
        if args.once:
            from auto_sync.synchronizer import RsyncSynchronizer

            synchronizer = RsyncSynchronizer(args.log)

            logger.info("Performing one-time sync for all projects")
            for project in projects:
                logger.info(f"Syncing project: {project['name']}")
                synchronizer.sync(
                    project["src"], project["dst"], project.get("exclude", [])
                )
            logger.info("One-time sync completed, exiting")
            sys.exit(0)

        # Start watching for file changes
        logger.info("Starting directory watcher")
        watcher.start_watching()

        # Keep program running
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received, shutting down...")
        if watcher:
            watcher.stop_watching()
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        if watcher:
            watcher.stop_watching()
        sys.exit(1)


if __name__ == "__main__":
    # Initialize global variables
    logger = None
    watcher = None

    main()
