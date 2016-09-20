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
        self.assertEqual(self.parser.parse_property_identifier(b'A[test]'), (b'[test]', 'A'))
    def test_multiple_letters(self):
        self.assertEqual(self.parser.parse_property_identifier(b'AB[test]'), (b'[test]', 'AB'))
    def test_non_ucletter_first(self):
        with self.assertRaises(tianyuan.sgfparser.SGFParserError) as cm:
            self.parser.parse_property_identifier(b'a[test]')
        self.assertEqual(cm.exception.position, 0)
    def test_non_ucletter_last(self):
        self.assertEqual(self.parser.parse_property_identifier(b'Ab[test]'), (b'b[test]', 'A'))

class TestProperty(unittest.TestCase):
    def setUp(self):
        self.parser = tianyuan.sgfparser.SGFParser(tianyuan.gametree.DotFileBuilder)
    def test_single_value(self):
        self.assertEqual(self.parser.parse_property(b'A[test]'), (b'', 'A', [b'test']))
    def test_multiple_values(self):
        self.assertEqual(self.parser.parse_property(b'AB[test][2]'), (b'', 'AB', [b'test', b'2']))
    def test_illegal_identifier(self):
        with self.assertRaises(tianyuan.sgfparser.SGFParserError) as cm:
            self.parser.parse_property(b'Ab[test]')
        self.assertEqual(cm.exception.position, 1)

class TestNode(unittest.TestCase):
    def setUp(self):
        self.parser = tianyuan.sgfparser.SGFParser(tianyuan.gametree.DotFileBuilder)
    def test_single_value(self):
        pass

class TestSequence(unittest.TestCase):
    def setUp(self):
        self.parser = tianyuan.sgfparser.SGFParser(tianyuan.gametree.DotFileBuilder)
    def test_single_value(self):
        pass

class TestGameTree(unittest.TestCase):
    def setUp(self):
        self.parser = tianyuan.sgfparser.SGFParser(tianyuan.gametree.DotFileBuilder)
    def test_single_value(self):
        pass

class TestCollection(unittest.TestCase):
    def setUp(self):
        self.parser = tianyuan.sgfparser.SGFParser(tianyuan.gametree.DotFileBuilder)
    def test_single_value(self):
        pass

class TestHelpers(unittest.TestCase):
    def setUp(self):
        self.parser = tianyuan.sgfparser.SGFParser(tianyuan.gametree.DotFileBuilder)
    def test_single_value(self):
        pass

