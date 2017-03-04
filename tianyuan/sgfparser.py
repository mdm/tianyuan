import string
import tianyuan.gametree

class SGFParserError(Exception):
    def __init__(self, position, message):
        self.position = position
        self.message = message

class SGFSemanticError(Exception):
    def __init__(self, message):
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
        while sgf_data and (sgf_data[0:1].decode('ascii') in string.whitespace):
            sgf_data = self.consume(sgf_data, 1)
        return sgf_data
    def parse_file(self, filename):
        sgf_file = open(filename, 'rb')
        sgf_data = sgf_file.read()
        sgf_file.close()
        return self.parse_collection(sgf_data)
    def parse_collection(self, sgf_data):
        collection = []
        builder = self.builder_class()
        sgf_data = self.parse_game_tree(sgf_data, builder)
        while True:
            game_tree = builder.get_game_tree()
            self.check_semantics(game_tree)
            collection.append(game_tree)
            try:
                builder = self.builder_class()
                sgf_data = self.parse_game_tree(sgf_data, builder)
            except SGFParserError:
                break
        sgf_data = self.skip_whitespace(sgf_data)
        if sgf_data:
            raise SGFParserError(self.bytes_consumed, 'Expected end-of-file while parsing collection.')
        return collection
    def parse_game_tree(self, sgf_data, builder):
        sgf_data = self.skip_whitespace(sgf_data)
        if sgf_data and sgf_data[0:1] == b'(':
            sgf_data = self.consume(sgf_data, 1)
            builder.start_variation()
            sgf_data = self.parse_sequence(sgf_data, builder)
            while True:
                try:
                    sgf_data = self.parse_game_tree(sgf_data, builder)
                except SGFParserError:
                    break
            sgf_data = self.skip_whitespace(sgf_data)
            if sgf_data and sgf_data[0:1] == b')':
                sgf_data = self.consume(sgf_data, 1)
                builder.end_variation()
            else:
                raise SGFParserError(self.bytes_consumed, 'Expected ")" while parsing game tree.')
        else:
            raise SGFParserError(self.bytes_consumed, 'Expected "(" while parsing game tree.')
        return sgf_data
    def parse_sequence(self, sgf_data, builder):
        sgf_data = self.parse_node(sgf_data, builder)
        while True:
            try:
                sgf_data = self.parse_node(sgf_data, builder)
            except SGFParserError:
                break
        return sgf_data
    def parse_node(self, sgf_data, builder):
        sgf_data = self.skip_whitespace(sgf_data)
        if sgf_data and sgf_data[0:1] == b';':
            sgf_data = self.consume(sgf_data, 1)
            game_tree_node = tianyuan.gametree.GameTreeNode()
            while True:
                try:
                    sgf_data, identifier, values = self.parse_property(sgf_data)
                    if identifier in game_tree_node.properties:
                        raise SGFSemanticError('Duplicate property in the same node.')
                    else:
                        game_tree_node.properties[identifier] = values
                except SGFParserError:
                    break
            builder.add_node(game_tree_node)
        else:
            raise SGFParserError(self.bytes_consumed, 'Expected ";" while parsing node.')
        return sgf_data
    def parse_property(self, sgf_data):
        values = []
        sgf_data, identifier = self.parse_property_identifier(sgf_data)
        sgf_data, value = self.parse_property_value(sgf_data)
        values.append(value)
        while True:
            try:
                sgf_data, value = self.parse_property_value(sgf_data)
                values.append(value)
            except SGFParserError:
                break
        return sgf_data, identifier, values
    def parse_property_identifier(self, sgf_data):
        identifier = b''
        sgf_data = self.skip_whitespace(sgf_data)
        if sgf_data and (sgf_data[0:1].decode('ascii') in string.ascii_uppercase):
            identifier += sgf_data[0:1]
            sgf_data = self.consume(sgf_data, 1)
            while sgf_data and (sgf_data[0:1].decode('ascii') in string.ascii_uppercase):
                identifier += sgf_data[0:1]
                sgf_data = self.consume(sgf_data, 1)
        else:
            raise SGFParserError(self.bytes_consumed, 'Expected uppercase letter while parsing property identifier.')
        return sgf_data, identifier.decode('ascii')
    def parse_property_value(self, sgf_data):
        value = b''
        sgf_data = self.skip_whitespace(sgf_data)
        if sgf_data and sgf_data[0:1] == b'[':
            sgf_data = self.consume(sgf_data, 1)
            while sgf_data and sgf_data[0:1] != b']':
                if sgf_data[0:1] == b'\\':
                    sgf_data = self.consume(sgf_data, 1)
                    # remove "soft" line breaks
                    if sgf_data and sgf_data[0:1] == b'\n': 
                        sgf_data = self.consume(sgf_data, 1)
                        if sgf_data and sgf_data[0:1] == b'\r': 
                            sgf_data = self.consume(sgf_data, 1)
                    elif sgf_data and sgf_data[0:1] == b'\r': 
                        sgf_data = self.consume(sgf_data, 1)
                        if sgf_data and sgf_data[0:1] == b'\n': 
                            sgf_data = self.consume(sgf_data, 1)
                if sgf_data:
                    value += sgf_data[0:1]
                    sgf_data = self.consume(sgf_data, 1)
            if sgf_data:
                sgf_data = self.consume(sgf_data, 1)
            else:
                raise SGFParserError(self.bytes_consumed, 'Expected "]" while parsing property value.')
        else:
            raise SGFParserError(self.bytes_consumed, 'Expected "[" while parsing property value.')
        return sgf_data, value
    def check_semantics(self, game_tree):
        if 'SZ' in game_tree.get_root().properties:
            game_tree.get_root().properties['SZ'][0] = self.validate_alternative(self.validate_composed(self.validate_number, self.validate_number), self.validate_number, game_tree.get_root().properties['SZ'][0])
        else:
            game_tree.get_root().properties['SZ'] = [19]
        if 'CA' in game_tree.get_root().properties:
            self.validate_simple_text(game_tree.get_root().properties['CA'][0])
        else:
            game_tree.get_root().properties['CA'] = ['iso-8859-1']
        self.check_node(game_tree.get_root(), game_tree)
    def check_node(self, node, game_tree):
        for property in node.properties:
            self.check_property(property, node, game_tree)
            # TODO: delete faulty properties
        print('\n')
        for child in game_tree.get_children(node):
            self.check_node(child, game_tree)
    def check_property(self, property, node, game_tree):
        print(property)
        print(repr(node.properties[property]))
        # TODO: check for superfluous values
        if property in ['DM', 'GB', 'GW', 'HO', 'UC', 'BM', 'TE']: # value type double
            node.properties[property][0] = self.validate_double(node.properties[property][0])
        if property in ['PL']: # value type color
            node.properties[property][0] = self.validate_color(node.properties[property][0])
        if property in ['B', 'W']: # value type stone, point or move
            node.properties[property][0] = self.validate_coordinate(node.properties[property][0])
        if property in ['AB', 'AE', 'AW', 'CR', 'MA', 'SL', 'SQ', 'TR']: # value type list of stone, point or move
            if node.properties[property] > 0:
                node.properties[property] = [self.convert_coordinate(value.decode('ascii')) for value in node.properties[property]]
            else:
                raise SGFSemanticError('List of value of property \'{property}\' must not be empty.')
        if property in ['DD', 'VW', 'TW', 'TB']: # value type possibly empty list of stone, point or move
            node.properties[property] = [self.convert_coordinate(value.decode('ascii')) for value in node.properties[property]]
    def validate_double(self, value):
        if value == b'1' or value == b'2':
            return int(value)
        else:
            raise SGFSemanticError('Value must be \'1\' or \'2\'.')
    def validate_color(self, value):
        if value == b'B' or value == b'W':
            return value.decode('ascii')
        else:
            raise SGFSemanticError('Value must be \'B\' or \'W\'.')
    def validate_coordinate(self, value):
        try:
            value = value.decode('ascii')
            coordinates = 'abcdefghijklmnopqrstuvwxyzABCEFGHIJKLMNOPQRSTUVWXYZ'
            board_size = game_tree.get_root().properties['SZ']
            if value == '' or (len(board_size) == 1 and board_size[0] <= 19) or (len(board_size) == 2 and board_size[0] <= 19 and board_size[1] <= 19): # via get root prop
                coordinate = None
            else:
                coordinate = (coordinates.index(value[0]), coordinates.index(value[1]))
            return coordinate
        except ValueError:
            raise SGFSemanticError('Value of property \'{property}\' must be a legal board coordinate.')    def validate_number(self, value):
        pass
    def validate_number(self, value):
        try:
            value = value.decode('ascii')
            return int(value)
        except ValueError:
            raise SGFSemanticError('Value must be an integer.')
    def validate_real(self, value):
        try:
            value = value.decode('ascii')
            return float(value)
        except ValueError:
            raise SGFSemanticError('Value must be a floating point number.')
    def validate_text(self, value, encoding = 'iso-8859-1'):
        value = value.decode(charset)
        lines = re.split('\r\n|\n\r|\r|\n', value)
        lines = [re.sub('\s', ' ', line) for line in lines]
        return '\n'.join(lines)
    def validate_simple_text(self, value, encoding = 'iso-8859-1'):
        value = self.validate_text(value, encoding)
        return re.sub('\n', ' ', value)
    def validate_list_or_none(self, values):
        return [element_validator(value) for value in values]
    def validate_list(self, element_validator, values):
        return [element_validator(value) for value in values]
    def validate_composed(self, value):
        pass
    def validate_alternative(self, value):
        pass

