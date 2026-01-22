"""
Helper utilities for the compiler.
"""

from typing import Any, Dict, List, Optional
import json


def format_code(code: str, indent_size: int = 4) -> str:
    """
    Format code with proper indentation.
    
    Args:
        code: Code to format
        indent_size: Number of spaces per indent level
        
    Returns:
        Formatted code
    """
    lines = code.split('\n')
    formatted_lines = []
    indent_level = 0
    
    for line in lines:
        stripped = line.strip()
        
        # Decrease indent for closing braces/brackets
        if stripped and stripped[0] in ['}', ']', ')']:
            indent_level = max(0, indent_level - 1)
        
        # Add indented line
        if stripped:
            formatted_lines.append(' ' * (indent_level * indent_size) + stripped)
        else:
            formatted_lines.append('')
        
        # Increase indent for opening braces/brackets
        if stripped and stripped[-1] in ['{', '[', '(', ':']:
            indent_level += 1
    
    return '\n'.join(formatted_lines)


def sanitize_identifier(name: str, language: str = "python") -> str:
    """
    Sanitize identifier name for target language.
    
    Args:
        name: Identifier name
        language: Target language
        
    Returns:
        Sanitized identifier
    """
    # Remove invalid characters
    sanitized = ''.join(c if c.isalnum() or c == '_' else '_' for c in name)
    
    # Ensure it doesn't start with a number
    if sanitized and sanitized[0].isdigit():
        sanitized = '_' + sanitized
    
    # Language-specific reserved words
    reserved_words = {
        'python': {'and', 'or', 'not', 'in', 'is', 'if', 'else', 'elif', 'while', 'for',
                   'def', 'class', 'return', 'import', 'from', 'as', 'try', 'except',
                   'finally', 'with', 'lambda', 'yield', 'pass', 'break', 'continue'},
        'java': {'abstract', 'assert', 'boolean', 'break', 'byte', 'case', 'catch',
                 'char', 'class', 'const', 'continue', 'default', 'do', 'double',
                 'else', 'enum', 'extends', 'final', 'finally', 'float', 'for',
                 'goto', 'if', 'implements', 'import', 'instanceof', 'int', 'interface',
                 'long', 'native', 'new', 'package', 'private', 'protected', 'public',
                 'return', 'short', 'static', 'strictfp', 'super', 'switch',
                 'synchronized', 'this', 'throw', 'throws', 'transient', 'try',
                 'void', 'volatile', 'while'},
        'cpp': {'alignas', 'alignof', 'and', 'and_eq', 'asm', 'auto', 'bitand',
                'bitor', 'bool', 'break', 'case', 'catch', 'char', 'class', 'compl',
                'const', 'constexpr', 'const_cast', 'continue', 'decltype', 'default',
                'delete', 'do', 'double', 'dynamic_cast', 'else', 'enum', 'explicit',
                'export', 'extern', 'false', 'float', 'for', 'friend', 'goto', 'if',
                'inline', 'int', 'long', 'mutable', 'namespace', 'new', 'noexcept',
                'not', 'not_eq', 'nullptr', 'operator', 'or', 'or_eq', 'private',
                'protected', 'public', 'register', 'reinterpret_cast', 'return',
                'short', 'signed', 'sizeof', 'static', 'static_assert', 'static_cast',
                'struct', 'switch', 'template', 'this', 'thread_local', 'throw',
                'true', 'try', 'typedef', 'typeid', 'typename', 'union', 'unsigned',
                'using', 'virtual', 'void', 'volatile', 'wchar_t', 'while', 'xor', 'xor_eq'}
    }
    
    # Add suffix if it's a reserved word
    if language in reserved_words and sanitized.lower() in reserved_words[language]:
        sanitized += '_var'
    
    return sanitized


def escape_string(s: str, language: str = "python") -> str:
    """
    Escape string for target language.
    
    Args:
        s: String to escape
        language: Target language
        
    Returns:
        Escaped string
    """
    # Common escapes
    s = s.replace('\\', '\\\\')
    s = s.replace('\n', '\\n')
    s = s.replace('\r', '\\r')
    s = s.replace('\t', '\\t')
    
    if language == "python":
        s = s.replace("'", "\\'")
    elif language in ["java", "cpp"]:
        s = s.replace('"', '\\"')
    
    return s


def get_default_value(type_name: str, language: str = "python") -> str:
    """
    Get default value for a type.
    
    Args:
        type_name: Type name
        language: Target language
        
    Returns:
        Default value as string
    """
    type_name = type_name.lower()
    
    if language == "python":
        defaults = {
            'int': '0',
            'float': '0.0',
            'str': '""',
            'string': '""',
            'bool': 'False',
            'list': '[]',
            'dict': '{}',
            'tuple': '()',
        }
    elif language == "java":
        defaults = {
            'int': '0',
            'float': '0.0f',
            'double': '0.0',
            'boolean': 'false',
            'string': '""',
            'char': "'\\0'",
            'byte': '0',
            'short': '0',
            'long': '0L',
        }
    elif language == "cpp":
        defaults = {
            'int': '0',
            'float': '0.0f',
            'double': '0.0',
            'bool': 'false',
            'string': '""',
            'char': "'\\0'",
            'long': '0L',
            'short': '0',
        }
    else:
        defaults = {}
    
    return defaults.get(type_name, 'null' if language in ['java', 'cpp'] else 'None')


def merge_dicts(*dicts: Dict) -> Dict:
    """
    Merge multiple dictionaries.
    
    Args:
        *dicts: Dictionaries to merge
        
    Returns:
        Merged dictionary
    """
    result = {}
    for d in dicts:
        result.update(d)
    return result


def pretty_print_json(data: Any, indent: int = 2) -> str:
    """
    Pretty print data as JSON.
    
    Args:
        data: Data to print
        indent: Indentation level
        
    Returns:
        Formatted JSON string
    """
    return json.dumps(data, indent=indent, default=str)


def count_lines(code: str) -> int:
    """
    Count lines of code.
    
    Args:
        code: Source code
        
    Returns:
        Number of lines
    """
    return len(code.split('\n'))


def remove_comments(code: str, language: str = "python") -> str:
    """
    Remove comments from code (simple implementation).
    
    Args:
        code: Source code
        language: Language
        
    Returns:
        Code without comments
    """
    lines = code.split('\n')
    cleaned_lines = []
    
    for line in lines:
        if language == "python":
            # Remove # comments
            if '#' in line:
                line = line[:line.index('#')]
        elif language in ["java", "cpp"]:
            # Remove // comments
            if '//' in line:
                line = line[:line.index('//')]
        
        cleaned_lines.append(line)
    
    return '\n'.join(cleaned_lines)


def calculate_complexity(ast_dict: Dict) -> int:
    """
    Calculate cyclomatic complexity from AST (simplified).
    
    Args:
        ast_dict: AST as dictionary
        
    Returns:
        Complexity score
    """
    complexity = 1  # Base complexity
    
    def count_decision_points(node: Any) -> int:
        """Count decision points in AST."""
        if not isinstance(node, dict):
            return 0
        
        count = 0
        node_type = node.get('type', '')
        
        # Decision points
        if node_type in ['IfStatement', 'WhileLoop', 'ForLoop', 'BinaryOp']:
            count += 1
        
        # Recursively count in children
        for key, value in node.items():
            if isinstance(value, dict):
                count += count_decision_points(value)
            elif isinstance(value, list):
                for item in value:
                    count += count_decision_points(item)
        
        return count
    
    complexity += count_decision_points(ast_dict)
    return complexity


def truncate_string(s: str, max_length: int = 50, suffix: str = "...") -> str:
    """
    Truncate string to maximum length.
    
    Args:
        s: String to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
        
    Returns:
        Truncated string
    """
    if len(s) <= max_length:
        return s
    return s[:max_length - len(suffix)] + suffix
