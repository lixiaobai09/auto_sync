import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from .logger import Logger
from .synchronizer import RsyncSynchronizer


class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, project_config, log_file_path=None):
        """Initialize file change handler for a specific project.

        Args:
            project_config (dict): Project configuration containing src, dst and exclude
            log_file_path (str, optional): Path to log file. Defaults to None.
        """
        super().__init__()
        self.project_config = project_config
        logger_instance = Logger(f"watcher_{project_config['name']}", log_file_path)
        self.logger = logger_instance.get_logger()
        self.synchronizer = RsyncSynchronizer(log_file_path)
        self.last_sync_time = 0
        self.cooldown_period = 2  # Cooldown period in seconds to avoid multiple syncs

    def on_any_event(self, event):
        """Handle any file system event.

        Args:
            event: File system event
        """
        # Skip directory events and temporary files
        if event.is_directory or self._is_temporary_file(event.src_path):
            return

        current_time = time.time()

        # Check if cooldown period has passed since last sync
        if current_time - self.last_sync_time >= self.cooldown_period:
            self.logger.info(f"Change detected: {event.event_type} - {event.src_path}")

            # Perform synchronization
            self.sync()
            self.last_sync_time = current_time

    def sync(self):
        """Perform synchronization for this project."""
        src_path = self.project_config["src"]
        dst_path = self.project_config["dst"]
        exclude_list = self.project_config.get("exclude", [])

        self.synchronizer.sync(src_path, dst_path, exclude_list)

    def _is_temporary_file(self, file_path):
        """Check if file is a temporary file.

        Args:
            file_path (str): Path to the file

        Returns:
            bool: True if it's a temporary file, False otherwise
        """
        temp_patterns = [".swp", ".tmp", "~", ".bak"]
        return any(file_path.endswith(pattern) for pattern in temp_patterns)


class DirectoryWatcher:
    def __init__(self, projects, log_file_path=None):
        """Initialize directory watcher for multiple projects.

        Args:
            projects (list): List of project configurations
            log_file_path (str, optional): Path to log file. Defaults to None.
        """
        logger_instance = Logger("directory_watcher", log_file_path)
        self.logger = logger_instance.get_logger()
        self.projects = projects
        self.observers = []
        self.handlers = []
        self.log_file_path = log_file_path

    def start_watching(self):
        """Start watching all project directories and perform initial sync."""
        for project in self.projects:
            try:
                src_path = project["src"]

                if not os.path.exists(src_path):
                    self.logger.error(f"Source directory does not exist: {src_path}")
                    continue

                # Create event handler for this project
                event_handler = FileChangeHandler(project, self.log_file_path)
                self.handlers.append(event_handler)

                # Perform initial synchronization for this project
                self.logger.info(
                    f"Performing initial sync for project: {project['name']}"
                )
                event_handler.sync()

                # Setup watching if enabled for this project
                watch_enabled = project.get(
                    "watch", False 
                )  # Default to True if not specified

                if watch_enabled:
                    # Create observer for this project
                    observer = Observer()
                    observer.schedule(event_handler, src_path, recursive=True)
                    observer.start()

                    self.observers.append(observer)

                    self.logger.info(
                        f"Started watching directory: {src_path} for project '{project['name']}'"
                    )
                else:
                    self.logger.info(
                        f"Watching disabled for project: {project['name']}"
                    )

            except Exception as e:
                self.logger.error(
                    f"Error setting up watcher for {project.get('name', 'unknown')}: {str(e)}"
                )

    def stop_watching(self):
        """Stop all directory watchers."""
        for observer in self.observers:
            observer.stop()

        for observer in self.observers:
            observer.join()

        self.logger.info("All directory watchers stopped")
