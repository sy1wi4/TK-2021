#!/usr/bin/python

import ply.yacc as yacc

import AST
import scanner

tokens = scanner.tokens + list(scanner.literals)

precedence = (
    ("nonassoc", 'IFX'),
    ("nonassoc", 'ELSE'),
    ("left", '<', '>', 'LEQUAL', 'GREQUAL', 'DIFFERS', 'EQUALS'),
    ("left", '+', '-', 'ADDMATRIX', 'SUBMATRIX'),
    ("left", '*', '/', 'MULMATRIX', 'DIVMATRIX'),
    ("left", 'UMINUS'),
    ("right", 'TRANSPOSE'),
)


def p_error(p):
    if p:
        print("Syntax error at line {0}: LexToken({1}, '{2}')".format(p.lineno, p.type, p.value))
    else:
        print("Unexpected end of input")


def p_program(p):
    """program : instructions_opt"""
    p[0] = p[1]


def p_instructions_opt_1(p):
    """instructions_opt : instructions """
    p[0] = AST.Program(p[1])


def p_instructions_opt_2(p):
    """instructions_opt : """
    p[0] = AST.Program()


def p_instructions_1(p):
    """instructions : instructions instruction """
    p[0] = p[1]
    p[0].instructions += [p[2]]


def p_instructions_2(p):
    """instructions : instruction """
    if isinstance(p[1], AST.Instructions):
        p[0] = p[1]
    else:
        p[0] = AST.Instructions(p[1])


def p_instruction(p):
    """ instruction : assignment ';'
                    | branch
                    | loop
                    | block_of_code
                    | sys_function ';' """
    p[0] = p[1]


def p_block_of_code(p):
    """ block_of_code : '{' instructions '}' """
    p[0] = p[2]


def p_assignment(p):
    """ assignment : identifier '=' ass_option
                   | identifier ADDASSIGN ass_option
                   | identifier SUBASSIGN ass_option
                   | identifier MULASSIGN ass_option
                   | identifier DIVASSIGN ass_option"""

    p[0] = AST.Assignment(p[2], p[1], p[3])
    p[0].lineno = p.lineno(2)
    print(p[:])


def p_identifier(p):
    """ identifier : ID row
                  | ID"""
    if len(p) == 2:
        p[0] = AST.Variable(p[1])
    else:
        p[0] = AST.Slice(p[1], p[2])

    p[0].lineno = p.lineno(1)


def p_ass_option(p):
    """ ass_option : matrix
                   | expression
                   | expr_unary
                   | row
                   | special_assign
                   | identifier
                   """
    p[0] = p[1]


def p_matrix(p):
    """ matrix : '[' row_list ']' """
    p[0] = p[2]
    p[0].lineno = p.lineno(1)


def p_expr_unary(p):
    """ expr_unary : '-' expression %prec UMINUS"""
    p[0] = - p[2]
    p[0].lineno = p.lineno(1)


def p_expression_1(p):
    """ expression : expression '+' expression %prec '+'
                    | expression '-' expression %prec '-'
                    | expression '/' expression %prec '/'
                    | expression '*' expression %prec '*'
                    | expression ADDMATRIX expression %prec ADDMATRIX
                    | expression SUBMATRIX expression %prec SUBMATRIX
                    | expression DIVMATRIX expression %prec DIVMATRIX
                    | expression MULMATRIX expression %prec MULMATRIX
                    | expression "\\'" %prec TRANSPOSE"""

    if p[len(p) - 1] == "\'":
        p[0] = AST.UnaryExpr('TRANSPOSE', p[1])
    else:
        p[0] = AST.BinExpr(p[2], p[1], p[3])
        p[0].lineno = p.lineno(2)


def p_expression_2(p):
    """ expression : ID"""
    p[0] = AST.Variable(p[1])
    p[0].lineno = p.lineno(1)


def p_expression_3(p):
    """ expression : number"""
    p[0] = p[1]


def p_expression_4(p):
    """ expression : '(' expression ')'"""
    p[0] = p[2]


def p_special_assign(p):
    """ special_assign : EYE '(' num_list ')'
                       | ZEROS '(' num_list ')'
                       | ONES '(' num_list ')' """
    p[0] = AST.Function(p[1], p[3])
    p[0].lineno = p.lineno(1)


def p_row_list(p):
    """ row_list : row
                 | row_list ',' row"""
    if len(p) == 2:
        p[0] = AST.Matrix(p[1])
    else:
        p[0] = p[1]
        p[0].rows += [p[3]]


def p_row(p):
    """row : '[' num_list ']' """
    p[0] = p[2]


def p_num_list(p):
    """ num_list : number
                 | num_list ',' number """

    if len(p) == 4:
        p[0] = p[1]
        p[0].values += [p[3]]
    else:
        p[0] = AST.Row(p[1])


def p_number(p):
    """ number : INTNUM
               | FLOAT"""
    if type(p[1]) == int:
        p[0] = AST.IntNum(p[1])
    else:
        p[0] = AST.FloatNum(p[1])


# TODO: reszta sys
def p_sys_function_1(p):
    """ sys_function : PRINT print_block """
    p[0] = AST.PrintF(p[2])


def p_sys_function(p):
    """ sys_function : BREAK
                     | RETURN expression
                     | CONTINUE """

    if p[1] == "return":
        p[0] = AST.ReturnStatement(p[2])
    else:
        p[0] = AST.ContBreakStatement(p[1])

    p[0].lineno = p.lineno(1)


def p_print_block_1(p):
    """ print_block : print_block ',' expression"""
    p[0] = p[1]
    p[0].expressions += [p[3]]


def p_print_block_2(p):
    """ print_block : expression"""
    p[0] = AST.Expressions(p[1])


def p_loop(p):
    """ loop : for_loop
             | while_loop"""
    p[0] = p[1]


def p_for_loop(p):
    """ for_loop : FOR ID '=' range instruction """
    p[0] = AST.ForLoop(AST.Variable(p[2]), p[4], p[5])


def p_range(p):
    """ range : expression ':' expression"""

    print("range ", p[:])
    p[0] = AST.Range(p[1], p[3])
    p[0].lineno = p.lineno(2)


def p_while_loop(p):
    """ while_loop : WHILE '(' expression comp_device expression ')' instruction"""
    p[0] = AST.WhileLoop(AST.BinExpr(p[4], p[3], p[5]), p[7])


def p_branch(p):
    """ branch : IF '(' expression comp_device expression ')' instruction %prec IFX
               | IF '(' expression comp_device expression ')' instruction ELSE instruction """
    if len(p) == 8:
        p[0] = AST.IfStatement(AST.BinExpr(p[4], p[3], p[5]), p[7])
    else:
        p[0] = AST.IfStatement(AST.BinExpr(p[4], p[3], p[5]), p[7], p[9])


def p_comp_device(p):
    """comp_device : LEQUAL
                   | GREQUAL
                   | DIFFERS
                   | EQUALS
                   | '<'
                   | '>' """
    p[0] = p[1]
    # p[0].lineno = p.lineno(2)


parser = yacc.yacc()
