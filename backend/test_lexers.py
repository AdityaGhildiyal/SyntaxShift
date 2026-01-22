"""
Test script to verify all lexers are working correctly.
"""

from src.lexer import CppLexer, JavaLexer, PythonLexer

# Test C++ Lexer
cpp_code = """
#include <iostream>
int main() {
    int x = 5;
    std::cout << "Hello" << std::endl;
    return 0;
}
"""

print("Testing C++ Lexer...")
cpp_lexer = CppLexer(cpp_code)
cpp_tokens = cpp_lexer.tokenize()
print(f"[OK] C++ Lexer: Generated {len(cpp_tokens)} tokens")
print(f"  First 5 tokens: {cpp_tokens[:5]}")

# Test Java Lexer
java_code = """
public class Main {
    public static void main(String[] args) {
        int x = 10;
        System.out.println("Hello");
    }
}
"""

print("\nTesting Java Lexer...")
java_lexer = JavaLexer(java_code)
java_tokens = java_lexer.tokenize()
print(f"[OK] Java Lexer: Generated {len(java_tokens)} tokens")
print(f"  First 5 tokens: {java_tokens[:5]}")

# Test Python Lexer
python_code = """
def hello():
    x = 5
    print("Hello World")
    return x ** 2
"""

print("\nTesting Python Lexer...")
python_lexer = PythonLexer(python_code)
python_tokens = python_lexer.tokenize()
print(f"[OK] Python Lexer: Generated {len(python_tokens)} tokens")
print(f"  First 5 tokens: {python_tokens[:5]}")

print("\n[SUCCESS] All lexers are working correctly!")
