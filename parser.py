from lexer import *


precedence = (
    ("left", 'EQ', 'NEQ'),
    ("left", 'GT', 'LT'),
    ("left", 'PLUS', 'MINUS'),
    ("left", 'TIMES', 'DIV', 'MOD'),
    ("right", 'POW'),
)


def p_wrapper(p):
    '''wrapper : instruction
             | block'''
    print(p[1])

# TODO instruction types:
# [x] expression
# [ ] declaration
# [ ] assignment
# [ ] return, break, continue
# [ ] if, else, while, for

def p_instructions(p):
    '''instruction : instruction SEMICOLON instruction'''
    p[0] = p[1] + p[3]

def p_instruction(p):
    '''instruction : instruction SEMICOLON'''
    p[0] = [p[1]]

def p_instruction_if_else(p):
    '''instruction : IF OPAREN expr CPAREN block ELSE block'''
    p[0] = ['IF', (p[3],p[5],p[7])]

def p_instruction_if(p):
    '''instruction : IF OPAREN expr CPAREN block '''
    p[0] = ['IF', (p[3], p[5], None)]

def p_instruction_while(p):
    '''instruction : WHILE OPAREN expr CPAREN block'''
    p[0] = ['WHILE', (p[3], p[5])]

def p_expr_instruction(p):
    '''instruction : expr'''
    p[0] = [p[1]]

def p_block(p):
    '''block : OBLOCK instruction CBLOCK'''
    p[0] = p[2]


def p_expr_function(p):
    '''expr : FUNCTION OPAREN expr CPAREN'''
    p[0] = p[1][1](p[3])

def p_expr_binop(p):
    '''expr : expr POW expr
            | expr PLUS expr
            | expr MINUS expr
            | expr TIMES expr
            | expr DIV expr
            | expr EQ expr
            | expr NEQ expr
            | expr GT expr
            | expr LT expr'''
    #TODO expand boolean types
    if p[2] == '^':
        p[0] = p[1]**p[3]
    elif p[2] == '+':
        p[0] = p[1]+p[3]
    elif p[2] == '-':
        p[0] = p[1]-p[3]    
    elif p[2] == '*':
        p[0] = p[1]*p[3]
    elif p[2] == '/':
        p[0] = p[1]/p[3]
    elif p[2] == '==':
        p[0] = p[1] == p[3]
    elif p[2] == '!=':
        p[0] = p[1] != p[3]
    elif p[2] == '<':
        p[0] = p[1] < p[3]
    elif p[2] == '>':
        p[0] = p[1] > p[3]

def p_expression_uminus(p):
    "expr : MINUS expr"
    p[0] = -p[2]

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