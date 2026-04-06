from src.lexer import Lexer
from src.tokens import TokenType

def demo():
    test_codes = [
        # Basic arithmetic
        "x = 3.14 + 5",
        
        # Trigonometric function
        "result = sin(45) + cos(30)",
        
        # Comparison
        "a == b != c < d > e",
        
        # Complex expression
        "value = tan( (2.5 + 3) / 4 ) ^ 2",
        
        # With comments
        """
        // This is a comment
        theta = 90
        answer = sin(theta) * cos(theta)
        """
    ]
    
    for code in test_codes:
        print(f"\n{'='*60}")
        print(f"Source code:\n{code.strip()}")
        print(f"\nTokens:")
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        for token in tokens:
            if token.type != TokenType.EOF:
                print(f"  {token}")

if __name__ == "__main__":
    demo()
