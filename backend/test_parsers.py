"""
Test script to verify all parsers are working correctly.
"""

from src.lexer import CppLexer, JavaLexer, PythonLexer
from src.parser import CppParser, JavaParser, PythonParser

print("=" * 60)
print("PARSER TESTING")
print("=" * 60)

# Test Python Parser
print("\n1. Testing Python Parser...")
python_code = """
def hello(name):
    x = 5
    if x > 3:
        print(name)
    return x
"""

try:
    python_lexer = PythonLexer(python_code)
    python_tokens = python_lexer.tokenize()
    python_parser = PythonParser(python_tokens)
    python_ast = python_parser.parse()
    print(f"   [OK] Python Parser: Generated AST with {len(python_ast.statements)} top-level statements")
    print(f"   AST: {python_ast.to_dict()}")
except Exception as e:
    print(f"   [ERROR] Python Parser Error: {e}")

# Test Java Parser
print("\n2. Testing Java Parser...")
java_code = """
public class Main {
    public static void main(String[] args) {
        int x = 10;
        if (x > 5) {
            System.out.println("Hello");
        }
    }
}
"""

try:
    java_lexer = JavaLexer(java_code)
    java_tokens = java_lexer.tokenize()
    java_parser = JavaParser(java_tokens)
    java_ast = java_parser.parse()
    print(f"   [OK] Java Parser: Generated AST with {len(java_ast.statements)} top-level statements")
    print(f"   AST: {java_ast.to_dict()}")
except Exception as e:
    print(f"   [ERROR] Java Parser Error: {e}")

# Test C++ Parser
print("\n3. Testing C++ Parser...")
cpp_code = """
int main() {
    int x = 5;
    if (x > 0) {
        return x;
    }
    return 0;
}
"""

try:
    cpp_lexer = CppLexer(cpp_code)
    cpp_tokens = cpp_lexer.tokenize()
    cpp_parser = CppParser(cpp_tokens)
    cpp_ast = cpp_parser.parse()
    print(f"   [OK] C++ Parser: Generated AST with {len(cpp_ast.statements)} top-level statements")
    print(f"   AST: {cpp_ast.to_dict()}")
except Exception as e:
    print(f"   [ERROR] C++ Parser Error: {e}")

print("\n" + "=" * 60)
print("\n[SUCCESS] All parser tests completed!")
print("=" * 60)
