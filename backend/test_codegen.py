"""
Test Code Generators - Save output to file
"""

from src.lexer import PythonLexer
from src.parser import PythonParser
from src.ir import IRGenerator
from src.codegen import PythonGenerator, JavaGenerator, CppGenerator

# Simple Python code
python_code = """
def add(a, b):
    result = a + b
    return result
"""

output_lines = []

def log(msg):
    print(msg)
    output_lines.append(msg)

log("="*80)
log("Testing Code Generators")
log("="*80)

# Step 1: Lex
log("\n[1] Lexing...")
lexer = PythonLexer(python_code)
tokens = lexer.tokenize()
log(f"[OK] {len(tokens)} tokens")

# Step 2: Parse
log("\n[2] Parsing...")
parser = PythonParser(tokens)
ast = parser.parse()
log(f"[OK] AST created")

# Step 3: Generate IR
log("\n[3] Generating IR...")
ir_gen = IRGenerator(source_language='python')
ir_program = ir_gen.generate(ast)
log(f"[OK] IR created with {len(ir_program.functions)} functions")

# Step 4: Generate Python
log("\n[4] Generating Python code...")
py_gen = PythonGenerator()
py_code = py_gen.generate(ir_program)
log("Generated Python:")
log("-"*80)
log(py_code)
log("-"*80)

# Step 5: Generate Java
log("\n[5] Generating Java code...")
java_gen = JavaGenerator()
java_code = java_gen.generate(ir_program)
log("Generated Java:")
log("-"*80)
log(java_code)
log("-"*80)

# Step 6: Generate C++
log("\n[6] Generating C++ code...")
cpp_gen = CppGenerator()
cpp_code = cpp_gen.generate(ir_program)
log("Generated C++:")
log("-"*80)
log(cpp_code)
log("-"*80)

log("\n[SUCCESS] All code generators working!")

# Save to file
with open('codegen_test_output.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output_lines))

print("\n[SAVED] Output written to codegen_test_output.txt")
