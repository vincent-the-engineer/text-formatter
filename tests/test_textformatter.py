# --- Imports ---
import unittest

import textformatter
from textformatter import textformatter
from textformatter.textformatter import (
    TrimType,
    replace_spaces_with_tab,
    replace_tab_with_spaces,
    trim_line,
)


# --- Test Classes ---

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

    def test_no_trim(self):
        line = "   No trim please   "
        new_line = trim_line(line, TrimType.NONE)
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

