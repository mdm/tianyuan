import unittest

import tianyuan.gametree
import tianyuan.sgfparser

class TestPropertyValue(unittest.TestCase):
    def setUp(self):
        self.parser = tianyuan.sgfparser.SGFParser(tianyuan.gametree.DotFileBuilder)
    def test_empty_value(self):
        self.assertEqual(self.parser.parse_property_value(b'[]'), (b'', b''))
    def test_simple_value(self):
        self.assertEqual(self.parser.parse_property_value(b'[test]'), (b'', b'test'))
    def test_leading_whitespace(self):
        self.assertEqual(self.parser.parse_property_value(b' \n \t [test]'), (b'', b'test'))
    def test_escaped_chars(self):
        self.assertEqual(self.parser.parse_property_value(b'[t\:e\\\\s\]t]'), (b'', b't:e\\s]t'))
    def test_trailing_chars(self):
        self.assertEqual(self.parser.parse_property_value(b'[test]abc'), (b'abc', b'test'))
    def test_unexpected_start(self):
        with self.assertRaises(tianyuan.sgfparser.SGFParserError) as cm:
            self.parser.parse_property_value(b'test]')
        self.assertEqual(cm.exception.position, 0)
    def test_unexpected_end(self):
        with self.assertRaises(tianyuan.sgfparser.SGFParserError) as cm:
            self.parser.parse_property_value(b'[test')
        self.assertEqual(cm.exception.position, 5)

class TestPropertyIdentifier(unittest.TestCase):
    def setUp(self):
        self.parser = tianyuan.sgfparser.SGFParser(tianyuan.gametree.DotFileBuilder)
    def test_single_letter(self):
        pass
    def test_multiple_letters(self):
        pass
    def test_non_letter_first(self):
        pass
    def test_non_letter_last(self):
        pass

