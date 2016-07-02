import arpeggio

def sgf_collection():
    return arpeggio.OneOrMore(sgf_game_tree), arpeggio.EOF
    
def sgf_game_tree():
    return '(', sgf_sequence, arpeggio.ZeroOrMore(sgf_game_tree), ')'
    
def sgf_sequence():
    return arpeggio.OneOrMore(sgf_node)
    
def sgf_node():
    return ';', arpeggio.ZeroOrMore(sgf_property)
    
def sgf_property():
    return sgf_property_identifier, arpeggio.OneOrMore(sgf_property_value)

def sgf_property_identifier():
    return arpeggio.OneOrMore(sgf_uppercase_letter)
    
def sgf_property_value():
    return '[', sgf_compose_or_value_type, ']'

def sgf_compose_or_value_type():
    return arpeggio.ZeroOrMore(sgf_value_type)
#    return [sgf_value_type, sgf_compose]
    
def sgf_value_type():
    return arpeggio.RegExMatch(r'[^\]]')
#    return [sgf_none, sgf_number, sgf_real, sgf_double, sgf_color, sgf_simple_text, sgf_text, sgf_point, sgf_move, sgf_stone]
    
def sgf_uppercase_letter():
    return arpeggio.RegExMatch('[A-Z]')
    
parser = arpeggio.ParserPython(sgf_collection, debug = True)
parser.parse(open('test.sgf', 'r').read())

