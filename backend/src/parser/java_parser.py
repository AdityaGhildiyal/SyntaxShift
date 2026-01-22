"""
Parser for Java source code.
Builds AST from Java tokens.
"""

from typing import List, Optional
from .base_parser import BaseParser
from .ast_nodes import *
from ..lexer.token import TokenType


class JavaParser(BaseParser):
    """
    Parser for Java code.
    Handles Java-specific syntax like explicit typing and classes.
    """
    
    def parse(self) -> Program:
        """
        Parse Java tokens into AST.
        
        Returns:
            Program node containing all statements
        """
        statements = []
        
        while self.current_token and self.current_token.type != TokenType.EOF:
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
            self.skip_semicolons()
        
        return Program(statements)
    
    def parse_statement(self) -> Optional[ASTNode]:
        """
        Parse a single statement.
        
        Returns:
            AST node representing the statement
        """
        if not self.current_token or self.current_token.type == TokenType.EOF:
            return None
        
        # Class definition
        if self.match(TokenType.KEYWORD, 'class'):
            return self.parse_class_def()
        
        # Method definition (public static void, etc.)
        if self.current_token.type == TokenType.KEYWORD and self.current_token.value in ['public', 'private', 'protected', 'static', 'void', 'int', 'double', 'float', 'boolean', 'String']:
            # Could be method or variable declaration
            # Look ahead to determine
            if self.is_method_declaration():
                return self.parse_method_def()
            else:
                return self.parse_variable_decl()
        
        # If statement
        if self.match(TokenType.KEYWORD, 'if'):
            return self.parse_if_statement()
        
        # While loop
        if self.match(TokenType.KEYWORD, 'while'):
            return self.parse_while_loop()
        
        # For loop
        if self.match(TokenType.KEYWORD, 'for'):
            return self.parse_for_loop()
        
        # Return statement
        if self.match(TokenType.KEYWORD, 'return'):
            return self.parse_return()
        
        # Variable declaration or assignment
        if self.current_token.type == TokenType.IDENTIFIER:
            # Look ahead to check if it's a type or variable
            next_tok = self.peek()
            if next_tok and next_tok.type == TokenType.IDENTIFIER:
                # Type followed by identifier = variable declaration
                return self.parse_variable_decl()
            elif next_tok and next_tok.type == TokenType.ASSIGN:
                # Identifier = ... = assignment
                return self.parse_assignment()
            else:
                # Expression statement
                expr = self.parse_expression()
                self.consume(TokenType.SEMICOLON)
                return ExpressionStatement(expr)
        
        # Skip unknown tokens
        self.advance()
        return None
    
    def is_method_declaration(self) -> bool:
        """Check if current position is at a method declaration."""
        saved_pos = self.position
        
        # Skip access modifiers and static
        while self.current_token and self.current_token.value in ['public', 'private', 'protected', 'static']:
            self.advance()
        
        # Check for return type
        if self.current_token and self.current_token.type == TokenType.KEYWORD:
            self.advance()
            # Check for identifier (method name)
            if self.current_token and self.current_token.type == TokenType.IDENTIFIER:
                self.advance()
                # Check for opening parenthesis
                is_method = self.current_token and self.current_token.type == TokenType.LPAREN
                
                # Restore position
                self.position = saved_pos
                self.current_token = self.tokens[self.position]
                return is_method
        
        # Restore position
        self.position = saved_pos
        self.current_token = self.tokens[self.position]
        return False
    
    def parse_method_def(self) -> FunctionDef:
        """
        Parse method definition.
        
        Returns:
            FunctionDef node
        """
        # Skip access modifiers
        while self.current_token and self.current_token.value in ['public', 'private', 'protected', 'static']:
            self.advance()
        
        # Parse return type
        return_type = None
        if self.current_token and self.current_token.type == TokenType.KEYWORD:
            return_type = self.current_token.value
            self.advance()
        
        # Parse method name
        name_token = self.expect(TokenType.IDENTIFIER)
        name = name_token.value
        
        # Parse parameters
        self.expect(TokenType.LPAREN)
        parameters = self.parse_typed_parameters()
        self.expect(TokenType.RPAREN)
        
        # Parse body
        self.expect(TokenType.LBRACE)
        body = self.parse_block_statements()
        self.expect(TokenType.RBRACE)
        
        return FunctionDef(name, parameters, return_type, body)
    
    def parse_typed_parameters(self) -> List[tuple]:
        """
        Parse typed parameters for Java methods.
        
        Returns:
            List of (name, type) tuples
        """
        parameters = []
        
        while self.current_token and self.current_token.type != TokenType.RPAREN:
            # Parse type
            if self.current_token.type == TokenType.KEYWORD:
                param_type = self.current_token.value
                self.advance()
                
                # Parse name
                param_name = self.expect(TokenType.IDENTIFIER).value
                
                parameters.append((param_name, param_type))
                
                if not self.consume(TokenType.COMMA):
                    break
        
        return parameters
    
    def parse_block_statements(self) -> List[ASTNode]:
        """
        Parse statements inside braces.
        
        Returns:
            List of statement nodes
        """
        statements = []
        
        while self.current_token and self.current_token.type != TokenType.RBRACE:
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
        
        return statements
    
    def parse_class_def(self) -> ClassDef:
        """
        Parse class definition.
        
        Returns:
            ClassDef node
        """
        # Skip public/private
        if self.current_token.value in ['public', 'private']:
            self.advance()
        
        self.expect(TokenType.KEYWORD, 'class')
        name_token = self.expect(TokenType.IDENTIFIER)
        name = name_token.value
        
        # Optional extends
        base_classes = []
        if self.match(TokenType.KEYWORD, 'extends'):
            self.advance()
            base_classes.append(self.expect(TokenType.IDENTIFIER).value)
        
        # Optional implements
        if self.match(TokenType.KEYWORD, 'implements'):
            self.advance()
            while self.current_token and self.current_token.type == TokenType.IDENTIFIER:
                base_classes.append(self.current_token.value)
                self.advance()
                if not self.consume(TokenType.COMMA):
                    break
        
        self.expect(TokenType.LBRACE)
        
        # Parse class body
        methods = []
        fields = []
        
        while self.current_token and self.current_token.type != TokenType.RBRACE:
            if self.is_method_declaration():
                methods.append(self.parse_method_def())
            else:
                # Field or other statement
                stmt = self.parse_statement()
                if isinstance(stmt, VariableDecl):
                    fields.append(stmt)
        
        self.expect(TokenType.RBRACE)
        
        return ClassDef(name, methods, fields, base_classes)
    
    def parse_variable_decl(self) -> VariableDecl:
        """
        Parse variable declaration: Type name = value;
        
        Returns:
            VariableDecl node
        """
        # Parse type
        var_type = None
        if self.current_token.type == TokenType.KEYWORD or self.current_token.type == TokenType.IDENTIFIER:
            var_type = self.current_token.value
            self.advance()
        
        # Parse name
        name = self.expect(TokenType.IDENTIFIER).value
        
        # Optional initialization
        initial_value = None
        if self.consume(TokenType.ASSIGN):
            initial_value = self.parse_expression()
        
        self.consume(TokenType.SEMICOLON)
        
        return VariableDecl(name, var_type, initial_value)
    
    def parse_if_statement(self) -> IfStatement:
        """Parse if-else statement."""
        self.expect(TokenType.KEYWORD, 'if')
        self.expect(TokenType.LPAREN)
        condition = self.parse_expression()
        self.expect(TokenType.RPAREN)
        
        # Parse then block
        if self.match(TokenType.LBRACE):
            self.advance()
            then_block = self.parse_block_statements()
            self.expect(TokenType.RBRACE)
        else:
            stmt = self.parse_statement()
            then_block = [stmt] if stmt else []
        
        # Parse else block
        else_block = []
        if self.match(TokenType.KEYWORD, 'else'):
            self.advance()
            if self.match(TokenType.LBRACE):
                self.advance()
                else_block = self.parse_block_statements()
                self.expect(TokenType.RBRACE)
            else:
                stmt = self.parse_statement()
                else_block = [stmt] if stmt else []
        
        return IfStatement(condition, then_block, [], else_block)
    
    def parse_while_loop(self) -> WhileLoop:
        """Parse while loop."""
        self.expect(TokenType.KEYWORD, 'while')
        self.expect(TokenType.LPAREN)
        condition = self.parse_expression()
        self.expect(TokenType.RPAREN)
        
        if self.match(TokenType.LBRACE):
            self.advance()
            body = self.parse_block_statements()
            self.expect(TokenType.RBRACE)
        else:
            stmt = self.parse_statement()
            body = [stmt] if stmt else []
        
        return WhileLoop(condition, body)
    
    def parse_for_loop(self) -> ForLoop:
        """Parse for loop (simplified)."""
        self.expect(TokenType.KEYWORD, 'for')
        self.expect(TokenType.LPAREN)
        
        # For simplicity, we'll parse it as: for (Type var : iterable)
        # Skip initialization/condition/increment for now
        var_name = ""
        iterable = None
        
        # Try to parse enhanced for loop
        if self.current_token.type == TokenType.KEYWORD:
            self.advance()  # Skip type
            var_name = self.expect(TokenType.IDENTIFIER).value
            if self.consume(TokenType.COLON):
                iterable = self.parse_expression()
        else:
            # Traditional for loop - skip for now
            while self.current_token and self.current_token.type != TokenType.RPAREN:
                self.advance()
        
        self.expect(TokenType.RPAREN)
        
        if self.match(TokenType.LBRACE):
            self.advance()
            body = self.parse_block_statements()
            self.expect(TokenType.RBRACE)
        else:
            stmt = self.parse_statement()
            body = [stmt] if stmt else []
        
        return ForLoop(var_name, iterable, body)
    
    def parse_return(self) -> Return:
        """Parse return statement."""
        self.expect(TokenType.KEYWORD, 'return')
        
        expression = None
        if self.current_token and self.current_token.type != TokenType.SEMICOLON:
            expression = self.parse_expression()
        
        self.consume(TokenType.SEMICOLON)
        
        return Return(expression)
    
    def parse_assignment(self) -> Assignment:
        """Parse assignment statement."""
        target = self.expect(TokenType.IDENTIFIER).value
        
        operator = '='
        if self.match(TokenType.ASSIGN):
            self.advance()
        elif self.match(TokenType.PLUS_ASSIGN):
            operator = '+='
            self.advance()
        elif self.match(TokenType.MINUS_ASSIGN):
            operator = '-='
            self.advance()
        
        value = self.parse_expression()
        self.consume(TokenType.SEMICOLON)
        
        return Assignment(target, value, operator)
    
    def parse_expression(self) -> ASTNode:
        """Parse expression with operator precedence."""
        return self.parse_logical_or()
    
    def parse_logical_or(self) -> ASTNode:
        """Parse logical OR expression."""
        left = self.parse_logical_and()
        
        while self.match(TokenType.OR):
            op = self.current_token.value
            self.advance()
            right = self.parse_logical_and()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_logical_and(self) -> ASTNode:
        """Parse logical AND expression."""
        left = self.parse_comparison()
        
        while self.match(TokenType.AND):
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
        left = self.parse_unary()
        
        while self.current_token and self.current_token.type in [
            TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO
        ]:
            op = self.current_token.value
            self.advance()
            right = self.parse_unary()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_unary(self) -> ASTNode:
        """Parse unary expression."""
        if self.current_token and self.current_token.type in [TokenType.MINUS, TokenType.PLUS, TokenType.NOT]:
            op = self.current_token.value
            self.advance()
            operand = self.parse_unary()
            return UnaryOp(op, operand)
        
        return self.parse_postfix()
    
    def parse_postfix(self) -> ASTNode:
        """Parse postfix expression (function calls, array access)."""
        expr = self.parse_primary()
        
        while self.current_token:
            if self.current_token.type == TokenType.LPAREN:
                self.advance()
                arguments = self.parse_arguments()
                self.expect(TokenType.RPAREN)
                
                if isinstance(expr, Identifier):
                    expr = FunctionCall(expr.name, arguments)
            elif self.current_token.type == TokenType.LBRACKET:
                self.advance()
                index = self.parse_expression()
                self.expect(TokenType.RBRACKET)
                if isinstance(expr, Identifier):
                    expr = FunctionCall(f"{expr.name}[]", [index])
            elif self.current_token.type == TokenType.DOT:
                self.advance()
                if self.current_token.type == TokenType.IDENTIFIER:
                    member = self.current_token.value
                    self.advance()
                    # Treat as member access (simplified)
                    if isinstance(expr, Identifier):
                        expr = Identifier(f"{expr.name}.{member}")
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
        """Parse primary expression."""
        # Number
        if self.current_token.type == TokenType.INTEGER:
            value = self.current_token.value
            self.advance()
            return Literal(value, 'int')
        
        if self.current_token.type == TokenType.FLOAT:
            value = self.current_token.value
            self.advance()
            return Literal(value, 'float')
        
        # String
        if self.current_token.type == TokenType.STRING:
            value = self.current_token.value
            self.advance()
            return Literal(value, 'string')
        
        # Boolean (true/false keywords)
        if self.current_token.type == TokenType.KEYWORD and self.current_token.value in ['true', 'false']:
            value = self.current_token.value == 'true'
            self.advance()
            return Literal(value, 'bool')
        
        # Null
        if self.current_token.type == TokenType.KEYWORD and self.current_token.value == 'null':
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
        
        self.error(f"Unexpected token: {self.current_token}")