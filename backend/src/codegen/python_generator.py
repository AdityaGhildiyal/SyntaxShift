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
                code = self.visit(statement)
                if code:
                    self.emit(code)
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
                code = self.visit(statement)
                if code:
                    self.emit(code)
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
                    code = self.visit(statement)
                    if code:
                        self.emit(code)
            else:
                self.emit("pass")
            self.dedent()
        
        # else block
        if node.else_block:
            self.emit("else:")
            self.indent()
            for statement in node.else_block:
                code = self.visit(statement)
                if code:
                    self.emit(code)
            self.dedent()
        
        return ""
    
    def visit_while(self, node: IRWhile) -> str:
        """Generate Python while loop."""
        condition = self.visit(node.condition)
        self.emit(f"while {condition}:")
        
        self.indent()
        if node.body:
            for statement in node.body:
                code = self.visit(statement)
                if code:
                    self.emit(code)
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
                code = self.visit(statement)
                if code:
                    self.emit(code)
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

    def generate(self, ir_program: IRProgram) -> str:
        code = super().generate(ir_program)
        
        # Check if main exists
        has_main = any(f.name == 'main' for f in ir_program.functions)
        if has_main:
            code += '\n\nif __name__ == "__main__":\n    main()'
            
        return code

    def visit_break(self, node: IRBreak) -> str:
        """Generate Python break."""
        self.emit("break")
        return ""

    def visit_call(self, node: IRCall) -> str:
        """Generate Python function call."""
        args_list = [self.visit(arg) for arg in node.arguments]
        args = ', '.join(args_list)
        
        # Mapping C++ and Java functions to Python
        func_map = {
            'stoi': 'int',
            'to_string': 'str',
            'read_input': 'input',
            'size': 'len',
            'length': 'len',
            # Java mappings
            'System.out.println': 'print',
            'System.out.print': 'print',
            'Integer.parseInt': 'int',
            'Double.parseDouble': 'float',
            'scanner.nextLine': 'input',
            'scanner.nextInt': 'int(input())', # Approximation
            'Math.max': 'max',
            'Math.min': 'min',
            'Math.abs': 'abs',
            'Math.sqrt': 'math.sqrt',
        }
        
        func_name = func_map.get(node.function_name, node.function_name)
        
        # Special handling for print end argument
        if node.function_name == 'System.out.print':
             return f"print({args}, end='')"
        
        return f"{func_name}({args})"
    
    def visit_binary_op(self, node: IRBinaryOp) -> str:
        """Generate Python binary operation."""
        # Handle C++ stream output
        if node.operator == '<<' and self.is_cout_stream(node):
            args = self.collect_stream_args(node)
            args_str = ", ".join(args)
            return f"print({args_str}, sep='', end='')"

        left = self.visit(node.left)
        right = self.visit(node.right)
        
        # Map operators
        op_map = {
            '&&': 'and',
            '||': 'or',
        }
        operator = op_map.get(node.operator, node.operator)
        
        # Remove redundant parens for simple string concat to avoid artifacts
        if operator == '+':
             # Check if we are concatenating strings, which might have led to excessive parens
             # For now, just return without outer parens if it's strict addition
             return f"{left} {operator} {right}"

        return f"({left} {operator} {right})"
    
    def is_cout_stream(self, node: IRNode) -> bool:
        """Check if binary op is part of cout stream."""
        if isinstance(node, IRIdentifier) and node.name == 'cout':
            return True
        if isinstance(node, IRBinaryOp) and node.operator == '<<':
            return self.is_cout_stream(node.left)
        return False

    def collect_stream_args(self, node: IRNode) -> List[str]:
        """Collect arguments from cout stream chain."""
        if isinstance(node, IRBinaryOp) and node.operator == '<<':
            return self.collect_stream_args(node.left) + self.collect_stream_args(node.right)
        elif isinstance(node, IRIdentifier) and node.name == 'cout':
            return []
        elif isinstance(node, IRIdentifier) and node.name == 'endl':
            return ["'\\n'"]
        else:
            return [self.visit(node)]

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

