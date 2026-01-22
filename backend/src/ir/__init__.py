"""
Intermediate Representation (IR) module.
Exports IR nodes and generator.
"""

from .ir_nodes import (
    IRNode,
    IRNodeType,
    IRType,
    IRProgram,
    IRFunction,
    IRClass,
    IRVariable,
    IRAssignment,
    IRIf,
    IRWhile,
    IRFor,
    IRReturn,
    IRCall,
    IRBinaryOp,
    IRUnaryOp,
    IRLiteral,
    IRIdentifier,
    IRBlock,
)
from .ir_generator import IRGenerator

__all__ = [
    'IRNode',
    'IRNodeType',
    'IRType',
    'IRProgram',
    'IRFunction',
    'IRClass',
    'IRVariable',
    'IRAssignment',
    'IRIf',
    'IRWhile',
    'IRFor',
    'IRReturn',
    'IRCall',
    'IRBinaryOp',
    'IRUnaryOp',
    'IRLiteral',
    'IRIdentifier',
    'IRBlock',
    'IRGenerator',
]
