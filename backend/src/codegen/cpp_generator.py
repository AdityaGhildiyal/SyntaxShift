"""
C++ Code Generator - Generates C++ code from IR.
"""

from typing import List
from .base_generator import BaseGenerator
from ..ir.ir_nodes import *


class CppGenerator(BaseGenerator):
    """Generates C++ code from IR."""
    
    def __init__(self):
        super().__init__("cpp")
    
    def generate_imports(self) -> None:
        """Generate C++ includes."""
        self.emit("#include <iostream>")
        self.emit("#include <string>")
        self.emit("using namespace std;")
        self.emit("")
    
    def generate_main(self, statements: List[IRNode]) -> None:
        """Generate C++ main function."""
        self.emit("int main() {")
        self.indent()
        
        for stmt in statements:
            code = self.visit(stmt)
            if code and code.strip():
                self.emit(code + ";")
            
        self.emit("return 0;")
        self.dedent()
        self.emit("}")
    
    def map_type(self, ir_type: IRType) -> str:
        """Map IR type to C++ type."""
        type_map = {
            IRType.INT: 'int',
            IRType.FLOAT: 'double',
            IRType.STRING: 'string',
            IRType.BOOL: 'bool',
            IRType.VOID: 'void',
            IRType.ARRAY: 'vector<int>',
            IRType.OBJECT: 'void*',
            IRType.ANY: 'auto'
        }
        return type_map.get(ir_type, 'auto')
    
    def visit_function(self, node: IRFunction) -> str:
        """Generate C++ function."""
        # Return type
        return_type = self.map_type(node.return_type)
        
        # Parameters
        params = []
        for param_name, param_type in node.parameters:
            cpp_type = self.map_type(param_type) if isinstance(param_type, IRType) else 'auto'
            params.append(f"{cpp_type} {param_name}")
        params_str = ', '.join(params) if params else ''
        
        # Function signature
        self.emit(f"{return_type} {node.name}({params_str}) {{")
        
        # Function body
        self.indent()
        if node.body:
            for statement in node.body:
                code = self.visit(statement)
                if code and code.strip():
                    self.emit(code + ";")
        self.dedent()
        
        self.emit("}")
        self.emit("")  # Blank line
        return ""
    
    def visit_class(self, node: IRClass) -> str:
        """Generate C++ class."""
        # Class definition
        if node.base_classes:
            bases = ', '.join([f"public {base}" for base in node.base_classes])
            self.emit(f"class {node.name} : {bases} {{")
        else:
            self.emit(f"class {node.name} {{")
        
        # Public section
        self.emit("public:")
        self.indent()
        
        # Class fields
        if node.fields:
            for field in node.fields:
                field_type = self.map_type(field.var_type)
                self.emit(f"{field_type} {field.name};")
            self.emit("")  # Blank line after fields
        
        # Class methods
        if node.methods:
            for method in node.methods:
                self.visit(method)
        
        self.dedent()
        self.emit("};")
        self.emit("")  # Blank line after class
        return ""
    
    def visit_variable(self, node: IRVariable) -> str:
        """Generate C++ variable declaration."""
        var_type = self.map_type(node.var_type)
        
        if node.initial_value:
            value = self.visit(node.initial_value)
            self.emit(f"{var_type} {node.name} = {value};")
        else:
            self.emit(f"{var_type} {node.name};")
        return ""
    
    def visit_assignment(self, node: IRAssignment) -> str:
        """Generate C++ assignment."""
        value = self.visit(node.value)
        self.emit(f"{node.target} {node.operator} {value};")
        return ""
    
    def visit_if(self, node: IRIf) -> str:
        """Generate C++ if statement."""
        condition = self.visit(node.condition)
        self.emit(f"if ({condition}) {{")
        
        self.indent()
        if node.then_block:
            for statement in node.then_block:
                code = self.visit(statement)
                if code and code.strip():
                    self.emit(code + ";")
        self.dedent()
        self.emit("}")
        
        # elif blocks (else if in C++)
        for elif_cond, elif_body in node.elif_blocks:
            elif_condition = self.visit(elif_cond)
            self.emit(f"else if ({elif_condition}) {{")
            self.indent()
            if elif_body:
                for statement in elif_body:
                    code = self.visit(statement)
                    if code and code.strip():
                        self.emit(code + ";")
            self.dedent()
            self.emit("}")
        
        # else block
        if node.else_block:
            self.emit("else {")
            self.indent()
            for statement in node.else_block:
                code = self.visit(statement)
                if code and code.strip():
                    self.emit(code + ";")
            self.dedent()
            self.emit("}")
        
        return ""
    
    def visit_while(self, node: IRWhile) -> str:
        """Generate C++ while loop."""
        condition = self.visit(node.condition)
        self.emit(f"while ({condition}) {{")
        
        self.indent()
        if node.body:
            for statement in node.body:
                code = self.visit(statement)
                if code and code.strip():
                    self.emit(code + ";")
        self.dedent()
        self.emit("}")
        
        return ""
    
    def visit_for(self, node: IRFor) -> str:
        """Generate C++ for loop (range-based)."""
        iterable = self.visit(node.iterable)
        self.emit(f"for (auto {node.variable} : {iterable}) {{")
        
        self.indent()
        if node.body:
            for statement in node.body:
                code = self.visit(statement)
                if code and code.strip():
                    self.emit(code + ";")
        self.dedent()
        self.emit("}")
        
        return ""
    
    def visit_return(self, node: IRReturn) -> str:
        """Generate C++ return statement."""
        if node.value:
            value = self.visit(node.value)
            self.emit(f"return {value};")
        else:
            self.emit("return;")
        return ""

    def visit_break(self, node: IRBreak) -> str:
        """Generate C++ break statement."""
        self.emit("break;")
        return ""
    
    def visit_call(self, node: IRCall) -> str:
        """Generate C++ function call."""
        # Handle array access hack from parser
        if node.function_name.endswith('[]'):
            real_name = node.function_name[:-2]
            if node.arguments:
                index = self.visit(node.arguments[0])
                return f"{real_name}[{index}]"
            return f"{real_name}[]"

        args = ', '.join([self.visit(arg) for arg in node.arguments])
        
        # Map common function names
        func_map = {
            'print': 'cout',
            'len': 'size',
            'input': 'cin >>', 
            'int': 'stoi',
            'str': 'to_string',
            'float': 'stof',
        }
        func_name = func_map.get(node.function_name, node.function_name)
        
        # Special handling for cout
        if func_name == 'cout':
            if args:
                return f"cout << {args} << endl"
            return "cout << endl"
            
        # Special handling for cin (input)
        if func_name == 'cin >>':
             # Python input(prompt) prints prompt then reads
             # C++: cout << prompt; cin >> var;
             # But this is an expression here. C++ cin is statement usually.
             # Return a placeholder or handle complex logic.
             # For now, just return a string read (mock)
             return "read_input()" 
        
        return f"{func_name}({args})"
    
    def visit_binary_op(self, node: IRBinaryOp) -> str:
        """Generate C++ binary operation."""
        left = self.visit(node.left)
        right = self.visit(node.right)
        
        # Map operators
        op_map = {
            'and': '&&',
            'or': '||',
            '//': '/',  # Integer division
        }
        operator = op_map.get(node.operator, node.operator)
        
        return f"({left} {operator} {right})"
    
    def visit_unary_op(self, node: IRUnaryOp) -> str:
        """Generate C++ unary operation."""
        operand = self.visit(node.operand)
        
        # Map operators
        op_map = {
            'not': '!',
        }
        operator = op_map.get(node.operator, node.operator)
        
        return f"{operator}{operand}"
    
    def visit_literal(self, node: IRLiteral) -> str:
        """Generate C++ literal."""
        if node.literal_type == IRType.STRING:
            # Escape quotes
            value = str(node.value).replace('"', '\\"')
            return f'"{value}"'
        elif node.literal_type == IRType.BOOL:
            return 'true' if node.value else 'false'
        elif node.literal_type == IRType.VOID or node.value is None:
            return 'nullptr'
        elif node.literal_type == IRType.FLOAT:
            return f"{node.value}"
        else:
            return str(node.value)
    
    def visit_identifier(self, node: IRIdentifier) -> str:
        """Generate C++ identifier."""
        return node.name
