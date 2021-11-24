#!/usr/bin/python

import scanner as scanner
import ply.yacc as yacc

tokens = scanner.tokens + list(scanner.literals)

precedence = (
    # to fill ...
    ("left", '+', '-'),
    # to fill ...
)


def p_error(p):
    if p:
        print("Syntax error at line {0}: LexToken({1}, '{2}')".format(p.lineno, p.type, p.value))
    else:
        print("Unexpected end of input")


def p_program(p):
    """program : instructions_opt"""


def p_instructions_opt_1(p):
    """instructions_opt : instructions """


def p_instructions_opt_2(p):
    """instructions_opt : """


def p_instructions_1(p):
    """instructions : instructions instruction """


def p_instructions_2(p):
    """instructions : instruction """

def p_instruction(p):
    """ instruction : assignment ';' """

def p_assignment(p):
    """ assignment : matrix_assignment
                   | variable_assignment
                   | row_col_assignment"""

def p_matrix_assignment(p):
    """ matrix_assignment : ID '=' m_ass_option"""

def p_m_ass_option(p):
    """ m_ass_option : function
                     | '[' row_list ']' """
def p_function(p):
    """ function : fun_name '(' INTNUM ')' """

def p_fun_name(p):
    """ fun_name : EYE
                 | ZEROS
                 | ONES"""

def p_row_list(p):
    """ row_list : row
                 | row_list ',' row"""

def p_row(p):
    """row : '[' num_list ']' """

def p_num_list(p):
    """ num_list : number
                 | number ',' num_list """

def p_number(p):
    """ number : INTNUM
               | FLOAT"""

def p_variable_assignment(p):
    """ variable_assignment : ID '=' number"""

def p_row_col_assignment(p):
    """ row_col_assignment : matrix_id '=' number """

def p_matrix_id(p):
    """matrix_id : ID '[' INTNUM ',' INTNUM ']' """


# to finish the grammar
# ....


parser = yacc.yacc()

