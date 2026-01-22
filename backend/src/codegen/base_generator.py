"""
Base Code Generator - Abstract base class for all code generators.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from ..ir.ir_nodes import *
from ..utils import format_code


class BaseGenerator(ABC):
    """
    Abstract base class for code generators.
    Generates target language code from IR.
    """
    
    def __init__(self, target_language: str):
        """
        Initialize code generator.
        
        Args:
            target_language: Target language name
        """
        self.target_language = target_language
        self.indent_level = 0
        self.indent_size = 4
        self.generated_code = []
    
    def generate(self, ir_program: IRProgram) -> str:
        """
        Generate code from IR program.
        
        Args:
            ir_program: IR program node
            
        Returns:
            Generated code as string
        """
        self.generated_code = []
        self.indent_level = 0
        
        # Generate imports/headers
        self.generate_imports()
        
        # Generate global variables
        for global_var in ir_program.globals:
            self.visit(global_var)
        
        # Generate classes
        for cls in ir_program.classes:
            self.visit(cls)
        
        # Generate functions
        for func in ir_program.functions:
            self.visit(func)
        
        return '\n'.join(self.generated_code)
    
    def visit(self, node: IRNode) -> str:
        """
        Visit an IR node and generate code.
        
        Args:
            node: IR node
            
        Returns:
            Generated code for this node
        """
        if node is None:
            return ""
        
        method_name = f"visit_{node.node_type.value}"
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)
    
    def generic_visit(self, node: IRNode) -> str:
        """Generic visitor for unknown node types."""
        return ""
    
    def emit(self, code: str) -> None:
        """
        Emit a line of code with proper indentation.
        
        Args:
            code: Code to emit
        """
        if code.strip():
            indent = ' ' * (self.indent_level * self.indent_size)
            self.generated_code.append(indent + code)
        else:
            self.generated_code.append('')
    
    def indent(self) -> None:
        """Increase indentation level."""
        self.indent_level += 1
    
    def dedent(self) -> None:
        """Decrease indentation level."""
        self.indent_level = max(0, self.indent_level - 1)
    
    # Abstract methods to be implemented by subclasses
    
    @abstractmethod
    def generate_imports(self) -> None:
        """Generate import statements."""
        pass
    
    @abstractmethod
    def visit_function(self, node: IRFunction) -> str:
        """Generate function definition."""
        pass
    
    @abstractmethod
    def visit_class(self, node: IRClass) -> str:
        """Generate class definition."""
        pass
    
    @abstractmethod
    def visit_variable(self, node: IRVariable) -> str:
        """Generate variable declaration."""
        pass
    
    @abstractmethod
    def visit_assignment(self, node: IRAssignment) -> str:
        """Generate assignment statement."""
        pass
    
    @abstractmethod
    def visit_if(self, node: IRIf) -> str:
        """Generate if statement."""
        pass
    
    @abstractmethod
    def visit_while(self, node: IRWhile) -> str:
        """Generate while loop."""
        pass
    
    @abstractmethod
    def visit_for(self, node: IRFor) -> str:
        """Generate for loop."""
        pass
    
    @abstractmethod
    def visit_return(self, node: IRReturn) -> str:
        """Generate return statement."""
        pass
    
    @abstractmethod
    def visit_call(self, node: IRCall) -> str:
        """Generate function call."""
        pass
    
    @abstractmethod
    def visit_binary_op(self, node: IRBinaryOp) -> str:
        """Generate binary operation."""
        pass
    
    @abstractmethod
    def visit_unary_op(self, node: IRUnaryOp) -> str:
        """Generate unary operation."""
        pass
    
    @abstractmethod
    def visit_literal(self, node: IRLiteral) -> str:
        """Generate literal value."""
        pass
    
    @abstractmethod
    def visit_identifier(self, node: IRIdentifier) -> str:
        """Generate identifier."""
        pass
    
    def visit_block(self, node: IRBlock) -> str:
        """Generate block of statements."""
        for statement in node.statements:
            self.visit(statement)
        return ""
