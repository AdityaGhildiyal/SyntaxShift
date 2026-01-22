from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

# Add parent directory to path to allow importing modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.lexer import PythonLexer, JavaLexer, CppLexer
from src.parser import PythonParser, JavaParser, CppParser
from src.semantic import TypeChecker
from src.ir import IRGenerator
from src.codegen import PythonGenerator, JavaGenerator, CppGenerator

app = FastAPI(title="SyntaxShift Compiler API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ConversionRequest(BaseModel):
    source_code: str
    source_language: str
    target_language: str

class ConversionResponse(BaseModel):
    target_code: str = ""
    error: str = ""
    success: bool

@app.get("/")
def health_check():
    return {"status": "ok", "version": "1.0.0"}

@app.post("/convert", response_model=ConversionResponse)
def convert_code(request: ConversionRequest):
    try:
        source_lang = request.source_language.lower()
        target_lang = request.target_language.lower()
        code = request.source_code

        # 1. Lexer
        lexer_map = {
            'python': PythonLexer,
            'java': JavaLexer,
            'cpp': CppLexer
        }
        
        if source_lang not in lexer_map:
            raise HTTPException(status_code=400, detail=f"Unsupported source language: {source_lang}")
            
        lexer = lexer_map[source_lang](code)
        tokens = lexer.tokenize()
        
        # 2. Parser
        parser_map = {
            'python': PythonParser,
            'java': JavaParser,
            'cpp': CppParser
        }
        
        parser = parser_map[source_lang](tokens)
        ast = parser.parse()
        
        # 3. Semantic Analysis
        checker = TypeChecker(language=source_lang)
        is_valid = checker.check(ast)
        
        if not is_valid:
            errors = "\n".join([str(e) for e in checker.get_errors()])
            return ConversionResponse(success=False, error=f"Semantic Errors:\n{errors}")
            
        # 4. IR Generation
        ir_gen = IRGenerator(source_language=source_lang)
        ir_program = ir_gen.generate(ast)
        
        # 5. Code Generation
        generator_map = {
            'python': PythonGenerator,
            'java': JavaGenerator,
            'cpp': CppGenerator
        }
        
        if target_lang not in generator_map:
            raise HTTPException(status_code=400, detail=f"Unsupported target language: {target_lang}")
            
        generator = generator_map[target_lang]()
        target_code = generator.generate(ir_program)
        
        return ConversionResponse(success=True, target_code=target_code)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return ConversionResponse(success=False, error=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
