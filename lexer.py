import ply.lex as lex

reserved = {
    #CONTROL FLOW
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'for': 'FOR',
    'return': 'RETURN',
    'break': 'BREAK',
    'continue': 'CONTINUE',
    #BOOLEAN VALUES
    'true' : 'TRUE',
    'false' : 'FALSE',
    #TYPES
    'int' : 'INT',
    'float' : 'FLOAT',
    'bool' : 'BOOL',
    'string' : 'STRING'
}

tokens = list(reserved.values()) + [
    #ARITHMETIC
    'PLUS', 'MINUS', 'TIMES', 'DIV', 'MOD', 'POW',
    #COMPARISON
    'EQ', 'NEQ', 'GT', 'LT', 'ASSIGN',
    #PARENTHESES
    'OPAREN', 'CPAREN', 'OBLOCK', 'CBLOCK',
    #SEPARATORS
    'SEMICOLON', 'COMMA',
    #OTHER
    'NAME', 'UNKNOWN'
]

def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value.lower(), 'NAME')
    return t

def t_STRING(t):
    r'\"(.*?)\"'
    t.value = t.value[1:-1]
    return t

#ARITHMETIC
t_PLUS  = r'\+'
t_MINUS = r'\-'
t_TIMES  = r'\*'
t_DIV   = r'\/'
t_MOD   = r'\%'
t_POW   = r'\^'
#COMPARISON
t_EQ    = r'\=\='
t_NEQ   = r'\!\='
t_GT    = r'\>'
t_LT    = r'\<'
t_ASSIGN    = r'='
#PARENTHESES
t_OPAREN    = r'\('
t_CPAREN    = r'\)'
t_OBLOCK    = r'\{'
t_CBLOCK    = r'\}'
#SEPARATORS
t_SEMICOLON = r'\;'
t_COMMA     = r'\,'


def t_FLOAT(t):
    r'\d*\.\d+|\d+\.\d*'
    t.value = float(t.value)
    return t

def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.value = "\n"
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    t.type = 'UNKNOWN'
    t.value = t.value[0]
    t.lexer.skip(1)
    return t

def make_lexer(inp=None):
    lexer = lex.lex()
    if inp != None:
        lexer.input(inp)
    return lexer

###### TESTS ######

lexer = make_lexer()

if __name__ == '__main__':

    tests = {
        '2' : 'INT',
        '.5' : 'FLOAT',
        '2.' : 'FLOAT',
        '.' : 'UNKNOWN'
    }

    def test_token(lexer, input, expected_type):
        lexer.input(input)
        return next(lexer).type == expected_type
       
    for key in tests:
        print(test_token(lexer, key, tests[key]))