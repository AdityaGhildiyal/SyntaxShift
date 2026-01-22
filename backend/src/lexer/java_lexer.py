"""
Lexer for Java source code.
"""

from typing import List
from .base_lexer import BaseLexer
from .token import Token, TokenType, JAVA_KEYWORDS


class JavaLexer(BaseLexer):
    """
    Lexer specifically for Java code.
    Handles Java-specific syntax like multi-line comments and type declarations.
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
    
    def tokenize(self) -> List[Token]:
        """
        Tokenize Java source code.
        
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
            
            # Strings (double quotes) and characters (single quotes)
            if self.current_char == '"':
                self.tokens.append(self.read_string('"'))
                continue
            
            if self.current_char == "'":
                # Java char literal
                self.tokens.append(self.read_string("'"))
                continue
            
            # Identifiers and keywords
            if self.is_alpha(self.current_char):
                self.tokens.append(self.read_identifier(JAVA_KEYWORDS))
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
            
            if self.current_char == '+' and self.peek() == '=':
                self.tokens.append(self.make_token(TokenType.PLUS_ASSIGN, '+='))
                self.advance()
                self.advance()
                continue
            
            if self.current_char == '+' and self.peek() == '+':
                self.tokens.append(self.make_token(TokenType.INCREMENT, '++'))
                self.advance()
                self.advance()
                continue
            
            if self.current_char == '-' and self.peek() == '=':
                self.tokens.append(self.make_token(TokenType.MINUS_ASSIGN, '-='))
                self.advance()
                self.advance()
                continue
            
            if self.current_char == '-' and self.peek() == '-':
                self.tokens.append(self.make_token(TokenType.DECREMENT, '--'))
                self.advance()
                self.advance()
                continue
            
            if self.current_char == '<' and self.peek() == '<':
                self.tokens.append(self.make_token(TokenType.LSHIFT, '<<'))
                self.advance()
                self.advance()
                continue
                
            if self.current_char == '>' and self.peek() == '>':
                self.tokens.append(self.make_token(TokenType.RSHIFT, '>>'))
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