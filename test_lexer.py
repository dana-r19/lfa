import unittest
from src.lexer import Lexer
from src.tokens import TokenType

class TestLexer(unittest.TestCase):
    def test_integer(self):
        lexer = Lexer("42")
        tokens = lexer.tokenize()
        self.assertEqual(tokens[0].type, TokenType.INTEGER)
        self.assertEqual(tokens[0].value, 42)
    
    def test_float(self):
        lexer = Lexer("3.1415")
        tokens = lexer.tokenize()
        self.assertEqual(tokens[0].type, TokenType.FLOAT)
        self.assertEqual(tokens[0].value, 3.1415)
    
    def test_trig_functions(self):
        lexer = Lexer("sin(30) + cos(45) - tan(60)")
        tokens = lexer.tokenize()
        types = [t.type for t in tokens]
        self.assertIn(TokenType.SIN, types)
        self.assertIn(TokenType.COS, types)
        self.assertIn(TokenType.TAN, types)
    
    def test_comparisons(self):
        lexer = Lexer("a == b != c < d > e")
        tokens = lexer.tokenize()
        types = [t.type for t in tokens]
        self.assertIn(TokenType.EQUALS, types)
        self.assertIn(TokenType.NOT_EQUALS, types)
        self.assertIn(TokenType.LESS_THAN, types)
        self.assertIn(TokenType.GREATER_THAN, types)
    
    def test_comment_skip(self):
        lexer = Lexer("42 // this is a comment\n+ 5")
        tokens = lexer.tokenize()
        self.assertEqual(tokens[0].type, TokenType.INTEGER)
        self.assertEqual(tokens[1].type, TokenType.PLUS)
        self.assertEqual(tokens[2].type, TokenType.INTEGER)

if __name__ == '__main__':
    unittest.main()
