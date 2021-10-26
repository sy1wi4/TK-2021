import sys

import ply.lex as lex


tokens = ('ADDASSIGN', 'SUBASSIGN','MULASSIGN', 'DIVADDIGN',
          'LEQUAL', 'REQUAL', 'DIFFERS', 'EQUALS', #, 'FLOAT', 'INTNUM',
          'ADDMATRIX', 'SUBMATRIX', 'MULMATRIX', 'DIVMATRIX',
          'NUMBER', 'ID',  'COMMENT')

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

literals = ['+', '-', '*', '/', '(', ')', '{','}','[',']','=', '<', '>', ':', "'",',',';','.']

reserved = {'if' : 'if',
            'else' : 'else',
            'for' : 'for',
            'while' : 'while'}


def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_ID(t):
    r'[a-zA-Z_]\w*'
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
