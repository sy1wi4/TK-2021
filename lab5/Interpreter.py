
import AST
from Memory import *
from Exceptions import *
from visit import *
import sys
import numpy as np

sys.setrecursionlimit(10000)

binop_func = {
    '+': lambda x, y: x+y,
    '.+': lambda x, y: x+y,
    '-': lambda x, y: x-y,
    '.-': lambda x, y: x-y,
    '*': lambda x, y: x*y if isinstance(y, int) else x@y,
    '.*': lambda x, y: x*y,
    '/': lambda x, y: x/y,
    './': lambda x, y: x/y,
    '>': lambda x, y: x > y,
    '<': lambda x, y: x < y,
    '>=': lambda x, y: x >= y,
    '<=': lambda x, y: x <= y,
    '==': lambda x, y: x == y,
    '!=': lambda x, y: x != y,
}

unary_func = {
    '-': lambda x: -x,
    'TRANSPOSE': lambda x: x.T
}

matrix_func = {
    'zeros': lambda x: np.zeros(x),
    'ones': lambda x: np.ones(x),
    'eye': lambda x: np.eye(*x)
}

memory_stack = MemoryStack(Memory('global'))


class Interpreter(object):

    @on('node')
    def visit(self, node):
        pass

    @when(AST.Program)
    def visit(self, node):
        if node.instructions:
            node.instructions.accept(self)

    @when(AST.Instructions)
    def visit(self, node):
        for instruction in node.instructions:
            instruction.accept(self)

    @when(AST.IntNum)
    def visit(self, node):
        return node.value

    @when(AST.FloatNum)
    def visit(self, node):
        return node.value

    @when(AST.String)
    def visit(self, node):
        return node.value

    @when(AST.Variable)
    def visit(self, node):
        return memory_stack.get(node.name)

    @when(AST.Matrix)
    def visit(self, node):
        return np.array([row.accept(self) for row in node.rows])

    @when(AST.Row)
    def visit(self, node):
        return np.array([value.accept(self) for value in node.values])

    @when(AST.Function)
    def visit(self, node):
        args = node.args.accept(self)
        if len(args) == 1:
            args *= 2

        return matrix_func[node.function](tuple(args))

    @when(AST.Assignment)
    def visit(self, node):
        value = node.right.accept(self)

        if node.op == '=':
            if isinstance(node.left, AST.Slice):
                node.left.assignable = True
                slice_ = node.left.accept(self)
                slice_[:] = value
                node.left.assignable = False
            else:
                memory_stack.set(node.left.name, value)
        else:
            if isinstance(node.left, AST.Slice):
                node.left.assignable = True
                slice_ = node.left.accept(self)
                slice_[:] = binop_func[node.op[0]](slice_, value)
                node.left.assignable = False
            else:
                old_value = memory_stack.get(node.left.name)
                new_value = binop_func[node.op[0]](old_value, value)
                memory_stack.set(node.left.name, new_value)

    @when(AST.Slice)
    def visit(self, node):
        indices = node.vector.accept(self)
        matrix = memory_stack.get(node.name)

        if len(indices) == 1:
            if isinstance(indices[0], tuple) and isinstance(indices[0][0], int) and isinstance(indices[0][1], int):
                return matrix[int(indices[0][0]):int(indices[0][1])]
                # xd
            elif node.assignable and isinstance(indices[0], int):
                return matrix[int(indices[0]):int(indices[0]+1)]
            elif isinstance(indices[0], int):
                return matrix[int(indices[0])]
            else:
                raise RuntimeError(f"{node.lineno}: Invalid indices type!")
        else:
            if isinstance(indices[0], tuple) and isinstance(indices[0][0], int) and isinstance(indices[0][1], int) and isinstance(indices[1][0], int) and isinstance(indices[1][1], int):
                return matrix[int(indices[0][0]):int(indices[0][1]), int(indices[1][0]):int(indices[1][1])]
            elif node.assignable and isinstance(indices[0], int) and isinstance(indices[1], int):
                return matrix[int(indices[0]):int(indices[0]+1), int(indices[1]):int(indices[1]+1)]
            elif isinstance(indices[0], int) and isinstance(indices[1], int):
                return matrix[int(indices[0]), int(indices[1])]
            else:
                raise RuntimeError(f"{node.lineno}: Invalid indices type!")


    @when(AST.BinExpr)
    def visit(self, node):
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)

        return binop_func[node.op](r1, r2)

    @when(AST.UnaryExpr)
    def visit(self, node):
        operand = node.operand.accept(self)
        return unary_func[node.op](operand)

    @when(AST.WhileLoop)
    def visit(self, node):
        memory_stack.push(Memory("while"))

        while node.condition.accept(self):
            try:
                node.instruction.accept(self)
            except BreakException:
                break
            except ContinueException:
                continue

        memory_stack.pop()

    @when(AST.ForLoop)
    def visit(self, node):
        memory_stack.push(Memory("for"))

        left_range = node.left_range.accept(self)
        right_range = node.right_range.accept(self)
        memory_stack.set(node.variable.name, left_range)

        i = left_range
        while i <= right_range:
            try:
                node.instruction.accept(self)
            except BreakException:
                break
            except ContinueException:
                pass

            i = node.variable.accept(self) + 1
            memory_stack.set(node.variable.name, i)

        memory_stack.pop()

    @when(AST.IfStatement)
    def visit(self, node):
        memory_stack.push(Memory("if"))
        if node.condition.accept(self):
            node._if.accept(self)
        elif node._else is not None:
            node._else.accept(self)
        memory_stack.pop()

    @when(AST.PrintF)
    def visit(self, node):
        expression_evals = node.expressions.accept(self)
        print(*expression_evals)

    @when(AST.ReturnStatement)
    def visit(self, node):
        print(node.expression.accept(self))
        sys.exit()

    @when(AST.ContBreakStatement)
    def visit(self, node):
        if node.statement == 'break':
            raise BreakException
        elif node.statement == 'continue':
            raise ContinueException

    @when(AST.Expressions)
    def visit(self, node):
        evals = []
        for expression in node.expressions:
            evals.append(expression.accept(self))
        return evals
