import os
import subprocess
from .logger import Logger


class RsyncSynchronizer:
    def __init__(self, log_file_path="logs/sync.log"):
        """Initialize the rsync synchronizer.

        Args:
            log_file_path (str, optional): Path to log file. Defaults to "logs/sync.log".
        """
        logger_instance = Logger("synchronizer", log_file_path)
        self.logger = logger_instance.get_logger()

    def sync(self, src_path, dst_path, exclude_list=None):
        """Synchronize source directory to destination using rsync.

        Args:
            src_path (str): Source directory path
            dst_path (str): Destination directory path
            exclude_list (list, optional): List of patterns to exclude. Defaults to None.

        Returns:
            bool: True if sync successful, False otherwise
        """
        if not os.path.exists(src_path):
            self.logger.error(f"Source path does not exist: {src_path}")
            return False

        # Construct rsync command
        rsync_cmd = ["rsync", "-aP"]

        # Add exclude patterns if provided
        if exclude_list:
            for pattern in exclude_list:
                rsync_cmd.extend(["--exclude", pattern])

        # Add source and destination paths
        rsync_cmd.extend([src_path, dst_path])

        self.logger.info(f"Executing rsync command: {' '.join(rsync_cmd)}")

        try:
            # Execute rsync command
            process = subprocess.Popen(
                rsync_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )

            # Get output
            stdout, stderr = process.communicate()

            # Check if command was successful
            if process.returncode == 0:
                self.logger.info(f"Sync successful from {src_path} to {dst_path}")
                self.logger.debug(f"Rsync output: {stdout}")
                return True
            else:
                self.logger.error(f"Sync failed with error code {process.returncode}")
                self.logger.error(f"Error: {stderr}")
                return False

        except Exception as e:
            self.logger.error(f"Exception during sync: {str(e)}")
            return False
