import math
from typing import List

from parser3 import parse, make_parser


class Symbol:
    def __init__(self, typ, value):
        self.typ = typ
        self.value = value


class Scope:
    def __init__(self):
        self.names = {}

    def add(self, name: str, symbol: Symbol):
        if name in self.names:
            raise Exception(f"{name} has already been defined")
        else:
            self.names[name] = symbol

    def update(self, name: str, symbol: Symbol):
        if name not in self.names:
            raise Exception(f"{name} is not defined")
        else:
            self.names[name] = symbol

    def contains(self, name: str):
        return name in self.names

    def get(self, name: str):
        return self.names[name]


def type_assertion(symbol: Symbol, typ):
    if symbol.typ != typ:
        raise Exception(f"Expected {typ}, got {symbol.typ}")


def number_assertion(symbol: Symbol):
    if symbol.typ not in ['int', 'float']:
        raise Exception(f"{Symbol.value} is not a number")


def number_check(symbol: Symbol) -> bool:
    return symbol.typ in ['int', 'float']


def evaluate(tokens, scope: Scope) -> Symbol:
    ################################################
    # ################ evaluators ################ #
    ################################################

    def eval_int(expr) -> Symbol:
        return Symbol("int", expr)

    def eval_float(expr) -> Symbol:
        return Symbol("float", expr)

    def eval_string(expr) -> Symbol:
        return Symbol("string", expr)

    def eval_bool(expr) -> Symbol:
        return Symbol("bool", expr)

    def eval_dec(expr: tuple) -> Symbol:
        name, typ, assigned = expr
        assigned_symbol = None
        if assigned is not None:
            assigned_symbol = evaluate(assigned, scope)
        if assigned_symbol is None:
            assigned_symbol = Symbol(typ, None)
        else:
            type_assertion(assigned_symbol, typ)
        scope.add(name, assigned_symbol)
        return Symbol("none", None)

    def eval_assign(expr: tuple) -> Symbol:
        name, assigned = expr
        assigned_symbol = evaluate(assigned, scope)
        if not scope.contains(name):
            raise Exception(f"{name} is not defined!")
        assigned_to = scope.get(name)
        type_assertion(assigned_symbol, assigned_to.typ)
        scope.update(name, assigned_symbol)
        return assigned_symbol

    def eval_increment(expr: tuple) -> Symbol:
        name, incremented = expr
        incremented_symbol = evaluate(incremented, scope)
        if not scope.contains(name):
            raise Exception(f"{name} is not defined!")
        incremented_to = scope.get(name)
        type_check(incremented_symbol, incremented_to.typ)
        scope.update(name, Symbol(incremented_to.typ, incremented_to.value + incremented_symbol.value))
        return incremented_symbol


    def eval_ref(expr) -> Symbol:
        if not scope.contains(expr):
            raise Exception(f"{expr} is not defined in current scope")
        return scope.get(expr)

    def eval_uminus(expr) -> Symbol:
        symbol = evaluate(expr, scope)
        number_assertion(symbol)
        symbol.value = (-1 * symbol.value)
        return symbol

    def binop_str(lhs, op, rhs):
        if op == 'PLUS':
            return Symbol('string', str(lhs.value) + str(rhs.value))
        return None

    def binop_num(lhs, op, rhs):
        typ = 'int'
        if lhs.typ == 'float' or rhs.typ == 'float':
            typ = 'float'
        lval = lhs.value
        rval = rhs.value
        if op == '+':
            return Symbol(typ, lval + rval)
        elif op == '-':
            return Symbol(typ, lval - rval)
        elif op == '*':
            return Symbol(typ, lval * rval)
        elif op == '/':
            return Symbol('float', lval / rval)
        elif op == '%':
            return Symbol(typ, lval % rval)
        elif op == '^':
            return Symbol(typ, lval ** rval)

    #
    # def binop_bool(lhs_symbol, op, rhs_symbol):
    #     if op == 'PLUS':
    #         return Symbol('bool', str(lhs) + str(rhs))

    def eval_binop(expr: tuple) -> Symbol:
        lhs, op, rhs = expr
        lhs_symbol = evaluate(lhs, scope)
        rhs_symbol = evaluate(rhs, scope)
        result = None
        if lhs_symbol.typ == 'string' or rhs_symbol.typ == 'string':
            result = binop_str(lhs_symbol, op, rhs_symbol)
        elif number_check(lhs_symbol) or number_check(rhs_symbol):
            result = binop_num(lhs_symbol, op, rhs_symbol)
        # elif lhs_symbol.typ == 'bool' and rhs_symbol.typ == 'bool':
        #      result = binop_str(lhs_symbol, op, rhs_symbol)

        if result is None:
            raise Exception(f"{op} not supported on arguments of types {lhs_symbol.typ}, {rhs_symbol.typ}")
        return result

    def eval_rel(expr: tuple) -> Symbol:
        lhs, op, rhs = expr
        lhs_symbol = evaluate(lhs, scope)
        rhs_symbol = evaluate(rhs, scope)
        result = None
        if number_check(lhs_symbol) and number_check(rhs_symbol):
            lval = lhs_symbol.value
            rval = rhs_symbol.value
            if op == '>':
                result = lval > rval
            elif op == '<':
                result = lval < rval
            elif op == '==':
                result = lval == rval
            elif op == '>=':
                result = lval >= rval
            elif op == '<=':
                result = lval <= rval
            elif op == '!=':
                result = lval != rval
        if result is None:
            raise Exception(f"{op} not supported on arguments of types {lhs_symbol.typ}, {rhs_symbol.typ}")
        return Symbol('bool', result)

    def eval_call(expr: tuple):
        name, exprlist = expr
        if not scope.contains(name):
            raise Exception(f"Function {name} is not defined")
        symbol = scope.get(name)
        func = symbol.value
        exprlist = [evaluate(exp, scope) for exp in exprlist]
        return func(scope, *exprlist)


    evaluators = {
        "INT": eval_int,
        "FLOAT": eval_float,
        "STRING": eval_string,
        "BOOL": eval_bool,
        "DEC": eval_dec,
        "ASSIGN": eval_assign,
        "INCREMENT": eval_increment,
        "REF": eval_ref,
        "UMINUS": eval_uminus,
        "BINOP": eval_binop,
        "REL": eval_rel,
        "CALL": eval_call,
        # "IF": eval_if,
        # "WHILE": eval_while,
        # "FOR": eval_for,
        # "FUNC": eval_func,
    }
    results = []
    tokens = tokens if isinstance(tokens, list) else [tokens]
    for (expr_type, expr) in tokens:
        results.append(evaluators[expr_type](expr))
    return results[-1]


command = \
[('REL', (('INT', 6), '>', ('INT', 5)))]
#     [('BINOP', (('BINOP', (('INT', 2), '*', ('INT', 2))), '+', ('INT', 2)))]


def test(expected, command):
    result = evaluate(command, Scope()).value
    if result == expected:
        print('OK')
    else:
        print("*****ERROR*******\n"+str(command)+'\n*********WAS**********\n'+str(result) + "\n**********SHOULD*BE*********\n" +str(expected) + "\n************************\n")

def test_raises(expected, command):
    result = None
    try:
        result = evaluate(command, Scope()).value
    except Exception as e:
        if str(e) == expected:
            print('OK')
            return 
        else:
            print("*****ERROR*******\n"+str(command)+'\n*********WAS**********\n'+str(e) + "\n**********SHOULD*BE*********\n" +str(expected) + "\n************************\n")
            return
    print("*****ERROR*******\n"+str(command)+'\n*********WAS**********\n'+str(result) + "\n**********SHOULD*BE*********\n" +str(expected) + "\n************************\n")
        


####################
# TESTS
####################

# int i = -5; i
test(-5, [('DEC', ('i', 'int', ('UMINUS', ('INT', 5)))), ('REF', 'i')])

# int a = 1; a = 3; a;
test(3, [('DEC', ('a', 'int', ('INT', 1))), ('ASSIGN', ('a', ('INT', 3))), ('REF', 'a')])

# int a = 1; a += 3; a;
test(4, [('DEC', ('a', 'int', ('INT', 1))), ('INCREMENT', ('a', ('INT', 3))), ('REF', 'a')])

# int a = 5; a = -a; a
test(-5, [('DEC', ('a', 'int', ('INT', 5))), ('ASSIGN', ('a', ('UMINUS', ('REF', 'a')))), ('REF', 'a')])

# int a = trala
test_raises('trala is not defined in current scope', [('DEC', ('a', 'int', ('REF', 'trala')))])

# -a
test_raises('a is not defined in current scope', [('UMINUS', ('REF', 'a'))])


