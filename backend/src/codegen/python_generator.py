"""
Python Code Generator - Generates Python code from IR.
"""

from typing import List
from .base_generator import BaseGenerator
from ..ir.ir_nodes import *


class PythonGenerator(BaseGenerator):
    """Generates Python code from IR."""
    
    def __init__(self):
        super().__init__("python")
    
    def generate_imports(self) -> None:
        """Generate Python imports."""
        # Add common imports if needed
        pass
    
    def visit_function(self, node: IRFunction) -> str:
        """Generate Python function."""
        # Function signature
        params = ', '.join([name for name, _ in node.parameters])
        self.emit(f"def {node.name}({params}):")
        
        # Function body
        self.indent()
        if node.body:
            for statement in node.body:
                self.visit(statement)
        else:
            self.emit("pass")
        self.dedent()
        
        self.emit("")  # Blank line after function
        return ""
    
    def visit_class(self, node: IRClass) -> str:
        """Generate Python class."""
        # Class definition
        if node.base_classes:
            bases = ', '.join(node.base_classes)
            self.emit(f"class {node.name}({bases}):")
        else:
            self.emit(f"class {node.name}:")
        
        self.indent()
        
        # Class fields
        if node.fields:
            for field in node.fields:
                self.visit(field)
        
        # Class methods
        if node.methods:
            for method in node.methods:
                self.visit(method)
        
        if not node.fields and not node.methods:
            self.emit("pass")
        
        self.dedent()
        self.emit("")  # Blank line after class
        return ""
    
    def visit_variable(self, node: IRVariable) -> str:
        """Generate Python variable declaration."""
        if node.initial_value:
            value = self.visit(node.initial_value)
            self.emit(f"{node.name} = {value}")
        else:
            self.emit(f"{node.name} = None")
        return ""
    
    def visit_assignment(self, node: IRAssignment) -> str:
        """Generate Python assignment."""
        value = self.visit(node.value)
        self.emit(f"{node.target} {node.operator} {value}")
        return ""
    
    def visit_if(self, node: IRIf) -> str:
        """Generate Python if statement."""
        condition = self.visit(node.condition)
        self.emit(f"if {condition}:")
        
        self.indent()
        if node.then_block:
            for statement in node.then_block:
                self.visit(statement)
        else:
            self.emit("pass")
        self.dedent()
        
        # elif blocks
        for elif_cond, elif_body in node.elif_blocks:
            elif_condition = self.visit(elif_cond)
            self.emit(f"elif {elif_condition}:")
            self.indent()
            if elif_body:
                for statement in elif_body:
                    self.visit(statement)
            else:
                self.emit("pass")
            self.dedent()
        
        # else block
        if node.else_block:
            self.emit("else:")
            self.indent()
            for statement in node.else_block:
                self.visit(statement)
            self.dedent()
        
        return ""
    
    def visit_while(self, node: IRWhile) -> str:
        """Generate Python while loop."""
        condition = self.visit(node.condition)
        self.emit(f"while {condition}:")
        
        self.indent()
        if node.body:
            for statement in node.body:
                self.visit(statement)
        else:
            self.emit("pass")
        self.dedent()
        
        return ""
    
    def visit_for(self, node: IRFor) -> str:
        """Generate Python for loop."""
        iterable = self.visit(node.iterable)
        self.emit(f"for {node.variable} in {iterable}:")
        
        self.indent()
        if node.body:
            for statement in node.body:
                self.visit(statement)
        else:
            self.emit("pass")
        self.dedent()
        
        return ""
    
    def visit_return(self, node: IRReturn) -> str:
        """Generate Python return statement."""
        if node.value:
            value = self.visit(node.value)
            self.emit(f"return {value}")
        else:
            self.emit("return")
        return ""
    
    def visit_call(self, node: IRCall) -> str:
        """Generate Python function call."""
        args = ', '.join([self.visit(arg) for arg in node.arguments])
        return f"{node.function_name}({args})"
    
    def visit_binary_op(self, node: IRBinaryOp) -> str:
        """Generate Python binary operation."""
        left = self.visit(node.left)
        right = self.visit(node.right)
        
        # Map operators
        op_map = {
            '&&': 'and',
            '||': 'or',
        }
        operator = op_map.get(node.operator, node.operator)
        
        return f"({left} {operator} {right})"
    
    def visit_unary_op(self, node: IRUnaryOp) -> str:
        """Generate Python unary operation."""
        operand = self.visit(node.operand)
        
        # Map operators
        op_map = {
            '!': 'not ',
        }
        operator = op_map.get(node.operator, node.operator)
        
        return f"{operator}{operand}"
    
    def visit_literal(self, node: IRLiteral) -> str:
        """Generate Python literal."""
        if node.literal_type == IRType.STRING:
            # Escape quotes
            value = str(node.value).replace("'", "\\'")
            return f"'{value}'"
        elif node.literal_type == IRType.BOOL:
            return 'True' if node.value else 'False'
        elif node.literal_type == IRType.VOID or node.value is None:
            return 'None'
        else:
            return str(node.value)
    
    def visit_identifier(self, node: IRIdentifier) -> str:
        """Generate Python identifier."""
        return node.name
