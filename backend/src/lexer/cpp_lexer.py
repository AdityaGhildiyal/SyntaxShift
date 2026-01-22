"""
Lexer for C++ source code.
"""

from typing import List
from .base_lexer import BaseLexer
from .token import Token, TokenType, CPP_KEYWORDS


class CppLexer(BaseLexer):
    """
    Lexer specifically for C++ code.
    Handles C++-specific syntax like preprocessor directives and scope resolution.
    """
    
    def skip_multiline_comment(self) -> None:
        """Skip multi-line comment /* ... */"""
        self.advance()  # Skip *
        self.advance()  # Skip first char after /*
        
        while self.current_char:
            if self.current_char == '*' and self.peek() == '/':
                self.advance()  # Skip *
                self.advance()  # Skip /
                break
            self.advance()
    
    def handle_preprocessor(self) -> Token:
        """
        Handle preprocessor directives like #include, #define.
        
        Returns:
            Token representing the preprocessor directive
        """
        start_line = self.line
        start_column = self.column
        directive = ''
        
        self.advance()  # Skip #
        
        # Read directive name
        while self.current_char and self.is_alpha(self.current_char):
            directive += self.current_char
            self.advance()
        
        # Skip the rest of the line for now
        while self.current_char and self.current_char != '\n':
            self.advance()
        
        return Token(TokenType.KEYWORD, f'#{directive}', start_line, start_column)
    
    def tokenize(self) -> List[Token]:
        """
        Tokenize C++ source code.
        
        Returns:
            List of tokens
        """
        self.tokens = []
        
        while self.current_char is not None:
            # Skip whitespace
            if self.current_char in ' \t\n\r':
                self.skip_whitespace()
                if self.current_char == '\n':
                    self.advance()
                continue
            
            # Preprocessor directives
            if self.current_char == '#':
                self.tokens.append(self.handle_preprocessor())
                continue
            
            # Skip single-line comments
            if self.current_char == '/' and self.peek() == '/':
                self.skip_line()
                continue
            
            # Skip multi-line comments
            if self.current_char == '/' and self.peek() == '*':
                self.skip_multiline_comment()
                continue
            
            # Numbers
            if self.is_digit(self.current_char):
                self.tokens.append(self.read_number())
                continue
            
            # Strings (double quotes)
            if self.current_char == '"':
                self.tokens.append(self.read_string('"'))
                continue
            
            # Characters (single quotes)
            if self.current_char == "'":
                self.tokens.append(self.read_string("'"))
                continue
            
            # Identifiers and keywords
            if self.is_alpha(self.current_char):
                self.tokens.append(self.read_identifier(CPP_KEYWORDS))
                continue
            
            # Scope resolution operator ::
            if self.current_char == ':' and self.peek() == ':':
                self.tokens.append(self.make_token(TokenType.DOUBLE_COLON, '::'))
                self.advance()
                self.advance()
                continue
            
            # Two-character operators
            if self.current_char == '&' and self.peek() == '&':
                self.tokens.append(self.make_token(TokenType.AND, '&&'))
                self.advance()
                self.advance()
                continue
            
            if self.current_char == '|' and self.peek() == '|':
                self.tokens.append(self.make_token(TokenType.OR, '||'))
                self.advance()
                self.advance()
                continue
            
            if self.current_char == '=' and self.peek() == '=':
                self.tokens.append(self.make_token(TokenType.EQUAL, '=='))
                self.advance()
                self.advance()
                continue
            
            if self.current_char == '!' and self.peek() == '=':
                self.tokens.append(self.make_token(TokenType.NOT_EQUAL, '!='))
                self.advance()
                self.advance()
                continue
            
            if self.current_char == '<' and self.peek() == '=':
                self.tokens.append(self.make_token(TokenType.LESS_EQUAL, '<='))
                self.advance()
                self.advance()
                continue
            
            if self.current_char == '>' and self.peek() == '=':
                self.tokens.append(self.make_token(TokenType.GREATER_EQUAL, '>='))
                self.advance()
                self.advance()
                continue
            
            if self.current_char == '-' and self.peek() == '>':
                self.tokens.append(self.make_token(TokenType.ARROW, '->'))
                self.advance()
                self.advance()
                continue
            
            if self.current_char == '+' and self.peek() == '=':
                self.tokens.append(self.make_token(TokenType.PLUS_ASSIGN, '+='))
                self.advance()
                self.advance()
                continue
            
            if self.current_char == '-' and self.peek() == '=':
                self.tokens.append(self.make_token(TokenType.MINUS_ASSIGN, '-='))
                self.advance()
                self.advance()
                continue
            
            if self.current_char == '<' and self.peek() == '<':
                # << operator (stream insertion or left shift)
                self.tokens.append(self.make_token(TokenType.IDENTIFIER, '<<'))
                self.advance()
                self.advance()
                continue
            
            if self.current_char == '>' and self.peek() == '>':
                # >> operator (stream extraction or right shift)
                self.tokens.append(self.make_token(TokenType.IDENTIFIER, '>>'))
                self.advance()
                self.advance()
                continue
            
            # Single-character operators and delimiters
            single_char_tokens = {
                '+': TokenType.PLUS,
                '-': TokenType.MINUS,
                '*': TokenType.MULTIPLY,
                '/': TokenType.DIVIDE,
                '%': TokenType.MODULO,
                '=': TokenType.ASSIGN,
                '<': TokenType.LESS_THAN,
                '>': TokenType.GREATER_THAN,
                '!': TokenType.NOT,
                '&': TokenType.IDENTIFIER,  # Reference or address-of
                '(': TokenType.LPAREN,
                ')': TokenType.RPAREN,
                '{': TokenType.LBRACE,
                '}': TokenType.RBRACE,
                '[': TokenType.LBRACKET,
                ']': TokenType.RBRACKET,
                ',': TokenType.COMMA,
                ';': TokenType.SEMICOLON,
                ':': TokenType.COLON,
                '.': TokenType.DOT,
            }
            
            if self.current_char in single_char_tokens:
                token_type = single_char_tokens[self.current_char]
                self.tokens.append(self.make_token(token_type, self.current_char))
                self.advance()
                continue
            
            # Unknown character - skip it
            self.advance()
        
        # Add EOF token
        self.tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        
        return self.tokens