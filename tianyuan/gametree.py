class GameTreeNode:
    def __init__(self):
        self.properties = {}
    def add_property(self, identifier, value):
        self.properties[identifier] = value
        
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
    def get_children(self, node):
        return self.children[node]

class GameTreeBuilder:
    def __init__(self, game_tree):
        self.game_tree = game_tree
        self.last_node = None
        self.variation_stack = []
    def start_variation(self):
        self.variation_stack.append(self.last_node)
    def end_variation(self):
        self.last_node = self.variation_stack.pop()
    def add_node(self, node):
        self.game_tree.add_node(node, self.last_node)
        self.last_node = node
        
class DotFileBuilder(GameTreeBuilder):
    def __init__(self, _):
        self.next_label = 1
        self.edges = []
    def add_node(self, node):
        self.edges.append('    {} -> {};\n'.format(self.last_node, self.next_label))
        self.last_node = self.next_label
        self.next_label++
    def save(self, filename):
        dot_file = open(filename, 'w')
        dot_file.write('digraph ' + filename + ' {\n')
        for edge in self.edges:
            dot_file.write(edge)
        dot_file.write('}\n')
        dot_file.close()
