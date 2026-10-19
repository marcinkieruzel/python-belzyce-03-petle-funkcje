![Logotypy: Fundusze Europejskie dla Lubelskiego, Rzeczpospolita Polska, Dofinansowane przez Unię Europejską, Lubelskie](../materialy/logotypy-fe.png)

Projekt „Czas zawodowców” współfinansowany przez Unię Europejską w ramach Europejskiego Funduszu Społecznego Plus

# 02. Pętle i decyzje — notatnik

Dziennik z błędami, tabliczka mnożenia, choinka, oszczędzanie na konsolę, rzuty kośćmi i słynna zagadka z teleturnieju. W notatniku [`petle-i-decyzje.ipynb`](petle-i-decyzje.ipynb) piszesz krótkie programy z `if` / `elif` / `else`, `match`, pętlami `for` i `while`, `break`, `continue` i pętlami jedna w drugiej.

**Czas:** 60–75 minut · **Dzień 1** (30.10) · czego nie zrobisz na zajęciach — dokończ w domu

## Jak otworzyć notatnik

Potrzebne jest środowisko `.venv` w katalogu repozytorium (README repozytorium, punkt „Notatniki”).

**VS Code:** otwórz folder repozytorium (`code ~/python-belzyce-03-petle-funkcje`), kliknij plik `.ipynb`, a w prawym górnym rogu **Select Kernel** → **Python Environments** → `.venv`.

**Przeglądarka:**

```bash
cd ~/python-belzyce-03-petle-funkcje
source .venv/bin/activate
jupyter notebook
```

Każde zadanie zaczyna się poleceniem „Napisz program, który…”. Pisz kod pod linijką `# Twój kod`, uruchom komórkę (**Shift+Enter**) i porównaj to, co wypisał program, z blokiem **Oczekiwany wynik** pod spodem. Wynik ma się zgadzać co do znaku.

## Co jest w notatniku

| Zadanie | Co ćwiczysz |
| --- | --- |
| Ściąga | Kotlin, JavaScript i Python obok siebie: `if`/`elif`, `when` a `match`, `range`, `enumerate`, `for … else`, `pass` |
| 1. Średnia ocen | `continue` dla ocen spoza skali, `if` / `elif` / `else` dla oceny słownej |
| 2. Napraw program: punkty na oceny | kolejność warunków w `elif`, `break` a `continue` |
| 3. Pierwsza jedynka | pętla w pętli, `break`, `else` przy pętli `for` |
| 4. Tabliczka mnożenia | pętla w pętli, f-stringi z szerokością, `print(..., end="")` |
| 5. Choinka z bombkami | trzy pętle jedna w drugiej, budowanie tekstu znak po znaku |
| 6. Oszczędzam na konsolę | `while`, gdy nie wiadomo z góry, ile będzie obrotów |
| 7. Bełż-yce | warunki z `%`; 7b — to samo z `match` na krotce |
| 8. Dwie kości | `random.seed`, słownik jako licznik, histogram; 8b — histogram pionowy |
| 9. Monty Hall | symulacja 10 000 gier i własny wniosek |

Zadania rób po kolei. Na zajęciach celuj w zadania 1–6; 7–9 dokończ, jeśli zostanie czas, albo w domu.
