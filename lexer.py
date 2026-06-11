import re
from enum import Enum, auto

class TokenType(Enum):
    KEYWORD = auto()
    IDENTIFIER = auto()
    NUMBER = auto()
    ASSIGN = auto()
    OPERATOR = auto()
    LPAREN = auto()
    RPAREN = auto()
    SEMICOLON = auto()

class Token:
    def __init__(self, type_: TokenType, value: str):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"Token({self.type.name}, '{self.value}')"

# Regex rules for matching tokens sequentially
TOKEN_REGEX = [
    (TokenType.KEYWORD, r'^(if|else|while|return|int|float)\b'),
    (TokenType.IDENTIFIER, r'^[a-zA-Z_][a-zA-Z0-9_]*'),
    (TokenType.NUMBER, r'^\d+(\.\d+)?'),
    (TokenType.ASSIGN, r'^='),
    (TokenType.OPERATOR, r'^[+\-**/]'),
    (TokenType.LPAREN, r'^\('),
    (TokenType.RPAREN, r'^\)'),
    (TokenType.SEMICOLON, r'^;'),
]

class Lexer:
    def __init__(self, text: str):
        self.text = text
        self.position = 0

    def tokenize(self):
        tokens = []
        while self.position < len(self.text):
            # Skip whitespace
            whitespace_match = re.match(r'^\s+', self.text[self.position:])
            if whitespace_match:
                self.position += whitespace_match.end()
                continue

            matched = False
            current_substring = self.text[self.position:]
            
            for token_type, regex_pattern in TOKEN_REGEX:
                match = re.match(regex_pattern, current_substring)
                if match:
                    value = match.group(0)
                    tokens.append(Token(token_type, value))
                    self.position += len(value)
                    matched = True
                    break
            
            if not matched:
                raise SyntaxError(f"Illegal character at position {self.position}: '{self.text[self.position]}'")
        
        return tokens
