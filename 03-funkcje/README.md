![Logotypy: Fundusze Europejskie dla Lubelskiego, Rzeczpospolita Polska, Dofinansowane przez Unię Europejską, Lubelskie](../materialy/logotypy-fe.png)

Projekt „Czas zawodowców” współfinansowany przez Unię Europejską w ramach Europejskiego Funduszu Społecznego Plus

# 03. Funkcje — notatnik

Kod z ćwiczenia 02 powtarzał się w kilku miejscach. Teraz zamkniesz go w funkcjach: z parametrami, wartościami domyślnymi, dowolną liczbą argumentów (`*args`) i wynikiem oddawanym przez `return`. Naprawisz program, który psuje się przez zasięg zmiennych, policzysz silnię rekurencyjnie i posortujesz klasę funkcją `lambda`. W notatniku [`funkcje.ipynb`](funkcje.ipynb).

**Czas:** 60–75 minut · **Dzień 2** (9.11) · czego nie zrobisz na zajęciach — dokończ w domu

## Jak otworzyć notatnik

Tak samo jak w ćwiczeniu 02: VS Code (**Select Kernel** → `.venv`) albo `jupyter notebook` w terminalu z aktywnym `.venv`. Pisz kod pod `# Twój kod`, uruchom komórkę (**Shift+Enter**) i porównaj wynik z blokiem **Oczekiwany wynik**.

Komórki uruchamiaj po kolei, od góry: późniejsze zadania korzystają z funkcji napisanych wcześniej (`srednia`, `ocena_slowna`). Po ponownym otwarciu notatnika uruchom wszystko od początku: **Run All**.

## Co jest w notatniku

| Zadanie | Co ćwiczysz |
| --- | --- |
| Ściąga | funkcje w Kotlinie, JavaScripcie i Pythonie: parametry domyślne, `vararg` a `*args`, lambdy, sortowanie, zasięg |
| 1. Ocena słowna | `def`, `return` (i dlaczego po `return` nie trzeba `elif`) |
| 2. Średnia z dowolnej liczby ocen | `*args`, `None`, rozpakowanie listy gwiazdką |
| 3. Pasek postępu | parametry domyślne, argumenty nazwane |
| 4. Napraw program: punkty gracza | zasięg zmiennych, `UnboundLocalError`, stan przez parametr i `return` zamiast `global` |
| 5. Silnia | rekurencja i pętla, wielkie liczby; 5b — ślad wywołań rekurencyjnych |
| 6. Ranking klasy | `sorted` z `key=lambda`, klucz-krotka; 6b — `max` z kluczem |
| 7. Refaktoryzacja | powtarzający się kod zamieniony na funkcje (i błąd z kopiowania, który znika) |
| Zadanie dodatkowe. Wieże Hanoi | rekurencja z trzema krokami, liczenie ruchów |

Na zajęciach celuj w zadania 1–6; 7 i wieże Hanoi dokończ, jeśli zostanie czas, albo w domu. Zadanie 4 przyda się od razu w ćwiczeniu 04.
