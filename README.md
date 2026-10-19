![Logotypy: Fundusze Europejskie dla Lubelskiego, Rzeczpospolita Polska, Dofinansowane przez Unię Europejską, Lubelskie](materialy/logotypy-fe.png)

Projekt „Czas zawodowców” współfinansowany przez Unię Europejską w ramach Europejskiego Funduszu Społecznego Plus

# Moduł 3 — Instrukcje sterujące, pętle i funkcje

**Kurs „Python Developer”** · Bełżyce · zajęcia 30 października i 9 listopada 2026

Ćwiczenia do trzeciego modułu kursu. Zaplanujesz grę w pseudokodzie i na diagramie przepływu, a potem ją napiszesz. Twój bot nauczy się zgadywać każdą liczbę od 1 do 100 w najwyżej 7 ruchach. Sprawdzisz, czy w teleturnieju opłaca się zmienić drzwi, i zamkniesz powtarzający się kod w funkcjach. Na koniec zbudujesz z funkcji menu i główną pętlę quizu — element waszego projektu końcowego.

## Jak pobrać ćwiczenia

W terminalu, w katalogu domowym:

```bash
cd ~
git clone https://github.com/marcinkieruzel/python-belzyce-03-petle-funkcje.git
cd python-belzyce-03-petle-funkcje
```

Bez Gita: zielony przycisk **Code** → **Download ZIP** na stronie repozytorium, a potem rozpakuj archiwum w katalogu domowym. Polecenia w ćwiczeniach zakładają, że repozytorium leży w `~/python-belzyce-03-petle-funkcje`.

## Ćwiczenia

| Nr | Ćwiczenie | Co ćwiczysz | Czas | Dzień |
| --- | --- | --- | --- | --- |
| 01 | [Zgadnij liczbę — gra i bot](01-zgadnij-liczbe/) | pseudokod i diagram przepływu, `if` / `elif` / `else`, `while`, `break`, `continue`, pętla w pętli; bot z połowieniem przedziału i sędzia | ok. 60 min | 1 (30.10) |
| 02 | [Pętle i decyzje](02-petle-i-decyzje/) — notatnik | `for`, `while`, `range`, `enumerate`, `break`, `continue`, `for … else`, `pass`, `match`, zagnieżdżone pętle, symulacje z `random` | 60–75 min | 1 (30.10) |
| 03 | [Funkcje](03-funkcje/) — notatnik | `def`, parametry, `return`, wartości domyślne, `*args`, zasięg zmiennych, rekurencja, `lambda` przy sortowaniu | 60–75 min | 2 (9.11) |
| 04 | [Quiz z funkcji](04-quiz-z-funkcji/) — element projektu końcowego | menu tekstowe i główna pętla z funkcji, `random.sample`, ranking z `lambda`; strażnik sprawdza każdą funkcję | ok. 60 min | 2 (9.11) |

Ćwiczenia robisz po kolei. Wszystko działa w terminalu Linuksa (na zajęciach: Ubuntu) z Pythonem 3.10 lub nowszym i nie wymaga instalowania bibliotek — poza Jupyterem do notatników.

## Notatniki (ćwiczenia 02 i 03)

Notatniki uruchamiasz w środowisku wirtualnym repozytorium, tak jak w module 1:

```bash
cd ~/python-belzyce-03-petle-funkcje
python3 -m venv .venv
source .venv/bin/activate
pip install notebook ipykernel
```

- **VS Code:** otwórz folder repozytorium (`code .`), kliknij plik `.ipynb`, a w prawym górnym rogu **Select Kernel** → **Python Environments** → `.venv`. Jeśli VS Code poprosi o pakiet `ipykernel`, zgódź się.
- **Przeglądarka:** w terminalu z aktywnym `.venv` wpisz `jupyter notebook`. Serwer zatrzymasz klawiszami **Ctrl+C**.

Komórkę uruchamiasz klawiszami **Shift+Enter**. Pisz kod pod linijką `# Twój kod` i porównaj to, co wypisał program, z blokiem **Oczekiwany wynik** pod spodem.

Ćwiczenia 01 i 04 to zwykłe pliki `.py` — uruchamiasz je w terminalu poleceniem `python3`, bez `.venv`.

## Co jest w repozytorium

- `01-zgadnij-liczbe/` … `04-quiz-z-funkcji/` — ćwiczenia; każde ma własne `README.md` z instrukcją.
- `materialy/` — pliki wspólne (logotypy projektu).
- `.gitignore` — lista plików, których Git ma nie śledzić: `.venv/`, `__pycache__/`, punkty kontrolne Jupytera.
