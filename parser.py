from lexer import *



# input wraps whole single input passed to parser
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