# SyntaxShift Backend - Complete Compiler Implementation

## 🎯 Overview

**SyntaxShift** is a multi-language compiler that translates code between Python, Java, and C++. It implements a complete compilation pipeline from lexical analysis through code generation.

## ✨ Features

- **Multi-Language Support**: Translate between Python, Java, and C++
- **Complete Pipeline**: Lexer → Parser → Semantic Analyzer → IR → Code Generator
- **9 Translation Combinations**: Any supported language to any other
- **Type Checking**: Comprehensive semantic analysis
- **Error Reporting**: Detailed error messages with line numbers
- **Modular Design**: Easy to extend with new languages

## 📦 Installation

No external dependencies required! Uses only Python standard library.

```bash
cd backend
python -m py_compile src/**/*.py  # Verify all modules
```

## 🚀 Quick Start

### Using the CLI

```bash
# Translate Python to Java
python cli.py python java input.py

# Translate Java to C++
python cli.py java cpp MyClass.java

# Translate C++ to Python
python cli.py cpp python main.cpp
```

### Using as a Library

```python
from src.lexer import PythonLexer
from src.parser import PythonParser
from src.semantic import TypeChecker
from src.ir import IRGenerator
from src.codegen import JavaGenerator

# Your Python code
code = """
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)
"""

# Complete translation pipeline
lexer = PythonLexer(code)
tokens = lexer.tokenize()

parser = PythonParser(tokens)
ast = parser.parse()

checker = TypeChecker(language='python')
checker.check(ast)

ir_gen = IRGenerator(source_language='python')
ir_program = ir_gen.generate(ast)

java_gen = JavaGenerator()
java_code = java_gen.generate(ir_program)

print(java_code)
```

## 📚 Architecture

### 1. Lexer (`src/lexer/`)
Tokenizes source code into a stream of tokens.

- `PythonLexer` - Handles Python syntax, indentation
- `JavaLexer` - Handles Java syntax, keywords
- `CppLexer` - Handles C++ syntax, preprocessor directives

### 2. Parser (`src/parser/`)
Converts tokens into an Abstract Syntax Tree (AST).

- `PythonParser` - Python grammar rules
- `JavaParser` - Java grammar rules
- `CppParser` - C++ grammar rules

### 3. Semantic Analyzer (`src/semantic/`)
Performs type checking and semantic validation.

- `SymbolTable` - Manages scopes and symbols
- `TypeChecker` - Validates types and semantics

### 4. IR Generator (`src/ir/`)
Converts AST to language-agnostic Intermediate Representation.

- `IRGenerator` - AST to IR conversion
- `IRNode` types - Language-independent representation

### 5. Code Generator (`src/codegen/`)
Generates target language code from IR.

- `PythonGenerator` - Generates Python code
- `JavaGenerator` - Generates Java code
- `CppGenerator` - Generates C++ code

### 6. Utilities (`src/utils/`)
Helper functions and error handling.

- `ErrorHandler` - Centralized error management
- `helpers` - Utility functions

## 🔄 Translation Examples

### Example 1: Python → Java

**Input (Python)**:
```python
def greet(name):
    message = "Hello, " + name
    return message
```

**Output (Java)**:
```java
public static String greet(String name) {
    String message = ("Hello, " + name);
    return message;
}
```

### Example 2: Python → C++

**Input (Python)**:
```python
def add(a, b):
    result = a + b
    return result
```

**Output (C++)**:
```cpp
#include <iostream>
#include <string>

using namespace std;

auto add(auto a, auto b) {
    auto result = (a + b);
    return result;
}
```

## 🧪 Testing

Run the test suites:

```bash
# Test lexers
python test_lexers.py

# Test parsers
python test_parsers.py

# Test semantic analyzer
python test_simple_semantic.py

# Test IR and utilities
python test_ir_utils.py

# Test code generators
python test_codegen.py

# Run complete demo
python demo_pipeline.py
```

## 📁 Project Structure

```
backend/
├── src/
│   ├── lexer/              # Lexical analysis
│   │   ├── token.py
│   │   ├── base_lexer.py
│   │   ├── python_lexer.py
│   │   ├── java_lexer.py
│   │   └── cpp_lexer.py
│   ├── parser/             # Syntax analysis
│   │   ├── ast_nodes.py
│   │   ├── base_parser.py
│   │   ├── python_parser.py
│   │   ├── java_parser.py
│   │   └── cpp_parser.py
│   ├── semantic/           # Semantic analysis
│   │   ├── symbol_table.py
│   │   └── type_checker.py
│   ├── ir/                 # Intermediate representation
│   │   ├── ir_nodes.py
│   │   └── ir_generator.py
│   ├── codegen/            # Code generation
│   │   ├── base_generator.py
│   │   ├── python_generator.py
│   │   ├── java_generator.py
│   │   └── cpp_generator.py
│   └── utils/              # Utilities
│       ├── error_handler.py
│       └── helpers.py
├── cli.py                  # Command-line interface
├── demo_pipeline.py        # Integration demo
├── complete_demo.py        # Full end-to-end demo
└── test_*.py              # Test files
```

## 🎓 Supported Language Features

### Python
- ✅ Functions and classes
- ✅ Control flow (if/elif/else, while, for)
- ✅ Operators and expressions
- ✅ Indentation-based syntax
- ✅ Type inference

### Java
- ✅ Classes and methods
- ✅ Access modifiers
- ✅ Control flow
- ✅ Type declarations
- ✅ Object-oriented features

### C++
- ✅ Functions and classes
- ✅ Namespaces
- ✅ Pointers and references
- ✅ Templates (basic)
- ✅ Preprocessor directives

## 🔧 Extending the Compiler

### Adding a New Language

1. **Create a Lexer** in `src/lexer/`
   - Extend `BaseLexer`
   - Define language-specific tokens

2. **Create a Parser** in `src/parser/`
   - Extend `BaseParser`
   - Implement grammar rules

3. **Create a Code Generator** in `src/codegen/`
   - Extend `BaseGenerator`
   - Implement code generation methods

4. **Update Mappings** in CLI and demos

## 📊 Compilation Pipeline

```
┌─────────────────┐
│  Source Code    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  LEXER          │  Tokenization
│  (Lexical       │  
│   Analysis)     │
└────────┬────────┘
         │ Tokens
         ▼
┌─────────────────┐
│  PARSER         │  Syntax Analysis
│  (Syntax        │  AST Generation
│   Analysis)     │
└────────┬────────┘
         │ AST
         ▼
┌─────────────────┐
│  SEMANTIC       │  Type Checking
│  ANALYZER       │  Symbol Resolution
│                 │
└────────┬────────┘
         │ Validated AST
         ▼
┌─────────────────┐
│  IR GENERATOR   │  Language-Agnostic
│                 │  Representation
└────────┬────────┘
         │ IR
         ▼
┌─────────────────┐
│  CODE           │  Target Language
│  GENERATOR      │  Code Generation
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Target Code    │
└─────────────────┘
```

## 🎯 Design Principles

1. **Separation of Concerns**: Each phase is independent
2. **Language Agnostic IR**: Universal intermediate representation
3. **Extensibility**: Easy to add new languages
4. **Error Handling**: Comprehensive error reporting
5. **Type Safety**: Strong type checking in semantic phase

## 📝 License

This project is part of the SyntaxShift application.

## 👥 Contributing

Contributions are welcome! Areas for improvement:
- Additional language support
- Optimization passes
- Better type inference
- Standard library support
- More comprehensive testing

## 🎉 Status

**✅ COMPLETE** - All core modules implemented and tested!

- Lexer: ✅ Complete
- Parser: ✅ Complete
- Semantic Analyzer: ✅ Complete
- IR Generator: ✅ Complete
- Code Generator: ✅ Complete
- Testing: ✅ Complete
- Documentation: ✅ Complete

---

**Happy Coding! 🚀**
