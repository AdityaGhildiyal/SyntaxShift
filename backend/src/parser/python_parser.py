"""
Parser for Python source code.
Builds AST from Python tokens.
"""

from typing import List, Optional
from .base_parser import BaseParser
from .ast_nodes import *
from ..lexer.token import TokenType


class PythonParser(BaseParser):
    """
    Parser for Python code.
    Handles Python-specific syntax like indentation and dynamic typing.
    """
    
    def parse(self) -> Program:
        """
        Parse Python tokens into AST.
        
        Returns:
            Program node containing all statements
        """
        statements = []
        
        self.skip_newlines()
        
        while self.current_token and self.current_token.type != TokenType.EOF:
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
            self.skip_newlines()
        
        return Program(statements)
    
    def parse_statement(self) -> Optional[ASTNode]:
        """
        Parse a single statement.
        
        Returns:
            AST node representing the statement
        """
        self.skip_newlines()
        
        if not self.current_token or self.current_token.type == TokenType.EOF:
            return None
        
        # Function definition
        if self.match(TokenType.KEYWORD, 'def'):
            return self.parse_function_def()
        
        # Class definition
        if self.match(TokenType.KEYWORD, 'class'):
            return self.parse_class_def()
        
        # If statement
        if self.match(TokenType.KEYWORD, 'if'):
            return self.parse_if_statement()
        
        # While loop
        if self.match(TokenType.KEYWORD, 'while'):
            return self.parse_while_loop()
        
        if self.match(TokenType.KEYWORD, 'for'):
            return self.parse_for_loop()
        
        # Break statement
        if self.match(TokenType.KEYWORD, 'break'):
            self.advance()
            return Break()
        
        # Return statement
        if self.match(TokenType.KEYWORD, 'return'):
            return self.parse_return()
        
        # Assignment or expression statement
        if self.current_token.type == TokenType.IDENTIFIER:
            # Check if it's an assignment
            if self.peek() and self.peek().type in [TokenType.ASSIGN, TokenType.PLUS_ASSIGN, TokenType.MINUS_ASSIGN]:
                return self.parse_assignment()
            else:
                # Expression statement (like function call)
                expr = self.parse_expression()
                return ExpressionStatement(expr)
        
        # Skip unknown tokens
        self.advance()
        return None
    
    def parse_function_def(self) -> FunctionDef:
        """
        Parse function definition: def name(params): body
        
        Returns:
            FunctionDef node
        """
        self.expect(TokenType.KEYWORD, 'def')
        name_token = self.expect(TokenType.IDENTIFIER)
        name = name_token.value
        
        self.expect(TokenType.LPAREN)
        parameters = self.parse_parameters()
        self.expect(TokenType.RPAREN)
        
        # Optional return type annotation (Python 3.5+)
        return_type = None
        if self.consume(TokenType.ARROW):
            if self.current_token.type == TokenType.IDENTIFIER:
                return_type = self.current_token.value
                self.advance()
        
        self.expect(TokenType.COLON)
        self.skip_newlines()
        
        # Parse function body
        body = self.parse_block()
        
        return FunctionDef(name, parameters, return_type, body)
    
    def parse_parameters(self) -> List[tuple]:
        """
        Parse function parameters.
        
        Returns:
            List of (name, type) tuples
        """
        parameters = []
        
        while self.current_token and self.current_token.type != TokenType.RPAREN:
            if self.current_token.type == TokenType.IDENTIFIER:
                param_name = self.current_token.value
                self.advance()
                
                # Optional type annotation
                param_type = None
                if self.consume(TokenType.COLON):
                    if self.current_token.type == TokenType.IDENTIFIER:
                        param_type = self.current_token.value
                        self.advance()
                
                parameters.append((param_name, param_type))
                
                if not self.consume(TokenType.COMMA):
                    break
        
        return parameters
    
    def parse_block(self) -> List[ASTNode]:
        """
        Parse a block of statements (indented code).
        
        Returns:
            List of statement nodes
        """
        statements = []
        
        # Expect indent
        if not self.consume(TokenType.INDENT):
            # Single-line block or error
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
            return statements
        
        # Parse statements until dedent
        while self.current_token and self.current_token.type != TokenType.DEDENT:
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
            self.skip_newlines()
        
        # Consume dedent
        self.consume(TokenType.DEDENT)
        
        return statements
    
    def parse_class_def(self) -> ClassDef:
        """
        Parse class definition: class Name: body
        
        Returns:
            ClassDef node
        """
        self.expect(TokenType.KEYWORD, 'class')
        name_token = self.expect(TokenType.IDENTIFIER)
        name = name_token.value
        
        # Optional base classes
        base_classes = []
        if self.consume(TokenType.LPAREN):
            while self.current_token and self.current_token.type != TokenType.RPAREN:
                if self.current_token.type == TokenType.IDENTIFIER:
                    base_classes.append(self.current_token.value)
                    self.advance()
                if not self.consume(TokenType.COMMA):
                    break
            self.expect(TokenType.RPAREN)
        
        self.expect(TokenType.COLON)
        self.skip_newlines()
        
        # Parse class body
        methods = []
        fields = []
        
        if self.consume(TokenType.INDENT):
            while self.current_token and self.current_token.type != TokenType.DEDENT:
                if self.match(TokenType.KEYWORD, 'def'):
                    methods.append(self.parse_function_def())
                else:
                    # Could be field declaration or other statement
                    self.parse_statement()
                self.skip_newlines()
            
            self.consume(TokenType.DEDENT)
        
        return ClassDef(name, methods, fields, base_classes)
    
    def parse_if_statement(self) -> IfStatement:
        """
        Parse if-elif-else statement.
        
        Returns:
            IfStatement node
        """
        self.expect(TokenType.KEYWORD, 'if')
        condition = self.parse_expression()
        self.expect(TokenType.COLON)
        self.skip_newlines()
        
        then_block = self.parse_block()
        
        # Parse elif blocks
        elif_blocks = []
        while self.match(TokenType.KEYWORD, 'elif'):
            self.advance()
            elif_condition = self.parse_expression()
            self.expect(TokenType.COLON)
            self.skip_newlines()
            elif_body = self.parse_block()
            elif_blocks.append((elif_condition, elif_body))
        
        # Parse else block
        else_block = []
        if self.match(TokenType.KEYWORD, 'else'):
            self.advance()
            self.expect(TokenType.COLON)
            self.skip_newlines()
            else_block = self.parse_block()
        
        return IfStatement(condition, then_block, elif_blocks, else_block)
    
    def parse_while_loop(self) -> WhileLoop:
        """
        Parse while loop.
        
        Returns:
            WhileLoop node
        """
        self.expect(TokenType.KEYWORD, 'while')
        condition = self.parse_expression()
        self.expect(TokenType.COLON)
        self.skip_newlines()
        
        body = self.parse_block()
        
        return WhileLoop(condition, body)
    
    def parse_for_loop(self) -> ForLoop:
        """
        Parse for loop: for var in iterable: body
        
        Returns:
            ForLoop node
        """
        self.expect(TokenType.KEYWORD, 'for')
        var_token = self.expect(TokenType.IDENTIFIER)
        variable = var_token.value
        
        self.expect(TokenType.KEYWORD, 'in')
        iterable = self.parse_expression()
        
        self.expect(TokenType.COLON)
        self.skip_newlines()
        
        body = self.parse_block()
        
        return ForLoop(variable, iterable, body)
    
    def parse_return(self) -> Return:
        """
        Parse return statement.
        
        Returns:
            Return node
        """
        self.expect(TokenType.KEYWORD, 'return')
        
        # Check if there's an expression
        if self.current_token and self.current_token.type not in [TokenType.NEWLINE, TokenType.EOF]:
            expression = self.parse_expression()
            return Return(expression)
        
        return Return(None)
    
    def parse_assignment(self) -> Assignment:
        """
        Parse assignment statement.
        
        Returns:
            Assignment node
        """
        target_token = self.expect(TokenType.IDENTIFIER)
        target = target_token.value
        
        # Get operator (=, +=, -=)
        operator = '='
        if self.match(TokenType.ASSIGN):
            operator = '='
            self.advance()
        elif self.match(TokenType.PLUS_ASSIGN):
            operator = '+='
            self.advance()
        elif self.match(TokenType.MINUS_ASSIGN):
            operator = '-='
            self.advance()
        
        value = self.parse_expression()
        
        return Assignment(target, value, operator)
    
    def parse_expression(self) -> ASTNode:
        """
        Parse an expression with operator precedence.
        
        Returns:
            Expression AST node
        """
        return self.parse_logical_or()
    
    def parse_logical_or(self) -> ASTNode:
        """Parse logical OR expression."""
        left = self.parse_logical_and()
        
        while self.match(TokenType.KEYWORD, 'or'):
            op = self.current_token.value
            self.advance()
            right = self.parse_logical_and()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_logical_and(self) -> ASTNode:
        """Parse logical AND expression."""
        left = self.parse_comparison()
        
        while self.match(TokenType.KEYWORD, 'and'):
            op = self.current_token.value
            self.advance()
            right = self.parse_comparison()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_comparison(self) -> ASTNode:
        """Parse comparison expression."""
        left = self.parse_additive()
        
        while self.current_token and self.current_token.type in [
            TokenType.EQUAL, TokenType.NOT_EQUAL,
            TokenType.LESS_THAN, TokenType.GREATER_THAN,
            TokenType.LESS_EQUAL, TokenType.GREATER_EQUAL
        ]:
            op = self.current_token.value
            self.advance()
            right = self.parse_additive()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_additive(self) -> ASTNode:
        """Parse addition/subtraction expression."""
        left = self.parse_multiplicative()
        
        while self.current_token and self.current_token.type in [TokenType.PLUS, TokenType.MINUS]:
            op = self.current_token.value
            self.advance()
            right = self.parse_multiplicative()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_multiplicative(self) -> ASTNode:
        """Parse multiplication/division expression."""
        left = self.parse_power()
        
        while self.current_token and self.current_token.type in [
            TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO, TokenType.FLOOR_DIVIDE
        ]:
            op = self.current_token.value
            self.advance()
            right = self.parse_power()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_power(self) -> ASTNode:
        """Parse power/exponentiation expression."""
        left = self.parse_unary()
        
        if self.current_token and self.current_token.type == TokenType.POWER:
            op = self.current_token.value
            self.advance()
            right = self.parse_power()  # Right associative
            return BinaryOp(left, op, right)
        
        return left
    
    def parse_unary(self) -> ASTNode:
        """Parse unary expression."""
        if self.current_token and self.current_token.type in [TokenType.MINUS, TokenType.PLUS]:
            op = self.current_token.value
            self.advance()
            operand = self.parse_unary()
            return UnaryOp(op, operand)
        
        if self.match(TokenType.KEYWORD, 'not'):
            op = self.current_token.value
            self.advance()
            operand = self.parse_unary()
            return UnaryOp(op, operand)
        
        return self.parse_postfix()
    
    def parse_postfix(self) -> ASTNode:
        """Parse postfix expression (function calls, array access, attribute access)."""
        expr = self.parse_primary()
        
        while self.current_token:
            # Attribute access (dot notation)
            if self.current_token.type == TokenType.DOT:
                self.advance()
                if self.current_token.type == TokenType.IDENTIFIER:
                    attr_name = self.current_token.value
                    self.advance()
                    
                    # Check if it's a method call (followed by parentheses)
                    if self.current_token and self.current_token.type == TokenType.LPAREN:
                        self.advance()
                        arguments = self.parse_arguments()
                        self.expect(TokenType.RPAREN)
                        
                        # Create method call: object.method(args)
                        # Store as FunctionCall with object as first argument
                        if isinstance(expr, Identifier):
                            # Method call: obj.method(args) -> method(obj, args)
                            expr = FunctionCall(f"{expr.name}.{attr_name}", arguments)
                        else:
                            # Complex expression
                            expr = FunctionCall(f"?.{attr_name}", arguments)
                    else:
                        # Attribute access: object.attribute
                        if isinstance(expr, Identifier):
                            expr = Identifier(f"{expr.name}.{attr_name}")
                        else:
                            expr = Identifier(f"?.{attr_name}")
            # Function call
            elif self.current_token.type == TokenType.LPAREN:
                self.advance()
                arguments = self.parse_arguments()
                self.expect(TokenType.RPAREN)
                
                # Get function name from expression
                if isinstance(expr, Identifier):
                    expr = FunctionCall(expr.name, arguments)
                else:
                    # Complex expression, keep as is
                    pass
            # Array/list access
            elif self.current_token.type == TokenType.LBRACKET:
                self.advance()
                index = self.parse_expression()
                self.expect(TokenType.RBRACKET)
                # For simplicity, treat as function call
                if isinstance(expr, Identifier):
                    expr = FunctionCall(f"{expr.name}[]", [index])
            else:
                break
        
        return expr
    
    def parse_arguments(self) -> List[ASTNode]:
        """Parse function call arguments."""
        arguments = []
        
        while self.current_token and self.current_token.type != TokenType.RPAREN:
            arguments.append(self.parse_expression())
            if not self.consume(TokenType.COMMA):
                break
        
        return arguments
    
    def parse_primary(self) -> ASTNode:
        """Parse primary expression (literals, identifiers, parentheses)."""
        # Number literal (integer)
        if self.current_token.type == TokenType.INTEGER:
            value = self.current_token.value
            self.advance()
            return Literal(value, 'int')
        
        # Number literal (float)
        if self.current_token.type == TokenType.FLOAT:
            value = self.current_token.value
            self.advance()
            return Literal(value, 'float')
    
        # String literal
        if self.current_token.type == TokenType.STRING:
            value = self.current_token.value
            self.advance()
            return Literal(value, 'string')
        
        # F-string literal - convert to string concatenation
        if self.current_token.type == TokenType.F_STRING:
            parts = self.current_token.value  # List of ('string', text) or ('expr', expr_str)
            self.advance()
            
            if not parts:
                return Literal('', 'string')
            
            if len(parts) == 1 and parts[0][0] == 'string':
                # Simple string with no interpolation
                return Literal(parts[0][1], 'string')
            
            # Build concatenation expression
            # For each part, create either a Literal or parse the expression
            result = None
            for part_type, part_value in parts:
                if part_type == 'string':
                    part_node = Literal(part_value, 'string')
                else:
                    # Parse the expression string
                    # Create a mini-lexer and parser for the expression
                    from ..lexer.python_lexer import PythonLexer
                    expr_lexer = PythonLexer(part_value)
                    expr_tokens = expr_lexer.tokenize()
                    # Remove EOF token
                    if expr_tokens and expr_tokens[-1].type == TokenType.EOF:
                        expr_tokens = expr_tokens[:-1]
                    
                    if expr_tokens:
                        # Create a temporary parser for the expression
                        temp_parser = PythonParser(expr_tokens + [expr_tokens[0].__class__(TokenType.EOF, None, 0, 0)])
                        part_node = temp_parser.parse_expression()
                        # Convert to string using str() function call
                        part_node = FunctionCall('str', [part_node])
                    else:
                        part_node = Literal('', 'string')
                
                if result is None:
                    result = part_node
                else:
                    # Concatenate with +
                    result = BinaryOp(result, '+', part_node)
            
            return result if result else Literal('', 'string')
        
        # Boolean literal (True/False keywords)
        if self.current_token.type == TokenType.KEYWORD and self.current_token.value in ['True', 'False']:
            value = self.current_token.value == 'True'
            self.advance()
            return Literal(value, 'bool')
        
        # None literal
        if self.current_token.type == TokenType.KEYWORD and self.current_token.value == 'None':
            self.advance()
            return Literal(None, 'null')
        
        # Identifier
        if self.current_token.type == TokenType.IDENTIFIER:
            name = self.current_token.value
            self.advance()
            return Identifier(name)
        
        # Parenthesized expression
        if self.current_token.type == TokenType.LPAREN:
            self.advance()
            expr = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return expr
        
        # List literal
        if self.current_token.type == TokenType.LBRACKET:
            self.advance()
            elements = []
            while self.current_token and self.current_token.type != TokenType.RBRACKET:
                elements.append(self.parse_expression())
                if not self.consume(TokenType.COMMA):
                    break
            self.expect(TokenType.RBRACKET)
            # Represent list as function call to 'list'
            return FunctionCall('list', elements)
        
        self.error(f"Unexpected token: {self.current_token}")