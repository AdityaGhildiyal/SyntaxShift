"""
IR Generator - Converts AST to Intermediate Representation.
"""

from typing import Optional, List
from ..parser.ast_nodes import *
from .ir_nodes import *


class IRGenerator:
    """
    Generates language-agnostic IR from AST.
    """
    
    def __init__(self, source_language: str = "python"):
        """
        Initialize IR generator.
        
        Args:
            source_language: Source language ("python", "java", "cpp")
        """
        self.source_language = source_language.lower()
        self.ir_program = IRProgram()
        self.scopes = [set()]  # Stack of defined variables
    
    def enter_scope(self):
        self.scopes.append(set())
        
    def exit_scope(self):
        self.scopes.pop()
        
    def define_var(self, name: str):
        self.scopes[-1].add(name)
        
    def is_defined(self, name: str) -> bool:
        for scope in reversed(self.scopes):
            if name in scope:
                return True
        return False
        
    # ... (generate method unchanged)

    def visit_functiondef(self, node: FunctionDef) -> IRFunction:
        """Convert FunctionDef to IRFunction."""
        # Map return type
        return_type = self.map_type(node.return_type) if node.return_type else IRType.VOID
        
        # New scope for function
        self.enter_scope()
        
        # Convert parameters
        ir_params = []
        for param_name, param_type in node.parameters:
            ir_param_type = self.map_type(param_type) if param_type else IRType.ANY
            ir_params.append((param_name, ir_param_type))
            self.define_var(param_name)
        
        # Convert body
        ir_body = []
        for statement in node.body:
            ir_stmt = self.visit(statement)
            if ir_stmt:
                ir_body.append(ir_stmt)
        
        self.exit_scope()
        
        ir_func = IRFunction(node.name, ir_params, return_type, ir_body)
        ir_func.metadata['source_line'] = node.line
        ir_func.metadata['source_column'] = node.column
        
        return ir_func

    # ... (visit_classdef - technically class creates scope too, but let's stick to functions first)
    
    def visit_assignment(self, node: Assignment) -> IRNode:
        """Convert Assignment to IRAssignment or IRVariable."""
        value = self.visit(node.value)
        
        if self.source_language == 'python':
            if not self.is_defined(node.target):
                self.define_var(node.target)
                # It's a new variable definition
                # We inferred type as ANY (auto)
                ir_var = IRVariable(node.target, IRType.ANY, value)
                ir_var.metadata['source_line'] = node.line
                ir_var.metadata['source_column'] = node.column
                return ir_var
        
        ir_assign = IRAssignment(node.target, value, node.operator)
        ir_assign.metadata['source_line'] = node.line
        ir_assign.metadata['source_column'] = node.column
        
        return ir_assign
    
    def generate(self, ast: Program) -> IRProgram:
        """
        Generate IR from AST.
        
        Args:
            ast: Program AST node
            
        Returns:
            IRProgram node
        """
        self.ir_program = IRProgram()
        
        for statement in ast.statements:
            ir_node = self.visit(statement)
            if ir_node:
                if isinstance(ir_node, IRFunction):
                    self.ir_program.functions.append(ir_node)
                elif isinstance(ir_node, IRClass):
                    self.ir_program.classes.append(ir_node)
                elif isinstance(ir_node, IRVariable):
                    self.ir_program.globals.append(ir_node)
                else:
                    # Any other top-level statement (calls, loops, if, assignments) goes to main body
                    self.ir_program.main_body.append(ir_node)
        
        return self.ir_program
    
    def visit(self, node: ASTNode) -> Optional[IRNode]:
        """
        Visit an AST node and convert to IR.
        
        Args:
            node: AST node
            
        Returns:
            IR node or None
        """
        if node is None:
            return None
        
        method_name = f"visit_{node.node_type.value.lower()}"
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)
    
    def generic_visit(self, node: ASTNode) -> Optional[IRNode]:
        """Generic visitor for unknown node types."""
        return None
    

    
    def visit_classdef(self, node: ClassDef) -> IRClass:
        """Convert ClassDef to IRClass."""
        # Convert methods
        ir_methods = []
        for method in node.methods:
            ir_method = self.visit(method)
            if isinstance(ir_method, IRFunction):
                ir_method.is_method = True
                ir_methods.append(ir_method)
        
        # Convert fields
        ir_fields = []
        for field in node.fields:
            ir_field = self.visit(field)
            if isinstance(ir_field, IRVariable):
                ir_fields.append(ir_field)
        
        ir_class = IRClass(node.name, ir_methods, ir_fields, node.base_classes)
        ir_class.metadata['source_line'] = node.line
        ir_class.metadata['source_column'] = node.column
        
        return ir_class
    
    def visit_variabledecl(self, node: VariableDecl) -> IRVariable:
        """Convert VariableDecl to IRVariable."""
        var_type = self.map_type(node.var_type) if node.var_type else IRType.ANY
        
        initial_value = None
        if node.initial_value:
            initial_value = self.visit(node.initial_value)
        
        ir_var = IRVariable(node.name, var_type, initial_value)
        ir_var.metadata['source_line'] = node.line
        ir_var.metadata['source_column'] = node.column
        
        return ir_var
    

    
    def visit_ifstatement(self, node: IfStatement) -> IRIf:
        """Convert IfStatement to IRIf."""
        condition = self.visit(node.condition)
        
        then_block = [self.visit(stmt) for stmt in node.then_block]
        then_block = [stmt for stmt in then_block if stmt is not None]
        
        elif_blocks = []
        for elif_cond, elif_body in node.elif_blocks:
            ir_elif_cond = self.visit(elif_cond)
            ir_elif_body = [self.visit(stmt) for stmt in elif_body]
            ir_elif_body = [stmt for stmt in ir_elif_body if stmt is not None]
            elif_blocks.append((ir_elif_cond, ir_elif_body))
        
        else_block = [self.visit(stmt) for stmt in node.else_block]
        else_block = [stmt for stmt in else_block if stmt is not None]
        
        ir_if = IRIf(condition, then_block, elif_blocks, else_block)
        ir_if.metadata['source_line'] = node.line
        ir_if.metadata['source_column'] = node.column
        
        return ir_if
    
    def visit_whileloop(self, node: WhileLoop) -> IRWhile:
        """Convert WhileLoop to IRWhile."""
        condition = self.visit(node.condition)
        
        body = [self.visit(stmt) for stmt in node.body]
        body = [stmt for stmt in body if stmt is not None]
        
        ir_while = IRWhile(condition, body)
        ir_while.metadata['source_line'] = node.line
        ir_while.metadata['source_column'] = node.column
        
        return ir_while
    
    def visit_forloop(self, node: ForLoop) -> IRFor:
        """Convert ForLoop to IRFor."""
        iterable = self.visit(node.iterable)
        
        body = [self.visit(stmt) for stmt in node.body]
        body = [stmt for stmt in body if stmt is not None]
        
        ir_for = IRFor(node.variable, iterable, body)
        ir_for.metadata['source_line'] = node.line
        ir_for.metadata['source_column'] = node.column
        
        return ir_for
    
    def visit_return(self, node: Return) -> IRReturn:
        """Convert Return to IRReturn."""
        value = None
        if node.expression:
            value = self.visit(node.expression)
        
        ir_return = IRReturn(value)
        ir_return.metadata['source_line'] = node.line
        ir_return.metadata['source_column'] = node.column
        
        return ir_return
    
    def visit_binaryop(self, node: BinaryOp) -> IRBinaryOp:
        """Convert BinaryOp to IRBinaryOp."""
        left = self.visit(node.left)
        right = self.visit(node.right)
        
        # Infer result type
        result_type = self.infer_binary_op_type(node.operator, left, right)
        
        ir_binop = IRBinaryOp(left, node.operator, right, result_type)
        ir_binop.metadata['source_line'] = node.line
        ir_binop.metadata['source_column'] = node.column
        
        return ir_binop
    
    def visit_unaryop(self, node: UnaryOp) -> IRUnaryOp:
        """Convert UnaryOp to IRUnaryOp."""
        operand = self.visit(node.operand)
        
        # Infer result type
        result_type = operand.ir_type if operand else IRType.ANY
        
        ir_unop = IRUnaryOp(node.operator, operand, result_type)
        ir_unop.metadata['source_line'] = node.line
        ir_unop.metadata['source_column'] = node.column
        
        return ir_unop
    
    def visit_functioncall(self, node: FunctionCall) -> IRCall:
        """Convert FunctionCall to IRCall."""
        arguments = [self.visit(arg) for arg in node.arguments]
        arguments = [arg for arg in arguments if arg is not None]
        
        ir_call = IRCall(node.function_name, arguments)
        ir_call.metadata['source_line'] = node.line
        ir_call.metadata['source_column'] = node.column
        
        return ir_call
    
    def visit_identifier(self, node: Identifier) -> IRIdentifier:
        """Convert Identifier to IRIdentifier."""
        ir_id = IRIdentifier(node.name)
        ir_id.metadata['source_line'] = node.line
        ir_id.metadata['source_column'] = node.column
        
        return ir_id
    
    def visit_literal(self, node: Literal) -> IRLiteral:
        """Convert Literal to IRLiteral."""
        literal_type = self.map_literal_type(node.literal_type)
        
        ir_lit = IRLiteral(node.value, literal_type)
        ir_lit.metadata['source_line'] = node.line
        ir_lit.metadata['source_column'] = node.column
        
        return ir_lit
    
    def visit_block(self, node: Block) -> IRBlock:
        """Convert Block to IRBlock."""
        statements = [self.visit(stmt) for stmt in node.statements]
        statements = [stmt for stmt in statements if stmt is not None]
        
        ir_block = IRBlock(statements)
        ir_block.metadata['source_line'] = node.line
        ir_block.metadata['source_column'] = node.column
        
        return ir_block
    
    def visit_expressionstatement(self, node: ExpressionStatement) -> Optional[IRNode]:
        """Convert ExpressionStatement."""
        return self.visit(node.expression)
    
    def visit_break(self, node: Break) -> IRBreak:
        """Convert Break to IRBreak."""
        ir_break = IRBreak()
        ir_break.metadata['source_line'] = node.line
        ir_break.metadata['source_column'] = node.column
        return ir_break
    
    def map_type(self, type_str: Optional[str]) -> IRType:
        """
        Map source language type to IR type.
        
        Args:
            type_str: Type string from source language
            
        Returns:
            IRType
        """
        if not type_str:
            return IRType.ANY
        
        type_str = type_str.lower()
        
        # Integer types
        if type_str in ['int', 'integer', 'long', 'short', 'byte']:
            return IRType.INT
        
        # Float types
        if type_str in ['float', 'double']:
            return IRType.FLOAT
        
        # String types
        if type_str in ['str', 'string']:
            return IRType.STRING
        
        # Boolean types
        if type_str in ['bool', 'boolean']:
            return IRType.BOOL
        
        # Void
        if type_str in ['void', 'none']:
            return IRType.VOID
        
        # Array/List
        if 'list' in type_str or 'array' in type_str or '[]' in type_str:
            return IRType.ARRAY
        
        # Default to object for custom types
        return IRType.OBJECT
    
    def map_literal_type(self, literal_type: str) -> IRType:
        """Map literal type string to IRType."""
        type_map = {
            'int': IRType.INT,
            'float': IRType.FLOAT,
            'string': IRType.STRING,
            'str': IRType.STRING,
            'bool': IRType.BOOL,
            'boolean': IRType.BOOL,
            'null': IRType.VOID,
            'None': IRType.VOID
        }
        return type_map.get(literal_type, IRType.ANY)
    
    def infer_binary_op_type(self, operator: str, left: IRNode, right: IRNode) -> IRType:
        """Infer result type of binary operation."""
        # Comparison operators always return bool
        if operator in ['==', '!=', '<', '>', '<=', '>=', 'and', 'or', '&&', '||']:
            return IRType.BOOL
        
        # Arithmetic operators
        if operator in ['+', '-', '*', '/', '%', '//', '**']:
            # If either operand is float, result is float
            if left and left.ir_type == IRType.FLOAT:
                return IRType.FLOAT
            if right and right.ir_type == IRType.FLOAT:
                return IRType.FLOAT
            # Otherwise int
            return IRType.INT
        
        return IRType.ANY
