"""
Error Handler - Centralized error handling and reporting.
"""

from typing import List, Optional
from enum import Enum


class ErrorLevel(Enum):
    """Error severity levels."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class CompilerError:
    """Represents a compiler error or warning."""
    
    def __init__(self, level: ErrorLevel, message: str, line: int = 0,
                 column: int = 0, source_file: Optional[str] = None,
                 phase: Optional[str] = None):
        """
        Initialize a compiler error.
        
        Args:
            level: Error severity level
            message: Error message
            line: Line number (0 if not applicable)
            column: Column number (0 if not applicable)
            source_file: Source file name
            phase: Compiler phase (lexer, parser, semantic, etc.)
        """
        self.level = level
        self.message = message
        self.line = line
        self.column = column
        self.source_file = source_file
        self.phase = phase
    
    def __str__(self) -> str:
        """String representation of error."""
        parts = []
        
        if self.source_file:
            parts.append(f"{self.source_file}")
        
        if self.line > 0:
            if self.column > 0:
                parts.append(f":{self.line}:{self.column}")
            else:
                parts.append(f":{self.line}")
        
        parts.append(f" [{self.level.value.upper()}]")
        
        if self.phase:
            parts.append(f" ({self.phase})")
        
        parts.append(f": {self.message}")
        
        return "".join(parts)
    
    def to_dict(self) -> dict:
        """Convert error to dictionary."""
        return {
            'level': self.level.value,
            'message': self.message,
            'line': self.line,
            'column': self.column,
            'source_file': self.source_file,
            'phase': self.phase
        }


class ErrorHandler:
    """
    Centralized error handler for the compiler.
    Collects and manages errors and warnings from all phases.
    """
    
    def __init__(self):
        """Initialize error handler."""
        self.errors: List[CompilerError] = []
        self.warnings: List[CompilerError] = []
        self.infos: List[CompilerError] = []
    
    def add_error(self, message: str, line: int = 0, column: int = 0,
                  source_file: Optional[str] = None, phase: Optional[str] = None) -> None:
        """
        Add an error.
        
        Args:
            message: Error message
            line: Line number
            column: Column number
            source_file: Source file name
            phase: Compiler phase
        """
        error = CompilerError(ErrorLevel.ERROR, message, line, column, source_file, phase)
        self.errors.append(error)
    
    def add_warning(self, message: str, line: int = 0, column: int = 0,
                    source_file: Optional[str] = None, phase: Optional[str] = None) -> None:
        """
        Add a warning.
        
        Args:
            message: Warning message
            line: Line number
            column: Column number
            source_file: Source file name
            phase: Compiler phase
        """
        warning = CompilerError(ErrorLevel.WARNING, message, line, column, source_file, phase)
        self.warnings.append(warning)
    
    def add_info(self, message: str, line: int = 0, column: int = 0,
                 source_file: Optional[str] = None, phase: Optional[str] = None) -> None:
        """
        Add an info message.
        
        Args:
            message: Info message
            line: Line number
            column: Column number
            source_file: Source file name
            phase: Compiler phase
        """
        info = CompilerError(ErrorLevel.INFO, message, line, column, source_file, phase)
        self.infos.append(info)
    
    def has_errors(self) -> bool:
        """Check if there are any errors."""
        return len(self.errors) > 0
    
    def has_warnings(self) -> bool:
        """Check if there are any warnings."""
        return len(self.warnings) > 0
    
    def get_errors(self) -> List[CompilerError]:
        """Get all errors."""
        return self.errors
    
    def get_warnings(self) -> List[CompilerError]:
        """Get all warnings."""
        return self.warnings
    
    def get_infos(self) -> List[CompilerError]:
        """Get all info messages."""
        return self.infos
    
    def get_all(self) -> List[CompilerError]:
        """Get all messages (errors, warnings, infos)."""
        return self.errors + self.warnings + self.infos
    
    def clear(self) -> None:
        """Clear all errors and warnings."""
        self.errors = []
        self.warnings = []
        self.infos = []
    
    def print_errors(self) -> None:
        """Print all errors to console."""
        for error in self.errors:
            print(f"ERROR: {error}")
    
    def print_warnings(self) -> None:
        """Print all warnings to console."""
        for warning in self.warnings:
            print(f"WARNING: {warning}")
    
    def print_all(self) -> None:
        """Print all messages to console."""
        for msg in self.get_all():
            print(str(msg))
    
    def get_summary(self) -> str:
        """Get a summary of errors and warnings."""
        return f"{len(self.errors)} error(s), {len(self.warnings)} warning(s)"
    
    def to_dict(self) -> dict:
        """Convert all messages to dictionary."""
        return {
            'errors': [e.to_dict() for e in self.errors],
            'warnings': [w.to_dict() for w in self.warnings],
            'infos': [i.to_dict() for i in self.infos],
            'summary': self.get_summary()
        }
