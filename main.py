import sys

import ply.lex as lex


reserved = {'if' : 'IF',
            'else' : 'ELSE',
            'for' : 'FOR',
            'while' : 'WHILE',
            'break' : 'BREAK',
            'continue' : 'CONTINUE',
            'return' : 'RETURN',
            'eye' : 'EYE',
            'zeros' : 'ZEROS',
            'ones' : 'ONES',
            'print' : 'PRINT'}

tokens = ['ADDASSIGN', 'SUBASSIGN','MULASSIGN', 'DIVADDIGN',
          'LEQUAL', 'REQUAL', 'DIFFERS', 'EQUALS', 'FLOAT',# 'INTNUM',
          'ADDMATRIX', 'SUBMATRIX', 'MULMATRIX', 'DIVMATRIX',
          'INTNUM', 'ID',  'COMMENT'] + list(reserved.values())

t_ignore = '  \t'
t_EQUALS = r'\=='
t_ADDASSIGN = r'\+='
t_SUBASSIGN = r'\-='
t_MULASSIGN = r'\*='
t_DIVADDIGN = r'\\='
t_LEQUAL = r'\<='
t_REQUAL = r'\>='
t_DIFFERS = r'\!='
t_ADDMATRIX = r'\.\+'
t_SUBMATRIX = r'\.-'

t_MULMATRIX = r'\.\*'
t_DIVMATRIX = r'\.\/'

literals = ['+', '-', '*', '/', '(', ')', '{','}','[',']','=', '<', '>', ':', "'",',',';','.', '"']



def t_FLOAT(t):
    r"(-?\d*\.\d+([eE][-+]?\d+)?) | (-?\d+[eE][-+]?\d+)"
    t.value = float(t.value)
    return t



def t_INTNUM(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_ID(t):
    r'[a-zA-Z_]\w*'
    t.type = reserved.get(t.value, 'ID')
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_COMMENT(t):
    r'\#.*'
    pass


def t_error(t) :
    print("Illegal character '%s'" %t.value[0])
    t.lexer.skip(1)

if __name__ == '__main__':
    lexer = lex.lex()
    #fh = open(sys.argv[1], "r")
    fh = open("example.txt", "r")
    lexer.input(fh.read())
    for token in lexer:
        print("(%d): %s (%s)" % (token.lineno, token.type, token.value))
