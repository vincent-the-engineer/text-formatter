# --- Imports ---
from enum import Enum


# --- Classes ---

class NewlineType(Enum):
    CR = "\r"
    CRLF = "\r\n"  # Windows
    LF = "\n"      # Unix, Linux, macOS
    LFCR = "\n\r"

class TrimType(Enum):
    NONE = "none"
    LEADING = "leading"
    TRAILING = "trailing"
    ALL = "all"


# --- Public Document Formatting Functions ---

def split_text_to_lines(text: str) -> list[str]:
    """
    Split text into lines of text using the newline characters.

    Parameters:
    text (str): The text to split.

    Returns:
    list[str]: The list of text lines.
    """
    return text.splitlines()


def join_lines_to_text(lines: list[str],
                       newline_type: NewlineType = NewlineType.LF) -> str:
    """
    Join lines of text using the specified newline character.

    Parameters:
    lines (list[str]): The list of text lines to join.

    Returns:
    str: The joined text.
    """
    if not isinstance(newline_type, NewlineType):
        raise ValueError("Invalid NewlineType.")
    return str(newline_type.value).join(lines)


#def convert_file_to_lines(file_path: str) -> list[str]:
#    with open(file_path) as f:
#        text = f.read()
#    return text_to_lines(text)
#    pass


#def convert_lines_to_file(file_path: str, lines: list[str]) -> None:
#    pass


# --- Public Line Formatting Functions ---

def replace_spaces_with_tab(line: str, num_spaces: int) -> str:
    """
    Replace consecutive space characters in a line of text with tabs
    instead and return the result.

    Parameters:
    line (str): The line of text to replace tabs.
    num_spaces (int): The number of spaces for each tab character.

    Returns:
    str: The line of text with the spaces replaced.
    """
    if num_spaces < 1:
        raise ValueError("The number of spaces must be a positive"
                         f" integer: ({num_spaces}).")
    return line.replace(" " * num_spaces, "\t")


def replace_tab_with_spaces(line: str, num_spaces: int) -> str:
    """
    Replace the tab characters in a line of text with spaces instead
    and return the result.

    Parameters:
    line (str): The line of text to replace tabs.
    num_spaces (int): The number of spaces for each tab character.

    Returns:
    str: The line of text with the tab characters replaced.
    """
    if num_spaces < 0:
        raise ValueError("The number of spaces must be a non-zero"
                         f" integer: ({num_spaces}).")
    return line.replace("\t", " " * num_spaces)


def trim_line(line: str, trim_type: TrimType = None) -> str:
    """
    Trim the leading and/or trailing whitespace of a line of text and
    return the result.

    Parameters:
    line (str): The line of text to trim.
    trim_type (TrimType): The trim option. Defaults to None, which means
        no trimming.

    Returns:
    str: The trimmed line of text.
    """
    if trim_type is None or trim_type == TrimType.NONE:
        return line
    if trim_type == TrimType.LEADING:
        return line.lstrip()
    if trim_type == TrimType.TRAILING:
        return line.rstrip()
    if trim_type == TrimType.ALL:
        return line.strip()
    raise ValueError("Invalid TrimType")

