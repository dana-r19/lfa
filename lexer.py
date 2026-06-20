import re
from .tokens import Token, TokenType

class Lexer:
    def __init__(self, source_code: str):
        self.source = source_code
        self.position = 0
        self.line = 1
        self.column = 1
        
        # Token specification: (regex pattern, token type, optional value transformer)
        self.token_specs = [
            (r'\s+', None, None),  # Skip whitespace
            (r'//.*', None, None),  # Skip single-line comments
            
            # Literals
            (r'\d+\.\d+', TokenType.FLOAT, float),
            (r'\d+', TokenType.INTEGER, int),
            (r'[a-zA-Z_][a-zA-Z0-9_]*', None, None),  # Handled separately for keywords
            
            # Operators
            (r'\+', TokenType.PLUS, lambda x: '+'),
            (r'-', TokenType.MINUS, lambda x: '-'),
            (r'\*', TokenType.MULTIPLY, lambda x: '*'),
            (r'/', TokenType.DIVIDE, lambda x: '/'),
            (r'\^', TokenType.POWER, lambda x: '^'),
            
            # Comparisons
            (r'==', TokenType.EQUALS, lambda x: '=='),
            (r'!=', TokenType.NOT_EQUALS, lambda x: '!='),
            (r'<', TokenType.LESS_THAN, lambda x: '<'),
            (r'>', TokenType.GREATER_THAN, lambda x: '>'),
            
            # Assignment and delimiters
            (r'=', TokenType.ASSIGN, lambda x: '='),
            (r'\(', TokenType.LPAREN, lambda x: '('),
            (r'\)', TokenType.RPAREN, lambda x: ')'),
            (r',', TokenType.COMMA, lambda x: ','),
            
            # Error fallback
            (r'.', TokenType.ERROR, lambda x: x),
        ]
        
        # Keywords (functions)
        self.keywords = {
            'sin': TokenType.SIN,
            'cos': TokenType.COS,
            'tan': TokenType.TAN,
        }
        
        self._compile_patterns()
    
    def _compile_patterns(self):
        """Compile all regex patterns into a single master regex"""
        patterns = []
        for regex, tok_type, _ in self.token_specs:
            if regex is not None:
                patterns.append(f"(?P<{tok_type.name if tok_type else 'SKIP'}> {regex})")
        self.master_regex = re.compile('|'.join(patterns), re.VERBOSE)
    
    def _get_token_type_and_value(self, match):
        """Determine token type and value from a regex match"""
        for regex, tok_type, transformer in self.token_specs:
            if regex is None:
                continue
            match_text = match.group(tok_type.name if tok_type else 'SKIP')
            if match_text is not None:
                if tok_type is None:  # Skip whitespace/comments
                    return None, None
                
                # Handle identifiers (check if keyword)
                if tok_type is None and regex == r'[a-zA-Z_][a-zA-Z0-9_]*':
                    if match_text in self.keywords:
                        tok_type = self.keywords[match_text]
                        return tok_type, match_text
                    else:
                        return TokenType.VARIABLE, match_text
                
                # Transform value if needed
                if transformer:
                    try:
                        value = transformer(match_text)
                    except:
                        value = match_text
                else:
                    value = match_text
                return tok_type, value
        return TokenType.ERROR, match.group(0)
    
    def get_next_token(self) -> Token:
        """Return the next token from the source code"""
        if self.position >= len(self.source):
            return Token(TokenType.EOF, None, self.line, self.column)
        
        # Match against master regex
        match = self.master_regex.match(self.source, self.position)
        if not match:
            # Unexpected character
            char = self.source[self.position]
            token = Token(TokenType.ERROR, char, self.line, self.column)
            self.position += 1
            self.column += 1
            return token
        
        # Update position and line/column info
        start_col = self.column
        matched_text = match.group(0)
        self.position = match.end()
        
        # Update line and column
        lines_in_match = matched_text.count('\n')
        if lines_in_match > 0:
            self.line += lines_in_match
            self.column = len(matched_text.split('\n')[-1]) + 1
        else:
            self.column += len(matched_text)
        
        # Determine token type and value
        tok_type, value = self._get_token_type_and_value(match)
        
        if tok_type is None:  # Skip token
            return self.get_next_token()
        
        return Token(tok_type, value, self.line - lines_in_match if lines_in_match else self.line, start_col)
    
    def tokenize(self):
        """Tokenize the entire source code"""
        tokens = []
        while True:
            token = self.get_next_token()
            tokens.append(token)
            if token.type == TokenType.EOF or token.type == TokenType.ERROR:
                break
        return tokens
