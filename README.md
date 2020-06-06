# Zadanie zaliczeniowe z kompilatorów
Autorzy: Jacek Gosztyła, Ignacy Grudziński

W głównym folderze projektu znajdują się kolejne komponenty kompilatora, przystosowane do kolejnych ćwiczeń z laboratorium. Np. `parser2.py` oznacza, że jest to parser napisany na potrzeby zadania 2 z przedmiotu kompilatory. 

## Zadanie 1 
Zostało wykonane już na zajęciach, dlatego nie przygotowaliśmy dla niego testów.

## Zadanie 2
Zrealizowane jako `parser2.py`.
W `parser_tests/lab2_test.py` napisane zostały testy to parsera. 

## Zadanie 3
Zrezalizowane jako `interpreter3.py`. 
Testy umieściliśmy na końcu powyższego pliku. 
Parser został wzbogacony o dodatkowe funkcjonalności. Testujemy je w `parser_tests/lab3_test.py`.

## Parser tester
`parser_tests/parser2_tester.py` oraz `parser_tests/parser3_tester.py` pozwalają na symulowanie wpisywania kodu na input parsera i porównywanie generowanego przez niego outputu z oczekiwanym rezultatem. Wykorzystujemy je w odpowiednio `parser_tests/lab2_test.py` oraz `parser_tests/lab3_test.py`

# kompilatory_2020
A simple language made for Compilers class with PLY.