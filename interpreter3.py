import copy
import math


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

    def pop_update(self):
        new_names = self.names
        self.names = self.stack.pop()
        for name in new_names.keys():
            if name in self.names.keys():
                self.update(name, new_names[name])


def type_assertion(symbol: Symbol, typ):
    if symbol.typ != typ:
        raise Exception(f"Expected {typ}, got {symbol.typ}")


def number_assertion(symbol: Symbol):
    if symbol.typ not in ['int', 'float']:
        raise Exception(f"{symbol.value} is not a number")


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
        if op == '+':
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

        def func(scope, *argv, name=name, body=body, arg_names=arg_names, ret_typ=ret_typ):
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

    def eval_if(expr: tuple):
        scope.push()
        cond, if_block, else_block = expr
        cond = evaluate(cond, scope)
        type_assertion(cond, 'bool')

        result = None

        if cond.value is True:
            result = evaluate(if_block, scope)
        elif else_block is not None:
            result = evaluate(else_block, scope)
        scope.pop_update()
        return result

    def eval_while(expr: tuple):
        scope.push()
        cond, block = expr
        while True:
            cond_symbol = evaluate(cond, scope)
            type_assertion(cond_symbol, 'bool')
            if cond_symbol.value:
                should_break = evaluate(block, scope)
                should_break = Symbol("none", None) if should_break is None else should_break
                if should_break.typ == 'return':
                    scope.pop_update()
                    return should_break
                if should_break.typ == 'break':
                    break
                if should_break.typ == 'continue':
                    pass
            else:
                break
        scope.pop_update()

    def eval_for(expr: tuple):
        pre, cond, post, block = expr
        evaluate(pre, scope)

        while True:
            symbol = evaluate(cond, scope)
            type_assertion(symbol, 'bool')

            if symbol.value is True:
                scope.push()

                brk = evaluate(block, scope)
                # If return, forward it to the function.
                if brk.typ == 'return':
                    scope.pop_update()
                    return brk
                # If break, just finish the loop.
                if brk.typ == 'break':
                    scope.pop_update()
                    break
                # It already stopped, so it can pass.
                if brk.typ == 'continue':
                    pass

                scope.pop_update()
                evaluate(post, scope)
            else:
                break

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
        "IF": eval_if,
        "WHILE": eval_while,
        "FOR": eval_for,

    }
    results = []
    tokens = tokens if isinstance(tokens, list) else [tokens]
    for (expr_type, expr) in tokens:
        results.append(evaluators[expr_type](expr))
    return results[-1]


def make_def_scope():
    scope = Scope()

    math_builtins = ["sin", "cos", "exp", "sqrt", "log"]
    for name in math_builtins:
        def builtin(scope, *args, name=name):
            if len(args) != 1:
                raise Exception("Function '%s'. Expected 1 argument. Got %d args." % (name, len(args)))
            symbol = args[0]
            if not number_check(symbol):
                raise Exception(f"Not a number{symbol.value}")
            result = getattr(math, name)(symbol.value)
            return Symbol('float', float(result))

        scope.add(name, Symbol('func', builtin))
        return scope

def test(expected, command):
    result = evaluate(command, make_def_scope()).value
    if result == expected:
        print('OK')
    else:
        print("*****ERROR*******\n" + str(command) + '\n*********WAS**********\n' + str(
            result) + "\n**********SHOULD*BE*********\n" + str(expected) + "\n************************\n")


def test_raises(expected, command):
    result = None
    try:
        result = evaluate(command, Scope()).value
    except Exception as e:
        if str(e) == expected:
            print('OK')
            return
        else:
            print("*****ERROR*******\n" + str(command) + '\n*********WAS**********\n' + str(
                e) + "\n**********SHOULD*BE*********\n" + str(expected) + "\n************************\n")
            return
    print("*****ERROR*******\n" + str(command) + '\n*********WAS**********\n' + str(
        result) + "\n**********SHOULD*BE*********\n" + str(expected) + "\n************************\n")


####################
# TESTS
####################

# 5
test(5, [('INT', 5)])
# int i = -5; i
test(-5, [('DEC', ('i', 'int', ('UMINUS', ('INT', 5)))), ('REF', 'i')])
# int a = 1; a += 3; a;
test(4, [('DEC', ('a', 'int', ('INT', 1))), ('INCREMENT', ('a', ('INT', 3))), ('REF', 'a')])

# 2.2.1 implementacja działań potęgowania, funkcji specjalnych, działań relacyjnych
# 2 ^ 3
test(8, [('BINOP', (('INT', 2), '^', ('INT', 3)))])
# 2 > 1
test(True, [('REL', (('INT', 2), '>', ('INT', 1)))])
# sin(0)
test(0, [('CALL', ('sin', (('INT', 0),)))])

# 2.2.1 - zmiana znaku, 2.2.2 implementacja instrukcji oddzielonych średnikiem
# int a = 5; a = -a; a
test(-5, [('DEC', ('a', 'int', ('INT', 5))), ('ASSIGN', ('a', ('UMINUS', ('REF', 'a')))), ('REF', 'a')])

# 2.2.3 kontynuacja parsowania kolejnych instrukcji w przypadku błędu
# hhhh, int i = 5; i
test(5, [('DEC', ('i', 'int', ('INT', 5))), ('REF', 'i')])

# 2.2.5 . instrukcje warunkowe i pętle
# int x = 5; if(7>2){x=9};x
test(9, [('DEC', ('x', 'int', ('INT', 5))),
         ('IF', (('REL', (('INT', 7), '>', ('INT', 2))), [('ASSIGN', ('x', ('INT', 9)))], None)), ('REF', 'x')])

# int i = 10; while(i>5){i=i-1}; i
test(5, [('DEC', ('i', 'int', ('INT', 10))), (
    'WHILE',
    (('REL', (('REF', 'i'), '>', ('INT', 5))), [('ASSIGN', ('i', ('BINOP', (('REF', 'i'), '-', ('INT', 1)))))])),
         ('REF', 'i')])

# string s = ""; for(int i = 5; i < 10; i = i+1){s = s + "a"}; s;
test('aaaaa', [('DEC', ('s', 'string', ('STRING', ''))), ('FOR', (
    ('DEC', ('i', 'int', ('INT', 5))), ('REL', (('REF', 'i'), '<', ('INT', 10))),
    ('ASSIGN', ('i', ('BINOP', (('REF', 'i'), '+', ('INT', 1))))),
    [('ASSIGN', ('s', ('BINOP', (('REF', 's'), '+', ('STRING', 'a')))))])), ('REF', 's')])

# LAB 3

# 2.3.2
# int i
test(None, [('DEC', ('i', 'int', None))])
# float f
test(None, [('DEC', ('f', 'float', None))])
# string s
test(None, [('DEC', ('s', 'string', None))])
# bool b
test(None, [('DEC', ('b', 'bool', None))])
# int h;  int h
test_raises('h has already been defined', [('DEC', ('h', 'int', None)), ('DEC', ('h', 'int', None))])

# 2.3.3 sprawdzanie typów
# int i; i = "string"
test_raises('Expected int, got string', [('DEC', ('i', 'int', None)), ('ASSIGN', ('i', ('STRING', 'string')))])
# string a = "a"; string b = "b"; a-b
test_raises('- not supported on arguments of types string, string',
            [('DEC', ('a', 'string', ('STRING', 'a'))), ('DEC', ('b', 'string', ('STRING', 'b'))),
             ('BINOP', (('REF', 'a'), '-', ('REF', 'b')))])

# 2.3.4 instrukcja przypisania
# int a = 1; a = 3; a;
test(3, [('DEC', ('a', 'int', ('INT', 1))), ('ASSIGN', ('a', ('INT', 3))), ('REF', 'a')])
# string s = "test"; s
test('test', [('DEC', ('s', 'string', ('STRING', 'test'))), ('REF', 's')])
# float f = 4.2; f
test(4.2, [('DEC', ('f', 'float', ('FLOAT', 4.2))), ('REF', 'f')])
# bool b; b = 2 < 6; b
test(True, [('DEC', ('b', 'bool', None)), ('ASSIGN', ('b', ('REL', (('INT', 2), '<', ('INT', 6))))), ('REF', 'b')])

# 2.3.5 przeciążanie operatorw
# string a = "a"; string b = "b"; a+b
test('ab', [('DEC', ('a', 'string', ('STRING', 'a'))), ('DEC', ('b', 'string', ('STRING', 'b'))),
            ('BINOP', (('REF', 'a'), '+', ('REF', 'b')))])

# 2.3.6 sprawdzanie syntaktyczne deklaracji zmiennych
# int a = "pociąg"
test_raises('Expected int, got string', [('DEC', ('a', 'int', ('STRING', 'pociąg')))])
# 2.3.7 sprawdzanie syntaktyczne instrukcji
# int a = trala
test_raises('trala is not defined in current scope', [('DEC', ('a', 'int', ('REF', 'trala')))])

# 2.4.1 definiowanie funkcij
# int x(int g){return g^2};x(5)
test(25, [('FUNC', ('int', 'x', [('int', 'g')], [('RETURN', ('BINOP', (('REF', 'g'), '^', ('INT', 2))))])),
          ('CALL', ('x', (('INT', 5),)))])

# 2.4.2 definiowanie blokw
# { int a; a=5; a}
test(5, [('DEC', ('a', 'int', None)), ('ASSIGN', ('a', ('INT', 5))), ('REF', 'a')])

# 2.4.3 definiowanie zmiennych globalnych i lokalnych
# string a = "global"; if (2>1) { a = "overwritten"}; a
test("overwritten", [('DEC', ('a', 'string', ('STRING', 'global'))), (
'IF', (('REL', (('INT', 2), '>', ('INT', 1))), [('ASSIGN', ('a', ('STRING', 'overwritten')))], None)), ('REF', 'a')])
# string a = "global"; if (2>1) { b = "local"}; b
test_raises('b is not defined!', [('DEC', ('a', 'string', ('STRING', 'global'))), (
'IF', (('REL', (('INT', 2), '>', ('INT', 1))), [('ASSIGN', ('b', ('STRING', 'local')))], None)), ('REF', 'b')])

# 2.4.4 instrukcja wywołania funkcji
# int add(int a, int b){return a+b}; add(12, 5)
test(17, [
    ('FUNC', ('int', 'add', [('int', 'a'), ('int', 'b')], [('RETURN', ('BINOP', (('REF', 'a'), '+', ('REF', 'b'))))])),
    ('CALL', ('add', (('INT', 12), ('INT', 5))))])

# 2.4.5 automatyczna konwersja typów
# string a = "a"; int b = 5; a+b
test("a5", [('DEC', ('a', 'string', ('STRING', 'a'))), ('DEC', ('b', 'int', ('INT', 5))),
            ('BINOP', (('REF', 'a'), '+', ('REF', 'b')))])

# 2.5.1 Zagnieżdżone wywołania funkcji
# int x(int g){return g^2};int y(int h){return x(h)};y(5)
test(25, [('FUNC', ('int', 'x', [('int', 'g')], [('RETURN', ('BINOP', (('REF', 'g'), '^', ('INT', 2))))])),
          ('FUNC', ('int', 'y', [('int', 'h')], [('RETURN', ('CALL', ('x', (('REF', 'h'),))))])),
          ('CALL', ('y', (('INT', 5),)))])

# -a
test_raises('a is not defined in current scope', [('UMINUS', ('REF', 'a'))])


