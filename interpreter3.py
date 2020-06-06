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


def type_check(symbol: Symbol, typ):
    if symbol.typ != typ:
        raise Exception(f"Expected {typ}, got {symbol.typ}")

def number_check(symbol: Symbol):
    if symbol.typ not in ['int', 'float']:
        raise Exception(f"{Symbol.value} is not a number")

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
            type_check(assigned_symbol, typ)
        scope.add(name, assigned_symbol)
        return Symbol("none", None)

    def eval_assign(expr: tuple) -> Symbol:
        name, assigned = expr
        assigned_symbol = evaluate(assigned, scope)
        if not scope.contains(name):
            raise Exception(f"{name} is not defined!")
        assigned_to = scope.get(name)
        type_check(assigned_symbol, assigned_to.typ)
        scope.update(name, assigned_symbol)
        return assigned_symbol

    def eval_ref(expr) -> Symbol:
        if not scope.contains(expr):
            raise Exception(f"{expr} is not defined in current scope")
        return scope.get(expr)

    def eval_uminus(expr) -> Symbol:
        symbol = evaluate(expr, scope)
        number_check(symbol)
        symbol.value = (-1 * symbol.value)
        return symbol



    evaluators = {
        "INT": eval_int,
        "FLOAT": eval_float,
        "STRING": eval_string,
        "BOOL": eval_bool,
        "DEC": eval_dec,
        "ASSIGN": eval_assign,
        "REF": eval_ref,
        "UMINUS": eval_uminus,
        # "BINOP": eval_binop,
        # "REL": eval_rel,
        # "CALL": eval_call,
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
[('DEC', ('i', 'int', ('UMINUS', ('INT', 5)))), ('REF', 'i')]

print(evaluate(command, Scope()).value)
