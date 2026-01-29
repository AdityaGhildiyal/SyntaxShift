"""
Token definitions for the lexer.
"""

from enum import Enum, auto
from dataclasses import dataclass
from typing import Optional, Any


class TokenType(Enum):
    # End of file
    EOF = auto()
    
    # Literals
    INTEGER = auto()
    FLOAT = auto()
    STRING = auto()
    F_STRING = auto()       # Python f-strings
    CHAR = auto()
    IDENTIFIER = auto()
    
    # Keywords
    KEYWORD = auto()
    
    # Operators
    PLUS = auto()           # +
    MINUS = auto()          # -
    MULTIPLY = auto()       # *
    DIVIDE = auto()         # /
    MODULO = auto()         # %
    POWER = auto()          # ** (Python)
    FLOOR_DIVIDE = auto()   # // (Python)
    ASSIGN = auto()         # =
    PLUS_ASSIGN = auto()    # +=
    MINUS_ASSIGN = auto()   # -=
    INCREMENT = auto()      # ++
    DECREMENT = auto()      # --
    LSHIFT = auto()         # <<
    RSHIFT = auto()         # >>
    
    # Comparison
    EQUAL = auto()          # ==
    NOT_EQUAL = auto()      # !=
    LESS_THAN = auto()      # <
    GREATER_THAN = auto()   # >
    LESS_EQUAL = auto()     # <=
    GREATER_EQUAL = auto()  # >=
    
    # Logical
    AND = auto()            # && or and
    OR = auto()             # || or or
    NOT = auto()            # ! or not
    
    # Delimiters
    LPAREN = auto()         # (
    RPAREN = auto()         # )
    LBRACE = auto()         # {
    RBRACE = auto()         # }
    LBRACKET = auto()       # [
    RBRACKET = auto()       # ]
    COMMA = auto()          # ,
    SEMICOLON = auto()      # ;
    COLON = auto()          # :
    DOT = auto()            # .
    
    # Language specific
    DOUBLE_COLON = auto()   # :: (C++)
    ARROW = auto()          # -> (C++, Java, Python)
    INDENT = auto()         # (Python)
    DEDENT = auto()         # (Python)
    NEWLINE = auto()        # (Python)


@dataclass
class Token:
    type: TokenType
    value: Any
    line: int
    column: int
    
    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)}, line={self.line}, col={self.column})"


# Keywords for different languages
CPP_KEYWORDS = {
    'auto', 'break', 'case', 'char', 'const', 'continue', 'default', 'do',
    'double', 'else', 'enum', 'extern', 'float', 'for', 'goto', 'if',
    'int', 'long', 'register', 'return', 'short', 'signed', 'sizeof', 'static',
    'struct', 'switch', 'typedef', 'union', 'unsigned', 'void', 'volatile', 'while',
    'class', 'namespace', 'template', 'typename', 'using', 'virtual', 'friend',
    'public', 'protected', 'private', 'this', 'new', 'delete', 'operator',
    'true', 'false', 'nullptr', 'bool', 'try', 'catch', 'throw'
}

JAVA_KEYWORDS = {
    'abstract', 'assert', 'boolean', 'break', 'byte', 'case', 'catch', 'char',
    'class', 'const', 'continue', 'default', 'do', 'double', 'else', 'enum',
    'extends', 'final', 'finally', 'float', 'for', 'goto', 'if', 'implements',
    'import', 'instanceof', 'int', 'interface', 'long', 'native', 'new', 'package',
    'private', 'protected', 'public', 'return', 'short', 'static', 'strictfp',
    'super', 'switch', 'synchronized', 'this', 'throw', 'throws', 'transient',
    'try', 'void', 'volatile', 'while', 'true', 'false', 'null'
}

PYTHON_KEYWORDS = {
    'and', 'as', 'assert', 'break', 'class', 'continue', 'def', 'del', 'elif',
    'else', 'except', 'finally', 'for', 'from', 'global', 'if', 'import', 'in',
    'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try',
    'while', 'with', 'yield', 'True', 'False', 'None'
}
