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
    def test_empty_node(self):
        self.assertEqual(self.parser.parse_node(b';', tianyuan.gametree.DotFileBuilder()), b'')
    def test_single_property(self):
        self.assertEqual(self.parser.parse_node(b';A[test]', tianyuan.gametree.DotFileBuilder()), b'')
    def test_multiple_properties(self):
        self.assertEqual(self.parser.parse_node(b';A[test]B[test]C[test]', tianyuan.gametree.DotFileBuilder()), b'')
    def test_illegal_node(self):
        with self.assertRaises(tianyuan.sgfparser.SGFParserError) as cm:
            self.parser.parse_node(b'A[test]', tianyuan.gametree.DotFileBuilder())
        self.assertEqual(cm.exception.position, 0)

class TestSequence(unittest.TestCase):
    def setUp(self):
        self.parser = tianyuan.sgfparser.SGFParser(tianyuan.gametree.DotFileBuilder)
    def test_single_node(self):
        self.assertEqual(self.parser.parse_sequence(b';A[test]', tianyuan.gametree.DotFileBuilder()), b'')
    def test_multiple_nodes(self):
        self.assertEqual(self.parser.parse_sequence(b';A[test];B[test];C[test]', tianyuan.gametree.DotFileBuilder()), b'')

class TestGameTree(unittest.TestCase):
    def setUp(self):
        self.parser = tianyuan.sgfparser.SGFParser(tianyuan.gametree.DotFileBuilder)
    def test_single_sequence(self):
        self.assertEqual(self.parser.parse_game_tree(b'(;A[test];B[test];C[test])', tianyuan.gametree.DotFileBuilder()), b'')
    def test_single_variation(self):
        self.assertEqual(self.parser.parse_game_tree(b'(;A[test](;B[test];C[test]))', tianyuan.gametree.DotFileBuilder()), b'')
    def test_variations(self):
        self.assertEqual(self.parser.parse_game_tree(b'(;A[test](;B[test])(;C[test]))', tianyuan.gametree.DotFileBuilder()), b'')
    def test_sequence_after_variation(self):
        with self.assertRaises(tianyuan.sgfparser.SGFParserError) as cm:
            self.parser.parse_game_tree(b'(;A[test](;B[test]);C[test])', tianyuan.gametree.DotFileBuilder())
        self.assertEqual(cm.exception.position, 19)

class TestCollection(unittest.TestCase):
    def setUp(self):
        self.parser = tianyuan.sgfparser.SGFParser(tianyuan.gametree.DotFileBuilder)
    def test_single_game_tree(self):
        self.assertEqual(len(self.parser.parse_collection(b'(;A[test];B[test];C[test])')), 1)
    def test_multiple_game_trees(self):
        self.assertEqual(len(self.parser.parse_collection(b'(;A[test];B[test];C[test])(;A[test];B[test];C[test])')), 2)
    def test_trailing_garbage(self):
        with self.assertRaises(tianyuan.sgfparser.SGFParserError) as cm:
            self.parser.parse_collection(b'(;A[test](;B[test])(;C[test]))test')
        self.assertEqual(cm.exception.position, 30)

class TestHelpers(unittest.TestCase):
    def setUp(self):
        self.parser = tianyuan.sgfparser.SGFParser(tianyuan.gametree.DotFileBuilder)
    def test_parse_file(self):
        self.parser.parse_file('tests/test.sgf')
    def test_skipping_whitespace(self):
        pass
    def test_not_skipping_chars(self):
        pass
    def test_consume_single_byte(self):
        pass
    def test_consume_multiple_bytes(self):
        pass

