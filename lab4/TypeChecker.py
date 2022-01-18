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
t_Function_names = {'zeros', 'ones', 'eye'}

std_operation_type_table = {
    t_Int: {
        t_Float: t_Float,
        t_Int: t_Int
    },
    t_Float: {
        t_Float: t_Float,
        t_Int: t_Float
    }
}

type_table = {
    op: std_operation_type_table for op in t_Binary_ops
}


def semantic_error(line, message):
    print(f"There is an error: {message} at line no. {line}")


def printTheError(line, error_mess):
    semantic_error(line, error_mess)


class NodeVisitor(object):

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):  # Called if no explicit visitor function exists for a node.
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
        self.visit(node.instructions)

    def visit_Instructions(self, node):
        for instr in node.instructions:
            self.visit(instr)

    def visit_IntNum(self, node):
        return t_Int

    def visit_FloatNum(self, node):
        return t_Float

    def visit_String(self, node):
        return t_Str

    def visit_Variable(self, node):
        t_of_variable = self.symbol_table.get(node.name)
        if t_of_variable is not None:
            return t_of_variable.type
        else:
            semantic_error(node.lineo, f'Niezidentyfikowana zmienna {node.name}')
            return t_None

    def visit_Matrix(self, node):
        dim_0 = len(node.rows)
        dim_1 = None
        for sublist in node.rows:
            len_o_sublist = self.visit(sublist)[1]
            if dim_1 is None:
                dim_1 = len_o_sublist
            elif dim_1 != len_o_sublist:
                semantic_error(node.lineno, " Unmatching lengths of submatrix")
                return t_Matrix, (dim_0, None)
        return t_Matrix, (dim_0, dim_1)

    def visit_Row(self, node):
        return t_Vector, len(node.values)

    def visit_Function(self, node):
        arg_types = self.visit(node.args)
        if arg_types[1] > 2:
            semantic_error(node.lineno, f"Wrong number of arguments, expected 1 or 2, got {arg_types[1]}")

        for i, value in enumerate(node.args.values):
            # t = self.visit(value)
            # if t != "Int":
            #     semantic_error(node.lineno, f"Argument #{i} must be Integer, not {t}")
            pass

        # TODO: ???

        if arg_types[1] == 1:
            return t_Matrix, (node.args.values[0], node.args.values[0])
        else:
            return t_Matrix, (node.args.values[0], node.args.values[1])



    def visit_Assignment(self, node):
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



    def visit_Slice(self, node):
        symbol = self.symbol_table.get(node.name)
        indices = self.visit(node.vector)
        if not symbol:
            semantic_error(node.lineno, f"Reference to undefined variable: {node.name}")
            return  # handle NullPointerException

        # matrix
        if not isinstance(symbol.type, Tuple):
            semantic_error(node.lineno, f"{symbol.type} is not subscriptable")
            return

        symbol_type = symbol.type[0]
        dims = symbol.type[1]

        if symbol_type == t_Matrix:
            if len(node.vector.values) != 2 and isinstance(dims, Tuple) and len(dims) == 2:
                semantic_error(node.lineno,
                               f"Provided {len(node.vector.values)} {'index' if len(indices) == 1 else 'indices'}, 2 required")
            else:
                for i in range(2):
                    v = node.vector.values[i].value
                    d = dims[i].value
                    if v and d and (v < 0 or v >= d):
                        semantic_error(node.lineno,
                                       f"Index {v} is out of range for matrix {symbol.name} with shape {dims} at axis {i}")

        # vector
        elif symbol_type == t_Vector:
            if len(indices) != 1:
                semantic_error(node.lineno, f"Provided {len(indices)} indices for vector {symbol.name}, 1 required")
            elif indices[0] and dims and (indices[0] < 0 or indices[0] >= dims):
                semantic_error(node.lineno, f"Index {indices[0]} is out of range for vector with length {dims}")

        else:
            semantic_error(node.lineno, f"{symbol.type} is not subscritable")

        return symbol_type, dims

    def visit_BinExpr(self, node):
        type1 = self.visit(node.left)
        type2 = self.visit(node.right)
        op = node.op

        if isinstance(type1, Tuple):
            type1, dims1 = type1

        if isinstance(type2, Tuple):
            type2, dims2 = type2


        if type1 is not None and type2 is not None:
            if op in t_Binary_ops:
                if type1 == t_Matrix or type2 == t_Matrix:
                    if type1 != type2:
                        semantic_error(node.lineno, f'{type1} {type2} not compatible with {op}')
                    elif op in {'+', '-'}:
                        if dims1 != dims2:
                            semantic_error(node.lineno,
                                           f'Cannot use {op} with matrices of different shapes ({dims1} and {dims2})')
                        else:
                            return t_Matrix, dims1
                    elif op == '*':
                        if dims1[1] != dims2[0]:
                            semantic_error(node.lineno,
                                           f'Cannot use {op} with matrices of incompatible shapes ({dims1} and {dims2})')
                        else:
                            return t_Matrix, (dims1[0], dims2[1])
                    elif op == '/':
                        semantic_error(node.lineno, 'Dzielenie macierzy jest niewspierane')

                elif type1 == t_Vector or type2 == t_Vector:
                    if type1 != type2:
                        semantic_error(node.lineno, f'Types {type1} and {type2} not compatible with {op}')
                    elif dims1 != dims2:
                        semantic_error(node.lineno, f'Cannot use {op} with vectors of different lengths ({dims1} and {dims2})')
                    else:
                        return t_Vector, dims1

                elif type1 not in t_Numerical or type2 not in t_Numerical:
                    semantic_error(node.lineno, f'Types {type1} and {type2} not compatible with {op}')
                else:
                    return type_table[op][type1][type2]

            elif op in t_Matrix_ops:
                if type1 != t_Matrix or type2 != t_Matrix:
                    semantic_error(node.lineno, f'{type1} {type2} not compatible with {op}')
                elif dims1 != dims2:
                    semantic_error(node.lineno, f'Cannot use {op} with matrices of different shapes ({dims1} and {dims2})')
            else:
                semantic_error("BinExpr: Unhandled arithmetic operation?!")
        else:
            if type1 is None:
                semantic_error(node.lineno, f"BinExpr: invalid left operand type: {type1}")
            if type2 is None:
                semantic_error(node.lineno, f"BinExpr: invalid right operand type: {type2}")
