from enum import Enum, auto
from dataclasses import dataclass

class TokenType(Enum):
    # Literals
    INTEGER = auto()
    FLOAT = auto()
    VARIABLE = auto()
    
    # Operators
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    POWER = auto()
    
    # Comparison
    EQUALS = auto()          # ==
    NOT_EQUALS = auto()      # !=
    LESS_THAN = auto()
    GREATER_THAN = auto()
    
    # Functions
    SIN = auto()
    COS = auto()
    TAN = auto()
    
    # Delimiters
    LPAREN = auto()
    RPAREN = auto()
    COMMA = auto()
    ASSIGN = auto()           # =
    
    # Special
    EOF = auto()
    ERROR = auto()

@dataclass
class Token:
    type: TokenType
    value: any
    line: int
    column: int
    
    def __repr__(self):
        return f"Token({self.type.name}, {repr(self.value)}, line={self.line}, col={self.column})"
