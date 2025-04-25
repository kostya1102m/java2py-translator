from entities.token import Token
from entities.node import Node

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            raise Exception(f"Expected {token_type}, got {self.current_token.type}")

    def peek(self):
        current_pos = self.lexer.pos
        current_char = self.lexer.current_char
        next_token = self.lexer.get_next_token()
        self.lexer.pos = current_pos
        self.lexer.current_char = current_char
        return next_token.value

    def factor(self):
        token = self.current_token
        if token.type == "NUMBER":
            self.eat("NUMBER")
            return Node("NUMBER", token.value)
        elif token.type == "STRING":
            self.eat("STRING")
            return Node("STRING", token.value)
        elif token.type == "IDENTIFIER":
            self.eat("IDENTIFIER")
            if self.current_token.type == "LPAREN":
                self.eat("LPAREN")
                args = []
                if self.current_token.type != "RPAREN":
                    args.append(self.expression())
                    while self.current_token.type == "COMMA":
                        self.eat("COMMA")
                        args.append(self.expression())
                self.eat("RPAREN")
                return Node("CALL", token.value, children=args)
            return Node("IDENTIFIER", token.value)
        raise Exception("Expected NUMBER, STRING, or IDENTIFIER")

    def term(self):
        node = self.factor()
        while self.current_token.type == "OPERATOR" and self.current_token.value in "*/":
            op = self.current_token.value
            self.eat("OPERATOR")
            node = Node(op, children=[node, self.factor()])
        return node

    def expression(self):
        node = self.term()
        while self.current_token.type == "OPERATOR" and self.current_token.value in "+-":
            op = self.current_token.value
            self.eat("OPERATOR")
            node = Node(op, children=[node, self.term()])
        return node

    def comparison(self):
        node = self.expression()
        if self.current_token.type in ["EQUALS", "LESS_THAN", "GREATER_THAN"]:
            op = self.current_token.value
            self.eat(self.current_token.type)
            node = Node(op, children=[node, self.expression()])
        return node

    def variable_declaration(self):
        if self.current_token.type in ["INT", "STRING_TYPE"]:
            var_type = self.current_token.value
            self.eat(self.current_token.type)
            var_name = self.current_token.value
            self.eat("IDENTIFIER")
            if self.current_token.type == "ASSIGN":
                self.eat("ASSIGN")
                expr = self.expression()
                return Node("ASSIGN", var_name, children=[expr])
            return Node("DECLARE", var_name)
        raise Exception("Expected variable declaration")

    def statement(self):
        if self.current_token.type in ["INT", "STRING_TYPE"]:  # Variable declaration
            node = self.variable_declaration()
            self.eat("SEMICOLON")
            return node
        elif self.current_token.type == "IDENTIFIER":  # Class type or method call
            type_name = self.current_token.value
            self.eat("IDENTIFIER")
            if self.current_token.type == "IDENTIFIER":  # e.g., ComplexExample example
                var_name = self.current_token.value
                self.eat("IDENTIFIER")
                self.eat("ASSIGN")
                if self.current_token.type == "NEW":
                    self.eat("NEW")
                    class_name = self.current_token.value
                    self.eat("IDENTIFIER")
                    self.eat("LPAREN")
                    self.eat("RPAREN")
                    self.eat("SEMICOLON")
                    return Node("ASSIGN", var_name, children=[Node("NEW", class_name)])
                else:
                    expr = self.expression()
                    self.eat("SEMICOLON")
                    return Node("ASSIGN", var_name, children=[expr])
            elif self.current_token.type == "LPAREN":  # Method call
                self.eat("LPAREN")
                args = []
                if self.current_token.type != "RPAREN":
                    args.append(self.expression())
                    while self.current_token.type == "COMMA":
                        self.eat("COMMA")
                        args.append(self.expression())
                self.eat("RPAREN")
                self.eat("SEMICOLON")
                return Node("CALL", type_name, children=args)
        elif self.current_token.type == "IF":
            self.eat("IF")
            self.eat("LPAREN")
            condition = self.comparison()
            self.eat("RPAREN")
            self.eat("LBRACE")
            body = self.statements()
            self.eat("RBRACE")
            return Node("IF", children=[condition, body])
        elif self.current_token.type == "WHILE":
            self.eat("WHILE")
            self.eat("LPAREN")
            condition = self.comparison()
            self.eat("RPAREN")
            self.eat("LBRACE")
            body = self.statements()
            self.eat("RBRACE")
            return Node("WHILE", children=[condition, body])
        elif self.current_token.type == "FOR":
            self.eat("FOR")
            self.eat("LPAREN")
            init = self.variable_declaration()
            self.eat("SEMICOLON")
            condition = self.comparison()
            self.eat("SEMICOLON")
            update = self.expression()
            self.eat("RPAREN")
            self.eat("LBRACE")
            body = self.statements()
            self.eat("RBRACE")
            return Node("FOR", children=[init, condition, update, body])
        elif self.current_token.type == "RETURN":
            self.eat("RETURN")
            expr = self.expression()
            self.eat("SEMICOLON")
            return Node("RETURN", children=[expr])
        raise Exception(f"Unexpected token: {self.current_token.type}")

    def statements(self):
        nodes = []
        while self.current_token.type not in ["RBRACE", "EOF"]:
            nodes.append(self.statement())
        return Node("BLOCK", children=nodes)

    def field_declaration(self):
        modifiers = []
        while self.current_token.type in ["PUBLIC", "PRIVATE", "STATIC", "FINAL"]:
            modifiers.append(self.current_token.value)
            self.eat(self.current_token.type)
        
        type_token = self.current_token.value if self.current_token.type in ["INT", "STRING_TYPE"] else self.current_token.type
        self.eat(self.current_token.type)
        
        name = self.current_token.value
        self.eat("IDENTIFIER")
        if self.current_token.type == "ASSIGN":
            self.eat("ASSIGN")
            value = self.expression()
            self.eat("SEMICOLON")
            return Node("FIELD", name, children=[value], modifiers=modifiers)
        self.eat("SEMICOLON")
        return Node("FIELD", name, modifiers=modifiers)

    def method(self):
        modifiers = []
        while self.current_token.type in ["PUBLIC", "PRIVATE", "STATIC"]:
            modifiers.append(self.current_token.value)
            self.eat(self.current_token.type)
        
        # Изменение здесь: обрабатываем как тип токена, так и значение для примитивных типов
        return_type = self.current_token.value if self.current_token.type in ["INT", "STRING_TYPE", "VOID"] else self.current_token.type
        self.eat(self.current_token.type)
        
        name = self.current_token.value
        self.eat("IDENTIFIER")
        self.eat("LPAREN")
        params = []
        if self.current_token.type != "RPAREN":
            param_type = self.current_token.value if self.current_token.type in ["INT", "STRING_TYPE"] else self.current_token.type
            self.eat(self.current_token.type)
            param_name = self.current_token.value
            self.eat("IDENTIFIER")
            params.append((param_type, param_name))
            while self.current_token.type == "COMMA":
                self.eat("COMMA")
                param_type = self.current_token.value if self.current_token.type in ["INT", "STRING_TYPE"] else self.current_token.type
                self.eat(self.current_token.type)
                param_name = self.current_token.value
                self.eat("IDENTIFIER")
                params.append((param_type, param_name))
        self.eat("RPAREN")
        self.eat("LBRACE")
        body = self.statements()
        self.eat("RBRACE")
        return Node("METHOD", name, children=[body], modifiers=modifiers, params=params)

    def class_member(self):
        if self.current_token.type in ["PUBLIC", "PRIVATE", "STATIC", "FINAL"]:
            next_value = self.peek()
            if next_value in ["int", "String"]:
                return self.field_declaration()
            return self.method()
        elif self.current_token.type in ["INT", "STRING_TYPE", "VOID"]:
            return self.method()
        raise Exception("Expected field or method declaration")

    def program(self):
        if self.current_token.type == "CLASS":
            self.eat("CLASS")
            class_name = self.current_token.value
            self.eat("IDENTIFIER")
            self.eat("LBRACE")
            members = []
            while self.current_token.type != "RBRACE":
                members.append(self.class_member())
            self.eat("RBRACE")
            return Node("CLASS", class_name, children=members)
        return self.statements()