"""
Intermediate Representation (IR) Node Definitions.
Language-agnostic IR for code translation.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any, Dict
from enum import Enum


class IRNodeType(Enum):
    """Types of IR nodes."""
    PROGRAM = "program"
    FUNCTION = "function"
    CLASS = "class"
    VARIABLE = "variable"
    ASSIGNMENT = "assignment"
    IF = "if"
    WHILE = "while"
    FOR = "for"
    RETURN = "return"
    CALL = "call"
    BINARY_OP = "binary_op"
    UNARY_OP = "unary_op"
    LITERAL = "literal"
    IDENTIFIER = "identifier"
    BLOCK = "block"


class IRType(Enum):
    """IR type system."""
    INT = "int"
    FLOAT = "float"
    STRING = "string"
    BOOL = "bool"
    VOID = "void"
    ARRAY = "array"
    OBJECT = "object"
    ANY = "any"


@dataclass
class IRNode:
    """Base class for all IR nodes."""
    node_type: IRNodeType
    ir_type: Optional[IRType] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict:
        """Convert IR node to dictionary."""
        result = {
            'node_type': self.node_type.value,
            'ir_type': self.ir_type.value if self.ir_type else None
        }
        for key, value in self.__dict__.items():
            if key in ['node_type', 'ir_type', 'metadata']:
                continue
            if isinstance(value, list):
                result[key] = [v.to_dict() if isinstance(v, IRNode) else v for v in value]
            elif isinstance(value, IRNode):
                result[key] = value.to_dict()
            else:
                result[key] = value
        if self.metadata:
            result['metadata'] = self.metadata
        return result


@dataclass
class IRProgram(IRNode):
    """IR Program node."""
    functions: List['IRFunction'] = field(default_factory=list)
    classes: List['IRClass'] = field(default_factory=list)
    globals: List['IRVariable'] = field(default_factory=list)
    
    def __init__(self):
        super().__init__(IRNodeType.PROGRAM)
        self.functions = []
        self.classes = []
        self.globals = []


@dataclass
class IRFunction(IRNode):
    """IR Function node."""
    name: str = ""
    parameters: List[tuple] = field(default_factory=list)  # [(name, type), ...]
    return_type: IRType = IRType.VOID
    body: List[IRNode] = field(default_factory=list)
    is_method: bool = False
    access_modifier: Optional[str] = None  # public, private, protected
    
    def __init__(self, name: str, parameters: List[tuple] = None, 
                 return_type: IRType = IRType.VOID, body: List[IRNode] = None):
        super().__init__(IRNodeType.FUNCTION)
        self.name = name
        self.parameters = parameters or []
        self.return_type = return_type
        self.body = body or []
        self.is_method = False
        self.access_modifier = None


@dataclass
class IRClass(IRNode):
    """IR Class node."""
    name: str = ""
    methods: List[IRFunction] = field(default_factory=list)
    fields: List['IRVariable'] = field(default_factory=list)
    base_classes: List[str] = field(default_factory=list)
    
    def __init__(self, name: str, methods: List[IRFunction] = None,
                 fields: List['IRVariable'] = None, base_classes: List[str] = None):
        super().__init__(IRNodeType.CLASS)
        self.name = name
        self.methods = methods or []
        self.fields = fields or []
        self.base_classes = base_classes or []


@dataclass
class IRVariable(IRNode):
    """IR Variable declaration node."""
    name: str = ""
    var_type: IRType = IRType.ANY
    initial_value: Optional[IRNode] = None
    is_const: bool = False
    
    def __init__(self, name: str, var_type: IRType = IRType.ANY,
                 initial_value: Optional[IRNode] = None):
        super().__init__(IRNodeType.VARIABLE, var_type)
        self.name = name
        self.var_type = var_type
        self.initial_value = initial_value
        self.is_const = False


@dataclass
class IRAssignment(IRNode):
    """IR Assignment node."""
    target: str = ""
    value: Optional[IRNode] = None
    operator: str = "="  # =, +=, -=, etc.
    
    def __init__(self, target: str, value: IRNode, operator: str = "="):
        super().__init__(IRNodeType.ASSIGNMENT)
        self.target = target
        self.value = value
        self.operator = operator


@dataclass
class IRIf(IRNode):
    """IR If statement node."""
    condition: Optional[IRNode] = None
    then_block: List[IRNode] = field(default_factory=list)
    elif_blocks: List[tuple] = field(default_factory=list)  # [(condition, block), ...]
    else_block: List[IRNode] = field(default_factory=list)
    
    def __init__(self, condition: IRNode, then_block: List[IRNode] = None,
                 elif_blocks: List[tuple] = None, else_block: List[IRNode] = None):
        super().__init__(IRNodeType.IF)
        self.condition = condition
        self.then_block = then_block or []
        self.elif_blocks = elif_blocks or []
        self.else_block = else_block or []


@dataclass
class IRWhile(IRNode):
    """IR While loop node."""
    condition: Optional[IRNode] = None
    body: List[IRNode] = field(default_factory=list)
    
    def __init__(self, condition: IRNode, body: List[IRNode] = None):
        super().__init__(IRNodeType.WHILE)
        self.condition = condition
        self.body = body or []


@dataclass
class IRFor(IRNode):
    """IR For loop node."""
    variable: str = ""
    iterable: Optional[IRNode] = None
    body: List[IRNode] = field(default_factory=list)
    
    def __init__(self, variable: str, iterable: IRNode, body: List[IRNode] = None):
        super().__init__(IRNodeType.FOR)
        self.variable = variable
        self.iterable = iterable
        self.body = body or []


@dataclass
class IRReturn(IRNode):
    """IR Return statement node."""
    value: Optional[IRNode] = None
    
    def __init__(self, value: Optional[IRNode] = None):
        super().__init__(IRNodeType.RETURN)
        self.value = value


@dataclass
class IRCall(IRNode):
    """IR Function call node."""
    function_name: str = ""
    arguments: List[IRNode] = field(default_factory=list)
    
    def __init__(self, function_name: str, arguments: List[IRNode] = None,
                 return_type: IRType = IRType.ANY):
        super().__init__(IRNodeType.CALL, return_type)
        self.function_name = function_name
        self.arguments = arguments or []


@dataclass
class IRBinaryOp(IRNode):
    """IR Binary operation node."""
    left: Optional[IRNode] = None
    operator: str = ""
    right: Optional[IRNode] = None
    
    def __init__(self, left: IRNode, operator: str, right: IRNode,
                 result_type: IRType = IRType.ANY):
        super().__init__(IRNodeType.BINARY_OP, result_type)
        self.left = left
        self.operator = operator
        self.right = right


@dataclass
class IRUnaryOp(IRNode):
    """IR Unary operation node."""
    operator: str = ""
    operand: Optional[IRNode] = None
    
    def __init__(self, operator: str, operand: IRNode,
                 result_type: IRType = IRType.ANY):
        super().__init__(IRNodeType.UNARY_OP, result_type)
        self.operator = operator
        self.operand = operand


@dataclass
class IRLiteral(IRNode):
    """IR Literal value node."""
    value: Any = None
    literal_type: IRType = IRType.ANY
    
    def __init__(self, value: Any, literal_type: IRType):
        super().__init__(IRNodeType.LITERAL, literal_type)
        self.value = value
        self.literal_type = literal_type


@dataclass
class IRIdentifier(IRNode):
    """IR Identifier node."""
    name: str = ""
    
    def __init__(self, name: str, id_type: IRType = IRType.ANY):
        super().__init__(IRNodeType.IDENTIFIER, id_type)
        self.name = name


@dataclass
class IRBlock(IRNode):
    """IR Block of statements."""
    statements: List[IRNode] = field(default_factory=list)
    
    def __init__(self, statements: List[IRNode] = None):
        super().__init__(IRNodeType.BLOCK)
        self.statements = statements or []
