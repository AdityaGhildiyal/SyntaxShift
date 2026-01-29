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
        # Infer return type from body if it's VOID but has return statements
        return_type = node.return_type
        if return_type == IRType.VOID and node.body:
            # Check if there are return statements with values
            for stmt in node.body:
                if isinstance(stmt, IRReturn) and stmt.value:
                    # Has a return value, so it's not void
                    return_type = IRType.ANY
                    break
        
        cpp_return_type = self.map_type(return_type)
        
        # Parameters - filter out 'self' for methods
        params = []
        for param_name, param_type in node.parameters:
            # Skip 'self' parameter (Python methods)
            if param_name == 'self':
                continue
            cpp_type = self.map_type(param_type) if isinstance(param_type, IRType) else 'auto'
            params.append(f"{cpp_type} {param_name}")
        params_str = ', '.join(params) if params else ''
        
        # Function signature
        self.emit(f"{cpp_return_type} {node.name}({params_str}) {{")
        
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
            
            # Handle special input markers
            if value == "INPUT_INT":
                # Generate: cout << prompt; int var; cin >> var;
                if hasattr(self, '_current_input_prompt'):
                    self.emit(f"cout << {self._current_input_prompt};")
                    delattr(self, '_current_input_prompt')
                self.emit(f"{var_type} {node.name};")
                self.emit(f"cin >> {node.name};")
            elif value == "INPUT_STRING":
                # Generate: cout << prompt; string var; getline(cin, var);
                if hasattr(self, '_current_input_prompt'):
                    self.emit(f"cout << {self._current_input_prompt};")
                    delattr(self, '_current_input_prompt')
                self.emit(f"{var_type} {node.name};")
                self.emit(f"getline(cin, {node.name});")
            else:
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
        
        # Handle method calls (object.method)
        if '.' in node.function_name:
            # This is a method call: object.method(args)
            args = ', '.join([self.visit(arg) for arg in node.arguments])
            return f"{node.function_name}({args})"

        # Special handling for int(input("prompt")) pattern
        # This is a common Python pattern that needs special C++ handling
        if node.function_name == 'int' and len(node.arguments) == 1:
            arg = node.arguments[0]
            if isinstance(arg, IRCall) and arg.function_name == 'input':
                # For int(input("prompt")), we need to:
                # 1. Print the prompt
                # 2. Read an integer
                # We'll return a special marker that the variable handler can use
                if arg.arguments:
                    prompt = self.visit(arg.arguments[0])
                    # Store the prompt for later use
                    self._current_input_prompt = prompt
                return "INPUT_INT"
        
        args = ', '.join([self.visit(arg) for arg in node.arguments])
        
        # Map common function names
        func_map = {
            'print': 'cout',
            'len': 'size',
            'str': 'to_string',
            'float': 'stof',
        }
        func_name = func_map.get(node.function_name, node.function_name)
        
        # Special handling for cout
        if func_name == 'cout':
            if args:
                return f"cout << {args} << endl"
            return "cout << endl"
            
        # Special handling for input (when not wrapped in int())
        if node.function_name == 'input':
            # For string input
            if args:
                self._current_input_prompt = args
            return "INPUT_STRING"
        
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
