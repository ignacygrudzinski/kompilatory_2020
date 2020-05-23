from lexer import *

def p_wrapper(p):
    'wrapper : expr'
    print(p[1])

def p_expr_function(p):
    '''expr : FUNCTION expr'''
    p[0] = p[1][1](p[2])

def p_expr_binop(p):
    '''expr : expr POW expr'''
    # for pip in p:
    #     print(pip)
    if p[2] == '^':
        p[0] = p[1]**p[3]

def p_expr_name(p):
    'expr : NAME'
    p[0] = p[1]

def p_expr_string(p):
    'expr : STRING'
    p[0] = p[1]


def p_input(p):
    'expr : number'
    p[0] = p[1]

def p_number(p):
    '''number : INT
              | FLOAT'''
    p[0] = p[1]

def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")

import ply.yacc as yacc
parser = yacc.yacc()

while True:
    try:
        s = input()
    except EOFError:
        break
    if not s:
        continue
    yacc.parse(s)