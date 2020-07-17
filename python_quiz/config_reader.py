import os
import yaml
from typing import Union, Dict, Hashable, Any

config_file_path = os.getenv("APP_CONFIG_FILE")


def get_config() -> Union[Dict[Hashable, Any], list]:
    with open(config_file_path) as f:
        config = yaml.load(f, Loader=yaml.Loader)
        if not config:
            raise ValueError(f"Error reading config file {config_file_path}")
        return config

