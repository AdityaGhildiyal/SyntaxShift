"""
Type Checker for semantic analysis.
Validates types and performs semantic checks on AST.
"""

from typing import Optional, List, Set
from ..parser.ast_nodes import *
from .symbol_table import SymbolTable, Symbol, SymbolKind


class SemanticError(Exception):
    """Exception raised for semantic errors."""
    pass


class TypeChecker:
    """
    Type checker for validating AST semantics.
    Performs type checking, variable usage validation, and other semantic checks.
    """
    
    def __init__(self, language: str = "python"):
        """
        Initialize the type checker.
        
        Args:
            language: Source language ("python", "java", "cpp")
        """
        self.language = language.lower()
        self.symbol_table = SymbolTable()
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.current_function: Optional[Symbol] = None
        self.current_class: Optional[Symbol] = None
        
        # Built-in types for each language
        self.builtin_types = {
            "python": {"int", "float", "str", "bool", "list", "dict", "tuple", "None"},
            "java": {"int", "float", "double", "boolean", "String", "void", "char", "byte", "short", "long"},
            "cpp": {"int", "float", "double", "bool", "char", "void", "string", "long", "short"}
        }
    
    def check(self, ast: Program) -> bool:
        """
        Check the AST for semantic errors.
        
        Args:
            ast: Program AST node
            
        Returns:
            True if no errors, False otherwise
        """
        self.errors = []
        self.warnings = []
        
        try:
            self.visit_program(ast)
        except SemanticError as e:
            self.errors.append(str(e))
        
        return len(self.errors) == 0
    
    def get_errors(self) -> List[str]:
        """Get all semantic errors."""
        return self.errors
    
    def get_warnings(self) -> List[str]:
        """Get all warnings."""
        return self.warnings
    
    def error(self, message: str) -> None:
        """Add an error message."""
        self.errors.append(message)
    
    def warning(self, message: str) -> None:
        """Add a warning message."""
        self.warnings.append(message)
    
    def visit_program(self, node: Program) -> None:
        """Visit Program node."""
        for statement in node.statements:
            self.visit(statement)
    
    def visit(self, node: ASTNode) -> Optional[str]:
        """
        Visit an AST node and return its type.
        
        Args:
            node: AST node to visit
            
        Returns:
            Type of the node (as string) or None
        """
        if node is None:
            return None
        
        method_name = f"visit_{node.node_type.value.lower()}"
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)
    
    def generic_visit(self, node: ASTNode) -> Optional[str]:
        """Generic visitor for unknown node types."""
        self.warning(f"No visitor for node type: {node.node_type.value}")
        return None
    
    def visit_functiondef(self, node: FunctionDef) -> None:
        """Visit FunctionDef node."""
        # Check if function already defined
        if self.symbol_table.is_defined(node.name, current_only=True):
            self.error(f"Function '{node.name}' is already defined")
            return
        
        # Create function symbol
        func_symbol = Symbol(
            name=node.name,
            kind=SymbolKind.FUNCTION,
            symbol_type="function",
            line=node.line,
            column=node.column
        )
        func_symbol.parameters = node.parameters
        func_symbol.return_type = node.return_type
        
        # Define function in current scope
        self.symbol_table.define(func_symbol)
        
        # Enter function scope
        self.symbol_table.enter_scope(f"function:{node.name}")
        self.current_function = func_symbol
        
        # Define parameters
        for param_name, param_type in node.parameters:
            param_symbol = Symbol(
                name=param_name,
                kind=SymbolKind.PARAMETER,
                symbol_type=param_type
            )
            self.symbol_table.define(param_symbol)
        
        # Visit function body
        for statement in node.body:
            self.visit(statement)
        
        # Exit function scope
        self.symbol_table.exit_scope()
        self.current_function = None
    
    def visit_classdef(self, node: ClassDef) -> None:
        """Visit ClassDef node."""
        # Check if class already defined
        if self.symbol_table.is_defined(node.name, current_only=True):
            self.error(f"Class '{node.name}' is already defined")
            return
        
        # Create class symbol
        class_symbol = Symbol(
            name=node.name,
            kind=SymbolKind.CLASS,
            symbol_type="class",
            line=node.line,
            column=node.column
        )
        class_symbol.base_classes = node.base_classes
        
        # Define class in current scope
        self.symbol_table.define(class_symbol)
        
        # Enter class scope
        self.symbol_table.enter_scope(f"class:{node.name}")
        self.current_class = class_symbol
        
        # Visit fields
        for field in node.fields:
            self.visit(field)
            if isinstance(field, VariableDecl):
                class_symbol.fields[field.name] = Symbol(
                    name=field.name,
                    kind=SymbolKind.VARIABLE,
                    symbol_type=field.var_type
                )
        
        # Visit methods
        for method in node.methods:
            self.visit(method)
            if isinstance(method, FunctionDef):
                class_symbol.methods[method.name] = Symbol(
                    name=method.name,
                    kind=SymbolKind.FUNCTION,
                    symbol_type="function"
                )
        
        # Exit class scope
        self.symbol_table.exit_scope()
        self.current_class = None
    
    def visit_variabledecl(self, node: VariableDecl) -> None:
        """Visit VariableDecl node."""
        # Check if variable already defined in current scope
        if self.symbol_table.is_defined(node.name, current_only=True):
            self.error(f"Variable '{node.name}' is already defined in this scope")
            return
        
        # Get type from initial value if not specified
        var_type = node.var_type
        if var_type is None and node.initial_value:
            var_type = self.visit(node.initial_value)
        
        # Create variable symbol
        var_symbol = Symbol(
            name=node.name,
            kind=SymbolKind.VARIABLE,
            symbol_type=var_type,
            value=node.initial_value,
            line=node.line,
            column=node.column
        )
        
        # Define variable
        self.symbol_table.define(var_symbol)
    
    def visit_assignment(self, node: Assignment) -> None:
        """Visit Assignment node."""
        # Check if variable is defined
        symbol = self.symbol_table.lookup(node.target)
        if symbol is None:
            # In Python, assignment creates variable
            if self.language == "python":
                value_type = self.visit(node.value)
                var_symbol = Symbol(
                    name=node.target,
                    kind=SymbolKind.VARIABLE,
                    symbol_type=value_type,
                    line=node.line,
                    column=node.column
                )
                self.symbol_table.define(var_symbol)
            else:
                self.error(f"Variable '{node.target}' is not defined")
                return
        else:
            # Check type compatibility
            value_type = self.visit(node.value)
            if symbol.symbol_type and value_type:
                if not self.is_type_compatible(symbol.symbol_type, value_type):
                    self.error(
                        f"Type mismatch: cannot assign {value_type} to {symbol.symbol_type}"
                    )
    
    def visit_ifstatement(self, node: IfStatement) -> None:
        """Visit IfStatement node."""
        # Check condition type
        condition_type = self.visit(node.condition)
        if condition_type and condition_type not in ["bool", "boolean", "int"]:
            self.warning(f"Condition has type {condition_type}, expected boolean")
        
        # Visit then block
        for statement in node.then_block:
            self.visit(statement)
        
        # Visit elif blocks
        for elif_condition, elif_body in node.elif_blocks:
            self.visit(elif_condition)
            for statement in elif_body:
                self.visit(statement)
        
        # Visit else block
        for statement in node.else_block:
            self.visit(statement)
    
    def visit_whileloop(self, node: WhileLoop) -> None:
        """Visit WhileLoop node."""
        # Check condition type
        condition_type = self.visit(node.condition)
        if condition_type and condition_type not in ["bool", "boolean", "int"]:
            self.warning(f"Condition has type {condition_type}, expected boolean")
        
        # Visit body
        for statement in node.body:
            self.visit(statement)
    
    def visit_forloop(self, node: ForLoop) -> None:
        """Visit ForLoop node."""
        # Visit iterable
        self.visit(node.iterable)
        
        # Define loop variable
        if node.variable:
            var_symbol = Symbol(
                name=node.variable,
                kind=SymbolKind.VARIABLE,
                symbol_type=None,  # Type inferred from iterable
                line=node.line,
                column=node.column
            )
            self.symbol_table.define(var_symbol)
        
        # Visit body
        for statement in node.body:
            self.visit(statement)
    
    def visit_return(self, node: Return) -> None:
        """Visit Return node."""
        if self.current_function is None:
            self.error("Return statement outside of function")
            return
        
        # Check return type
        if node.expression:
            return_type = self.visit(node.expression)
            expected_type = self.current_function.return_type
            
            if expected_type and return_type:
                if not self.is_type_compatible(expected_type, return_type):
                    self.error(
                        f"Return type mismatch: expected {expected_type}, got {return_type}"
                    )
    
    def visit_binaryop(self, node: BinaryOp) -> Optional[str]:
        """Visit BinaryOp node and return result type."""
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        
        if left_type is None or right_type is None:
            return None
        
        # Arithmetic operators
        if node.operator in ['+', '-', '*', '/', '%', '//', '**']:
            if left_type in ['int', 'float', 'double'] and right_type in ['int', 'float', 'double']:
                # Return float if either operand is float
                if 'float' in [left_type, right_type] or 'double' in [left_type, right_type]:
                    return 'float'
                return 'int'
            elif node.operator == '+' and left_type == 'str' and right_type == 'str':
                return 'str'  # String concatenation
            else:
                self.error(f"Invalid operands for {node.operator}: {left_type} and {right_type}")
                return None
        
        # Comparison operators
        elif node.operator in ['==', '!=', '<', '>', '<=', '>=']:
            return 'bool' if self.language == 'python' else 'boolean'
        
        # Logical operators
        elif node.operator in ['and', 'or', '&&', '||']:
            return 'bool' if self.language == 'python' else 'boolean'
        
        return None
    
    def visit_unaryop(self, node: UnaryOp) -> Optional[str]:
        """Visit UnaryOp node and return result type."""
        operand_type = self.visit(node.operand)
        
        if node.operator in ['-', '+']:
            if operand_type in ['int', 'float', 'double']:
                return operand_type
            else:
                self.error(f"Invalid operand for {node.operator}: {operand_type}")
                return None
        
        elif node.operator in ['not', '!']:
            return 'bool' if self.language == 'python' else 'boolean'
        
        return None
    
    def visit_functioncall(self, node: FunctionCall) -> Optional[str]:
        """Visit FunctionCall node and return return type."""
        # Look up function
        func_symbol = self.symbol_table.lookup(node.function_name)
        
        if func_symbol is None:
            # Built-in functions
            if node.function_name in ['print', 'println', 'cout', 'len', 'range', 'list']:
                # Visit arguments
                for arg in node.arguments:
                    self.visit(arg)
                return None
            else:
                self.error(f"Function '{node.function_name}' is not defined")
                return None
        
        if func_symbol.kind != SymbolKind.FUNCTION:
            self.error(f"'{node.function_name}' is not a function")
            return None
        
        # Check argument count
        if len(node.arguments) != len(func_symbol.parameters):
            self.error(
                f"Function '{node.function_name}' expects {len(func_symbol.parameters)} "
                f"arguments, got {len(node.arguments)}"
            )
        
        # Visit arguments
        for arg in node.arguments:
            self.visit(arg)
        
        return func_symbol.return_type
    
    def visit_identifier(self, node: Identifier) -> Optional[str]:
        """Visit Identifier node and return its type."""
        symbol = self.symbol_table.lookup(node.name)
        
        if symbol is None:
            self.error(f"Variable '{node.name}' is not defined")
            return None
        
        return symbol.symbol_type
    
    def visit_literal(self, node: Literal) -> str:
        """Visit Literal node and return its type."""
        # Normalize type names
        type_map = {
            'int': 'int',
            'float': 'float',
            'string': 'str',
            'str': 'str',
            'bool': 'bool',
            'boolean': 'bool',
            'null': 'None'
        }
        return type_map.get(node.literal_type, node.literal_type)
    
    def visit_block(self, node: Block) -> None:
        """Visit Block node."""
        for statement in node.statements:
            self.visit(statement)
    
    def visit_expressionstatement(self, node: ExpressionStatement) -> None:
        """Visit ExpressionStatement node."""
        self.visit(node.expression)
    
    def is_type_compatible(self, expected: str, actual: str) -> bool:
        """
        Check if two types are compatible.
        
        Args:
            expected: Expected type
            actual: Actual type
            
        Returns:
            True if compatible, False otherwise
        """
        if expected == actual:
            return True
        
        # Numeric type compatibility
        numeric_types = {'int', 'float', 'double', 'long', 'short'}
        if expected in numeric_types and actual in numeric_types:
            return True
        
        # Boolean compatibility
        if expected in {'bool', 'boolean'} and actual in {'bool', 'boolean'}:
            return True
        
        return False
