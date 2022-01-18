class Node(object):
    count = 0

    def __init__(self, children=None):
        self.ID = str(Node.count)
        Node.count += 1
        self.lineno = None

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
        super().__init__()
        self.instructions = instructions


class Instructions(Node):
    def __init__(self, instruction):
        super().__init__()
        if hasattr(instruction, '__len__'):
            self.instructions = instruction
        else:
            self.instructions = [instruction]


class IntNum(Node):
    def __init__(self, value):
        super().__init__()
        self.value = value


class FloatNum(Node):
    def __init__(self, value):
        super().__init__()
        self.value = value


class String(Node):
    def __init__(self, value):
        super().__init__()
        self.value = value


class Assignment(Node):
    def __init__(self, op, left, right):
        super().__init__()
        self.op = op
        self.left = left
        self.right = right


class Variable(Node):
    def __init__(self, name):
        super().__init__()
        self.name = name


class Slice(Node):
    def __init__(self, name, vector):
        super().__init__()
        self.name = name
        self.vector = vector


class Matrix(Node):
    def __init__(self, rows):
        super().__init__()
        self.rows = [rows]


class Row_list(Node):
    def __init__(self, row):
        super().__init__()
        if row is None:
            self.rows = []
        else:
            self.rows = [row]


class Row(Node):
    def __init__(self, value=None):
        super().__init__()
        if value is None:
            self.values = []
        else:
            self.values = [value]


class Function(Node):
    def __init__(self, function, arg):
        super().__init__()
        self.function = function
        self.arg = arg


class BinExpr(Node):
    def __init__(self, op, left, right):
        super().__init__()
        self.op = op
        self.left = left
        self.right = right

        self.children = [left, right]


class UnaryExpr(Node):
    def __init__(self, op, operand):
        super().__init__()
        self.op = op
        self.operand = operand


class WhileLoop(Node):
    def __init__(self, condition, instruction):
        super().__init__()
        self.condition = condition
        self.instruction = instruction


class ForLoop(Node):
    def __init__(self, variable, left_range, right_range, instruction):
        super().__init__()
        self.variable = variable
        self.left_range = left_range
        self.right_range = right_range
        self.instruction = instruction


class IfStatement(Node):
    def __init__(self, condition, _if, _else=None):
        super().__init__()
        self.condition = condition
        self._if = _if
        self._else = _else


class PrintF(Node):
    def __init__(self, expressions):
        super().__init__()
        self.expressions = expressions
