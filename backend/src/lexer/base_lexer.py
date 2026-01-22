"""
Base lexer class with common functionality.
"""

from typing import List, Optional, Set, Any
from abc import ABC, abstractmethod
from .token import Token, TokenType


class BaseLexer(ABC):
    """
    Abstract base class for all lexers.
    Provides common methods for character consumption and token creation.
    """
    
    def __init__(self, source_code: str):
        self.source_code = source_code
        self.length = len(source_code)
        self.pos = 0
        self.line = 1
        self.column = 1
        self.current_char = self.source_code[0] if self.length > 0 else None
        self.tokens: List[Token] = []

    def advance(self) -> None:
        """Advance the 'pos' pointer and set the 'current_char' variable."""
        self.pos += 1
        if self.pos < self.length:
            self.current_char = self.source_code[self.pos]
            self.column += 1
        else:
            self.current_char = None

    def peek(self, offset: int = 1) -> Optional[str]:
        """Peek at the character at 'offset' positions ahead."""
        peek_pos = self.pos + offset
        if peek_pos < self.length:
            return self.source_code[peek_pos]
        return None

    def skip_whitespace(self) -> None:
        """Skip whitespace characters."""
        while self.current_char is not None and self.current_char in ' \t\r':
            self.advance()

    def skip_line(self) -> None:
        """Skip the rest of the current line (for single-line comments)."""
        while self.current_char is not None and self.current_char != '\n':
            self.advance()

    def is_digit(self, char: str) -> bool:
        """Check if character is a digit."""
        return char.isdigit()

    def is_alpha(self, char: str) -> bool:
        """Check if character is alphabetic or underscore."""
        return char.isalpha() or char == '_'

    def is_alnum(self, char: str) -> bool:
        """Check if character is alphanumeric or underscore."""
        return char.isalnum() or char == '_'

    def read_number(self) -> Token:
        """Read a number (integer or float)."""
        start_line = self.line
        start_column = self.column
        result = ''
        is_float = False
        
        while self.current_char is not None and (self.is_digit(self.current_char) or self.current_char == '.'):
            if self.current_char == '.':
                if is_float:
                    break  # Second decimal point
                is_float = True
            
            result += self.current_char
            self.advance()
            
        if is_float:
            return Token(TokenType.FLOAT, float(result), start_line, start_column)
        return Token(TokenType.INTEGER, int(result), start_line, start_column)

    def read_string(self, quote_char: str) -> Token:
        """Read a string literal enclosed in quote_char."""
        start_line = self.line
        start_column = self.column
        result = ''
        self.advance()  # Skip opening quote
        
        while self.current_char is not None and self.current_char != quote_char:
            if self.current_char == '\\':
                self.advance()
                if self.current_char == 'n':
                    result += '\n'
                elif self.current_char == 't':
                    result += '\t'
                elif self.current_char == 'r':
                    result += '\r'
                elif self.current_char == '\\':
                    result += '\\'
                elif self.current_char == '"':
                    result += '"'
                elif self.current_char == "'":
                    result += "'"
                else:
                    result += self.current_char
            else:
                result += self.current_char
            self.advance()
            
        if self.current_char == quote_char:
            self.advance()  # Skip closing quote
            
        return Token(TokenType.STRING, result, start_line, start_column)

    def read_identifier(self, keywords: Set[str]) -> Token:
        """Read an identifier or keyword."""
        start_line = self.line
        start_column = self.column
        result = ''
        
        while self.current_char is not None and self.is_alnum(self.current_char):
            result += self.current_char
            self.advance()
            
        token_type = TokenType.KEYWORD if result in keywords else TokenType.IDENTIFIER
        return Token(token_type, result, start_line, start_column)
        
    def make_token(self, type: TokenType, value: Any) -> Token:
        """Helper to create a token at the current position (corrected for length)."""
        # Note: This helper assumes the token was just consumed, so we might need to adjust
        # For simplicity, we create tokens as we go usually, or pass start pos.
        # But commonly we just use the current line/col if we track start manually.
        # Here we largely use it for operators where we don't track start explicitly in the loop.
        # We'll use self.line and self.column - len(str(value)) roughly.
        return Token(type, value, self.line, self.column - len(str(value)))

    @abstractmethod
    def tokenize(self) -> List[Token]:
        """Tokenize the source code."""
        pass