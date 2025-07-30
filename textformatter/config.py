# --- Imports ---
import yaml


# --- Public Configuration File Reading/Writing Functions ---

def read_config(file_path: str) -> object:
    """
    Read a YAML configuration file and return the configuration data.

    Parameters:
    file_path (str): The file to read.

    Returns:
    object: The object representing the configuration data.
    """
    with open(file_path) as f:
        config_data = yaml.safe_load(f)
    return config_data


def write_config(file_path: str, config_data: object) -> None:
    """
    Write the configuration data to a YAML configuration file.

    Parameters:
    file_path (str): The file to write to.
    config_data (object): The object representing the configuration data.

    Returns:
    None
    """
    with open(file_path, "w") as f:
        yaml.safe_dump(config_data, f, default_flow_style=False)

