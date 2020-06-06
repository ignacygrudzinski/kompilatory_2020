import math
import ply.yacc as yacc
from lexer3 import *

precedence = (
    ('left', 'EQ', 'NEQ'),
    ('left', 'GT', 'LT'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'DIV', 'TIMES', 'MOD'),
    ("left", 'SEMICOLON'),
    ('right', 'POW'),
)

#for printing out, delete if not needed
def p_wrapper(p):
    '''wrapper : instruction
                | block'''
    print(p[1])

#TODO: fix things unneccessarily split in 2

def p_instructions(p):
    '''instruction : instruction SEMICOLON instruction'''
    p[0] = p[1] + p[3]

def p_instruction_expr(p):
    '''instruction : expression'''
    p[0] = [p[1]]

def p_instruction_expr_semi(p):
    '''instruction : instruction SEMICOLON'''
    p[0] = p[1]

def p_declaration_empty(p):
    '''decl_empty : TYPE_SPEC NAME'''
    p[0] = ('DEC', (p[2], p[1], None))

def p_declaration_2(p):
    '''decl_initial : TYPE_SPEC NAME ASSIGN expression'''
    p[0] = ('DEC', (p[2], p[1], p[4]))

def p_instruction_declaration(p):
    '''instruction : decl_empty
                 | decl_initial'''
    p[0] = [p[1]]

def p_assign(p):
    '''assign : NAME ASSIGN expression'''
    p[0] = ('ASSIGN', (p[1], p[3]))

def p_instruction_assign(p):
    '''instruction : assign'''
    p[0] = [p[1]]

def p_instruction_return(p):
    '''instruction : RETURN expression'''
    p[0] = [("RETURN", p[2])]

def p_instruction_continue(p):
    '''instruction : CONTINUE'''
    p[0] = [("CONTINUE", None)]

def p_instruction_break(p):
    '''instruction : BREAK'''
    p[0] = [("BREAK", None)]

def p_instruction_if_1(p):
    '''instruction : IF condition block ELSE block'''
    p[0] = [('IF', (p[2], p[3], p[5]))]

def p_instruction_if_2(p):
    '''instruction : IF condition block'''
    p[0] = [('IF', (p[2], p[3], None))]

def p_instruction_while(p):
    '''instruction : WHILE condition block'''
    p[0] = [('WHILE', (p[2], p[3]))]

def p_instruction_for(p):
    '''instruction : FOR OPAREN decl_initial SEMICOLON expression SEMICOLON assign CPAREN block'''
    p[0] = [('FOR', (p[3], p[5], p[7], p[9]))]

def p_block(p):
    '''block : OBLOCK instruction CBLOCK'''
    p[0] = p[2]

def p_condition(p):
    '''condition : OPAREN expression CPAREN'''
    p[0] = p[2]

def p_arglist_1(p):
    '''arglist : TYPE_SPEC NAME COMMA arglist'''
    p[0] = [(p[1], p[2])] + p[4]

def p_arglist_2(p):
    '''arglist : TYPE_SPEC NAME'''
    p[0] = [(p[1], p[2])]

def p_func_argless(p):
    '''instruction : TYPE_SPEC NAME OPAREN CPAREN block'''
    p[0] = [('FUNC', (p[1], p[2], [], p[5]))]

def p_func_args(p):
    '''instruction : TYPE_SPEC NAME OPAREN arglist CPAREN block'''
    p[0] = [('FUNC', (p[1], p[2], p[4], p[6]))]

def p_expression_uminus(p):
    '''expression : MINUS expression'''
    p[0] = ('UMINUS', (p[1], p[2]))

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIV expression
                  | expression MOD expression
                  | expression POW expression'''
    p[0] = ('BINOP', (p[1], p[2], p[3]))

def p_expression_relation(p):
    '''expression : relation'''
    p[0] = p[1]

def p_relation(p):
    '''relation : expression EQ expression
                | expression NEQ expression
                | expression GT expression
                | expression LT expression'''
    p[0] = ('REL', (p[1], p[2], p[3]))

def p_exprlist_1(p):
    '''exprlist : expression COMMA exprlist'''
    p[0] = [p[1]] + p[3]

def p_exprlist_2(p):
    '''exprlist : expression'''
    p[0] = [p[1]]

def p_expression_call_args(p):
    '''expression : NAME OPAREN exprlist CPAREN'''
    p[0] = ('CALL', (p[1], tuple(p[3])))

def p_expression_call_argless(p):
    '''expression : NAME OPAREN CPAREN'''
    p[0] = ('CALL', (p[1], tuple()))

def p_expression_group(p):
    "expression : OPAREN expression CPAREN"
    p[0] = p[2]

def p_expression_string(p):
    '''expression : STRING'''
    p[0] = ('STRING', p[1])

def p_expression_integer(p):
    '''expression : INT'''
    p[0] = ('INT', p[1])

def p_expression_FLOAT(p):
    '''expression : FLOAT'''
    p[0] = ('FLOAT', float(p[1]))

def p_expression_bool(p):
    '''expression : BOOL'''
    p[0] = ('BOOL', bool(p[1]))

def p_expression_ref(p):
    "expression : NAME"
    p[0] = ('REF', p[1])

def p_error(p):
    mk_err("Syntax error at '%s'" % p.value if p else "Syntax error at EOF")

def mk_err(err):
    # errors.append(err)
    print(err)

def make_parser():
    return (make_lexer(), yacc.yacc())

def parse(parser, inp):
    global errors
    errors = []

    lex, parser = parser
    lex.input(inp)

    result = parser.parse(inp)
    return (errors, result)

if __name__ == '__main__':
    parser = yacc.yacc()
    while True:
        try:
            s = input()
        except EOFError:
            break
        if not s:
            continue
        yacc.parse(s)
