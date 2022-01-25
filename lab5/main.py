
import sys
import ply.yacc as yacc
from lab5 import Mparser
from lab5.TypeChecker import TypeChecker
from TreePrinter import TreePrinter
from Interpreter import Interpreter


if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "examples/primes.m"
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
    