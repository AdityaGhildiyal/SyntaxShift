"""
Base parser class with common functionality for all language parsers.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from ..lexer.token import Token, TokenType
from .ast_nodes import *


class ParseError(Exception):
    """Exception raised when parsing fails."""
    pass


class BaseParser(ABC):
    """
    Abstract base class for all parsers.
    Provides common functionality for parsing tokens into AST.
    """
    
    def __init__(self, tokens: List[Token]):
        """
        Initialize the parser with a list of tokens.
        
        Args:
            tokens: List of tokens from lexer
        """
        self.tokens = tokens
        self.position = 0
        self.current_token = self.tokens[0] if tokens else None
    
    def advance(self) -> None:
        """Move to the next token."""
        self.position += 1
        if self.position < len(self.tokens):
            self.current_token = self.tokens[self.position]
        else:
            self.current_token = None
    
    def peek(self, offset: int = 1) -> Optional[Token]:
        """
        Look ahead at upcoming tokens without advancing.
        
        Args:
            offset: Number of tokens to look ahead (default 1)
            
        Returns:
            Token at position + offset, or None if out of bounds
        """
        peek_pos = self.position + offset
        if peek_pos < len(self.tokens):
            return self.tokens[peek_pos]
        return None
    
    def expect(self, token_type: TokenType, value: Optional[str] = None) -> Token:
        """
        Expect current token to be of specific type (and optionally value).
        Advances if match, raises error otherwise.
        
        Args:
            token_type: Expected token type
            value: Expected token value (optional)
            
        Returns:
            The matched token
            
        Raises:
            ParseError: If token doesn't match
        """
        if not self.current_token:
            raise ParseError(f"Expected {token_type.value} but reached end of file")
        
        if self.current_token.type != token_type:
            raise ParseError(
                f"Expected {token_type.value} but got {self.current_token.type.value} "
                f"at line {self.current_token.line}, column {self.current_token.column}"
            )
        
        if value is not None and self.current_token.value != value:
            raise ParseError(
                f"Expected '{value}' but got '{self.current_token.value}' "
                f"at line {self.current_token.line}, column {self.current_token.column}"
            )
        
        token = self.current_token
        self.advance()
        return token
    
    def match(self, token_type: TokenType, value: Optional[str] = None) -> bool:
        """
        Check if current token matches type (and optionally value) without advancing.
        
        Args:
            token_type: Token type to check
            value: Token value to check (optional)
            
        Returns:
            True if matches, False otherwise
        """
        if not self.current_token:
            return False
        
        if self.current_token.type != token_type:
            return False
        
        if value is not None and self.current_token.value != value:
            return False
        
        return True
    
    def consume(self, token_type: TokenType, value: Optional[str] = None) -> bool:
        """
        If current token matches, advance and return True. Otherwise return False.
        
        Args:
            token_type: Token type to check
            value: Token value to check (optional)
            
        Returns:
            True if matched and consumed, False otherwise
        """
        if self.match(token_type, value):
            self.advance()
            return True
        return False
    
    def skip_newlines(self) -> None:
        """Skip all newline tokens."""
        while self.current_token and self.current_token.type == TokenType.NEWLINE:
            self.advance()
    
    def skip_semicolons(self) -> None:
        """Skip all semicolon tokens."""
        while self.current_token and self.current_token.type == TokenType.SEMICOLON:
            self.advance()
    
    def error(self, message: str) -> None:
        """
        Raise a parse error with location information.
        
        Args:
            message: Error message
            
        Raises:
            ParseError: Always raises
        """
        if self.current_token:
            raise ParseError(
                f"{message} at line {self.current_token.line}, "
                f"column {self.current_token.column}"
            )
        else:
            raise ParseError(f"{message} at end of file")
    
    @abstractmethod
    def parse(self) -> Program:
        """
        Parse tokens into an AST.
        Must be implemented by subclasses.
        
        Returns:
            Program AST node
        """
        pass