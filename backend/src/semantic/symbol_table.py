"""
Symbol Table for semantic analysis.
Tracks variables, functions, and classes in different scopes.
"""

from typing import Dict, List, Optional, Any
from enum import Enum


class SymbolKind(Enum):
    """Types of symbols."""
    VARIABLE = "variable"
    FUNCTION = "function"
    CLASS = "class"
    PARAMETER = "parameter"


class Symbol:
    """
    Represents a symbol in the symbol table.
    """
    
    def __init__(self, name: str, kind: SymbolKind, symbol_type: Optional[str] = None,
                 value: Any = None, line: int = 0, column: int = 0):
        """
        Initialize a symbol.
        
        Args:
            name: Symbol name
            kind: Symbol kind (variable, function, class, parameter)
            symbol_type: Type of the symbol (int, str, etc.)
            value: Initial value (for constants)
            line: Line number where defined
            column: Column number where defined
        """
        self.name = name
        self.kind = kind
        self.symbol_type = symbol_type
        self.value = value
        self.line = line
        self.column = column
        self.is_initialized = value is not None
        
        # For functions
        self.parameters: List[tuple] = []  # [(name, type), ...]
        self.return_type: Optional[str] = None
        
        # For classes
        self.methods: Dict[str, Symbol] = {}
        self.fields: Dict[str, Symbol] = {}
        self.base_classes: List[str] = []
    
    def __repr__(self):
        return f"Symbol({self.name}, {self.kind.value}, type={self.symbol_type})"


class Scope:
    """
    Represents a lexical scope.
    """
    
    def __init__(self, name: str, parent: Optional['Scope'] = None):
        """
        Initialize a scope.
        
        Args:
            name: Scope name (e.g., "global", "function:main", "class:MyClass")
            parent: Parent scope
        """
        self.name = name
        self.parent = parent
        self.symbols: Dict[str, Symbol] = {}
    
    def define(self, symbol: Symbol) -> None:
        """
        Define a symbol in this scope.
        
        Args:
            symbol: Symbol to define
        """
        self.symbols[symbol.name] = symbol
    
    def lookup(self, name: str, current_only: bool = False) -> Optional[Symbol]:
        """
        Look up a symbol by name.
        
        Args:
            name: Symbol name
            current_only: Only search current scope (don't check parent)
            
        Returns:
            Symbol if found, None otherwise
        """
        if name in self.symbols:
            return self.symbols[name]
        
        if not current_only and self.parent:
            return self.parent.lookup(name)
        
        return None
    
    def __repr__(self):
        return f"Scope({self.name}, {len(self.symbols)} symbols)"


class SymbolTable:
    """
    Symbol table for tracking all symbols across scopes.
    """
    
    def __init__(self):
        """Initialize the symbol table with global scope."""
        self.global_scope = Scope("global")
        self.current_scope = self.global_scope
        self.scopes: List[Scope] = [self.global_scope]
    
    def enter_scope(self, name: str) -> None:
        """
        Enter a new scope.
        
        Args:
            name: Scope name
        """
        new_scope = Scope(name, self.current_scope)
        self.current_scope = new_scope
        self.scopes.append(new_scope)
    
    def exit_scope(self) -> None:
        """Exit the current scope and return to parent."""
        if self.current_scope.parent:
            self.current_scope = self.current_scope.parent
    
    def define(self, symbol: Symbol) -> None:
        """
        Define a symbol in the current scope.
        
        Args:
            symbol: Symbol to define
        """
        self.current_scope.define(symbol)
    
    def lookup(self, name: str, current_only: bool = False) -> Optional[Symbol]:
        """
        Look up a symbol by name.
        
        Args:
            name: Symbol name
            current_only: Only search current scope
            
        Returns:
            Symbol if found, None otherwise
        """
        return self.current_scope.lookup(name, current_only)
    
    def is_defined(self, name: str, current_only: bool = False) -> bool:
        """
        Check if a symbol is defined.
        
        Args:
            name: Symbol name
            current_only: Only check current scope
            
        Returns:
            True if symbol is defined, False otherwise
        """
        return self.lookup(name, current_only) is not None
    
    def get_all_symbols(self) -> List[Symbol]:
        """
        Get all symbols from all scopes.
        
        Returns:
            List of all symbols
        """
        symbols = []
        for scope in self.scopes:
            symbols.extend(scope.symbols.values())
        return symbols
    
    def __repr__(self):
        return f"SymbolTable({len(self.scopes)} scopes, current={self.current_scope.name})"
