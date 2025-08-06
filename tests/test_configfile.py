# --- Imports ---
import os
import unittest

from pathlib import Path

import textformatter
from textformatter import configfile
from textformatter import textformatter
from textformatter.configfile import (
    # Configuration file reading/writing functions
    read_config_file,
    write_config_file,
)
from textformatter.textformatter import (
   # Classes
    BlankLineType,
    CaseType,
    NewlineType,
    TrimType,
    TextFormatterConfig,
)


# --- Constants ---
TESTS_DIR: Path = Path(__file__).parent
DATA_DIR: Path = TESTS_DIR / "data"
OUTPUTS_DIR: Path = TESTS_DIR / "outputs"


# --- Test Classes for Reading/Writing Configuration Files ---

class TestReadConfig(unittest.TestCase):
    def test_read_config_file(self):
        config_data = read_config_file(DATA_DIR / "test_read_config.yaml")
        self.assertFalse(config_data is None)
        self.assertEqual(config_data.newline_type, NewlineType.CRLF)
        self.assertEqual(config_data.case_type, CaseType.LOWER)
        self.assertEqual(config_data.trim_type, TrimType.TRAILING)
        self.assertEqual(config_data.blank_line_type, BlankLineType.REMOVE)

class TestWriteConfig(unittest.TestCase):
    def test_write_config_file(self):
        file_path = OUTPUTS_DIR / "test_write_config.yaml"
        _delete_file(file_path)
        self.assertFalse(os.path.exists(file_path))
        config_data = TextFormatterConfig(
            blank_line_type=BlankLineType.COLLAPSE,
            case_type=CaseType.UPPER,
            newline_type=NewlineType.LF,
            trim_type=TrimType.ALL,
        )
        write_config_file(file_path, config_data)
        self.assertTrue(os.path.exists(file_path))
        file_content = _read_file_content(file_path)
        self.assertTrue("blank-lines: collapse" in file_content)
        self.assertTrue("letter-case: upper" in file_content)
        self.assertTrue("newline: \\n" in file_content)
        self.assertTrue("trim: all" in file_content)


# --- Helper Functions ---

def _delete_file(file_path: str) -> None:
    if os.path.exists(file_path):
        os.remove(file_path)


def _read_file_content(file_path: str) -> str:
    with open(file_path) as f:
        return f.read()
