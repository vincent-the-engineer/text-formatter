# --- Imports ---
import yaml

import textformatter
from textformatter import textformatter
from textformatter.textformatter import TextFormatterConfig


# --- Public Configuration File Reading/Writing Functions ---

def read_config_file(file_path: str) -> TextFormatterConfig:
    """
    Read a YAML configuration file and return the configuration data.

    Parameters:
    file_path (str): The file to read.

    Returns:
    TextFormatterConfig: The text-formatter configuration object.
    """
    with open(file_path) as f:
        data = yaml.safe_load(f)
    config_data = TextFormatterConfig.from_dict(data)
    return config_data


def write_config_file(file_path: str, config_data: TextFormatterConfig) -> None:
    """
    Write the configuration data to a YAML configuration file.

    Parameters:
    file_path (str): The file to write to.
    config_data (TextFormatterConfig): The text-formatter configuration object
        to write.

    Returns:
    None
    """
    with open(file_path, "w") as f:
        yaml.safe_dump(config_data.to_dict(), f, default_flow_style=False)

