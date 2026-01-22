"""
Complete Integration Example - Lexer → Parser → Semantic Analyzer
Demonstrates the full pipeline for SyntaxShift
"""

from src.lexer import PythonLexer, JavaLexer, CppLexer
from src.parser import PythonParser, JavaParser, CppParser
from src.semantic import TypeChecker

def analyze_code(code: str, language: str):
    """
    Analyze code through the complete pipeline.
    
    Args:
        code: Source code to analyze
        language: Language ("python", "java", "cpp")
    """
    print(f"\n{'='*70}")
    print(f"Analyzing {language.upper()} Code")
    print(f"{'='*70}")
    print(f"Code:\n{code}")
    print(f"{'-'*70}")
    
    # Step 1: Lexical Analysis
    lexer_map = {
        "python": PythonLexer,
        "java": JavaLexer,
        "cpp": CppLexer
    }
    
    lexer = lexer_map[language](code)
    tokens = lexer.tokenize()
    print(f"[OK] Lexer: Generated {len(tokens)} tokens")
    
    # Step 2: Syntax Analysis (Parsing)
    parser_map = {
        "python": PythonParser,
        "java": JavaParser,
        "cpp": CppParser
    }
    
    parser = parser_map[language](tokens)
    ast = parser.parse()
    print(f"[OK] Parser: Generated AST with {len(ast.statements)} top-level statements")
    
    # Step 3: Semantic Analysis
    checker = TypeChecker(language=language)
    is_valid = checker.check(ast)
    
    print(f"[OK] Semantic Analyzer: {'PASSED' if is_valid else 'FAILED'}")
    print(f"  - Errors: {len(checker.get_errors())}")
    print(f"  - Warnings: {len(checker.get_warnings())}")
    
    # Show errors if any
    if checker.get_errors():
        print(f"\n  Errors:")
        for error in checker.get_errors():
            print(f"    [X] {error}")
    
    # Show warnings if any
    if checker.get_warnings():
        print(f"\n  Warnings:")
        for warning in checker.get_warnings():
            print(f"    [!] {warning}")
    
    # Show symbol table
    symbols = checker.symbol_table.get_all_symbols()
    if symbols:
        print(f"\n  Symbol Table ({len(symbols)} symbols):")
        for symbol in symbols:
            print(f"    - {symbol.name} ({symbol.kind.value}): {symbol.symbol_type or 'unknown'}")
    
    return is_valid, ast, checker


if __name__ == "__main__":
    print("="*70)
    print("SYNTAXSHIFT - COMPLETE PIPELINE DEMONSTRATION")
    print("="*70)
    
    # Example 1: Valid Python Code
    python_code = """
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

result = factorial(5)
"""
    analyze_code(python_code, "python")
    
    # Example 2: Python with Error
    python_error = """
def test():
    x = 5
    y = undefined_var + 10
    return y
"""
    analyze_code(python_error, "python")
    
    # Example 3: Valid Java Code
    java_code = """
public class Calculator {
    public int add(int a, int b) {
        return a + b;
    }
}
"""
    analyze_code(java_code, "java")
    
    # Example 4: Valid C++ Code
    cpp_code = """
int main() {
    int x = 5;
    int y = 10;
    int sum = x + y;
    return 0;
}
"""
    analyze_code(cpp_code, "cpp")
    
    print("\n" + "="*70)
    print("[SUCCESS] Pipeline demonstration complete!")
    print("="*70)
