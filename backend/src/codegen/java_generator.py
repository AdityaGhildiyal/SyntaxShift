"""
Java Code Generator - Generates Java code from IR.
"""

from typing import List
from .base_generator import BaseGenerator
from ..ir.ir_nodes import *


class JavaGenerator(BaseGenerator):
    """Generates Java code from IR."""
    
    def __init__(self):
        super().__init__("java")
    
    def generate_imports(self) -> None:
        """Generate Java imports."""
        # Add common imports
        pass
    
    def map_type(self, ir_type: IRType) -> str:
        """Map IR type to Java type."""
        type_map = {
            IRType.INT: 'int',
            IRType.FLOAT: 'double',
            IRType.STRING: 'String',
            IRType.BOOL: 'boolean',
            IRType.VOID: 'void',
            IRType.ARRAY: 'Object[]',
            IRType.OBJECT: 'Object',
            IRType.ANY: 'Object'
        }
        return type_map.get(ir_type, 'Object')
    
    def visit_function(self, node: IRFunction) -> str:
        """Generate Java method."""
        # Access modifier
        access = node.access_modifier or 'public'
        if node.is_method:
            access = 'public'
        
        # Return type
        return_type = self.map_type(node.return_type)
        
        # Parameters
        params = []
        for param_name, param_type in node.parameters:
            java_type = self.map_type(param_type) if isinstance(param_type, IRType) else 'Object'
            params.append(f"{java_type} {param_name}")
        params_str = ', '.join(params)
        
        # Method signature
        if node.is_method:
            self.emit(f"{access} {return_type} {node.name}({params_str}) {{")
        else:
            self.emit(f"{access} static {return_type} {node.name}({params_str}) {{")
        
        # Method body
        self.indent()
        if node.body:
            for statement in node.body:
                self.visit(statement)
        self.dedent()
        
        self.emit("}")
        self.emit("")  # Blank line
        return ""
    
    def visit_class(self, node: IRClass) -> str:
        """Generate Java class."""
        # Class definition
        if node.base_classes:
            # Java only supports single inheritance
            base = node.base_classes[0]
            self.emit(f"public class {node.name} extends {base} {{")
        else:
            self.emit(f"public class {node.name} {{")
        
        self.indent()
        
        # Class fields
        if node.fields:
            for field in node.fields:
                field_type = self.map_type(field.var_type)
                if field.initial_value:
                    value = self.visit(field.initial_value)
                    self.emit(f"private {field_type} {field.name} = {value};")
                else:
                    self.emit(f"private {field_type} {field.name};")
            self.emit("")  # Blank line after fields
        
        # Class methods
        if node.methods:
            for method in node.methods:
                self.visit(method)
        
        self.dedent()
        self.emit("}")
        self.emit("")  # Blank line after class
        return ""
    
    def visit_variable(self, node: IRVariable) -> str:
        """Generate Java variable declaration."""
        var_type = self.map_type(node.var_type)
        
        if node.initial_value:
            value = self.visit(node.initial_value)
            self.emit(f"{var_type} {node.name} = {value};")
        else:
            self.emit(f"{var_type} {node.name};")
        return ""
    
    def visit_assignment(self, node: IRAssignment) -> str:
        """Generate Java assignment."""
        value = self.visit(node.value)
        self.emit(f"{node.target} {node.operator} {value};")
        return ""
    
    def visit_if(self, node: IRIf) -> str:
        """Generate Java if statement."""
        condition = self.visit(node.condition)
        self.emit(f"if ({condition}) {{")
        
        self.indent()
        if node.then_block:
            for statement in node.then_block:
                self.visit(statement)
        self.dedent()
        self.emit("}")
        
        # elif blocks (else if in Java)
        for elif_cond, elif_body in node.elif_blocks:
            elif_condition = self.visit(elif_cond)
            self.emit(f"else if ({elif_condition}) {{")
            self.indent()
            if elif_body:
                for statement in elif_body:
                    self.visit(statement)
            self.dedent()
            self.emit("}")
        
        # else block
        if node.else_block:
            self.emit("else {")
            self.indent()
            for statement in node.else_block:
                self.visit(statement)
            self.dedent()
            self.emit("}")
        
        return ""
    
    def visit_while(self, node: IRWhile) -> str:
        """Generate Java while loop."""
        condition = self.visit(node.condition)
        self.emit(f"while ({condition}) {{")
        
        self.indent()
        if node.body:
            for statement in node.body:
                self.visit(statement)
        self.dedent()
        self.emit("}")
        
        return ""
    
    def visit_for(self, node: IRFor) -> str:
        """Generate Java for loop (enhanced for)."""
        iterable = self.visit(node.iterable)
        self.emit(f"for (Object {node.variable} : {iterable}) {{")
        
        self.indent()
        if node.body:
            for statement in node.body:
                self.visit(statement)
        self.dedent()
        self.emit("}")
        
        return ""
    
    def visit_return(self, node: IRReturn) -> str:
        """Generate Java return statement."""
        if node.value:
            value = self.visit(node.value)
            self.emit(f"return {value};")
        else:
            self.emit("return;")
        return ""
    
    def visit_call(self, node: IRCall) -> str:
        """Generate Java function call."""
        args = ', '.join([self.visit(arg) for arg in node.arguments])
        
        # Map common function names
        func_map = {
            'print': 'System.out.println',
            'len': 'length',
        }
        func_name = func_map.get(node.function_name, node.function_name)
        
        return f"{func_name}({args})"
    
    def visit_binary_op(self, node: IRBinaryOp) -> str:
        """Generate Java binary operation."""
        left = self.visit(node.left)
        right = self.visit(node.right)
        
        # Map operators
        op_map = {
            'and': '&&',
            'or': '||',
            '//': '/',  # Integer division in Java
        }
        operator = op_map.get(node.operator, node.operator)
        
        return f"({left} {operator} {right})"
    
    def visit_unary_op(self, node: IRUnaryOp) -> str:
        """Generate Java unary operation."""
        operand = self.visit(node.operand)
        
        # Map operators
        op_map = {
            'not': '!',
        }
        operator = op_map.get(node.operator, node.operator)
        
        return f"{operator}{operand}"
    
    def visit_literal(self, node: IRLiteral) -> str:
        """Generate Java literal."""
        if node.literal_type == IRType.STRING:
            # Escape quotes
            value = str(node.value).replace('"', '\\"')
            return f'"{value}"'
        elif node.literal_type == IRType.BOOL:
            return 'true' if node.value else 'false'
        elif node.literal_type == IRType.VOID or node.value is None:
            return 'null'
        elif node.literal_type == IRType.FLOAT:
            return f"{node.value}d"
        else:
            return str(node.value)
    
    def visit_identifier(self, node: IRIdentifier) -> str:
        """Generate Java identifier."""
        return node.name
