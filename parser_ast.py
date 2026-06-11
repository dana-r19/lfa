from lexer import TokenType, Token

class ASTNode:
    def print_tree(self, indent=""):
        raise NotImplementedError()

class AssignNode(ASTNode):
    def __init__(self, identifier: str, expression: ASTNode):
        self.identifier = identifier
        self.expression = expression

    def print_tree(self, indent=""):
        print(f"{indent}Assignment: {self.identifier} =")
        self.expression.print_tree(indent + "  ")

class BinOpNode(ASTNode):
    def __init__(self, left: ASTNode, operator: str, right: ASTNode):
        self.left = left
        self.operator = operator
        self.right = right

    def print_tree(self, indent=""):
        print(f"{indent}BinaryOp: {self.operator}")
        self.left.print_tree(indent + "  ")
        self.right.print_tree(indent + "  ")

class VariableNode(ASTNode):
    def __init__(self, name: str):
        self.name = name

    def print_tree(self, indent=""):
        print(f"{indent}Identifier: {self.name}")

class NumberNode(ASTNode):
    def __init__(self, value: str):
        self.value = value

    def print_tree(self, indent=""):
        print(f"{indent}Number: {self.value}")

class Parser:
    def __init__(self, tokens: list):
        self.tokens = tokens
        self.pos = 0

    def peek(self) -> Token:
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def consume(self, expected_type: TokenType) -> Token:
        token = self.peek()
        if token and token.type == expected_type:
            self.pos += 1
            return token
        actual = token.type.name if token else "EOF"
        raise SyntaxError(f"Expected token {expected_type.name}, found: {actual}")

    def parse(self) -> ASTNode:
        # Top-level handler: handles syntax patterns starting with variable assignments
        if self.peek() and self.peek().type == TokenType.IDENTIFIER:
            if self.pos + 1 < len(self.tokens) and self.tokens[self.pos + 1].type == TokenType.ASSIGN:
                id_token = self.consume(TokenType.IDENTIFIER)
                self.consume(TokenType.ASSIGN)
                expr = self.parse_expression()
                if self.peek() and self.peek().type == TokenType.SEMICOLON:
                    self.consume(TokenType.SEMICOLON)
                return AssignNode(id_token.value, expr)
        return self.parse_expression()

    def parse_expression(self) -> ASTNode:
        # Handles low precedence binary arithmetic layers (+, -)
        left = self.parse_term()
        while self.peek() and self.peek().type == TokenType.OPERATOR and self.peek().value in ('+', '-'):
            op_token = self.consume(TokenType.OPERATOR)
            right = self.parse_term()
            left = BinOpNode(left, op_token.value, right)
        return left

    def parse_term(self) -> ASTNode:
        # Handles higher precedence binary arithmetic layers (*, /)
        left = self.parse_factor()
        while self.peek() and self.peek().type == TokenType.OPERATOR and self.peek().value in ('*', '/'):
            op_token = self.consume(TokenType.OPERATOR)
            right = self.parse_factor()
            left = BinOpNode(left, op_token.value, right)
        return left

    def parse_factor(self) -> ASTNode:
        # Lowest atomic elements (Integers, variable strings, parenthesis logic)
        token = self.peek()
        if token and token.type == TokenType.NUMBER:
            self.consume(TokenType.NUMBER)
            return NumberNode(token.value)
        elif token and token.type == TokenType.IDENTIFIER:
            self.consume(TokenType.IDENTIFIER)
            return VariableNode(token.value)
        elif token and token.type == TokenType.LPAREN:
            self.consume(TokenType.LPAREN)
            expr = self.parse_expression()
            self.consume(TokenType.RPAREN)
            return expr
        raise SyntaxError(f"Unexpected token in expression: {token}")
