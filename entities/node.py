class Node:
    def __init__(self, type, value=None, children=None, modifiers=None):
        self.type = type
        self.value = value
        self.children = children if children is not None else []
        self.modifiers = modifiers if modifiers is not None else []

    def add_child(self, child):
        self.children.append(child)