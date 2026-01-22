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
        # Add common imports if needed
        # We manually added Scanner in generate_main
        pass

    def generate(self, ir_program: IRProgram) -> str:
        """Override generate to wrap in Main class."""
        self.generated_code = []
        self.indent_level = 0
        
        self.generate_imports()
        
        self.emit("public class Main {")
        self.indent()
        
        # Don't generate globals as static fields - they'll be in main()
        # Python scripts typically have top-level code, not true globals
            
        # Generate functions (as static methods)
        for func in ir_program.functions:
            self.visit(func)
            
        # Generate main body
        if ir_program.main_body or ir_program.globals:
            self.generate_main(ir_program.globals + ir_program.main_body)
            
        self.dedent()
        self.emit("}")
        
        return '\n'.join(self.generated_code)

    def generate_main(self, statements: List[IRNode]) -> None:
        """Generate Java main method."""
        self.emit("public static void main(String[] args) {")
        self.indent()
        
        # Check if we need Scanner (look for input calls)
        needs_scanner = self._needs_scanner(statements)
        if needs_scanner:
            self.emit("java.util.Scanner scanner = new java.util.Scanner(System.in);")
        
        for stmt in statements:
            code = self.visit(stmt)
            if code and code.strip():
                self.emit(code + ";")
        
        if needs_scanner:
            self.emit("scanner.close();")
        self.dedent()
        self.emit("}")
    
    def _needs_scanner(self, statements: List[IRNode]) -> bool:
        """Check if any statement uses input functions."""
        for stmt in statements:
            if self._contains_input_call(stmt):
                return True
        return False
    
    def _contains_input_call(self, node: IRNode) -> bool:
        """Recursively check if node contains input calls."""
        if isinstance(node, IRCall):
            if 'input' in node.function_name or 'scanner' in node.function_name:
                return True
        # Check children
        if hasattr(node, 'body') and isinstance(node.body, list):
            for child in node.body:
                if self._contains_input_call(child):
                    return True
        if hasattr(node, 'value') and node.value:
            if self._contains_input_call(node.value):
                return True
        return False

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
                code = self.visit(statement)
                if code and code.strip():
                    self.emit(code + ";")
        self.dedent()
        
        self.emit("}")
        self.emit("")  # Blank line
        return ""
    
    def visit_class(self, node: IRClass, as_static: bool = False) -> str:
        """Generate Java class."""
        # Class definition
        modifier = "static " if as_static else ""
        if node.base_classes:
            # Java only supports single inheritance
            base = node.base_classes[0]
            self.emit(f"public {modifier}class {node.name} extends {base} {{")
        else:
            self.emit(f"public {modifier}class {node.name} {{")
        
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
                code = self.visit(statement)
                if code and code.strip():
                    self.emit(code + ";")
        self.dedent()
        self.emit("}")
        
        # elif blocks (else if in Java)
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
        """Generate Java while loop."""
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
        """Generate Java for loop (enhanced for)."""
        iterable = self.visit(node.iterable)
        self.emit(f"for (Object {node.variable} : {iterable}) {{")
        
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
        """Generate Java return statement."""
        if node.value:
            value = self.visit(node.value)
            self.emit(f"return {value};")
        else:
            self.emit("return;")
        return ""
        
    def visit_break(self, node: IRBreak) -> str:
        """Generate Java break statement."""
        self.emit("break;")
        return ""
    
    def visit_call(self, node: IRCall) -> str:
        """Generate Java function call."""
        # Handle array access hack
        if node.function_name.endswith('[]'):
            real_name = node.function_name[:-2]
            if node.arguments:
                index = self.visit(node.arguments[0])
                return f"{real_name}[{index}]"
            return f"{real_name}[]"

        args = ', '.join([self.visit(arg) for arg in node.arguments])
        
        # Map common function names
        func_map = {
            'print': 'System.out.println',
            'len': 'length',
            'input': 'scanner.nextLine',
            'read_input': 'scanner.nextLine',
            'int': 'Integer.parseInt',
            'stoi': 'Integer.parseInt',
            'str': 'String.valueOf',
            'to_string': 'String.valueOf',
            'float': 'Double.parseDouble',
            'stof': 'Double.parseDouble',
            'size': 'length',
            'length': 'length',
        }
        func_name = func_map.get(node.function_name, node.function_name)
        
        # Special handling
        if node.function_name == 'len':
             if args:
                 return f"{args}.length()"
        
        if node.function_name in ['input', 'read_input']:
             return "scanner.nextLine()"
        
        return f"{func_name}({args})"
    
    def visit_binary_op(self, node: IRBinaryOp) -> str:
        """Generate Java binary operation."""
        # Handle C++ stream output
        if node.operator == '<<' and self.is_cout_stream(node):
            args = self.collect_stream_args(node)
            # Combine args with +
            if not args:
                return ""
            
            # Filter escaped newlines if they are separate args? 
            # System.out.print(A + B);
            # We must be careful about types. If A is string, + works.
            
            print_stmt = "System.out.print(" + " + ".join(args) + ")"
            # If we know it ends with endl (\n), we could use println?
            # But we replaced endl with "\n".
            return print_stmt

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
            return ['"\\n"']
        else:
            return [self.visit(node)]
    
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
            IRType.ANY: 'var'  # Use var for type inference (Java 10+)
        }
        return type_map.get(ir_type, 'var')
