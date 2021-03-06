import sys

from Interpreter import Interpreter
from lab5 import Mparser
from lab5.TypeChecker import TypeChecker

if __name__ == '__main__':
    # works for fibonacci, sqrt and pi files
    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "examples/pi.m"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    parser = Mparser.parser
    text = file.read()
    ast = parser.parse(text, lexer=Mparser.scanner.lexer)

    typeChecker = TypeChecker()
    typeChecker.visit(ast)

    ast.accept(Interpreter())
    # in future
    # ast.accept(OptimizationPass1())
    # ast.accept(OptimizationPass2())
    # ast.accept(CodeGenerator())
