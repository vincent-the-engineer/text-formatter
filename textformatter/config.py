# --- Imports ---
import yaml

from textformatter.textformatter import (
    BlankLineType,
    CaseType,
    NewlineType,
    TrimType,
)


# --- Private Constants ---
_BLANK_LINES = "blank-lines"
_LETTER_CASE = "letter-case"
_NEWLINE = "newline"
_TRIM = "trim"
_WHITESPACE = "whitespace"


# --- Classes ---
class TextFormatterConfig:
    def __init__(self, *, blank_line_type=None, case_type=None,
                 newline_type=None, trim_type=None):
        self.blank_line_type = blank_line_type
        self.case_type = case_type
        self.newline_type = newline_type
        self.trim_type = trim_type

    def __dict__(self):
        whitespace_dict = {}
        if self.BlankLineType is not None:
            whitespace_dict[_BLANK_LINES] = self.BlankLineType.value
        if self.TrimType is not None:
            whitespace_dict[_TRIM] = self.TrimType.value
        result = {}
        if self.CaseType is not None:
            result[_LETTER_CASE] = self.CaseType.value
        if self.NewLineType is not None:
            result[_NEWLINE] = self.NewLineType.value
        if whitespace_dict:
            result[_WHITESPACE] = whitespace_dict
        return result


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

