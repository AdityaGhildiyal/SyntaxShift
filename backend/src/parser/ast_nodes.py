"""
Abstract Syntax Tree node definitions.
All syntactic constructs are represented as AST nodes.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any
from enum import Enum


class ASTNodeType(Enum):
    """Types of AST nodes."""
    PROGRAM = "Program"
    FUNCTION_DEF = "FunctionDef"
    CLASS_DEF = "ClassDef"
    VARIABLE_DECL = "VariableDecl"
    IF_STATEMENT = "IfStatement"
    WHILE_LOOP = "WhileLoop"
    FOR_LOOP = "ForLoop"
    RETURN = "Return"
    ASSIGNMENT = "Assignment"
    BINARY_OP = "BinaryOp"
    UNARY_OP = "UnaryOp"
    FUNCTION_CALL = "FunctionCall"
    IDENTIFIER = "Identifier"
    LITERAL = "Literal"
    BLOCK = "Block"
    EXPRESSION_STMT = "ExpressionStatement"


@dataclass
class ASTNode:
    """Base class for all AST nodes."""
    node_type: ASTNodeType
    line: int = 0
    column: int = 0
    
    def to_dict(self) -> dict:
        """Convert AST node to dictionary for JSON serialization."""
        result = {'type': self.node_type.value}
        for key, value in self.__dict__.items():
            if key in ['node_type', 'line', 'column']:
                continue
            if isinstance(value, list):
                result[key] = [v.to_dict() if isinstance(v, ASTNode) else v for v in value]
            elif isinstance(value, ASTNode):
                result[key] = value.to_dict()
            elif isinstance(value, tuple) and len(value) > 0:
                # Handle tuples (like parameters)
                if isinstance(value[0], ASTNode):
                    result[key] = [v.to_dict() for v in value]
                else:
                    result[key] = value
            else:
                result[key] = value
        return result


@dataclass
class Program(ASTNode):
    """Root node representing entire program."""
    statements: List[ASTNode] = field(default_factory=list)
    
    def __init__(self, statements: List[ASTNode] = None):
        super().__init__(ASTNodeType.PROGRAM)
        self.statements = statements or []


@dataclass
class FunctionDef(ASTNode):
    """Function definition node."""
    name: str = ""
    parameters: List[tuple] = field(default_factory=list)  # [(name, type), ...]
    return_type: Optional[str] = None
    body: List[ASTNode] = field(default_factory=list)
    
    def __init__(self, name: str, parameters: List[tuple] = None, 
                 return_type: Optional[str] = None, body: List[ASTNode] = None):
        super().__init__(ASTNodeType.FUNCTION_DEF)
        self.name = name
        self.parameters = parameters or []
        self.return_type = return_type
        self.body = body or []


@dataclass
class ClassDef(ASTNode):
    """Class definition node."""
    name: str = ""
    methods: List[FunctionDef] = field(default_factory=list)
    fields: List['VariableDecl'] = field(default_factory=list)
    base_classes: List[str] = field(default_factory=list)
    
    def __init__(self, name: str, methods: List[FunctionDef] = None,
                 fields: List['VariableDecl'] = None, base_classes: List[str] = None):
        super().__init__(ASTNodeType.CLASS_DEF)
        self.name = name
        self.methods = methods or []
        self.fields = fields or []
        self.base_classes = base_classes or []


@dataclass
class VariableDecl(ASTNode):
    """Variable declaration node."""
    name: str = ""
    var_type: Optional[str] = None
    initial_value: Optional[ASTNode] = None
    
    def __init__(self, name: str, var_type: Optional[str] = None,
                 initial_value: Optional[ASTNode] = None):
        super().__init__(ASTNodeType.VARIABLE_DECL)
        self.name = name
        self.var_type = var_type
        self.initial_value = initial_value


@dataclass
class IfStatement(ASTNode):
    """If-elif-else statement node."""
    condition: ASTNode = None
    then_block: List[ASTNode] = field(default_factory=list)
    elif_blocks: List[tuple] = field(default_factory=list)  # [(condition, block), ...]
    else_block: List[ASTNode] = field(default_factory=list)
    
    def __init__(self, condition: ASTNode, then_block: List[ASTNode] = None,
                 elif_blocks: List[tuple] = None, else_block: List[ASTNode] = None):
        super().__init__(ASTNodeType.IF_STATEMENT)
        self.condition = condition
        self.then_block = then_block or []
        self.elif_blocks = elif_blocks or []
        self.else_block = else_block or []


@dataclass
class WhileLoop(ASTNode):
    """While loop node."""
    condition: ASTNode = None
    body: List[ASTNode] = field(default_factory=list)
    
    def __init__(self, condition: ASTNode, body: List[ASTNode] = None):
        super().__init__(ASTNodeType.WHILE_LOOP)
        self.condition = condition
        self.body = body or []


@dataclass
class ForLoop(ASTNode):
    """For loop node."""
    variable: str = ""
    iterable: ASTNode = None
    body: List[ASTNode] = field(default_factory=list)
    
    def __init__(self, variable: str, iterable: ASTNode, body: List[ASTNode] = None):
        super().__init__(ASTNodeType.FOR_LOOP)
        self.variable = variable
        self.iterable = iterable
        self.body = body or []


@dataclass
class Return(ASTNode):
    """Return statement node."""
    expression: Optional[ASTNode] = None
    
    def __init__(self, expression: Optional[ASTNode] = None):
        super().__init__(ASTNodeType.RETURN)
        self.expression = expression


@dataclass
class Assignment(ASTNode):
    """Assignment statement node."""
    target: str = ""
    value: ASTNode = None
    operator: str = "="  # =, +=, -=, etc.
    
    def __init__(self, target: str, value: ASTNode, operator: str = "="):
        super().__init__(ASTNodeType.ASSIGNMENT)
        self.target = target
        self.value = value
        self.operator = operator


@dataclass
class BinaryOp(ASTNode):
    """Binary operation node."""
    left: ASTNode = None
    operator: str = ""
    right: ASTNode = None
    
    def __init__(self, left: ASTNode, operator: str, right: ASTNode):
        super().__init__(ASTNodeType.BINARY_OP)
        self.left = left
        self.operator = operator
        self.right = right


@dataclass
class UnaryOp(ASTNode):
    """Unary operation node."""
    operator: str = ""
    operand: ASTNode = None
    
    def __init__(self, operator: str, operand: ASTNode):
        super().__init__(ASTNodeType.UNARY_OP)
        self.operator = operator
        self.operand = operand


@dataclass
class FunctionCall(ASTNode):
    """Function call node."""
    function_name: str = ""
    arguments: List[ASTNode] = field(default_factory=list)
    
    def __init__(self, function_name: str, arguments: List[ASTNode] = None):
        super().__init__(ASTNodeType.FUNCTION_CALL)
        self.function_name = function_name
        self.arguments = arguments or []


@dataclass
class Identifier(ASTNode):
    """Identifier node (variable/function name reference)."""
    name: str = ""
    
    def __init__(self, name: str):
        super().__init__(ASTNodeType.IDENTIFIER)
        self.name = name


@dataclass
class Literal(ASTNode):
    """Literal value node."""
    value: Any = None
    literal_type: str = ""  # 'int', 'float', 'string', 'bool', 'null'
    
    def __init__(self, value: Any, literal_type: str):
        super().__init__(ASTNodeType.LITERAL)
        self.value = value
        self.literal_type = literal_type


@dataclass
class Block(ASTNode):
    """Block of statements."""
    statements: List[ASTNode] = field(default_factory=list)
    
    def __init__(self, statements: List[ASTNode] = None):
        super().__init__(ASTNodeType.BLOCK)
        self.statements = statements or []


@dataclass
class ExpressionStatement(ASTNode):
    """Expression used as a statement."""
    expression: ASTNode = None
    
    def __init__(self, expression: ASTNode):
        super().__init__(ASTNodeType.EXPRESSION_STMT)
        self.expression = expression