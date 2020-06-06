from lexer import *


precedence = (
    ("left", 'EQ', 'NEQ'),
    ("left", 'GT', 'LT'),
    ("left", 'PLUS', 'MINUS'),
    ("left", 'TIMES', 'DIV', 'MOD'),
    ("left", 'SEMICOLON'),
    ("right", 'POW'),
)


def p_wrapper(p):
    '''wrapper : instruction
             | block'''
    print(p[1])

# TODO: find that old S/R conflict
# TODO relations, conditions, function arg lists
# TODO 2 fix returns to make them interpreter-digestible
# minor TODO: refactor function names (unify thing_instruction and instruction_thing)

#instr1, instr2
def p_instructions(p):
    '''instruction : instruction SEMICOLON instruction'''
    p[0] = p[1] + p[3]

#instr1
def p_instruction(p):
    '''instruction : instruction SEMICOLON'''
    p[0] = [p[1]]

#[IF, (cond, then_block, else_block)]
def p_instruction_if_else(p):
    '''instruction : IF OPAREN expr CPAREN block ELSE block'''
    p[0] = ['IF', (p[3],p[5],p[7])]

#[IF, (cond, then_block, None)]
def p_instruction_if(p):
    '''instruction : IF OPAREN expr CPAREN block '''
    p[0] = ['IF', (p[3], p[5], None)]

#[FOR, (i_declaration, condition, assignment, block)]
def p_instruction_for(p):
    '''instruction : FOR OPAREN full_dec SEMICOLON expr SEMICOLON assignment CPAREN block'''
    p[0] = [('FOR', (p[3], p[5], p[7], p[9]))]

#[WHILE, (condition, block)]
def p_instruction_while(p):
    '''instruction : WHILE OPAREN expr CPAREN block'''
    p[0] = ['WHILE', (p[3], p[5])]

#[expr]
def p_expr_instruction(p):
    '''instruction : expr'''
    p[0] = [p[1]]

#("RETURN", expr)
def p_return_instruction(p):
    '''instruction : RETURN expr'''
    p[0] = [("RETURN", p[2])]

#[("CONTINUE", None)]
def p_continue_instruction(p):
    '''instruction : CONTINUE'''
    p[0] = [("CONTINUE", None)]

#[("BREAK", None)]
def p_break_instruction(p):
    '''instruction : BREAK'''
    p[0] = [("BREAK", None)]

#("DEC_FULL", (DEC, (TYPE, NAME)), expr))                   ###important for parser!
def p_full_declaration(p):
    '''full_dec : type_dec ASSIGN expr'''
    p[0] = ('DEC_FULL', (p[1], p[3]))

#("DEC", (TYPE, NAME))
def p_type_declaration(p):
    '''type_dec : INT NAME
                | FLOAT NAME
                | STRING NAME
                | BOOL NAME'''
    p[0] = ('DEC', (p[1], p[2]))


#[declaration]
def p_instruction_declaration(p):
    '''instruction : type_dec
                   | full_dec'''
    p[0] = [p[1]]

#("ASSIGN", (NAME, VALUE))
def p_assignment(p):
    '''assignment : NAME ASSIGN expr'''
    p[0] = ('ASSIGN', (p[1], p[3]))

#[assignment]
def p_instruction_assignment(p):
    '''instruction : assignment'''
    p[0] = [p[1]]

#block
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
    #TODO expand to boolean types
    #TODO redefine everything to interpreter-digestible form (long list of stuff)
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

def p_expr_number(p):
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