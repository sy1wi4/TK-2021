#!/usr/bin/python

import lab2.scanner as scanner
import ply.yacc as yacc

tokens = scanner.tokens + list(scanner.literals)

precedence = (
    # to fill ...
    ("nonassoc", 'IFX'),
    ("nonassoc", 'ELSE'),
    ("left", '<', '>', 'LEQUAL', 'GREQUAL', 'DIFFERS', 'EQUALS'),
    ("left", 'TRANSPOSE'),
    ("left", '+', '-', 'ADDMATRIX', 'SUBMATRIX'),
    ("left", '*', '/', 'MULMATRIX', 'DIVMATRIX'),
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
    """ assignment : identificator ass_operation ass_option"""


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
                   | special_assign"""


def p_matrix_assignment(p):
    """ matrix_assignment : expression
                          | expr_unary
                          | '[' row_list ']' """


def p_expr_unary(p):
    """ expr_unary : '-' expression %prec UMINUS
                   | expression "'" %prec TRANSPOSE """


def p_expression(p):
    """ expression : expression '+' expression %prec '+'
                    | expression '-' expression %prec '-'
                    | expression '/' expression %prec '/'
                    | expression '*' expression %prec '*'
                    | expression ADDMATRIX expression %prec ADDMATRIX
                    | expression SUBMATRIX expression %prec SUBMATRIX
                    | expression DIVMATRIX expression %prec DIVMATRIX
                    | expression MULMATRIX expression %prec MULMATRIX
                    | '(' expression ')'
                    | ID
                    | number """


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


def p_sys_function(p):
    """ sys_function : PRINT print_block
                     | BREAK
                     | RETURN expression
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
    """ comparison : expression comp_device expression"""


def p_comp_device(p):
    """comp_device : LEQUAL
                   | GREQUAL
                   | DIFFERS
                   | EQUALS
                   | '<'
                   | '>' """


def p_branch(p):
    """ branch : IF '(' comparison ')' instruction %prec IFX
               | IF '(' comparison ')' instruction ELSE instruction """


parser = yacc.yacc()
