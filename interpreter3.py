import math
from typing import List

from parser3 import parse, make_parser


class Symbol:
    def __init__(self, typ, value):
        self.typ = typ
        self._value = value


class Scope:
    def __init__(self):
        self.names = {}

    def add(self, name: str, symbol: Symbol):
        if name in self.names:
            raise Exception(f"{name} has already been defined")
        else:
            self.names[name] = symbol


def type_check(symbol: Symbol, typ):
    if symbol.typ != typ:
        raise Exception(f"Expected {typ}, got {symbol.typ}")


def evaluate(tokens, scope: Scope):

    ################################################
    # ################ evaluators ################ #
    ################################################

    def eval_dec(expr: tuple):
        name, typ, assigned = expr
        assigned_symbol = None
        if assigned is not None:
            assigned_symbol = evaluate(assigned, scope)
        if assigned_symbol is None:
            assigned_symbol = Symbol(typ, None)
        else:
            type_check(assigned_symbol, typ)
        scope.add(name, assigned_symbol)

    def eval_assign(expr: tuple):
        name, assigned = expr
        assigned_symbol = evaluate(expr, scope)


    evaluators = {
        "DEC": eval_dec,
        "ASSIGN": eval_assign,
        "UMINUS": eval_uminus,
        "BINOP": eval_binop,
        "REL": eval_rel,
        "CALL": eval_call,
        "REF": eval_ref,
        "INT": eval_int,
        "REAL": eval_real,
        "BOOL": eval_bool,
        "STRING": eval_string,
        "IF": eval_if,
        "WHILE": eval_while,
        "FOR": eval_for,
        "FUNC": eval_func,
    }
    results = []
    tokens = tokens if isinstance(tokens, list) else [tokens]
    for (expr_type, expr) in tokens:
        results.append(evaluators[expr_type](expr))
    return results[-1]
