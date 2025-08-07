# --- Imports ---
import os
import unittest

from pathlib import Path

import textformatter
from textformatter import textformatter
from textformatter.textformatter import (
    # Constants
    _BACKUP_FILE,
    _BLANK_LINES,
    _LETTER_CASE,
    _NEWLINE,
    _TRIM,
    _WHITESPACE,
    # Classes
    BlankLineType,
    CaseType,
    NewlineType,
    TrimType,
    TextFormatterConfig,
    # Document formatting functions
   split_text_to_lines,
    join_lines_to_text,
    read_lines_from_file,
    write_lines_to_file,
    remove_blank_lines,
    # Line whitespace formatting functions
    replace_spaces_with_tab,
    replace_tab_with_spaces,
    trim_line,
    # Line text formatting functions
    convert_case,
)


# --- Constants ---
TESTS_DIR: Path = Path(__file__).parent
DATA_DIR: Path = TESTS_DIR / "data"
OUTPUTS_DIR: Path = TESTS_DIR / "outputs"


# --- Test Classes for Enum Classes ---
class TestNewlineType(unittest.TestCase):
    def test_to_file_eol(self):
        self.assertEqual(NewlineType.CR.to_file_eol(), "\r")
        self.assertEqual(NewlineType.CRLF.to_file_eol(), "\r\n")
        self.assertEqual(NewlineType.LF.to_file_eol(), "\n")
        self.assertTrue(NewlineType.SPACE.to_file_eol() is None)
        self.assertTrue(NewlineType.REMOVE.to_file_eol() is None)

    def test_from_text(self):
        self.assertEqual(NewlineType.from_text("\\r"), NewlineType.CR)
        self.assertEqual(NewlineType.from_text("\\r\\n"), NewlineType.CRLF)
        self.assertEqual(NewlineType.from_text("\\n"), NewlineType.LF)
        self.assertEqual(NewlineType.from_text("space"), NewlineType.SPACE)
        self.assertEqual(NewlineType.from_text("remove"), NewlineType.REMOVE)

    def test_to_text(self):
        self.assertEqual(NewlineType.CR.to_text(), "\\r")
        self.assertEqual(NewlineType.CRLF.to_text(), "\\r\\n")
        self.assertEqual(NewlineType.LF.to_text(), "\\n")
        self.assertEqual(NewlineType.SPACE.to_text(), "space")
        self.assertEqual(NewlineType.REMOVE.to_text(), "remove")

# --- Test Classes for TextFormatterConfig ---

class TestTextFormatterConfigInit(unittest.TestCase):
    def test_init_set_attributes(self):
        test_blank_line_type = BlankLineType.REMOVE
        test_case_type = CaseType.UPPER
        test_newline_type = NewlineType.CRLF
        test_trim_type = TrimType.ALL
        config = TextFormatterConfig(backup_file=False,
                                     blank_line_type=test_blank_line_type,
                                     case_type=test_case_type,
                                     newline_type=test_newline_type,
                                     trim_type=test_trim_type)
        self.assertEqual(config.backup_file, False)
        self.assertEqual(config.blank_line_type, test_blank_line_type)
        self.assertEqual(config.case_type, test_case_type)
        self.assertEqual(config.newline_type, test_newline_type)
        self.assertEqual(config.trim_type, test_trim_type)


class TestTextFormatterConfigFromDict(unittest.TestCase):
    def test_dict(self):
        config_dict = {
            _BACKUP_FILE: "false",
            _NEWLINE: "\\n",
            _LETTER_CASE: "upper",
            _WHITESPACE: {
                _BLANK_LINES: "collapse",
                _TRIM: "all",
            },
        }
        config = TextFormatterConfig.from_dict(config_dict)
        self.assertTrue(config is not None)
        self.assertEqual(config.backup_file, False)
        self.assertEqual(config.blank_line_type, BlankLineType.COLLAPSE)
        self.assertEqual(config.case_type, CaseType.UPPER)
        self.assertEqual(config.newline_type, NewlineType.LF)
        self.assertEqual(config.trim_type, TrimType.ALL)

class TestTextFormatterConfigToDict(unittest.TestCase):
    def test_dict(self):
        config = TextFormatterConfig(
            backup_file=False,
            blank_line_type=BlankLineType.REMOVE,
            case_type=CaseType.LOWER,
            newline_type=NewlineType.CRLF,
            trim_type=TrimType.TRAILING,
            )
        config_dict = config.to_dict()
        self.assertEqual(config_dict.get(_BACKUP_FILE), "false")
        self.assertEqual(config_dict.get(_LETTER_CASE), "lower")
        self.assertEqual(config_dict.get(_NEWLINE), "\\r\\n")
        whitespace_dict = config_dict.get(_WHITESPACE)
        self.assertTrue(whitespace_dict is not None)
        self.assertEqual(whitespace_dict.get(_BLANK_LINES), "remove")
        self.assertEqual(whitespace_dict.get(_TRIM), "trailing")


# --- Test Classes for Document Formatting Functions ---

class TestSplitTextToLines(unittest.TestCase):
    def test_standard_text(self):
        text = "Line 1\nLine 2\n\nLine 4\n"
        lines = split_text_to_lines(text)
        self.assertListEqual(lines,
            [
                "Line 1",
                "Line 2",
                "",
                "Line 4",
            ]
        )

    def test_windows_text(self):
        text = "Line 1\r\n\r\nThis is Line 3\r\nLine 4\r\n"
        lines = split_text_to_lines(text)
        self.assertListEqual(lines,
            [
                "Line 1",
                "",
                "This is Line 3",
                "Line 4",
            ]
        )

    def test_mixed_text(self):
        text = "Line A\n\r\nThis is Line C\r\nLine D"
        lines = split_text_to_lines(text)
        self.assertListEqual(lines,
            [
                "Line A",
                "",
                "This is Line C",
                "Line D",
            ]
        )

    def test_no_text(self):
        text = ""
        lines = split_text_to_lines(text)
        self.assertListEqual(lines, [])


class TestJoinLinesToText(unittest.TestCase):
    def test_default_text(self):
        lines = [
            "Line 1",
            "Line 2",
            "",
            "Line 4",
        ]
        text = join_lines_to_text(lines)
        self.assertEqual(text, "Line 1\nLine 2\n\nLine 4")

    def test_lf_text(self):
        lines = [
            "Line 1",
            "Line 2",
            "",
            "Line 4",
        ]
        text = join_lines_to_text(lines, NewlineType.LF)
        self.assertEqual(text, "Line 1\nLine 2\n\nLine 4")

    def test_cr_lf_text(self):
        lines = [
                "Line 1",
                "",
                "This is Line 3",
                "Line 4",
            ]
        text = join_lines_to_text(lines, NewlineType.CRLF)
        self.assertEqual(text, "Line 1\r\n\r\nThis is Line 3\r\nLine 4")

    def test_cr_text(self):
        lines = [
            "Line A",
            "",
            "",
            "Line D",
        ]
        text = join_lines_to_text(lines, NewlineType.CR)
        self.assertEqual(text, "Line A\r\r\rLine D")

    def test_no_lines(self):
        lines = []
        text = join_lines_to_text(lines)
        self.assertEqual(text, "")

    def test_space(self):
        lines = [
            "Line 1",
            "Line 2",
            "",
            "Line 4",
        ]
        text = join_lines_to_text(lines, NewlineType.SPACE)
        self.assertEqual(text, "Line 1 Line 2  Line 4")

    def test_remove(self):
        lines = [
            "Line 1",
            "Line 2",
            "",
            "Line 4",
        ]
        text = join_lines_to_text(lines, NewlineType.REMOVE)
        self.assertEqual(text, "Line 1Line 2Line 4")


class TestReadLinesFromFile(unittest.TestCase):
    def test_read_linux_file(self):
        lines = read_lines_from_file(DATA_DIR / "read_file_linux.txt")
        self.assertEqual(len(lines), 11)
        self.assertTrue(lines[2].startswith("Lorem ipsum"))

    def test_read_windows_file(self):
        lines = read_lines_from_file(DATA_DIR / "read_file_windows.txt")
        self.assertEqual(len(lines), 5)
        self.assertTrue(lines[3].endswith("accumsan et."))


class TestWriteLinesToFile(unittest.TestCase):
    def test_write_linux_file(self):
        file_path = OUTPUTS_DIR / "write_file_linux.txt"
        _delete_file(file_path)
        self.assertFalse(os.path.exists(file_path))
        lines = [
            "Line 1",
            "Line 2",
            "",
            "Line 4",
        ]
        newline_type = NewlineType.LF
        write_lines_to_file(file_path, lines, newline_type)
        self.assertTrue(os.path.exists(file_path))
        file_content = _read_file_content(file_path, newline_type)
        self.assertEqual(file_content, "Line 1\nLine 2\n\nLine 4")

    def test_write_windows_file(self):
        file_path = OUTPUTS_DIR / "write_file_windows.txt"
        _delete_file(file_path)
        self.assertFalse(os.path.exists(file_path))
        if os.path.exists(file_path):
            os.remove(file_path)
        self.assertFalse(os.path.exists(file_path))
        lines = [
            "Line A",
            "",
            "Line C",
            "",
            "",
        ]
        newline_type = NewlineType.CRLF
        write_lines_to_file(file_path, lines, newline_type)
        self.assertTrue(os.path.exists(file_path))
        file_content = _read_file_content(file_path, newline_type)
        self.assertEqual(file_content, "Line A\r\n\r\nLine C\r\n\r\n")

    def test_write_replace_newline_with_space_file(self):
        file_path = OUTPUTS_DIR / "write_replace_newline_with_space.txt"
        _delete_file(file_path)
        self.assertFalse(os.path.exists(file_path))
        lines = [
            "Line 1",
            "Line 2",
            "",
            "Line 4",
        ]
        newline_type = NewlineType.SPACE
        write_lines_to_file(file_path, lines, newline_type)
        self.assertTrue(os.path.exists(file_path))
        file_content = _read_file_content(file_path, newline_type)
        self.assertEqual(file_content, "Line 1 Line 2  Line 4")

    def test_write_remove_newline_file(self):
        file_path = OUTPUTS_DIR / "write_remove_newline.txt"
        _delete_file(file_path)
        self.assertFalse(os.path.exists(file_path))
        lines = [
            "Line 1",
            "Line 2",
            "",
            "Line 4",
        ]
        newline_type = NewlineType.REMOVE
        write_lines_to_file(file_path, lines, newline_type)
        self.assertTrue(os.path.exists(file_path))
        file_content = _read_file_content(file_path, newline_type)
        self.assertEqual(file_content, "Line 1Line 2Line 4")

 
class TestRemoveBlankLines(unittest.TestCase):
    def test_default(self):
        lines = [
            "Line 1",
            "",
            "Line 3",
            "",
        ]
        new_lines = remove_blank_lines(lines)
        self.assertListEqual(new_lines, lines)

    def test_remove_all(self):
        lines = [
            "Line 1",
            "",
            "Line 3",
            "",
            "",
            "Line 6",
            "",
        ]
        new_lines = remove_blank_lines(lines, BlankLineType.REMOVE)
        self.assertListEqual(new_lines,
            [
                "Line 1",
                "Line 3",
                "Line 6",
            ]
        )

    def test_collpase(self):
        lines = [
            "Line 1",
            "",
            "Line 3",
            "",
            "",
            "",
            "Line 7",
            "",
            "",
        ]
        new_lines = remove_blank_lines(lines, BlankLineType.COLLAPSE)
        self.assertListEqual(new_lines,
            [
                "Line 1",
                "",
                "Line 3",
                "",
                "Line 7",
                "",
            ]
        )

    def test_empty_list(self):
        lines = []
        new_lines = remove_blank_lines(lines, BlankLineType.REMOVE)
        self.assertListEqual(new_lines, [])


# --- Test Classes for Line Whitespace Formatting Functions ---

class TestReplaceSpacesWithTab(unittest.TestCase):
    def test_replace_single_tab(self):
        line = "      Some text"
        new_line = replace_spaces_with_tab(line, 4)
        self.assertEqual(new_line, "\t  Some text")

    def test_replace_multiple_tabs(self):
        line = "     Some more text  "
        new_line = replace_spaces_with_tab(line, 2)
        self.assertEqual(new_line, "\t\t Some more text\t")

    def test_replace_single_spaces(self):
        line = "  A quick brown fox..."
        new_line = replace_spaces_with_tab(line, 1)
        self.assertEqual(new_line, "\t\tA\tquick\tbrown\tfox...")

    def test_empty_str(self):
        line = ""
        new_line = replace_spaces_with_tab(line, 4)
        self.assertEqual(new_line, "")

    def test_zero_number(self):
        line = "    An example"
        try:
            new_line = replace_spaces_with_tab(line, 0)
        except ValueError:
            pass
        except Exception:
            self.fail("Unexpected exception raised")
        else:
            self.fail("ValueError not raised")

    def test_negative_number(self):
        line = "    An example"
        try:
            new_line = replace_spaces_with_tab(line, -1)
        except ValueError:
            pass
        except Exception:
            self.fail("Unexpected exception raised")
        else:
            self.fail("ValueError not raised")


class TestReplaceTabWithSpaces(unittest.TestCase):
    def test_replace_single_tab(self):
        line = "\tSome text"
        new_line = replace_tab_with_spaces(line, 4)
        self.assertEqual(new_line, "    Some text")

    def test_replace_multiple_tabs(self):
        line = " \t  Some more text\t\t"
        new_line = replace_tab_with_spaces(line, 2)
        self.assertEqual(new_line, "     Some more text    ")

    def test_replace_tabs_with_no_space(self):
        line = "\tTest\ttext\t"
        new_line = replace_tab_with_spaces(line, 0)
        self.assertEqual(new_line, "Testtext")

    def test_empty_str(self):
        line = ""
        new_line = replace_tab_with_spaces(line, 4)
        self.assertEqual(new_line, "")

    def test_negative_number(self):
        line = "\tAn example"
        try:
            new_line = replace_tab_with_spaces(line, -1)
        except ValueError:
            pass
        except Exception:
            self.fail("Unexpected exception raised")
        else:
            self.fail("ValueError not raised")


class TestTrimLine(unittest.TestCase):
    def test_default(self):
        line = "   Default behaviour   "
        new_line = trim_line(line)
        self.assertEqual(new_line, line)

    def test_trim_leading(self):
        line = " \t  Trim leading test  \t "
        new_line = trim_line(line, TrimType.LEADING)
        self.assertEqual(new_line, "Trim leading test  \t ")

    def test_trim_trailing(self):
        line = "\t    Trim trailing example\t   "
        new_line = trim_line(line, TrimType.TRAILING)
        self.assertEqual(new_line, "\t    Trim trailing example")

    def test_trim_all(self):
        line = "  \t   Trim both ends    \t"
        new_line = trim_line(line, TrimType.ALL)
        self.assertEqual(new_line, "Trim both ends")

    def test_trim_empty_str(self):
        line = ""
        new_line = trim_line(line, TrimType.ALL)
        self.assertEqual(new_line, "")


# --- Test Classes for Line Text Formatting Functions ---

class TestConvertCase(unittest.TestCase):
    def test_default(self):
        line = "Hello world!"
        new_line = convert_case(line)
        self.assertEqual(new_line, line)

    def test_lowercase(self):
        line = "Hello world!"
        new_line = convert_case(line, CaseType.UPPER)
        self.assertEqual(new_line, "HELLO WORLD!")

    def test_uppercase(self):
        line = "Hello world!"
        new_line = convert_case(line, CaseType.LOWER)
        self.assertEqual(new_line, "hello world!")

    def test_empty_str(self):
        line = ""
        new_line = convert_case(line, CaseType.UPPER)
        self.assertEqual(new_line, "")


# --- Helper Functions ---

def _delete_file(file_path: str) -> None:
    if os.path.exists(file_path):
        os.remove(file_path)


def _read_file_content(file_path: str,
                       newline_type: NewlineType = None) -> str:
    if newline_type:
        newline_value = newline_type.to_file_eol()
    else:
        newline_value = None
    with open(file_path, newline=newline_value) as f:
        return f.read()

