class GameTreeNode:
    def __init__(self):
        self.properties = {}
    def property(self, identifier, value):
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
        self.parent_stack = []
    def add_variation(self):
        pass
    def add_node(self, node):
        pass
        

