from __future__ import print_function
from lab3 import AST


def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func

    return decorator


class TreePrinter:

    @addToClass(AST.IntNum)
    def printTree(self, indent=0):
        print("|  " * indent, end="")
        print(self.value)

    @addToClass(AST.Program)
    def printTree(self, indent=0):
        if self.instructions:
            self.instructions.printTree(indent)

    @addToClass(AST.Instructions)
    def printTree(self, indent=0):
        for instruction in self.instructions:
            instruction.printTree(indent)

    @addToClass(AST.Assignment)
    def printTree(self, indent=0):
        print("|  " * indent, end='')
        print(self.op)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.Variable)
    def printTree(self, indent=0):
        print("|  " * indent, end='')
        print(self.name)

    @addToClass(AST.Slice)
    def printTree(self, indent=0):
        print("|  " * indent, end='')
        print('REF')

        print("|  " * (indent + 1), end='')
        print(self.name)

        self.vector.printTree(indent + 1)

    @addToClass(AST.Row)
    def printTree(self, indent=0):
        print("|  " * indent, end='')
        print('VECTOR')

        for value in self.values:
            value.printTree(indent + 1)

    @addToClass(AST.Function)
    def printTree(self, indent=0):
        print("|  " * indent, end='')
        print(self.function)

        print("|  " * (indent + 1), end='')
        print(self.arg)

    @addToClass(AST.BinExpr)
    def printTree(self, indent=0):
        print("|  " * indent, end='')
        print(self.op)

        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.UnaryExpr)
    def printTree(self, indent=0):
        print("|  " * indent, end='')
        print(self.op)

        self.operand.printTree(indent + 1)

    @addToClass(AST.WhileLoop)
    def printTree(self, indent=0):
        print("|  " * indent, end='')
        print('WHILE')

        self.condition.printTree(indent + 1)
        self.instruction.printTree(indent + 1)

    @addToClass(AST.ForLoop)
    def printTree(self, indent=0):
        print("|  " * indent, end='')
        print('FOR')

        self.variable.printTree(indent + 1)

        print("|  " * (indent + 1), end='')
        print('RANGE')
        self.left_range.printTree(indent + 2)
        self.right_range.printTree(indent + 2)
        self.instruction.printTree(indent + 1)

    @addToClass(AST.IfStatement)
    def printTree(self, indent=0):
        print("|  " * indent, end='')
        print("IF")
        self.condition.printTree(indent + 1)

        print("|  " * indent, end='')
        print("THEN")
        self._if.printTree(indent + 1)

        if self._else:
            print("|  " * indent, end='')
            print("ELSE")
            self._else.printTree(indent + 1)

    @addToClass(AST.PrintF)
    def printTree(self, indent=0):
        print("|  " * indent, end='')
        print('PRINT')

        self.expressions.printTree(indent + 1)
