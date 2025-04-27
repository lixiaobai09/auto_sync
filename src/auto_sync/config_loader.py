import os
import yaml


class ConfigLoader:
    def __init__(self, config_path):
        """Initialize config loader with the path to the config file.

        Args:
            config_path (str): Path to the YAML configuration file
        """
        self.config_path = config_path
        self.config = None

    def load_config(self):
        """Load configuration from YAML file.

        Returns:
            dict: Configuration data

        Raises:
            FileNotFoundError: If config file doesn't exist
            yaml.YAMLError: If config file has invalid YAML syntax
        """
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Config file not found: {self.config_path}")

        with open(self.config_path, "r") as config_file:
            try:
                self.config = yaml.safe_load(config_file)
                return self.config
            except yaml.YAMLError as e:
                raise yaml.YAMLError(f"Error parsing config file: {e}")

    def get_projects(self):
        """Get the list of projects from the loaded configuration.

        Returns:
            list: List of project configurations
        """
        if not self.config:
            self.load_config()

        return self.config.get("projects", [])
