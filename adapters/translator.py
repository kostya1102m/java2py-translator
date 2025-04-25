from use_cases.lexer import Lexer
from use_cases.parser import Parser
from use_cases.code_generator import CodeGenerator

def translate(input_file_path, output_file_path):
    
    with open(input_file_path, 'r', encoding='utf-8') as java_file:
        java_code = java_file.read()
    

    lexer = Lexer(java_code)
    parser = Parser(lexer)
    ast = parser.program()
    generator = CodeGenerator()
    python_code = generator.generate(ast)
    
  
    with open(output_file_path, 'w', encoding='utf-8') as py_file:
        py_file.write(python_code)
    
    return output_file_path  