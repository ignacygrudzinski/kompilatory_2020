# Pytanie 1
1. 5

2. 5

3. 5

4. 5

5. 5

6. 5

7. 4

Sumaryczna sugerowana liczba punktów za to laboratorium: 34

Każdy test powinien składać się z pól: nazwa testu:, komentarz:, kod testu: czy wykonany poprawnie:, wyjście z konsoli:

 

Testy do poszczególnych kryteriów (do każdego kryterium może być wiele testów):

Kod testów 1-4:

tests = {
'2':    'INT',
'.5':   'FLOAT',
'2.':   'FLOAT',
'sin':  'NAME',
'^':    'POW',
'%':    'MOD',
'.':    'UNKNOWN'
}
def test_token(lexer, input, expected_type):
    lexer.input(input)
    return next(lexer).type == expected_type
for key in tests:
    print(test_token(lexer, key, tests[key]))
1. Obsługa tokenów dla liczb:

3 pierwsze przypadki testowe sprawdzają czy liczby są odpowiednio rozpoznawane; testy przechodzą poprawnie; wyjście z konsoli:

True
True
True
2. Obsługa tokenów dla funkcji specjalnych sin, cos, itd

Czwarty przypadek sprawdza czy nazwa funkcji jest rozpoznawana jako nazwa - na obecnym etapie prac funkcje wbudowane obsługuje interpreter; test przechodzi; wyjście:

True
3. Obsługa tokenów dla operatora potęgowania itd

Piąty i szósty przypadek sprawdza czy operatory są poprawnie rozpoznawane; test przechodzi; wyjście:

True
True
4. Automatyczna koretka błędów w tokenach

Niepoprawne tokeny są uznawane za typ UNKNOWN i ignorowane; test przechodzi; wyjście:
True
Dodatkowe zadania dotyczące języka Markdown i html (nie uwzględnione w projekcie języka kalkulatora): zadanie wykonane na pierwszych ćwiczeniach, kod z ćwiczeń w załączniku.

 5,6,7 definiowanie wzorów w tekście i konwersja tokenów dla języka Markdown

Test polega na wypisaniu rozpoznanych przez lekser tokenów języka HTML i odpowiadających im wartości języka Markdown.

Test:

lexer.input('''<h1>Heading</h1>
<h2>Sub-heading</h2>
<p>Paragraphs are separated
by a blank line.</p>''')

Test wykonany poprawnie.

Wyjście:

line 1: H1(# )
line 1: TEXT(Heading)
line 1: P_OR_CLOSE(
)
line 1: TEXT(
)
line 1: H2(## )
line 1: TEXT(Sub-heading)
line 1: P_OR_CLOSE(
)
line 1: TEXT(
)
line 1: P_OR_CLOSE(
)
line 1: TEXT(Paragraphs are separated
by a blank line.)
line 1: P_OR_CLOSE(
)

 # Pytanie 2
 Sugerowana liczba punktów za poszczególne kryteria:

1. 5

2. 5

3. 5

4. 5

5. 5
6. 5

Sumaryczna sugerowana liczba punktów za to laboratorium: 30

Każdy test powinien składać się z pól: nazwa testu:, komentarz:, kod testu: czy wykonany poprawnie:, wyjście z konsoli:

Testy do poszczególnych kryteriów (do każdego kryterium może być wiele testów):

1. 
**Komentarz do testów**
`test(input, output)`, gdzie
- input - input dla parsera
- output - oczekiwany output wygenerowany przez parser

**Potęgowanie**
```
test("3^3", "[27]")
OK
```

**Funkcje specjalne**
```
test("sin(0)","[0.0]")
OK
```


**Działanie relacyjne**
```
test("5==5","[True]")
OK
```

**Zmiana znaku**
```
test("-5","[-5]")
OK
```
 
2. 

**Funkcje oddzielone średnikiem**
```
test("2+2; 4*4","[4, 16]")
OK
```

3.
**Kontynuowanie kolejnych funkcji w przypadku błędu**
```
test("ź; 2+2; 7*7", "Syntax error at 'ź'\n[4, 49]")
OK
```

4.**Możliwość wykonywania obliczeń dla odwrotnej notacji polskiej**
Do notacji RPN wykorzystywany jest osobny parser, w pełni kompatybliny z używanym w dalszej części zadania
```
test("2 2 + 3 *", "[('BINOP', (('BINOP', (('INT', 2), '+', ('INT', 2))), '*', ('INT', 3)))]")
OK
```

5.
**instrukcje warunkowe i pętle**
```
test("if(2>6){4+5}else{2+4}","['IF', (False, [9], [6])]")
OK
```
```
test("while(2<5){2*3}","['WHILE', (True, [6])]")
OK
```

# Pytanie 3
 Sugerowana liczba punktów za poszczególne kryteria:

1. 5

2. 5

3. 5

4. 5

5. 5

6. 5

7. 5

8. 0

9. 5

Sumaryczna sugerowana liczba punktów za to laboratorium: 40

Każdy test powinien składać się z pól: nazwa testu:, komentarz:, kod testu: czy wykonany poprawnie:, wyjście z konsoli:

Testy do poszczególnych kryteriów (do każdego kryterium może być wiele testów):

1. 
**Wizualizacja drzewa składniowego**
Test udany, przykładowe drzewo w załączniku.

Komentarz do dalszych testów:
W kolejnych testach testowany jest głównie interpreter, co wymaga zmiany formuły testu:
```python
# wejście programu
test (oczekiwany wynik, wyjście_parsera)
WYNIK
```

2.
**Deklarowanie typów dla zmiennych**
```
# int i
test(None, [('DEC', ('i', 'int', None))])
OK
# float f
test(None, [('DEC', ('f', 'float', None))])
OK
# string s
test(None, [('DEC', ('s', 'string', None))])
OK
# bool b
test(None, [('DEC', ('b', 'bool', None))])
OK
# int h;  int h
test_raises('h has already been defined', [('DEC', ('h', 'int', None)), ('DEC', ('h', 'int', None))])
OK
```
3.
**Sprawdzanie typów**
```
# int i; i = "string"
test_raises('Expected int, got string', [('DEC', ('i', 'int', None)), ('ASSIGN', ('i', ('STRING', 'string')))])
OK
# string a = "a"; string b = "b"; a-b
test_raises('- not supported on arguments of types string, string',
            [('DEC', ('a', 'string', ('STRING', 'a'))), ('DEC', ('b', 'string', ('STRING', 'b'))),
             ('BINOP', (('REF', 'a'), '-', ('REF', 'b')))])
OK
```
4.
**Instrukcja przypisania**
```
# int a = 1; a = 3; a;
test(3, [('DEC', ('a', 'int', ('INT', 1))), ('ASSIGN', ('a', ('INT', 3))), ('REF', 'a')])
OK
# string s = "test"; s
test('test', [('DEC', ('s', 'string', ('STRING', 'test'))), ('REF', 's')])
OK
# float f = 4.2; f
test(4.2, [('DEC', ('f', 'float', ('FLOAT', 4.2))), ('REF', 'f')])
OK
# bool b; b = 2 < 6; b
test(True, [('DEC', ('b', 'bool', None)), ('ASSIGN', ('b', ('REL', (('INT', 2), '<', ('INT', 6))))), ('REF', 'b')])
OK
```

5.
**Przeciążanie operatorów**
```
# string a = "a"; string b = "b"; a+b
test('ab', [('DEC', ('a', 'string', ('STRING', 'a'))), ('DEC', ('b', 'string', ('STRING', 'b'))),
            ('BINOP', (('REF', 'a'), '+', ('REF', 'b')))])OK
```
 
6. 

**Sprawdzanie syntaktyczne deklaracji zmiennych**
```
# int a = "pociąg"
test_raises('Expected int, got string', [('DEC', ('a', 'int', ('STRING', 'pociąg')))])
OK
```

7.
**Sprawdzanie syntaktyczne instrukcji**
```
# int a = trala
test_raises('trala is not defined in current scope', [('DEC', ('a', 'int', ('REF', 'trala')))])
OK
```

8.**konwersja typów za pomocą dodatkowego operatora**
<brak>

# Pytanie 4
 Sugerowana liczba punktów za poszczególne kryteria:

1. 5

2. 3

3. 5

4. 5

5. 5

Sumaryczna sugerowana liczba punktów za to laboratorium: 28

Każdy test powinien składać się z pól: nazwa testu:, komentarz:, kod testu: czy wykonany poprawnie:, wyjście z konsoli:

Testy do poszczególnych kryteriów (do każdego kryterium może być wiele testów):

**Komentarz do testów**
Analogicznie jak w zadaniach z lab3

1.**Definiowanie funkcji**
```
# int x(int g){return g^2};x(5)
test(25, [('FUNC', ('int', 'x', [('int', 'g')], [('RETURN', ('BINOP', (('REF', 'g'), '^', ('INT', 2))))])),
          ('CALL', ('x', (('INT', 5),)))])
OK
```

2.**Definiowanie bloków instrukcji**  
_bloki instrukcji traktowane są jako ciągi instrukcji i jakiekolwiek znaczenie dla zasięgu zmiennych mają nadane 
kiedy stanowią ciało funkcji lub pętli_
```
# { int a; a=5; a}
test(5, [('DEC', ('a', 'int', None)), ('ASSIGN', ('a', ('INT', 5))), ('REF', 'a')])
OK
```

3.**Definiowanie zmiennych globalnych i lokalnych**  
_Zasięgi zmiennych (scopes) wrzucane są na stos, co umożliwia na definiowanie zmiennych na wielu poziomach_
```
# string a = "global"; if (2>1) { a = "overwritten"}; a
test("overwritten", [('DEC', ('a', 'string', ('STRING', 'global'))), (
'IF', (('REL', (('INT', 2), '>', ('INT', 1))), [('ASSIGN', ('a', ('STRING', 'overwritten')))], None)), ('REF', 'a')])
OK
# string a = "global"; if (2>1) { b = "local"}; b
test_raises('b is not defined!', [('DEC', ('a', 'string', ('STRING', 'global'))), (
'IF', (('REL', (('INT', 2), '>', ('INT', 1))), [('ASSIGN', ('b', ('STRING', 'local')))], None)), ('REF', 'b')])
OK
```

4.**Instrukcja wywołania funkcji**  
```
# int add(int a, int b){return a+b}; add(12, 5)
test(17, [
    ('FUNC', ('int', 'add', [('int', 'a'), ('int', 'b')], [('RETURN', ('BINOP', (('REF', 'a'), '+', ('REF', 'b'))))])),
    ('CALL', ('add', (('INT', 12), ('INT', 5))))])
OK
```

5.**Automatyczna konwersja typów**  
```
# string a = "a"; int b = 5; a+b
test("a5", [('DEC', ('a', 'string', ('STRING', 'a'))), ('DEC', ('b', 'int', ('INT', 5))),
            ('BINOP', (('REF', 'a'), '+', ('REF', 'b')))])
OK
```

# Pytanie 5
 Sugerowana liczba punktów za poszczególne kryteria:

1. 5

2. 0

3. 0

4. 0

5. 2

Sumaryczna sugerowana liczba punktów za to laboratorium: 7

Każdy test powinien składać się z pól: nazwa testu:, komentarz:, kod testu: czy wykonany poprawnie:, wyjście z konsoli:

Testy do poszczególnych kryteriów (do każdego kryterium może być wiele testów):

**Komentarz do testów**
Analogicznie jak w zadaniach z lab3

1.**Zagnieżdżone wywołania funkcji**
```
# int x(int g){return g^2};int y(int h){return x(h)};y(5)
test(25, [('FUNC', ('int', 'x', [('int', 'g')], [('RETURN', ('BINOP', (('REF', 'g'), '^', ('INT', 2))))])),
          ('FUNC', ('int', 'y', [('int', 'h')], [('RETURN', ('CALL', ('x', (('REF', 'h'),))))])),
          ('CALL', ('y', (('INT', 5),)))])
OK
```
##2-4 \<brak\>

# Pytanie 6
 Sugerowana liczba punktów za poszczególne kryteria:

1. 5
2. 3
3. 3
4. 3
5. 3
6. 3
7. 0

Sumaryczna sugerowana liczba punktów za to laboratorium: 20
Sumaryczna sugerowana liczba punktów za wszystkie laboratoria: 155
Sugerowana ocena po przeliczeniu punktów wg skali AGH: 4.0



