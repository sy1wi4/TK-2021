class Node(object):
    pass


class IntNum(Node):
    def __init__(self, value):
        self.value = value


class FloatNum(Node):
    def __init__(self, value):
        self.value = value


class Variable(Node):
    def __init__(self, name):
        self.name = name


class BinExpr(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right


class Program(Node):
    def __init__(self, instructions=None):
        self.instructions = instructions


class Instructions(Node):
    def __init__(self, instruction):
        if hasattr(instruction, '__len__'):
            self.instructions = instruction
        else:
            self.instructions = [instruction]


class Error(Node):
    def __init__(self):
        pass
