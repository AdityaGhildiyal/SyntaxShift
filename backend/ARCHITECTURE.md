# SyntaxShift Backend - Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         SYNTAXSHIFT COMPILER BACKEND                        │
│                         Multi-Language Code Translator                      │
└─────────────────────────────────────────────────────────────────────────────┘

                                INPUT SOURCES
                    ┌──────────┬──────────┬──────────┐
                    │  Python  │   Java   │   C++    │
                    │  .py     │  .java   │  .cpp    │
                    └────┬─────┴────┬─────┴────┬─────┘
                         │          │          │
                         └──────────┼──────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  PHASE 1: LEXICAL ANALYSIS (Tokenization)                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                     │
│  │PythonLexer   │  │ JavaLexer    │  │  CppLexer    │                     │
│  │- Indentation │  │- Keywords    │  │- Preprocessor│                     │
│  │- Keywords    │  │- Operators   │  │- Operators   │                     │
│  └──────────────┘  └──────────────┘  └──────────────┘                     │
│                                                                              │
│  Output: Token Stream [KEYWORD, IDENTIFIER, OPERATOR, LITERAL, ...]        │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  PHASE 2: SYNTAX ANALYSIS (Parsing)                                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                     │
│  │PythonParser  │  │ JavaParser   │  │  CppParser   │                     │
│  │- Functions   │  │- Classes     │  │- Functions   │                     │
│  │- Classes     │  │- Methods     │  │- Classes     │                     │
│  │- Control Flow│  │- Control Flow│  │- Namespaces  │                     │
│  └──────────────┘  └──────────────┘  └──────────────┘                     │
│                                                                              │
│  Output: Abstract Syntax Tree (AST)                                         │
│  ┌─ Program                                                                 │
│  ├─── FunctionDef                                                           │
│  ├─── ClassDef                                                              │
│  └─── Statements                                                            │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  PHASE 3: SEMANTIC ANALYSIS (Type Checking & Validation)                   │
│  ┌──────────────────────────────────────────────────────────┐              │
│  │  TypeChecker                                             │              │
│  │  ┌────────────────┐  ┌──────────────────────────────┐   │              │
│  │  │ SymbolTable    │  │  Type Checking               │   │              │
│  │  │- Scopes        │  │  - Variable types            │   │              │
│  │  │- Symbols       │  │  - Function signatures       │   │              │
│  │  │- Lookup        │  │  - Expression types          │   │              │
│  │  └────────────────┘  └──────────────────────────────┘   │              │
│  └──────────────────────────────────────────────────────────┘              │
│                                                                              │
│  Output: Validated AST + Symbol Table + Type Information                    │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  PHASE 4: INTERMEDIATE REPRESENTATION (Language-Agnostic IR)               │
│  ┌──────────────────────────────────────────────────────────┐              │
│  │  IRGenerator                                             │              │
│  │  Converts AST → IR                                       │              │
│  │                                                           │              │
│  │  IR Node Types:                                          │              │
│  │  - IRFunction    - IRClass      - IRVariable             │              │
│  │  - IRIf          - IRWhile      - IRFor                  │              │
│  │  - IRBinaryOp    - IRUnaryOp    - IRCall                 │              │
│  │  - IRLiteral     - IRIdentifier - IRReturn               │              │
│  └──────────────────────────────────────────────────────────┘              │
│                                                                              │
│  Output: IR Program (Language-Independent Representation)                   │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  PHASE 5: CODE GENERATION (Target Language Code)                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                     │
│  │PythonGen     │  │ JavaGen      │  │  CppGen      │                     │
│  │- def/class   │  │- public/     │  │- #include    │                     │
│  │- Indentation │  │  private     │  │- namespace   │                     │
│  │- Python ops  │  │- Semicolons  │  │- Semicolons  │                     │
│  │- None/True   │  │- null/true   │  │- nullptr/true│                     │
│  └──────────────┘  └──────────────┘  └──────────────┘                     │
│                                                                              │
│  Output: Target Language Source Code                                        │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
                                OUTPUT
                    ┌──────────┬──────────┬──────────┐
                    │  Python  │   Java   │   C++    │
                    │  .py     │  .java   │  .cpp    │
                    └──────────┴──────────┴──────────┘


═══════════════════════════════════════════════════════════════════════════════
                            SUPPORTING MODULES
═══════════════════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────────────┐
│  UTILITIES MODULE                                                           │
│  ┌──────────────────────────┐  ┌──────────────────────────┐                │
│  │  ErrorHandler            │  │  Helpers                 │                │
│  │  - Error collection      │  │  - Code formatting       │                │
│  │  - Warning management    │  │  - String manipulation   │                │
│  │  - Error reporting       │  │  - Complexity calc       │                │
│  └──────────────────────────┘  └──────────────────────────┘                │
└─────────────────────────────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════════════
                        SUPPORTED TRANSLATION MATRIX
═══════════════════════════════════════════════════════════════════════════════

                    TARGET LANGUAGE
                    ┌────────┬────────┬────────┐
                    │ Python │  Java  │  C++   │
        ┌───────────┼────────┼────────┼────────┤
        │  Python   │   ✓    │   ✓    │   ✓    │
SOURCE  │  Java     │   ✓    │   ✓    │   ✓    │
LANG    │  C++      │   ✓    │   ✓    │   ✓    │
        └───────────┴────────┴────────┴────────┘

        Total: 9 Translation Combinations


═══════════════════════════════════════════════════════════════════════════════
                            DATA FLOW EXAMPLE
═══════════════════════════════════════════════════════════════════════════════

Python Code:                    IR:                         Java Code:
┌──────────────┐               ┌──────────────┐            ┌──────────────────┐
│def add(a, b):│  ──Lexer──►   │IRFunction    │  ──Gen──►  │public static     │
│  return a + b│  ──Parser─►   │  name: "add" │            │Object add(       │
└──────────────┘  ──Semantic►  │  params: [a,b│            │  Object a,       │
                  ──IR Gen──►   │  body: [     │            │  Object b) {     │
                                │    IRReturn  │            │  return (a + b); │
                                │      IRBinOp │            │}                 │
                                │  ]           │            └──────────────────┘
                                └──────────────┘


═══════════════════════════════════════════════════════════════════════════════
                            PROJECT STATUS
═══════════════════════════════════════════════════════════════════════════════

Module              Status      Files    Lines    Tests
─────────────────────────────────────────────────────────────────────────────
Lexer               ✅ DONE      5        ~600     ✅
Parser              ✅ DONE      5        ~1200    ✅
Semantic            ✅ DONE      2        ~600     ✅
IR                  ✅ DONE      2        ~500     ✅
CodeGen             ✅ DONE      4        ~600     ✅
Utils               ✅ DONE      2        ~500     ✅
─────────────────────────────────────────────────────────────────────────────
TOTAL               ✅ COMPLETE  20       ~4000    ✅

═══════════════════════════════════════════════════════════════════════════════
```
