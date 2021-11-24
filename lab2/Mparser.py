#!/usr/bin/python

import scanner
import ply.yacc as yacc

tokens = scanner.tokens + list(scanner.literals)

precedence = (


    ("left", '+', '-'),
    ("left", '*', '/'),
    ('right', 'UMINUS'),

    # to fill ...
)

def p_program(p):
    """program : instructions_opt"""
    p[0] = p[1]


def p_instructions_opt_1(p):
    """instructions_opt : instructions """
    p[0] = p[1]


def p_instructions_1(p):
    """instructions : instructions instruction ';' """
    p[0] = p[1]

def p_instructions_2(p):
    """instructions : instruction ';' """
    p[0] = p[1]

def p_instruction(p):
    """instruction : init
                   | matrix_binop"""
    p[0] = p[1]

def p_init(p):
    """init : id '=' expression_opt """
    p[0] = p[2]

def p_expression_opt_1(p):
    """expression_opt : expression """
    p[0] = p[1]


def p_expression_opt_2(p):
    '''expression_opt : '-' expression %prec UMINUS '''
    p[0] = -1* p[2]


def p_id(p):
    """id : id_opt"""
    p[0] = p[1]

def p_id_opt_1(p):
    """id_opt : ID """
    p[0] = p[1]

def p_id_opt_2(p):
    """id_opt : matrix_spec"""
    p[0] = p[1]


def p_matrix_spec(p):
    """matrix_spec : ID '[' number ',' number ']'  """


def p_number(p):
    """number : number_opt"""
    p[0] = p[1]


def p_number_opt_1(p):
    """number_opt : INTNUM"""
    p[0] = p[1]


def p_number_opt_2(p):
    """number_opt : FLOAT"""
    p[0] = p[1]

def p_expression(p):
    """expression : function
                 | matrix_init
                 | number
                 | matrix_binop
                 | id"""
    p[0] = p[1]

def p_matrix_binop(p):
    """matrix_binop : ID '+' ID
                    | ID '-' ID
                    | ID '*' ID
                    | ID '/' ID"""
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]


def p_function(p):
    """function : function_opt '(' INTNUM ')' """


def p_function_opt_1(p):
    """function_opt : EYE"""
    p[0] = p[1]

def p_function_opt_2(p):
    """function_opt : ZEROS"""
    p[0] = p[1]

def p_function_opt_3(p):
    """function_opt : ONES"""
    p[0] = p[1]

def p_matrix_init(p):
    """matrix_init : '[' row_list ']' """
    p[0] = [p[2]]

def p_row_list(p):
    """row_list : row_opt  """
    p[0] = p[1]

def p_row_opt_1(p):
    """row_opt : row"""
    p[0] = p[1]

def p_row_opt_2(p):
    """row_opt : row_list ',' row"""
    p[0] = p[1], p[3]

def p_row(p):
    """row : '[' value_list ']' """
    p[0] = [p[2]]

def p_value_list(p):
    """value_list : value_list_opt """
    p[0] = p[1]


def p_value_list_opt_1(p):
    """value_list_opt : number"""
    p[0] = p[1]

def p_value_list_opt_2(p):
    """value_list_opt : number ',' value_list"""
    p[0] = p[1] , p[3]

def p_error(p):
    if p:
        print("Syntax error at line {0}: LexToken({1}, '{2}')".format(p.lineno, p.type, p.value))
    else:
        print("Unexpected end of input")


parser = yacc.yacc()
