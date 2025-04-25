from entities.node import Node

class CodeGenerator:
    def __init__(self):
        self.indent_level = 0

    def indent(self):
        return "    " * self.indent_level

    def generate(self, node):
        if node.type == "ASSIGN":
            return f"{self.indent()}{node.value} = {self.generate(node.children[0])}"
        elif node.type == "NEW":
            return f"{node.value}()"
        elif node.type == "CALL":
            args = ", ".join(self.generate(arg) for arg in node.children)
            return f"{node.value}({args})"
        elif node.type == "ASSIGN":
            return f"{self.indent()}{node.value} = {self.generate(node.children[0])}"
        elif node.type == "NUMBER":
            return str(node.value)
        elif node.type == "STRING":
            return f'"{node.value}"'
        elif node.type == "IDENTIFIER":
            return node.value
        elif node.type in "+-*/":
            return f"{self.generate(node.children[0])} {node.type} {self.generate(node.children[1])}"
        elif node.type in ["==", "<", ">"]:
            return f"{self.generate(node.children[0])} {node.type} {self.generate(node.children[1])}"
        elif node.type == "IF":
            self.indent_level += 1
            body = self.generate(node.children[1])
            self.indent_level -= 1
            return f"{self.indent()}if {self.generate(node.children[0])}:\n{body}"
        elif node.type == "WHILE":
            self.indent_level += 1
            body = self.generate(node.children[1])
            self.indent_level -= 1
            return f"{self.indent()}while {self.generate(node.children[0])}:\n{body}"
        elif node.type == "BLOCK":
            return "\n".join(self.generate(child) for child in node.children)
        elif node.type == "FIELD":
            if node.children:
                return f"{self.indent()}{node.value} = {self.generate(node.children[0])}"
            return f"{self.indent()}{node.value} = None"
        elif node.type == "METHOD":
            self.indent_level += 1
            body = self.generate(node.children[0])
            self.indent_level -= 1
            params = ", ".join(param[1] for param in node.params)
            return f"{self.indent()}def {node.value}({params}):\n{body}"
        elif node.type == "CALL":
            args = ", ".join(self.generate(arg) for arg in node.children)
            return f"{node.value}({args})"
        elif node.type == "CLASS":
            self.indent_level += 1
            members = "\n\n".join(self.generate(child) for child in node.children)
            self.indent_level -= 1
            return f"class {node.value}:\n{members}"
        elif node.type == "FOR":
            self.indent_level += 1
            init = self.generate(node.children[0])
            condition = self.generate(node.children[1])
            update = self.generate(node.children[2])
            body = self.generate(node.children[3])
            self.indent_level -= 1
            # Convert Java for loop to Python equivalent (using while for simplicity)
            return f"{init}\n{self.indent()}while {condition}:\n{body}\n{self.indent()}{update}"
        elif node.type == "RETURN":
            return f"{self.indent()}return {self.generate(node.children[0])}"