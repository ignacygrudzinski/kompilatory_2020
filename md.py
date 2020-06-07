# -----------------------------------------------------------------------------
# calc.py
#
# A simple calculator with variables.   This is from O'Reilly's
# "Lex and Yacc", p. 63.
# -----------------------------------------------------------------------------

import sys

sys.path.insert(0, "../..")

tokens = (
    'H1', 'H2', 'H3', 'BREAK', 'P_OR_CLOSE', 'TEXT',
)


# literals = ['=', '+', '-', '*', '/', '(', ')']

# Tokens

# t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'


def t_H1(t):
    r'<h1>'
    t.value = "# "
    return t


def t_H2(t):
    r'<h2>'
    t.value = "## "
    return t


def t_H3(t):
    r'<h3>'
    t.value = "### "
    return t


def t_P_OR_CLOSE(t):
    r'<p>|</p>|</h\d>'
    t.value = "\n"
    return t


def t_BREAK(t):
    r'<br/>'
    t.value = "  "
    return t


def t_TEXT(t):
    r'[^\<]+'
    t.value = str(t.value)
    return t


t_ignore = " \t"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer
import ply.lex as lex

lexer = lex.lex()

lexer.input('''<h1>Heading</h1>
<h2>Sub-heading</h2>
<p>Paragraphs are separated
by a blank line.</p>''')

for token in lexer:
    print("line %d: %s(%s)" % (token.lineno, token.type, token.value))
