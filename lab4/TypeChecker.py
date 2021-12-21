#!/usr/bin/python
from lab4 import AST


def semantic_error(line, message):
    print(f"There is an error: { message } at line no. {line}" )


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

    def visit_row_list(self, node):
        print(" I am going ")
        dim_0 = len(node.rows)
        dim_1 = None
        for sublist in node.rows:
            len_o_sublist = self.visit(sublist)[1]
            if dim_1 is None:
                dim_1 = len_o_sublist
            elif dim_1 != len_o_sublist:
                semantic_error(node.lineno, " Unmatching lengths of submatrix")
        return "Typ_Macierzowy", (dim_0, dim_1)

    def visit_Variable(self, node):
        pass


    def visit_Assignment(self, node):
        operator = node.op
        self.visit(node.right)



    def visit_Row(self, node):
        print(node.__class__.__name__)
        type = node.values.__class__.__name__






