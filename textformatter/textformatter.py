# --- Imports ---
from collections.abc import Sequence
from enum import Enum
from typing import Self


# --- Private Constants ---
_BACKUP_FILE = "backup-file"
_BLANK_LINES = "blank-lines"
_LETTER_CASE = "letter-case"
_NEWLINE = "newline"
_TRIM = "trim"
_WHITESPACE = "whitespace"


# --- Classes ---

class BlankLineType(Enum):
    REMOVE = "remove"
    COLLAPSE = "collapse"


class CaseType(Enum):
    LOWER = "lower"
    UPPER = "upper"
#    TITLE = "title"  # TODO later due to complexity


class NewlineType(Enum):
    CR = "\r"
    CRLF = "\r\n"  # Windows
    LF = "\n"      # Unix, Linux, macOS
    SPACE = " "    # Replace with space
    REMOVE = ""

    def to_file_eol(self) -> str:
        if self == NewlineType.SPACE or self == NewlineType.REMOVE:
            return None
        return self.value

    @classmethod
    def from_text(cls,  text: str) -> Self:
        if text == "\\n":
            return NewlineType.LF
        if text == "\\r\\n":
            return NewlineType.CRLF
        if text == "\\r":
            return NewlineType.CR
        if text == "space":
            return NewlineType.SPACE
        if text == "remove":
            return NewlineType.REMOVE
        return None

    def to_text(self) -> str:
        if self == NewlineType.LF:
            return "\\n"
        if self == NewlineType.CRLF:
            return "\\r\\n"
        if self == NewlineType.CR:
            return "\\r"
        if self == NewlineType.SPACE:
            return "space"
        if self == NewlineType.REMOVE:
            return "remove"
        raise ValueError("Unsupported NewlineType")


class TrimType(Enum):
    LEADING = "leading"
    TRAILING = "trailing"
    ALL = "all"


class TextFormatterConfig:
    def __init__(self, *,
                 backup_file: bool=True,
                 blank_line_type: BlankLineType=None,
                 case_type: CaseType=None,
                 newline_type: NewlineType=None,
                 trim_type: TrimType=None) -> None:
        self.backup_file = backup_file
        self.blank_line_type = blank_line_type
        self.case_type = case_type
        self.newline_type = newline_type
        self.trim_type = trim_type

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        config = TextFormatterConfig()
        try:
            value = data.get(_BACKUP_FILE)
            if value is not None:
                value = value.lower()
                if value == "true":
                    config.backup_file = True
                elif value == "false":
                    config.backup_file = False
        except ValueError:
            pass
        try:
            config.case_type = CaseType(data.get(_LETTER_CASE))
        except ValueError:
            pass
        try:
            config.newline_type = NewlineType.from_text(data.get(_NEWLINE))
        except ValueError:
            pass
        whitespace_dict = data.get(_WHITESPACE)
        if whitespace_dict:
            try:
                config.blank_line_type = BlankLineType(
                    whitespace_dict.get(_BLANK_LINES)
                )
            except ValueError:
                pass
            try:
                config.trim_type = TrimType(whitespace_dict.get(_TRIM))
            except ValueError:
                pass
        return config

    def to_dict(self) -> dict:
        whitespace_dict = {}
        if self.blank_line_type is not None:
            whitespace_dict[_BLANK_LINES] = self.blank_line_type.value
        if self.trim_type is not None:
            whitespace_dict[_TRIM] = self.trim_type.value
        result = {}
        if self.backup_file is not None:
            result[_BACKUP_FILE] = str(self.backup_file).lower()
        if self.case_type is not None:
            result[_LETTER_CASE] = self.case_type.value
        if self.newline_type is not None:
            result[_NEWLINE] = self.newline_type.to_text()
        if whitespace_dict:
            result[_WHITESPACE] = whitespace_dict
        return result


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


def join_lines_to_text(lines: Sequence[str],
                       newline_type: NewlineType = NewlineType.LF) -> str:
    """
    Join lines of text using the specified newline character.

    Parameters:
    lines (Sequence[str]): The list of text lines to join.
    newline_type (NewlineType): The newline character(s) to use. Default
        value is linefeed character only.

    Returns:
    str: The joined text.
    """
    if not isinstance(newline_type, NewlineType):
        raise ValueError("Invalid NewlineType.")
    return str(newline_type.value).join(lines)


def read_lines_from_file(file_path: str) -> list[str]:
    """
    Read a file and then split its text into lines of text using the
    newline characters.

    Parameters:
    file_path (str): The file to read.

    Returns:
    list[str]: The list of text lines.
    """
    with open(file_path) as f:
        text = f.read()
    return split_text_to_lines(text)


def write_lines_to_file(file_path: str, lines: Sequence[str],
                        newline_type: NewlineType = NewlineType.LF) -> None:
    """
    Join lines of text using the specified newline character and write
    the text to a file.

    Parameters:
    file_path (str): The file to write to.
    lines (Sequence[str]): The list of text lines to join.
    newline_type (NewlineType): The newline character(s) to use. Default
        value is the linefeed character only.

    Returns:
    None
    """
    if not isinstance(newline_type, NewlineType):
        raise ValueError("Invalid NewlineType.")
    newline_value = newline_type.to_file_eol()
    if newline_value:
        # Use default newline for lines.
        # Write file will write the correct newline characters.
        text = join_lines_to_text(lines)
    else:
        # Join as a single line.
        text = join_lines_to_text(lines, newline_type)
    with open(file_path, "w", newline=newline_value) as f:
        f.write(text)


def remove_blank_lines(lines: Sequence[str],
                       blank_line_type: BlankLineType = None) -> list[str]:
    """
    Remove the blank lines using the specified option and return the
    result.

    Parameters:
    lines (Sequence[str]): The list of text lines to remove blank lines.
    blank_line_type (BlankLineType): The remove blank line option. Default
        value is None, which means no removal.

    Returns:
    The list of text lines with the blank lines removed.
    """
    if blank_line_type is None:
        return lines.copy()
    if blank_line_type == BlankLineType.REMOVE:
        return list(filter(lambda s: s, lines))
    if blank_line_type == BlankLineType.COLLAPSE:
        new_lines = []
        is_last_line_empty = False
        for line in lines:
            if line:
                new_lines.append(line)
                is_last_line_empty = False
            elif not is_last_line_empty:
                new_lines.append(line)
                is_last_line_empty = True
        return new_lines
    raise ValueError("Invalid BlankLineType")


# --- Public Line Whitespace Formatting Functions ---

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
    if trim_type is None:
        return line
    if trim_type == TrimType.LEADING:
        return line.lstrip()
    if trim_type == TrimType.TRAILING:
        return line.rstrip()
    if trim_type == TrimType.ALL:
        return line.strip()
    raise ValueError("Invalid TrimType")


# --- Public Line Text Formatting Functions ---

def convert_case(line: str, case_type: CaseType=None) -> str:
    """
    Convert the letter case of the line of text and return the result.

    Parameters:
    line (str): The line of text to convert.
    case_type (CaseType): The letter case option. Defaults to None,
        which means no conversion.

    Returns:
    str: The line of text with the letter case converted.
    """
    if case_type is None:
        return line
    if case_type == CaseType.LOWER:
        return line.lower()
    if case_type == CaseType.UPPER:
        return line.upper()
    raise ValueError("Invalid CaseType")

