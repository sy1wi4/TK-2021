#!/usr/bin/python
from collections import defaultdict
from enum import Enum


class Levels(Enum):
    BASE = 0,
    IF = 1,
    ELSE = 2,
    FOR = 3,
    WHILE = 4


class Symbol(object):
    pass


class VariableSymbol(Symbol):

    def __init__(self, name, _type):
        self.name = name
        self.type = _type


class SymbolTable(object):

    def __init__(self, parent=None, name=Levels.BASE):  # parent scope and symbol table name
        self.symbols = defaultdict()
        self.levels_stack = [name]

    def put(self, name, symbol):  # put variable symbol or fundef under <name> entry
        self.symbols[name] = symbol

    def get(self, name):  # get variable symbol or fundef from <name> entry
        return self.symbols[name]

    def getParentScope(self):
        return self.levels_stack[-1]

    def pushScope(self, name):
        self.levels_stack.append(name)

    def popScope(self):
        if len(self.levels_stack) == 1:
            raise IOError("Don't pop BASE level")
        self.levels_stack.pop()

