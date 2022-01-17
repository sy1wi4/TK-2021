#!/usr/bin/python
from lab4 import AST
from lab4 import SymbolTable
from typing import Union, Tuple

t_Int = 'Int'
t_Float = 'Float'
t_Str = "Str"
t_var = t_Str
t_Matrix = "Matrix"
t_Row_list = t_Matrix
t_Vector = "Vector"
t_Num_list = t_Vector
t_Bool = "Boolean"
t_None = "None"
t_Variable = Union[
    t_Int,
    t_Float,
    t_Str,
    t_Matrix,
    t_Vector,
    t_Bool
]
t_VisitReturn = Union[
    t_Variable,
    t_var
]
t_Numerical = {t_Int, t_Float}
t_Assignment_ops = {'/=', '+=', '-=', '*='}
t_Matrix_ops = {'.+', '.-', '.*', './'}
t_Binary_ops = {'+', '-', '*', '/'}


def semantic_error(line, message):
    print(f"There is an error: {message} at line no. {line}")


def printTheError(line, error_mess):
    semantic_error(line, error_mess)


class NodeVisitor(object):

    def visit(self, node):
        print("general_visit " + node.__class__.__name__)
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):  # Called if no explicit visitor function exists for a node.
        print("other general_visit")
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        else:
            for child in node.children:
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, AST.Node):
                            self.visit(item)
                elif isinstance(child, AST.Node):
                    self.visit(child)

    # # simpler version of generic_visit, not so general
    # def generic_visit(self, node):
    #    for child in node.children:
    #        self.visit(child)


class TypeChecker(NodeVisitor):
    def __init__(self):
        self.symbol_table = SymbolTable.SymbolTable()

    # def visit_BinExpr(self, node):
    #     # alternative usage,
    #     # requires definition of accept method in class Node
    #     type1 = self.visit(node.left)  # type1 = node.left.accept(self)
    #     type2 = self.visit(node.right)  # type2 = node.right.accept(self)
    #     op = node.op
    #     # ...
    #     #

    def visit_Program(self, node):
        print("Program_visit")
        self.visit(node.instructions)

    def visit_Instructions(self, node):
        print("Instruction_visit")
        for instr in node.instructions:
            self.visit(instr)

    def visit_IntNum(self, node):
        print("Int_visit")
        return t_Int

    def visit_FloatNum(self, node):
        print("Float_visit")
        return t_Float

    def visit_String(self, node):
        print("String_visit")
        return t_Str

    def visit_Variable(self, node):
        print("Var_visit")
        t_of_variable = self.symbol_table.get(node.name)
        if t_of_variable is not None:
            return t_of_variable.type
        else:
            semantic_error(node.lineo, f'Niezidentyfikowana zmienna {node.name}')
            return t_None

    def visit_Matrix(self, node):
        print("Row_List_visit")
        dim_0 = len(node.rows)
        dim_1 = None
        for sublist in node.rows:
            print("podmacierze")
            len_o_sublist = self.visit(sublist)[1]
            if dim_1 is None:
                dim_1 = len_o_sublist
            elif dim_1 != len_o_sublist:
                semantic_error(node.lineno, " Unmatching lengths of submatrix")
                return t_Matrix, (dim_0, None)
        return t_Matrix, (dim_0, dim_1)

    def visit_Row(self, node):
        return t_Vector, len(node.values)

    def visit_Assignment(self, node):
        print("Assignment_visit_visit")
        operator = node.op
        t_right = self.visit(node.right)
        if operator == '=':
            if isinstance(node.left, AST.Slice):
                t_left = self.visit(node.left)
                if not node.right in t_Numerical:
                    semantic_error(node.lineo, f"Zła wartość dla koordynatu komórki macierzy")
                else:
                    self.symbol_table.put(node.left.name, SymbolTable.VariableSymbol(node.left.name, t_right))
            else:
                self.symbol_table.put(
                    node.left.name, SymbolTable.VariableSymbol(node.left.name, t_right))
        else:
            if operator in t_Assignment_ops:
                t_left = self.visit(node.left)
                if isinstance(node.left, AST.Slice):
                    if t_right not in t_Numerical:
                        semantic_error(node.lineno, f"Nie przypiszemy {t_right} do {t_left[0]} komórki")
                elif t_left != t_right:
                    semantic_error(node.lineno, f"Zły typ dla'{operator}' operatora")


        # self.visit(node.left)

    def visit_BinExpr(self, node):
        type1 = self.visit(node.left)
        type2 = self.visit(node.right)
        op = node.op



        return
