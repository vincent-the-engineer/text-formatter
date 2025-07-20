from enum import Enum


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


def trim_line(line: str, trim_type: TrimType = None) -> str:
    """
    Trim the leading and/or trailing whitespace of a line of text and
    returns the result.

    Parameters:
    line (str): The line of text to trim.
    trim_type (TrimType): The trim option, defaults to None which means no
        trimming.

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

