import collections

class GameTreeNode:
    def __init__(self):
        self.properties = collections.OrderedDict()

class GameTree:
    def __init__(self):
        self.root = None
        self.children = {}
    def add_node(self, node, parent = None):
        if parent:
            self.children.setdefault(parent, []).append(node)
        else:
            self.root = node
    def remove_node(self, node):
        del(self.children[node])
    def get_root(self):
        return self.root
    def get_children(self, node):
        return self.children.setdefault(node, [])
    def set_root_property(self, identifier, values):
        self.root.properties[identifier] = values
    def get_root_property(self, identifier):
        return self.root.properties[identifier]

class GameTreeBuilder:
    def __init__(self):
        self.game_tree = GameTree()
        self.last_node = None
        self.variation_stack = []
    def start_variation(self):
        self.variation_stack.append(self.last_node)
    def end_variation(self):
        self.last_node = self.variation_stack.pop()
    def add_node(self, node):
        self.game_tree.add_node(node, self.last_node)
        self.last_node = node
    def get_game_tree(self):
        return self.game_tree
        
class DotFileBuilder(GameTreeBuilder):
    def __init__(self):
        super().__init__()
        self.next_label = 1
        self.edges = []
    def add_node(self, _):
        if self.last_node:
            self.edges.append('    {} -> {};\n'.format(self.last_node, self.next_label))
        self.last_node = self.next_label
        self.next_label += 1
    def get_game_tree(self):
        filename = 'tests/test.dot'
        dot_file = open(filename, 'w')
        dot_file.write('digraph ' + 'test' + ' {\n')
        for edge in self.edges:
            dot_file.write(edge)
        dot_file.write('}\n')
        dot_file.close()
        game_tree = GameTree()
        game_tree.add_node({})
        return game_tree
