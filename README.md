# Zadanie zaliczeniowe z kompilatorów - dokumentacja
Autorzy: Jacek Gosztyła, Ignacy Grudziński

W głównym folderze projektu znajdują się kolejne komponenty kompilatora, przystosowane do kolejnych ćwiczeń z laboratorium. Np. `parser2.py` oznacza, że jest to parser napisany na potrzeby zadania 2 z przedmiotu kompilatory. 


## Opis sposobu użycia języka kalkulatora
Kolejne instrukcje języka muszą być oddzielone średnikiem `;`. 
Kalkulator wspiera wszystkie podstawowe działania matematyczne oraz relacyjne (`2+5`, `3^7`, `4%2`, `3<4`, ... ).
Możemy korzystać z funkcji matematycznych (`sin(0.1)`, `tan(0.0)`, `exp(2.3)`, ...)
W celu zdeklarowania nowej zmiennej, należy podać jej typ, np. `int a`.
Do zmiennej możemy przypisać wartość zgodną z jej typem w momencie deklaracji `int a = 5` lub po uprzednim zdeklarowaniu `int a; a = 5`.
Zmienną możemy wykorzystywać wielokrotnie w obliczeniach. 
Powyższe instrukcje możemy wykorzystywać w blockach kodu zajdujących się pomiędzy klamrami `{}`
Instrukcja warunkowa `if` ma postać:
```
if(warunek){
    instrukcja 1;
    instrukcja 2;
    ...
}else{
    instrukcja 1;
    ...
}
```
Blok `else` jest opcjonalny. 
W kalkulatorze mamy do dyspozycji pętle `while` oraz `for`. Mają one postać:
```
while(warunek){
    instrukcje...
}
```
```
for(instrukacja poczatkowa; warunek zakonczenia; instrukcja po wykonaniu petli){
    instrukcje...
}
```
Możemy definiować własne funkcje w postaci:






## Realizacja konkretnych zadań
### Zadanie 1 
Testy do zadania w `md.py`. 

### Zadanie 2
Zrealizowane jako `parser2.py`.
W `parser_tests/lab2_test.py` napisane zostały testy to parsera. 

### Zadania 3,4,5,6
Zrealizowane jako `interpreter3.py`. 
Testy umieściliśmy na końcu powyższego pliku. 

Dodatkowo: 
- Wizualizacja drzewa składniowego w `ast.py`.
- Parser został wzbogacony o dodatkowe funkcjonalności. Testujemy je w `parser_tests/lab3_test.py`.


### Parser tester
`parser_tests/parser2_tester.py` oraz `parser_tests/parser3_tester.py` pozwalają na symulowanie wpisywania kodu na input parsera i porównywanie generowanego przez niego outputu z oczekiwanym rezultatem. Wykorzystujemy je w odpowiednio `parser_tests/lab2_test.py` oraz `parser_tests/lab3_test.py`

# kompilatory_2020
A simple language made for Compilers class with PLY.