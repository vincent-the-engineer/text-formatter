import unittest

import textformatter
from textformatter import textformatter
from textformatter.textformatter import (
    TrimType,
    trim_line,
)


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

