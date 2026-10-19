![Logotypy: Fundusze Europejskie dla Lubelskiego, Rzeczpospolita Polska, Dofinansowane przez Unię Europejską, Lubelskie](../materialy/logotypy-fe.png)

Projekt „Czas zawodowców” współfinansowany przez Unię Europejską w ramach Europejskiego Funduszu Społecznego Plus

# 04. Quiz z funkcji — menu i główna pętla

Element projektu końcowego. Zbudujesz szkielet quizu: menu tekstowe, główną pętlę programu, losowanie pytań, liczenie punktów i ranking. Każdy kawałek to osobna, mała funkcja. Strażnik `sprawdz.py` sprawdza je po kolei i mówi, co już działa, a co nie i dlaczego. Na koniec zespół przenosi quiz do swojego repozytorium, obok bazy pytań z modułu 2.

**Czas:** ok. 60 minut · **Dzień 2** (9.11)

```bash
cd ~/python-belzyce-03-petle-funkcje/04-quiz-z-funkcji
python3 sprawdz.py
```

| Plik | Co to |
| --- | --- |
| `quiz.py` | szkielet quizu: nagłówki funkcji z opisami, w środku `pass` — to piszesz ty |
| `pytania.py` | przykładowa baza 14 pytań (Python, Linux, informatyka) w formacie z modułu 2 |
| `sprawdz.py` | strażnik: sprawdza bazę pytań i każdą funkcję osobno (nie zmieniaj go) |

## Jak zbudowany jest quiz

Główna pętla programu (`main`) w kółko pokazuje menu, czyta wybór gracza i wykonuje akcję:

```text
          ( START )
              │
              ▼
      [ ranking = [] ]
              │
              ▼
   ┌─► / pokaz_menu() /
   │          │
   │          ▼
   │   / wybor = wczytaj_wybor(["1", "2", "3", "0"]) /
   │          │
   │          ▼
   │     < wybor? > ── "0" ──► / „Do zobaczenia!” / ──► ( KONIEC )
   │          │
   │          ├── "1" ──► imię, rozegraj(PYTANIA), wynik, dodaj_wynik(...)
   │          ├── "2" ──► pokaz_ranking(ranking)
   │          └── "3" ──► pokaz_zasady()
   │                         │
   └─────────────────────────┘   po opcji 1, 2 albo 3 — z powrotem do menu
```

Oznaczenia jak na diagramie przepływu z ćwiczenia 01: `( )` owal — początek i koniec, `/ /` równoległobok — wejście i wyjście, `[ ]` prostokąt — działanie, `< >` romb — decyzja.

Która funkcja korzysta z której:

```text
main
 ├── pokaz_menu ──────── ramka
 ├── wczytaj_wybor
 ├── rozegraj
 │    ├── random.sample
 │    ├── zadaj_pytanie ── wczytaj_wybor, czy_poprawna
 │    └── policz_punkty ── czy_poprawna
 ├── dodaj_wynik
 ├── pokaz_ranking
 └── pokaz_zasady
```

Dwie zasady:

- **Funkcje nie zmieniają zmiennych globalnych.** To, czego potrzebują, dostają w parametrach, a wynik oddają przez `return` (pamiętasz zadanie 4 z notatnika „Funkcje”?). Ranking żyje w zmiennej lokalnej funkcji `main`.
- **Funkcje czyste** — `czy_poprawna` i `policz_punkty` — niczego nie wypisują i o nic nie pytają. Tylko liczą. Dzięki temu łatwo je sprawdzić, a w module 4 napiszecie do nich testy.

Pytanie w bazie to słownik:

```python
{"pytanie": "Ile bitów ma bajt?", "odpowiedzi": ["4", "8", "16", "32"], "poprawna": 1, "kategoria": "informatyka"}
```

`"poprawna"` to numer odpowiedzi **liczony od 0** (tu: `"8"`). Gracz wpisuje numery od 1 do 4, więc program zamienia jego odpowiedź na numer od 0 — odejmuje 1.

## Krok 0. Strażnik

```bash
python3 sprawdz.py
```

Na razie działa tylko baza pytań, a przy każdej funkcji jest „nie działa, bo jeszcze nic nie robi”. Pisz funkcje po kolei, od góry pliku, i po każdej uruchamiaj strażnika. Strażnik wywołuje każdą funkcję osobno i zamiast gracza wpisuje przygotowane odpowiedzi.

Opis w potrójnym cudzysłowie pod `def` (*docstring*) mówi dokładnie, co funkcja ma robić. Zostaw go, a zamiast `pass` napisz ciało funkcji.

## Krok 1. `czy_poprawna(pytanie, wybor)`

Jedna linijka: porównaj `wybor` z `pytanie["poprawna"]` i zwróć wynik porównania — to już jest `True` albo `False`.

## Krok 2. `policz_punkty(pytania, wybory)`

Pętla po numerach pytań i licznik. Dla każdego numeru `i` sprawdź `czy_poprawna(pytania[i], wybory[i])`.

<details>
<summary>Podpowiedź</summary>

```python
punkty = 0
for i in range(len(pytania)):
    ...
return punkty
```

Krócej to samo zrobi `zip`, który idzie po dwóch listach naraz: `for pytanie, wybor in zip(pytania, wybory):`.
</details>

## Krok 3. `ramka(*linie, znak="#")`

`*linie` zbiera dowolnie wiele argumentów w krotkę: `ramka("Quiz")`, `ramka("QUIZ", "1) Graj", "2) Ranking")`. Funkcja **zwraca** tekst ramki, nie wypisuje go. Przykłady są w opisie funkcji.

<details>
<summary>Podpowiedź 1</summary>

Najpierw znajdź długość najdłuższej linii (pętla albo `max`). Brzeg ramki to `znak` powtórzony `szerokosc + 4` razy: po jednym znaku i jednej spacji z każdej strony.
</details>

<details>
<summary>Podpowiedź 2</summary>

Linię wyrównaną do lewej do szerokości `szerokosc` daje `linia.ljust(szerokosc)` albo f-string `f"{linia:<{szerokosc}}"`. Wiersze ramki zbierz na liście, a na końcu połącz: `"\n".join(wiersze)` — znak nowej linii między wierszami, bez nowej linii na końcu.
</details>

## Krok 4. `pokaz_menu()`

Wypisz menu w ramce: `print(ramka(...))` z tytułem quizu i czterema opcjami: `1) Graj`, `2) Ranking`, `3) Zasady`, `0) Wyjście`.

## Krok 5. `wczytaj_wybor(dozwolone, komunikat="Twój wybór: ")`

Pętla `while True`: zapytaj `input(komunikat)`, usuń spacje (`strip()`), a jeśli odpowiedź jest na liście `dozwolone` — zwróć ją. Jeśli nie — wypisz, co można wpisać, i pytaj dalej. `return` kończy funkcję, a więc i pętlę.

Parametr domyślny `komunikat` sprawia, że w menu wywołujesz po prostu `wczytaj_wybor(["1", "2", "3", "0"])`, a przy pytaniu możesz podać inny tekst: `wczytaj_wybor(["1", "2", "3", "4"], "Twoja odpowiedź: ")`.

## Krok 6. `zadaj_pytanie(pytanie)`

Wypisz kategorię i pytanie, potem ponumerowane odpowiedzi. Numer odpowiedzi wczytaj funkcją `wczytaj_wybor` — lista dozwolonych to `"1"`, `"2"`, … tyle, ile jest odpowiedzi. Sprawdź odpowiedź funkcją `czy_poprawna`, powiedz graczowi, czy dobrze, i zwróć numer odpowiedzi **liczony od 0**.

<details>
<summary>Podpowiedź 1</summary>

```python
dozwolone = []
for nr, odpowiedz in enumerate(pytanie["odpowiedzi"], start=1):
    print(f"  {nr}) {odpowiedz}")
    dozwolone.append(str(nr))
```
</details>

<details>
<summary>Podpowiedź 2</summary>

`wczytaj_wybor` zwraca tekst, np. `"2"`. Numer od 0: `int(...) - 1`. Poprawna odpowiedź jako tekst: `pytanie["odpowiedzi"][pytanie["poprawna"]]`.
</details>

## Krok 7. `rozegraj(pytania, liczba_pytan=5)`

Wylosuj pytania bez powtórzeń: `random.sample(pytania, ile)`. Zadawaj je po kolei, a odpowiedzi gracza dopisuj do listy `wybory`. Na końcu zwróć `policz_punkty(wylosowane, wybory)`.

<details>
<summary>Podpowiedź</summary>

`random.sample` kończy się błędem, gdy prosisz o więcej elementów, niż jest na liście. Dlatego `ile = min(liczba_pytan, len(pytania))`. Numer pytania przed każdym z nich: `enumerate(wylosowane, start=1)` i `print(f"Pytanie {nr}/{ile}")`.
</details>

## Krok 8. `dodaj_wynik` i `pokaz_ranking`

`dodaj_wynik(ranking, imie, punkty)` zwraca ranking z nowym wynikiem na końcu, np. `ranking + [{"imie": imie, "punkty": punkty}]`.

`pokaz_ranking(ranking, ile=5)` sortuje wyniki od największej liczby punktów i wypisuje `ile` pierwszych, z miejscem w rankingu.

<details>
<summary>Podpowiedź</summary>

```python
najlepsi = sorted(ranking, key=lambda wynik: wynik["punkty"], reverse=True)
```

`najlepsi[:ile]` to pierwsze `ile` elementów. `sorted` przy remisie zostawia kolejność z oryginalnej listy — kto zagrał wcześniej, jest wyżej.
</details>

## Krok 9. `main()` — opcje 1 i 2

Główna pętla jest prawie gotowa: menu, `match` na wyborze, zasady i wyjście. Dopisz opcje 1 (gra) i 2 (ranking) według komentarzy `TODO`. Ranking to zmienna lokalna `main`: po każdej grze zapisujesz w niej nowy ranking zwrócony przez `dodaj_wynik`.

Gotowe, gdy strażnik pisze: `Działa 12 z 12`.

## Krok 10. Zagraj

```bash
python3 quiz.py
```

Zagrajcie w kilka osób przy jednym komputerze i sprawdźcie ranking. Ranking znika po wyjściu z programu — zapisywanie go do pliku zrobicie w module 4.

## Krok 11. Przenieście quiz do repozytorium zespołu

Wasze repozytorium z modułów 1 i 2 (np. `~/quiz-o-kosmosie`) ma już `quiz/main.py` z ekranem tytułowym i losowaniem pytań oraz `quiz/pytania.py` z waszą bazą `PYTANIA`. Teraz `main.py` dostaje menu i główną pętlę z tego ćwiczenia.

1. Wybierzcie w zespole jedną wersję `quiz.py` — taką, przy której strażnik pisze `Działa 12 z 12`.
2. Jedna osoba pobiera zmiany kolegów i kopiuje `quiz.py` do repozytorium zespołu jako `quiz/main.py`:
   ```bash
   cd ~/quiz-o-kosmosie
   git pull
   cp ~/python-belzyce-03-petle-funkcje/04-quiz-z-funkcji/quiz.py quiz/main.py
   ```
   Kod z modułu 2 (losowanie rundy, klucz odpowiedzi, `random.seed(2026)`) znika — robią to teraz funkcje `rozegraj` i `zadaj_pytanie`. Gdyby coś było potrzebne, stara wersja jest w historii: `git show HEAD:quiz/main.py`.
3. `quiz/pytania.py` zostaje: to wasza baza z modułu 2, w tym samym formacie co w tym ćwiczeniu. Kto nie ma jeszcze tego pliku, kopiuje przykład: `cp ~/python-belzyce-03-petle-funkcje/04-quiz-z-funkcji/pytania.py quiz/pytania.py`. Import w `quiz/main.py` się nie zmienia: `from pytania import PYTANIA`.
4. Ekran tytułowy z modułu 1 przenieście do funkcji, np. `ekran_tytulowy()`, i wywołajcie ją na początku `main()`. Tytuł w `pokaz_menu` zmieńcie na nazwę waszego quizu.
5. Uruchomcie quiz z głównego katalogu repozytorium:
   ```bash
   python3 quiz/main.py
   ```
   Python szuka modułów w katalogu uruchamianego pliku (`quiz/`), więc `from pytania import PYTANIA` znajdzie `quiz/pytania.py`.
6. Zapiszcie i wyślijcie zmiany, a reszta zespołu je pobiera:
   ```bash
   git add quiz/main.py
   git commit -m "Menu i główna pętla quizu z funkcji"
   git push
   ```
   Pozostali: `git pull` i `python3 quiz/main.py`.

Bazę zespołu nadal sprawdza walidator z modułu 2: `python3 ~/python-belzyce-02-typy-danych/04-baza-pytan/sprawdz_baze.py .` (w katalogu repozytorium zespołu).

Zespoły, które robią grę tekstową zamiast quizu, budują to samo w katalogu `gra/`: menu (np. `1) Nowa gra`, `2) Wyniki`, `3) Zasady`, `0) Wyjście`) i główną pętlę gry z funkcji, a zagadki z modułu 2 zadają funkcją podobną do `zadaj_pytanie`. Uruchomienie: `python3 gra/main.py`.

## Dla chętnych

- **kategoria:** przed grą zapytaj, z jakiej kategorii mają być pytania (`Python`, `Linux`, `informatyka` albo wszystkie) i losuj tylko z niej,
- **czas:** zmierz czas gry (`time.time()` przed i po) i dopisz go w rankingu,
- **pomieszane odpowiedzi:** wypisuj odpowiedzi w losowej kolejności, jak w module 2 (`random.sample`) — uważaj, żeby `zadaj_pytanie` nadal zwracała numer odpowiedzi z oryginalnej listy, bo tak liczy `czy_poprawna`.
