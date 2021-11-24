#!/usr/bin/python

import Lab1.scanner as scanner
import ply.yacc as yacc

tokens = scanner.tokens + list(scanner.literals)

precedence = (
    # to fill ...
    ("left", '+', '-'),
    ("left", 'TRANSPOSE'),
    ("right", 'UMINUS')
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
                   | uminus_matrix
                   | variable_assignment
                   | uminus_variable
                   | row_col_assignment
                   | uminus_row_col
                   | id_assignment
                   | uminus_id
                   | special_assign"""

def p_uminus_matrix(p):
    """ uminus_matrix : ID '=' '-' transposing %prec UMINUS """

def p_matrix_assignment(p):
    """ matrix_assignment : ID '=' transposing"""

def p_transposing(p):
    """transposing : transpose
                   | m_ass_option"""

def p_transpose(p):
    """transpose : m_ass_option "'" %prec TRANSPOSE """

def p_m_ass_option(p):
    """ m_ass_option : function
                     | '[' row_list ']'  """
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
                 | num_list ',' number """

def p_number(p):
    """ number : INTNUM
               | FLOAT"""

def p_variable_assignment(p):
    """ variable_assignment : ID '=' number"""

def p_uminus_variable(p):
    """ uminus_variable : ID '=' '-' number %prec UMINUS """

def p_row_col_assignment(p):
    """ row_col_assignment : matrix_id '=' number """

def p_uminus_row_col(p):
    """ uminus_row_col : matrix_id '=' '-' number %prec UMINUS """

def p_matrix_id(p):
    """matrix_id : ID '[' INTNUM ',' INTNUM ']' """

def p_id_assignment(p):
    """ id_assignment : ID '=' id_expression """

def p_uminus_id(p):
    """ uminus_id : ID '=' '-' id_expression %prec UMINUS"""

def p_id_expression(p):
    """ id_expression : dot_expr
                      | '(' bin_expr ')' """

def p_dot_exp(p):
    """ dot_expr : dot_expr ADDMATRIX dot_mul_expr
                 | dot_expr SUBMATRIX dot_mul_expr
                 | dot_mul_expr"""

def p_dot_mul_expr(p):
    """ dot_mul_expr : dot_mul_expr MULMATRIX bin_expr
                     | dot_mul_expr DIVMATRIX bin_expr
                     | bin_expr"""

def p_bin_expr(p):
    """ bin_expr : bin_expr '+' bin_mul_expr
                 | bin_expr '-' bin_mul_expr
                 | bin_mul_expr"""

def p_bin_mul_expr(p):
    """ bin_mul_expr : bin_mul_expr '*' id_transpose
                     | bin_mul_expr '/' id_transpose
                     | id_transpose"""

def p_id_transpose(p):
    """ id_transpose : ID "'" %prec TRANSPOSE
                     | ID"""

def p_special_assign(p):
    """ special_assign : ID special_operation id_expression"""

def p_special_operation(p):
    """ special_operation : ADDASSIGN
                          | SUBASSIGN
                          | MULASSIGN
                          | DIVASSIGN"""


# to finish the grammar
# ....


parser = yacc.yacc()

