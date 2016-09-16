import string
import gametree

class SGFParserError(Exception):
    def __init__(self, position, message):
        self.position = position
        self.message = message

class SGFParser:
    def __init__(self, builder_class):
        self.builder_class = builder_class
        self.bytes_consumed = 0
    def consume(self, sgf_data, count):
        sgf_data = sgf_data[count:]
        self.bytes_consumed += count
        return sgf_data
    def skip_whitespace(self, sgf_data):
        while sgf_data and (sgf_data[0].decode('ascii') in string.whitespace):
            sgf_data = consume(sgf_data, 1)
        return sgf_data
    def parse_file(self, filename):
        sgf_file = open(filename, 'rb')
        sgf_data = sgf_file.read()
        sgf_file.close()
        return parse_collection(sgf_data)
    def parse_collection(self, sgf_data):
        collection = []
        sgf_data, game_tree = parse_game_tree(sgf_data)
        while True:
            collection.append(game_tree)
            try:
                sgf_data, game_tree = parse_game_tree(sgf_data)
            except SGFParserError:
                break
        sgf_data = skip_whitespace(sgf_data)
        if sgf_data:
            raise SGFParserError(self.bytes_consumed, 'Expected end-of-file while parsing collection.')
        return collection
    def parse_game_tree(self, sgf_data, builder = None):
        game_tree = None
        sgf_data = skip_whitespace(sgf_data)
        if sgf_data and sgf_data[0] == b'(':
            sgf_data = consume(sgf_data, 1)
            if not builder:
                game_tree = gametree.GameTree()
                builder = self.builder_class(game_tree)
            builder.start_variation()
            sgf_data = parse_sequence(sgf_data, builder)
            while True:
                try:
                    sgf_data, _ = parse_game_tree(sgf_data, builder)
                except SGFParserError:
                    break
            sgf_data = skip_whitespace(sgf_data)
            if sgf_data and sgf_data[0] == b')':
                sgf_data = consume(sgf_data, 1)
                builder.end_variation()
            else:
                raise SGFParserError(self.bytes_consumed, 'Expected ")" while parsing game tree.')
        else:
            raise SGFParserError(self.bytes_consumed, 'Expected "(" while parsing game tree.')
        return sgf_data, game_tree
    def parse_sequence(self, sgf_data, builder):
        sgf_data = parse_node(sgf_data, builder)
        while True:
            try:
                sgf_data = parse_node(sgf_data, builder)
            except SGFParserError:
                break
    def parse_node(self, sgf_data, builder):
        sgf_data = skip_whitespace(sgf_data)
        if sgf_data and sgf_data[0] == b';':
            sgf_data = consume(sgf_data, 1)
            game_tree_node = gametree.GameTreeNode()
            while True:
                try:
                    sgf_data, identifier, values = parse_property(sgf_data)
                    #TODO update node
                except SGFParserError:
                    break
            builder.add_node(game_tree_node)
        else:
            raise SGFParserError(self.bytes_consumed, 'Expected ";" while parsing node.')
    def parse_property(self, sgf_data):
        sgf_data = skip_whitespace(sgf_data)

