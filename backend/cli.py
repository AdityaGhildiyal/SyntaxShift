"""
SyntaxShift CLI - Command Line Interface for Code Translation
Usage: python cli.py <source_lang> <target_lang> <input_file>
Example: python cli.py python java input.py
"""

import sys
from src.lexer import PythonLexer, JavaLexer, CppLexer
from src.parser import PythonParser, JavaParser, CppParser
from src.semantic import TypeChecker
from src.ir import IRGenerator
from src.codegen import PythonGenerator, JavaGenerator, CppGenerator


def translate(source_code, source_lang, target_lang):
    """
    Translate code from source language to target language.
    
    Args:
        source_code: Source code string
        source_lang: Source language (python, java, cpp)
        target_lang: Target language (python, java, cpp)
        
    Returns:
        Translated code or None if errors occurred
    """
    # Lexer mapping
    lexer_map = {
        'python': PythonLexer,
        'java': JavaLexer,
        'cpp': CppLexer
    }
    
    # Parser mapping
    parser_map = {
        'python': PythonParser,
        'java': JavaParser,
        'cpp': CppParser
    }
    
    # Generator mapping
    generator_map = {
        'python': PythonGenerator,
        'java': JavaGenerator,
        'cpp': CppGenerator
    }
    
    try:
        # Step 1: Lexical Analysis
        print(f"[1/5] Lexing {source_lang} code...")
        lexer = lexer_map[source_lang](source_code)
        tokens = lexer.tokenize()
        print(f"      Generated {len(tokens)} tokens")
        
        # Step 2: Parsing
        print(f"[2/5] Parsing...")
        parser = parser_map[source_lang](tokens)
        ast = parser.parse()
        print(f"      Generated AST")
        
        # Step 3: Semantic Analysis
        print(f"[3/5] Semantic analysis...")
        checker = TypeChecker(language=source_lang)
        is_valid = checker.check(ast)
        
        if not is_valid:
            print(f"      ERROR: Semantic errors found:")
            for error in checker.get_errors():
                print(f"        - {error}")
            return None
        
        print(f"      No errors found")
        
        # Step 4: IR Generation
        print(f"[4/5] Generating IR...")
        ir_gen = IRGenerator(source_language=source_lang)
        ir_program = ir_gen.generate(ast)
        print(f"      Generated IR")
        
        # Step 5: Code Generation
        print(f"[5/5] Generating {target_lang} code...")
        generator = generator_map[target_lang]()
        target_code = generator.generate(ir_program)
        print(f"      Generated {len(target_code.split(chr(10)))} lines of code")
        
        return target_code
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


def main():
    """Main CLI entry point."""
    print("="*80)
    print(" " * 28 + "SYNTAXSHIFT CLI")
    print(" " * 22 + "Code Translation Tool")
    print("="*80)
    
    if len(sys.argv) < 4:
        print("\nUsage: python cli.py <source_lang> <target_lang> <input_file>")
        print("\nSupported languages: python, java, cpp")
        print("\nExamples:")
        print("  python cli.py python java input.py")
        print("  python cli.py java cpp MyClass.java")
        print("  python cli.py cpp python main.cpp")
        sys.exit(1)
    
    source_lang = sys.argv[1].lower()
    target_lang = sys.argv[2].lower()
    input_file = sys.argv[3]
    
    # Validate languages
    supported_langs = ['python', 'java', 'cpp']
    if source_lang not in supported_langs:
        print(f"ERROR: Unsupported source language '{source_lang}'")
        print(f"Supported: {', '.join(supported_langs)}")
        sys.exit(1)
    
    if target_lang not in supported_langs:
        print(f"ERROR: Unsupported target language '{target_lang}'")
        print(f"Supported: {', '.join(supported_langs)}")
        sys.exit(1)
    
    # Read input file
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            source_code = f.read()
    except FileNotFoundError:
        print(f"ERROR: File not found: {input_file}")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR reading file: {str(e)}")
        sys.exit(1)
    
    print(f"\nTranslating: {source_lang.upper()} -> {target_lang.upper()}")
    print(f"Input file: {input_file}")
    print("-"*80)
    
    # Translate
    result = translate(source_code, source_lang, target_lang)
    
    if result:
        print("\n" + "="*80)
        print("TRANSLATION SUCCESSFUL")
        print("="*80)
        print("\nGenerated Code:")
        print("-"*80)
        print(result)
        print("-"*80)
        
        # Save output
        output_file = f"output.{target_lang}"
        if target_lang == 'cpp':
            output_file = "output.cpp"
        elif target_lang == 'java':
            output_file = "Output.java"
        elif target_lang == 'python':
            output_file = "output.py"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result)
        
        print(f"\nOutput saved to: {output_file}")
    else:
        print("\n" + "="*80)
        print("TRANSLATION FAILED")
        print("="*80)
        sys.exit(1)


if __name__ == "__main__":
    main()
