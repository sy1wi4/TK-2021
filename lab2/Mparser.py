#!/usr/bin/python

import Lab1.scanner as scanner
import ply.yacc as yacc

tokens = scanner.tokens + list(scanner.literals)

precedence = (
    # to fill ...
    ("nonassoc", 'IFX'),
    ("nonassoc", 'ELSE'),
    ("left", '<', '>', 'LEQUAL', 'GREQUAL', 'DIFFERS', 'EQUALS'),
    ("left", '+', '-', 'ADDMATRIX', 'SUBMATRIX'),
    ("left", '*', '/', 'MULMATRIX', 'DIVMATRIX'),
    ("left", 'TRANSPOSE'),
    ("left", 'UMINUS'),
    # to fill ...
)


def p_error(p):
    if p:
        print("Syntax error at line {0}: LexToken({1}, '{2}')".format(p.lineno, p.type, p.value))
    else:
        print("Unexpected end of input")


def p_program(p):
    """ program : instructions_opt"""
    p[0] = p[1]


def p_instructions_opt_1(p):
    """ instructions_opt : instructions """
    p[0] = p[1]

def p_instructions_opt_2(p):
    """ instructions_opt : """
    p[0] = p[1]

def p_instructions_1(p):
    """ instructions : instructions instruction """
    p[0] = p[1], p[2]

def p_instructions_2(p):
    """ instructions : instruction """


def p_instruction(p):
    """ instruction : assignment ';'
                    | branch
                    | loop
                    | block_of_code
                    | sys_function ';' """


def p_block_of_code(p):
    """ block_of_code : '{' instructions '}' """


def p_assignment(p):
    """ assignment : identificator ass_operation ass_option
                   | identificator ass_operation '-' ass_option %prec UMINUS"""

def p_ass_operation(p):
    """ ass_operation : '='
                      | ADDASSIGN
                      | SUBASSIGN
                      | MULASSIGN
                      | DIVASSIGN  """


def p_identificator(p):
    """ identificator : matrix_id
                      | ID"""


def p_matrix_id(p):
    """ matrix_id : ID '[' INTNUM ',' INTNUM ']'"""


def p_ass_option(p):
    """ ass_option : matrix_assignment
                   | var_expression
                   | special_assign"""

# rozpisz sobie przypisywanie i zobaczymy jak to wygląda
def p_matrix_assignment(p):
    """ matrix_assignment : matrix_expression
                          | '[' row_list ']' """

def p_matrix_expression(p):
    """ matrix_expression : matrix_expression binop matrix_expression
                          | matrix_expression matrix_binop matrix_expression
                          | matrix_expression
                          | matrix_expression "'" %prec TRANSPOSE
                          | '(' matrix_expression ')'
                          | var_expression
                          | ID """

def p_binop(p):
    """ binop : '+'
              | '-'
              | '*'
              | '/' """


def p_matrix_binop(p):
    """ matrix_binop : ADDMATRIX
                     | SUBMATRIX
                     | MULMATRIX
                     | DIVMATRIX """


def p_special_assign(p):
    """ special_assign : fun_name '(' INTNUM ')'"""


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


def p_var_expression(p):
    """ var_expression : var_expression binop var_expression
                       | '(' var_expression ')'
                       | number
                       | ID """

def p_sys_function(p):
    """ sys_function : PRINT print_block
                     | BREAK
                     | RETURN var_expression
                     | CONTINUE """


def p_print_block(p):
    """ print_block : print_block ',' ID
                    | print_block ',' STRING
                    | STRING
                    | ID """


def p_loop(p):
    """ loop : for_loop
             | while_loop"""

def p_while_loop(p):
    """ while_loop : WHILE '(' comparison ')' instruction"""


def p_for_loop(p):
    """ for_loop : FOR for_specifier instruction """


def p_for_specifier(p):
    """ for_specifier : ID '=' INTNUM ':' INTNUM
                      | ID '=' INTNUM ':' ID
                      | ID '=' ID ':' ID """


def p_comparison(p):
    """ comparison : var_expression comp_device var_expression"""

def p_comp_device(p):
    """comp_device : LEQUAL
                   | GREQUAL
                   | DIFFERS
                   | EQUALS
                   | '<'
                   | '>' """

def p_branch(p):
    """ branch : IF '(' comparison ')' instruction %prec IFX
               | IF '(' comparison ')' instruction ELSE branch
               | IF '(' comparison ')' instruction ELSE instruction"""



parser = yacc.yacc()
