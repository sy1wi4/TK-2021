class Node(object):
    count = 0

    def __init__(self, children=None):
        self.ID = str(Node.count)
        Node.count += 1

        if not children:
            self.children = []

        elif hasattr(children, '__len__ '):
            self.children = children
            print(children, self.children)
        else:
            self.children = [children]
            self.next = []


class Program(Node):
    def __init__(self, instructions=None):
        self.instructions = instructions


class Instructions(Node):
    def __init__(self, instruction):
        if hasattr(instruction, '__len__'):
            self.instructions = instruction
        else:
            self.instructions = [instruction]


class IntNum(Node):
    def __init__(self, value):
        self.value = value


class FloatNum(Node):
    def __init__(self, value):
        self.value = value


class Assignment(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right


class Variable(Node):
    def __init__(self, name):
        self.name = name


class Slice(Node):
    def __init__(self, name, vector):
        self.name = name
        self.vector = vector


class Row(Node):
    def __init__(self, value=None):
        if value is None:
            self.values = []
        else:
            self.values = [value]


class Function(Node):
    def __init__(self, function, arg):
        self.function = function
        self.arg = arg


class BinExpr(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

        self.children = [left, right]


class UnaryExpr(Node):
    def __init__(self, op, operand):
        self.op = op
        self.operand = operand


class WhileLoop(Node):
    def __init__(self, condition, instruction):
        self.condition = condition
        self.instruction = instruction


class ForLoop(Node):
    def __init__(self, variable, left_range, right_range, instruction):
        self.variable = variable
        self.left_range = left_range
        self.right_range = right_range
        self.instruction = instruction


class IfStatement(Node):
    def __init__(self, condition, _if, _else=None):
        self.condition = condition
        self._if = _if
        self._else = _else


class PrintF(Node):
    def __init__(self, expressions):
        self.expressions = expressions
