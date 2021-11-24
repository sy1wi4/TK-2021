#!/usr/bin/python

import Lab1.scanner as scanner
import ply.yacc as yacc

tokens = scanner.tokens + list(scanner.literals)

precedence = (
    # to fill ...
    ("left", '+', '-'),
    ("left", '*', '/'),
    ("left", 'TRANSPOSE'),
    ("right", 'UMINUS'),
    ("nonassoc", 'IFX'),
    ("nonassoc", 'ELSE'),
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
    """ instruction : assignment ';'
                    | branch
                    | loop
                    | block_of_code"""

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
    """ variable_assignment : ID '=' math_expression"""

def p_uminus_variable(p):
    """ uminus_variable : ID '=' '-' math_expression %prec UMINUS """

def p_row_col_assignment(p):
    """ row_col_assignment : matrix_id '=' math_expression """

def p_uminus_row_col(p):
    """ uminus_row_col : matrix_id '=' '-' math_expression %prec UMINUS """

def p_matrix_id(p):
    """matrix_id : ID '[' INTNUM ',' INTNUM ']' """

def p_id_assignment(p):
    """ id_assignment : ID '=' id_expression"""

def p_uminus_id(p):
    """ uminus_id : ID '=' '-' id_expression %prec UMINUS"""

def p_id_expression(p):
    """ id_expression : dot_expr""" #

def p_dot_exp(p):
    """ dot_expr : dot_expr ADDMATRIX dot_mul_expr
                 | dot_expr SUBMATRIX dot_mul_expr
                 | dot_mul_expr
                 | '(' bin_expr ')' """

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
                     | number
                     | id_transpose"""

def p_id_transpose(p):
    """ id_transpose : ID "'" %prec TRANSPOSE
                     | ID """

def p_special_assign(p):
    """ special_assign : ID special_operation id_expression"""

def p_special_operation(p):
    """ special_operation : ADDASSIGN
                          | SUBASSIGN
                          | MULASSIGN
                          | DIVASSIGN"""

def p_math_expression(p):
    """math_expression : math_expression '+' mul_math_expr
                       | math_expression '-' mul_math_expr
                       | mul_math_expr"""

def p_mul_math_expr(p):
    """ mul_math_expr : mul_math_expr '*' number
                     | mul_math_expr '/' number
                     | '(' math_expression ')'
                     | number
                     | ID"""


def p_block_of_code(p):
    """block_of_code : '{' block_operations '}' """

def p_block_operations(p):
    """block_operations : block_operation
                        | block_operations block_operation"""


def p_block_operation(p):
    """ block_operation : assignment ';'
                        | branch
                        | io_function ';' """

def p_io_function(p):
    """ io_function : PRINT print_block
                    | BREAK
                    | RETURN math_expression
                    | CONTINUE """

def p_print_block(p):
    """print_block : STRING
                   | id_chain"""

def p_id_chain(p):
    """ id_chain : ID
                 | id_chain ',' ID"""

def p_branch(p):
    """ branch : IF '(' comparison ')' if_block %prec IFX
               | IF '(' comparison ')' if_block ELSE branch
               | IF '(' comparison ')' if_block ELSE if_block"""

def p_if_block(p):
    """ if_block : block_of_code
                 | assignment ';'
                 | io_function ';'  """

def p_comparison(p):
    """ comparison : ID comp_device math_expression"""

def p_comp_device(p):
    """comp_device : LEQUAL
                   | GREQUAL
                   | DIFFERS
                   | EQUALS
                   | '<'
                   | '>' """

def p_loop(p):
    """ loop : for_loop
             | while_loop"""

def p_while_loop(p):
    """ while_loop : WHILE '(' comparison ')' while_code"""

def p_while_code(p):
    """ while_code : block_of_code
                   | loop
                   | branch
                   | assignment ';'
                   | io_function ';' """

def p_for_loop(p):
    """ for_loop : FOR for_specifier for_block"""


def p_for_specifier(p):
    """ for_specifier : ID '=' INTNUM ':' INTNUM
                      | ID '=' INTNUM ':' ID
                      | ID '=' ID ':' ID """

def p_for_block(p):
    """ for_block : block_of_code
                   | loop
                   | branch
                   | assignment ';'
                   | io_function ';' """

# to finish the grammar
# ....


parser = yacc.yacc()

