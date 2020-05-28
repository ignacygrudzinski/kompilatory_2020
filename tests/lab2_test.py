from parser_tester import test



test("3+7", "[10]")

test("8-6", "[2]")

test("7*8", "[56]")

test("100/10", "[10.0]")

test("3^3", "[27]")

test("sin(0)","[0.0]")

test("cos(0)", "[1.0]")

test("-5","[-5]")

test("5==5","[True]")

test("5.5<5.74","[True]")

test("13<8","[False]")

test("3!=8","[True]")

test("2+2; 4*4","[4, 16]")

test("7; 19","[7, 19]")

test("ź; 2+2; 7*7", "Syntax error at 'ź'\n[4, 49]")

test("{2+2; 6*6}", "[4, 36]")

test("if(2<5){2+5;2-5}","[7, -3]")