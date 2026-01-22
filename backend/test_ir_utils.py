"""
Test IR and Utils modules
"""

from src.lexer import PythonLexer
from src.parser import PythonParser
from src.ir import IRGenerator, IRType
from src.utils import ErrorHandler, format_code, sanitize_identifier

print("="*70)
print("IR AND UTILS MODULE TESTING")
print("="*70)

# Test 1: IR Generator
print("\n" + "="*70)
print("TEST 1: IR Generator - Convert AST to IR")
print("="*70)

code = """
def add(a, b):
    result = a + b
    return result
"""

try:
    lexer = PythonLexer(code)
    tokens = lexer.tokenize()
    parser = PythonParser(tokens)
    ast = parser.parse()
    
    # Generate IR
    ir_gen = IRGenerator(source_language="python")
    ir_program = ir_gen.generate(ast)
    
    print(f"[OK] AST to IR conversion successful")
    print(f"  Functions in IR: {len(ir_program.functions)}")
    print(f"  Classes in IR: {len(ir_program.classes)}")
    
    if ir_program.functions:
        func = ir_program.functions[0]
        print(f"\n  Function: {func.name}")
        print(f"    Parameters: {len(func.parameters)}")
        print(f"    Return type: {func.return_type.value}")
        print(f"    Body statements: {len(func.body)}")
    
    # Convert to dict
    ir_dict = ir_program.to_dict()
    print(f"\n  IR serializable: {isinstance(ir_dict, dict)}")
    
except Exception as e:
    print(f"[ERROR] Error: {e}")
    import traceback
    traceback.print_exc()

# Test 2: Error Handler
print("\n" + "="*70)
print("TEST 2: Error Handler")
print("="*70)

try:
    error_handler = ErrorHandler()
    
    # Add errors and warnings
    error_handler.add_error("Undefined variable 'x'", line=5, column=10, phase="semantic")
    error_handler.add_warning("Unused variable 'y'", line=8, column=5, phase="semantic")
    error_handler.add_info("Compilation started", phase="general")
    
    print(f"[OK] Error handler created")
    print(f"  Errors: {len(error_handler.get_errors())}")
    print(f"  Warnings: {len(error_handler.get_warnings())}")
    print(f"  Infos: {len(error_handler.get_infos())}")
    print(f"  Has errors: {error_handler.has_errors()}")
    print(f"  Summary: {error_handler.get_summary()}")
    
    print(f"\n  Error messages:")
    for error in error_handler.get_errors():
        print(f"    - {error}")
    
    print(f"\n  Warning messages:")
    for warning in error_handler.get_warnings():
        print(f"    - {warning}")
    
    # Convert to dict
    error_dict = error_handler.to_dict()
    print(f"\n  Serializable: {isinstance(error_dict, dict)}")
    
except Exception as e:
    print(f"[ERROR] Error: {e}")
    import traceback
    traceback.print_exc()

# Test 3: Helper Functions
print("\n" + "="*70)
print("TEST 3: Helper Functions")
print("="*70)

try:
    # Test sanitize_identifier
    test_names = ["class", "my-var", "123abc", "valid_name"]
    print("  Sanitize identifiers:")
    for name in test_names:
        sanitized = sanitize_identifier(name, "python")
        print(f"    '{name}' -> '{sanitized}'")
    
    # Test format_code
    messy_code = "def foo():\nx=5\nif x>0:\nreturn x"
    formatted = format_code(messy_code)
    print(f"\n  Code formatting:")
    print(f"    Before: {repr(messy_code[:30])}")
    print(f"    After: {repr(formatted[:30])}")
    
    print(f"\n[OK] Helper functions working")
    
except Exception as e:
    print(f"[ERROR] Error: {e}")
    import traceback
    traceback.print_exc()

# Test 4: Complete Pipeline with IR
print("\n" + "="*70)
print("TEST 4: Complete Pipeline - Source to IR")
print("="*70)

full_code = """
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)
"""

try:
    # Lex
    lexer = PythonLexer(full_code)
    tokens = lexer.tokenize()
    print(f"[OK] Lexer: {len(tokens)} tokens")
    
    # Parse
    parser = PythonParser(tokens)
    ast = parser.parse()
    print(f"[OK] Parser: {len(ast.statements)} statements")
    
    # Generate IR
    ir_gen = IRGenerator(source_language="python")
    ir_program = ir_gen.generate(ast)
    print(f"[OK] IR Generator: {len(ir_program.functions)} functions")
    
    if ir_program.functions:
        func = ir_program.functions[0]
        print(f"\n  Generated IR for function: {func.name}")
        print(f"    Parameters: {func.parameters}")
        print(f"    Return type: {func.return_type.value}")
        print(f"    Body has {len(func.body)} statements")
        
        # Show first statement
        if func.body:
            first_stmt = func.body[0]
            print(f"    First statement type: {first_stmt.node_type.value}")
    
    print(f"\n[OK] Complete pipeline successful!")
    
except Exception as e:
    print(f"[ERROR] Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*70)
print("\n[SUCCESS] All IR and Utils tests completed!")
print("="*70)
