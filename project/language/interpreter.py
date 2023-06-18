from project.language.interpreter_visitor import *
from project.language.lang_parser import *


def interpreter(program: str):
    parser = parse_lang(program)
    tree = parser.program()
    visitor = LangVisitor()

    errorsCnt = parser.getNumberOfSyntaxErrors()
    if errorsCnt != 0:
        raise InterpreterException(f"Exceptions in syntax errors, total count is {errorsCnt}")

    visitor.visit(tree)
