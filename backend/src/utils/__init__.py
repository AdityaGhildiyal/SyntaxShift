"""
Utility modules for the compiler.
Exports error handler and helper functions.
"""

from .error_handler import ErrorHandler, CompilerError, ErrorLevel
from .helpers import (
    format_code,
    sanitize_identifier,
    escape_string,
    get_default_value,
    merge_dicts,
    pretty_print_json,
    count_lines,
    remove_comments,
    calculate_complexity,
    truncate_string,
)

__all__ = [
    'ErrorHandler',
    'CompilerError',
    'ErrorLevel',
    'format_code',
    'sanitize_identifier',
    'escape_string',
    'get_default_value',
    'merge_dicts',
    'pretty_print_json',
    'count_lines',
    'remove_comments',
    'calculate_complexity',
    'truncate_string',
]
