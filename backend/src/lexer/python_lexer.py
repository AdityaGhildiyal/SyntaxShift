"""
Lexer for Python source code.
"""

from typing import List
from .base_lexer import BaseLexer
from .token import Token, TokenType, PYTHON_KEYWORDS


class PythonLexer(BaseLexer):
    """
    Lexer specifically for Python code.
    Handles Python-specific syntax like indentation and colons.
    """
    
    def __init__(self, source_code: str):
        super().__init__(source_code)
        self.indent_stack = [0]  # Stack to track indentation levels
    
    def skip_whitespace_inline(self) -> None:
        """Skip spaces and tabs but not newlines."""
        while self.current_char and self.current_char in ' \t':
            self.advance()
    
    def handle_indentation(self) -> List[Token]:
        """
        Handle Python indentation at the start of a line.
        
        Returns:
            List of INDENT or DEDENT tokens
        """
        tokens = []
        indent_level = 0
        
        # Count spaces/tabs
        while self.current_char and self.current_char in ' \t':
            if self.current_char == ' ':
                indent_level += 1
            elif self.current_char == '\t':
                indent_level += 4  # Treat tab as 4 spaces
            self.advance()
        
        # Compare with current indentation
        current_indent = self.indent_stack[-1]
        
        if indent_level > current_indent:
            # Increase indentation
            self.indent_stack.append(indent_level)
            tokens.append(Token(TokenType.INDENT, indent_level, self.line, 1))
        elif indent_level < current_indent:
            # Decrease indentation
            while self.indent_stack and self.indent_stack[-1] > indent_level:
                self.indent_stack.pop()
                tokens.append(Token(TokenType.DEDENT, indent_level, self.line, 1))
        
        return tokens
    
    def tokenize(self) -> List[Token]:
        """
        Tokenize Python source code.
        
        Returns:
            List of tokens
        """
        self.tokens = []
        at_line_start = True
        
        while self.current_char is not None:
            # Handle indentation at line start
            if at_line_start:
                # Ignore blank lines and comments for indentation
                if self.current_char not in ['\n', '#']:
                    indent_tokens = self.handle_indentation()
                    self.tokens.extend(indent_tokens)
                    at_line_start = False
                    
                    # If we consumed whitespace, we restart loop to check next char
                    # But if we didn't (0 indent), we fall through to process char
                    if self.current_char in ' \t':
                        continue
            
            # Skip whitespace (spaces, tabs)
            if self.current_char in ' \t':
                self.skip_whitespace_inline()
                continue
            
            # Handle newline
            if self.current_char == '\n':
                self.tokens.append(self.make_token(TokenType.NEWLINE, '\n'))
                self.advance()
                at_line_start = True
                continue
            
            at_line_start = False
            
            # Skip comments
            if self.current_char == '#':
                self.skip_line()
                continue
            
            # Numbers
            if self.is_digit(self.current_char):
                self.tokens.append(self.read_number())
                continue
            
            # F-strings (f"..." or f'...')
            if self.current_char in ('f', 'F') and self.peek(1) in ('"', "'"):
                self.advance()  # Skip 'f' or 'F'
                quote = self.current_char
                self.advance()  # Skip opening quote
                
                # Read f-string content
                parts = []  # Will store string parts and expressions
                current_part = ''
                
                while self.current_char and self.current_char != quote:
                    if self.current_char == '\\':
                        # Handle escape sequences
                        self.advance()
                        if self.current_char:
                            current_part += self.current_char
                            self.advance()
                    elif self.current_char == '{':
                        # Check for escaped brace
                        if self.peek(1) == '{':
                            current_part += '{'
                            self.advance()
                            self.advance()
                        else:
                            # Start of expression
                            if current_part:
                                parts.append(('string', current_part))
                                current_part = ''
                            
                            self.advance()  # Skip '{'
                            expr = ''
                            brace_depth = 1
                            while self.current_char and brace_depth > 0:
                                if self.current_char == '{':
                                    brace_depth += 1
                                elif self.current_char == '}':
                                    brace_depth -= 1
                                    if brace_depth == 0:
                                        break
                                expr += self.current_char
                                self.advance()
                            
                            if expr:
                                parts.append(('expr', expr))
                            self.advance()  # Skip '}'
                    elif self.current_char == '}':
                        # Check for escaped brace
                        if self.peek(1) == '}':
                            current_part += '}'
                            self.advance()
                            self.advance()
                        else:
                            # Unmatched closing brace - just include it
                            current_part += self.current_char
                            self.advance()
                    else:
                        current_part += self.current_char
                        self.advance()
                
                if current_part:
                    parts.append(('string', current_part))
                
                self.advance()  # Skip closing quote
                
                # Create F_STRING token with parts as value
                # The value is a list of tuples: [('string', 'text'), ('expr', 'variable'), ...]
                self.tokens.append(Token(TokenType.F_STRING, parts, self.line, self.column))
                continue
            
            # Strings (single or double quotes)
            if self.current_char in ('"', "'"):
                quote = self.current_char
                # Check for triple quotes
                if self.peek(1) == quote and self.peek(2) == quote:
                    # Triple quoted string
                    self.advance()  # First quote
                    self.advance()  # Second quote
                    self.advance()  # Third quote
                    string_val = ''
                    while self.current_char:
                        if (self.current_char == quote and 
                            self.peek(1) == quote and 
                            self.peek(2) == quote):
                            self.advance()
                            self.advance()
                            self.advance()
                            break
                        string_val += self.current_char
                        self.advance()
                    self.tokens.append(Token(TokenType.STRING, string_val, self.line, self.column))
                else:
                    self.tokens.append(self.read_string(quote))
                continue
            
            # Identifiers and keywords
            if self.is_alpha(self.current_char):
                self.tokens.append(self.read_identifier(PYTHON_KEYWORDS))
                continue
            
            # Two-character operators
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
            
            if self.current_char == '*' and self.peek() == '*':
                self.tokens.append(self.make_token(TokenType.POWER, '**'))
                self.advance()
                self.advance()
                continue
            
            if self.current_char == '/' and self.peek() == '/':
                self.tokens.append(self.make_token(TokenType.FLOOR_DIVIDE, '//'))
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
            
            if self.current_char == '-' and self.peek() == '>':
                self.tokens.append(self.make_token(TokenType.ARROW, '->'))
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
        
        # Add remaining DEDENT tokens
        while len(self.indent_stack) > 1:
            self.indent_stack.pop()
            self.tokens.append(Token(TokenType.DEDENT, 0, self.line, self.column))
        
        # Add EOF token
        self.tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        
        return self.tokens