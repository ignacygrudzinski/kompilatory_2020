import copy
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
        self.stack = []

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

    def push(self):
        self.stack.append(copy.deepcopy(self.names))

    def pop(self):
        self.names = self.stack.pop()




def type_assertion(symbol: Symbol, typ):
    if symbol.typ != typ:
        raise Exception(f"Expected {typ}, got {symbol.typ}")


def number_assertion(symbol: Symbol):
    if symbol.typ not in ['int', 'float']:
        raise Exception(f"{Symbol.value} is not a number")


def number_check(symbol: Symbol) -> bool:
    return symbol.typ in ['int', 'float']


def try_convert(symbol: Symbol, typ: str) -> Symbol:
    if symbol.typ == typ:
        return symbol
    if symbol.typ == 'int' and typ == 'float':
        return Symbol('float', float(symbol.value))
    if typ == 'string':
        return Symbol('string', str(symbol.value))



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
        type_assertion(incremented_symbol, incremented_to.typ)
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

    def eval_return(expr) -> Symbol:
        symbol = evaluate(expr, scope)
        return Symbol('return', symbol)

    def eval_break(_) -> Symbol:
        return Symbol('break', None)

    def eval_continue(_) -> Symbol:
        return Symbol('continue', None)

    def eval_func(expr: tuple) -> Symbol:
        ret_typ, name, arg_names, body = expr

        def func(scope, *argv, name=name, body=body, arg_names = arg_names, ret_typ=ret_typ):
            scope.push()
            if len(argv) != len(arg_names):
                raise Exception(f"Function {name} expected {len(arg_names)} arguments, got {len(argv)}")
            for ((arg_ty, arg_name), symbol) in zip(arg_names, argv):
                converted = try_convert(symbol, arg_ty)
                type_assertion(converted, arg_ty)
                scope.add(arg_name, converted)
            result = evaluate(body, scope)
            if result.typ == 'return':
                result = result.value
            elif result.typ in ['break', 'continue']:
                raise Exception("Break or continue without corresponding loop.")

            type_assertion(result, ret_typ)
            scope.pop()
            return result

        scope.add(name, Symbol('func', func))
        return Symbol('none', None)

    def eval_call(expr: tuple):
        name, exprlist = expr
        if not scope.contains(name):
            raise Exception(f"Function {name} is not defined")
        symbol = scope.get(name)
        if symbol.typ != 'func':
            raise Exception(f"{name} is not a function")

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
        "RETURN": eval_return,
        "BREAK": eval_break,
        "CONTINUE": eval_continue,
        "FUNC": eval_func,
        "CALL": eval_call,
        # "IF": eval_if,
        # "WHILE": eval_while,
        # "FOR": eval_for,

    }
    results = []
    tokens = tokens if isinstance(tokens, list) else [tokens]
    for (expr_type, expr) in tokens:
        results.append(evaluators[expr_type](expr))
    return results[-1]



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

#int x(int g){return g^2};x(5)
test(25, [('FUNC', ('int', 'x', [('int', 'g')], [('RETURN', ('BINOP', (('REF', 'g'), '^', ('INT', 2))))])), ('CALL', ('x', (('INT', 5),)))])

#int x(int g){return g^2};int y(int h){return x(h)};y(5)
test(25, [('FUNC', ('int', 'x', [('int', 'g')], [('RETURN', ('BINOP', (('REF', 'g'), '^', ('INT', 2))))])), ('FUNC', ('int', 'y', [('int', 'h')], [('RETURN', ('CALL', ('x', (('REF', 'h'),))))])), ('CALL', ('y', (('INT', 5),)))])
