from entities.token import Token

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if text else None

    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def peek(self):
        peek_pos = self.pos + 1
        return self.text[peek_pos] if peek_pos < len(self.text) else None

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        result = ""
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def string(self):
        result = ""
        self.advance()  # Skip opening quote
        while self.current_char is not None and self.current_char != '"':
            result += self.current_char
            self.advance()
        self.advance()  # Skip closing quote
        return result

    def identifier(self):
        result = ""
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        return result

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            if self.current_char.isalpha():
                ident = self.identifier()
                keywords = {
                    "int": "INT", "if": "IF", "while": "WHILE", "class": "CLASS",
                    "public": "PUBLIC", "private": "PRIVATE", "static": "STATIC",
                    "void": "VOID", "final": "FINAL", "String": "STRING_TYPE",
                    "return": "RETURN", "for": "FOR", "new": "NEW"
                }
                return Token(keywords.get(ident, "IDENTIFIER"), ident)
            if self.current_char.isdigit():
                return Token("NUMBER", self.integer())
            if self.current_char == '"':
                return Token("STRING", self.string())
            if self.current_char == '=':
                if self.peek() == '=':
                    self.advance()
                    self.advance()
                    return Token("EQUALS", "==")
                self.advance()
                return Token("ASSIGN", "=")
            if self.current_char in "+-*/":
                op = self.current_char
                self.advance()
                return Token("OPERATOR", op)
            if self.current_char == '<':
                self.advance()
                return Token("LESS_THAN", "<")
            if self.current_char == '>':
                self.advance()
                return Token("GREATER_THAN", ">")
            if self.current_char == ';':
                self.advance()
                return Token("SEMICOLON", ";")
            if self.current_char == '{':
                self.advance()
                return Token("LBRACE", "{")
            if self.current_char == '}':
                self.advance()
                return Token("RBRACE", "}")
            if self.current_char == '(':
                self.advance()
                return Token("LPAREN", "(")
            if self.current_char == ')':
                self.advance()
                return Token("RPAREN", ")")
            raise Exception(f"Invalid character: {self.current_char}")
        return Token("EOF", None)