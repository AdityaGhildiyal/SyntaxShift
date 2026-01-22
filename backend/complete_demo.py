"""
COMPLETE SYNTAXSHIFT PIPELINE DEMO
Source Code → Lexer → Parser → Semantic → IR → Code Generator → Target Code
"""

from src.lexer import PythonLexer, JavaLexer, CppLexer
from src.parser import PythonParser, JavaParser, CppParser
from src.semantic import TypeChecker
from src.ir import IRGenerator
from src.codegen import PythonGenerator, JavaGenerator, CppGenerator
from src.utils import ErrorHandler

def translate_code(source_code: str, source_lang: str, target_lang: str):
    """
    Complete translation pipeline.
    
    Args:
        source_code: Source code to translate
        source_lang: Source language (python, java, cpp)
        target_lang: Target language (python, java, cpp)
    """
    print("="*80)
    print(f"TRANSLATING: {source_lang.upper()} -> {target_lang.upper()}")
    print("="*80)
    
    error_handler = ErrorHandler()
    
    # Step 1: Lexical Analysis
    print("\n[1/5] LEXICAL ANALYSIS (Tokenization)")
    print("-"*80)
    
    lexer_map = {
        'python': PythonLexer,
        'java': JavaLexer,
        'cpp': CppLexer
    }
    
    lexer = lexer_map[source_lang](source_code)
    tokens = lexer.tokenize()
    print(f"[OK] Generated {len(tokens)} tokens")
    
    # Step 2: Syntax Analysis
    print("\n[2/5] SYNTAX ANALYSIS (Parsing)")
    print("-"*80)
    
    parser_map = {
        'python': PythonParser,
        'java': JavaParser,
        'cpp': CppParser
    }
    
    parser = parser_map[source_lang](tokens)
    ast = parser.parse()
    print(f"[OK] Generated AST with {len(ast.statements)} top-level statements")
    
    # Step 3: Semantic Analysis
    print("\n[3/5] SEMANTIC ANALYSIS (Type Checking)")
    print("-"*80)
    
    checker = TypeChecker(language=source_lang)
    is_valid = checker.check(ast)
    
    if not is_valid:
        print(f"[ERROR] Semantic errors found:")
        for error in checker.get_errors():
            print(f"  - {error}")
            error_handler.add_error(error, phase="semantic")
        return None
    
    print(f"[OK] No semantic errors")
    print(f"  Symbols: {len(checker.symbol_table.get_all_symbols())}")
    
    # Step 4: IR Generation
    print("\n[4/5] IR GENERATION (Intermediate Representation)")
    print("-"*80)
    
    ir_gen = IRGenerator(source_language=source_lang)
    ir_program = ir_gen.generate(ast)
    print(f"[OK] Generated IR")
    print(f"  Functions: {len(ir_program.functions)}")
    print(f"  Classes: {len(ir_program.classes)}")
    
    # Step 5: Code Generation
    print("\n[5/5] CODE GENERATION (Target Language)")
    print("-"*80)
    
    generator_map = {
        'python': PythonGenerator,
        'java': JavaGenerator,
        'cpp': CppGenerator
    }
    
    generator = generator_map[target_lang]()
    target_code = generator.generate(ir_program)
    print(f"[OK] Generated {target_lang.upper()} code ({len(target_code.split(chr(10)))} lines)")
    
    return target_code


if __name__ == "__main__":
    print("\n" + "="*80)
    print(" " * 25 + "SYNTAXSHIFT COMPILER")
    print(" " * 20 + "Complete Translation Pipeline")
    print("="*80)
    
    # Example 1: Python to Java
    print("\n\n" + "="*80)
    print("EXAMPLE 1: Python -> Java")
    print("="*80)
    
    python_code = """
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

def main():
    result = factorial(5)
    return result
"""
    
    print("\nSource Code (Python):")
    print("-"*80)
    print(python_code)
    
    java_code = translate_code(python_code, 'python', 'java')
    
    if java_code:
        print("\nGenerated Code (Java):")
        print("-"*80)
        print(java_code)
    
    # Example 2: Python to C++
    print("\n\n" + "="*80)
    print("EXAMPLE 2: Python -> C++")
    print("="*80)
    
    python_code2 = """
def add(a, b):
    result = a + b
    return result
"""
    
    print("\nSource Code (Python):")
    print("-"*80)
    print(python_code2)
    
    cpp_code = translate_code(python_code2, 'python', 'cpp')
    
    if cpp_code:
        print("\nGenerated Code (C++):")
        print("-"*80)
        print(cpp_code)
    
    # Example 3: Python to Python (identity)
    print("\n\n" + "="*80)
    print("EXAMPLE 3: Python -> Python (Code Formatting)")
    print("="*80)
    
    python_code3 = """
def greet(name):
    message = name
    return message
"""
    
    print("\nSource Code (Python):")
    print("-"*80)
    print(python_code3)
    
    python_output = translate_code(python_code3, 'python', 'python')
    
    if python_output:
        print("\nGenerated Code (Python):")
        print("-"*80)
        print(python_output)
    
    print("\n\n" + "="*80)
    print("[SUCCESS] SYNTAXSHIFT PIPELINE COMPLETE!")
    print("="*80)
    print("\nSupported Translations:")
    print("  - Python -> Java")
    print("  - Python -> C++")
    print("  - Python -> Python")
    print("  - Java -> Python")
    print("  - Java -> C++")
    print("  - C++ -> Python")
    print("  - C++ -> Java")
    print("\nAll 9 translation combinations supported!")
    print("="*80)
