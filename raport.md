# Pytanie 1
Sugerowana liczba punktów za poszczególne kryteria:

1. 5

2. 5

3. 5

4. 5

5. 5

6. 5

7. 5

Sumaryczna sugerowana liczba punktów za to laboratorium: 35

Każdy test powinien składać się z pól: nazwa testu:, komentarz:, kod testu: czy wykonany poprawnie:, wyjście z konsoli:

Testy do poszczególnych kryteriów (do każdego kryterium może być wiele testów):

###

Zadanie wykonane na zajęciach. 

 # Pytanie 2
 Sugerowana liczba punktów za poszczególne kryteria:

1. 5

2. 5

3. 5

4. 5

5. 5

Sumaryczna sugerowana liczba punktów za to laboratorium: 25

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

4.

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



