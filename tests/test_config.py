# --- Imports ---
import os
import unittest

from pathlib import Path

import textformatter
from textformatter import config
from textformatter.config import (
    # Classes,
    TextFormatterConfig,
    # Configuration file reading/writing functions
    read_config,
    write_config,
)


# --- Constants ---
TESTS_DIR: Path = Path(__file__).parent
DATA_DIR: Path = TESTS_DIR / "data"
OUTPUTS_DIR: Path = TESTS_DIR / "outputs"


# --- Test Classes for TextFormatterConfig ---

class TestTextFormatterConfigInit:
    def test_init_set_attributes(self):
        test_blank_line_type = BlankLineType.REMOVE
        test_case_type = CaseType.UPPER
        test_newline_type = NewLineType.CRLF
        test_trim_type = TrimType.ALL
        config = TextFormatterConfig(blank_line_type=test_blank_line_type,
                                     case_type=test_case_type,
                                     newline_type=test_newline_type,
                                     trim_type=test_trim_type)
        self.assertEqual(config.blank_line_type, test_blank_line_type)
        self.assertEqual(config.case_type, test_case_type)
        self.assertEqual(config.newline_type, test_newline_type)
        self.assertEqual(config.trim_type, test_trim_type)


# --- Test Classes for Reading/Writing Configuration Files ---

class TestReadConfig(unittest.TestCase):
    def test_read_config(self):
        config_data = read_config(DATA_DIR / "sample.yaml")
        self.assertFalse(config_data is None)
        self.assertEqual(len(config_data), 5)
        self.assertTrue("tutorial" in config_data)
        self.assertEqual(len(config_data["tutorial"]), 3)


class TestWriteConfig(unittest.TestCase):
    def test_write_config(self):
        file_path = OUTPUTS_DIR / "test_write.yaml"
        _delete_file(file_path)
        self.assertFalse(os.path.exists(file_path))
        config_data = {
            "name": "John Doe",
            "age": "30",
            "email": "john.doe@example.com",
        }
        write_config(file_path, config_data)
        self.assertTrue(os.path.exists(file_path))
        file_content = _read_file_content(file_path)
        self.assertTrue("30" in file_content)
        self.assertTrue("john.doe@example.com" in file_content)


# --- Helper Functions ---

def _delete_file(file_path: str) -> None:
    if os.path.exists(file_path):
        os.remove(file_path)


def _read_file_content(file_path: str) -> str:
    with open(file_path) as f:
        return f.read()
