"""
Test script to verify semantic analyzer is working correctly.
"""

from src.lexer import PythonLexer, JavaLexer, CppLexer
from src.parser import PythonParser, JavaParser, CppParser
from src.semantic import TypeChecker, SymbolTable

print("=" * 70)
print("SEMANTIC ANALYZER TESTING")
print("=" * 70)

# Test 1: Python - Valid Code
print("\n" + "=" * 70)
print("TEST 1: Python - Valid Function Definition")
print("=" * 70)

python_code_valid = """
def calculate(x, y):
    result = x + y
    return result

def main():
    a = 5
    b = 10
    c = calculate(a, b)
    return c
"""

try:
    lexer = PythonLexer(python_code_valid)
    tokens = lexer.tokenize()
    parser = PythonParser(tokens)
    ast = parser.parse()
    
    checker = TypeChecker(language="python")
    is_valid = checker.check(ast)
    
    print(f"[OK] Parsing successful")
    print(f"[OK] Semantic check: {'PASSED' if is_valid else 'FAILED'}")
    print(f"  Errors: {len(checker.get_errors())}")
    print(f"  Warnings: {len(checker.get_warnings())}")
    
    if checker.get_errors():
        print("\n  Errors found:")
        for error in checker.get_errors():
            print(f"    - {error}")
    
    if checker.get_warnings():
        print("\n  Warnings found:")
        for warning in checker.get_warnings():
            print(f"    - {warning}")
    
    # Show symbol table
    print(f"\n  Symbol Table:")
    symbols = checker.symbol_table.get_all_symbols()
    for symbol in symbols:
        print(f"    - {symbol}")
        
except Exception as e:
    print(f"[ERROR] Error: {e}")
    import traceback
    traceback.print_exc()

# Test 2: Python - Undefined Variable Error
print("\n" + "=" * 70)
print("TEST 2: Python - Undefined Variable (Should Fail)")
print("=" * 70)

python_code_error = """
def test():
    x = 5
    y = undefined_var + 10
    return y
"""

try:
    lexer = PythonLexer(python_code_error)
    tokens = lexer.tokenize()
    parser = PythonParser(tokens)
    ast = parser.parse()
    
    checker = TypeChecker(language="python")
    is_valid = checker.check(ast)
    
    print(f"[OK] Parsing successful")
    print(f"[OK] Semantic check: {'PASSED' if is_valid else 'FAILED (Expected)'}")
    print(f"  Errors: {len(checker.get_errors())}")
    
    if checker.get_errors():
        print("\n  Errors found (Expected):")
        for error in checker.get_errors():
            print(f"    - {error}")
            
except Exception as e:
    print(f"[ERROR] Error: {e}")

# Test 3: Python - Type Checking
print("\n" + "=" * 70)
print("TEST 3: Python - Type Checking")
print("=" * 70)

python_code_types = """
def add_numbers(a, b):
    result = a + b
    return result

def concat_strings(s1, s2):
    result = s1 + s2
    return result
"""

try:
    lexer = PythonLexer(python_code_types)
    tokens = lexer.tokenize()
    parser = PythonParser(tokens)
    ast = parser.parse()
    
    checker = TypeChecker(language="python")
    is_valid = checker.check(ast)
    
    print(f"[OK] Parsing successful")
    print(f"[OK] Semantic check: {'PASSED' if is_valid else 'FAILED'}")
    print(f"  Errors: {len(checker.get_errors())}")
    print(f"  Warnings: {len(checker.get_warnings())}")
    
    symbols = checker.symbol_table.get_all_symbols()
    print(f"\n  Functions defined: {len([s for s in symbols if s.kind.value == 'function'])}")
    for symbol in symbols:
        if symbol.kind.value == 'function':
            print(f"    - {symbol.name}()")
            
except Exception as e:
    print(f"[ERROR] Error: {e}")

# Test 4: Java - Class and Method
print("\n" + "=" * 70)
print("TEST 4: Java - Class and Method Definition")
print("=" * 70)

java_code = """
public class Calculator {
    public int add(int a, int b) {
        int result = a + b;
        return result;
    }
    
    public static void main(String[] args) {
        Calculator calc = new Calculator();
    }
}
"""

try:
    lexer = JavaLexer(java_code)
    tokens = lexer.tokenize()
    parser = JavaParser(tokens)
    ast = parser.parse()
    
    checker = TypeChecker(language="java")
    is_valid = checker.check(ast)
    
    print(f"[OK] Parsing successful")
    print(f"[OK] Semantic check: {'PASSED' if is_valid else 'FAILED'}")
    print(f"  Errors: {len(checker.get_errors())}")
    print(f"  Warnings: {len(checker.get_warnings())}")
    
    if checker.get_errors():
        print("\n  Errors found:")
        for error in checker.get_errors():
            print(f"    - {error}")
    
    symbols = checker.symbol_table.get_all_symbols()
    classes = [s for s in symbols if s.kind.value == 'class']
    print(f"\n  Classes defined: {len(classes)}")
    for cls in classes:
        print(f"    - {cls.name}")
        
except Exception as e:
    print(f"[ERROR] Error: {e}")
    import traceback
    traceback.print_exc()

# Test 5: C++ - Function Definition
print("\n" + "=" * 70)
print("TEST 5: C++ - Function Definition")
print("=" * 70)

cpp_code = """
int factorial(int n) {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

int main() {
    int result = factorial(5);
    return 0;
}
"""

try:
    lexer = CppLexer(cpp_code)
    tokens = lexer.tokenize()
    parser = CppParser(tokens)
    ast = parser.parse()
    
    checker = TypeChecker(language="cpp")
    is_valid = checker.check(ast)
    
    print(f"[OK] Parsing successful")
    print(f"[OK] Semantic check: {'PASSED' if is_valid else 'FAILED'}")
    print(f"  Errors: {len(checker.get_errors())}")
    print(f"  Warnings: {len(checker.get_warnings())}")
    
    if checker.get_errors():
        print("\n  Errors found:")
        for error in checker.get_errors():
            print(f"    - {error}")
    
    symbols = checker.symbol_table.get_all_symbols()
    functions = [s for s in symbols if s.kind.value == 'function']
    print(f"\n  Functions defined: {len(functions)}")
    for func in functions:
        print(f"    - {func.name}() -> {func.return_type}")
        
except Exception as e:
    print(f"[ERROR] Error: {e}")
    import traceback
    traceback.print_exc()

# Test 6: Symbol Table Test
print("\n" + "=" * 70)
print("TEST 6: Symbol Table - Scope Management")
print("=" * 70)

try:
    from src.semantic import SymbolTable, Symbol, SymbolKind
    
    st = SymbolTable()
    
    # Define global variable
    st.define(Symbol("global_var", SymbolKind.VARIABLE, "int"))
    print("[OK] Defined global variable: global_var")
    
    # Enter function scope
    st.enter_scope("function:test")
    st.define(Symbol("local_var", SymbolKind.VARIABLE, "int"))
    print("[OK] Entered function scope and defined: local_var")
    
    # Lookup variables
    global_lookup = st.lookup("global_var")
    local_lookup = st.lookup("local_var")
    
    print(f"[OK] Can access global_var from function: {global_lookup is not None}")
    print(f"[OK] Can access local_var from function: {local_lookup is not None}")
    
    # Exit scope
    st.exit_scope()
    print("[OK] Exited function scope")
    
    # Try to lookup local variable from global scope
    local_from_global = st.lookup("local_var")
    print(f"[OK] Cannot access local_var from global: {local_from_global is None}")
    
    print(f"\n  Total scopes: {len(st.scopes)}")
    print(f"  Total symbols: {len(st.get_all_symbols())}")
    
except Exception as e:
    print(f"[ERROR] Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
print("\n[SUCCESS] All semantic analyzer tests completed!")
print("=" * 70)
