from parser3_tester import test


# lab 3

test("int a", "[('DEC', ('a', 'int', None))]")

test("a = 5", "[('ASSIGN', ('a', ('INT', 5)))]")

test("int a = 5", "[('DEC', ('a', 'int', ('INT', 5)))]")

test("a += 5","[('INCREMENT', ('a', ('INT', 5)))]")

test("true", "[('BOOL', true)]")