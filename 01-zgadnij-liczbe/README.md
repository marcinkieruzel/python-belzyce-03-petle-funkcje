![Logotypy: Fundusze Europejskie dla Lubelskiego, Rzeczpospolita Polska, Dofinansowane przez Unię Europejską, Lubelskie](../materialy/logotypy-fe.png)

Projekt „Czas zawodowców” współfinansowany przez Unię Europejską w ramach Europejskiego Funduszu Społecznego Plus

# 01. Zgadnij liczbę — gra i bot

Komputer myśli o liczbie od 1 do 100, a ty zgadujesz. Po każdej próbie słyszysz „za mało” albo „za dużo”. Najpierw zaplanujesz grę na kartce, potem ją napiszesz. Na koniec zamienicie się rolami: to twój program będzie zgadywał, a sędzia sprawdzi, czy zgaduje sprytnie. Jest sposób, żeby każdą liczbę od 1 do 100 trafić w najwyżej 7 próbach — znajdziesz go?

**Czas:** ok. 60 minut (część A: 30–35 min, część B: 25–30 min) · **Dzień 1** (30.10)

```bash
cd ~/python-belzyce-03-petle-funkcje/01-zgadnij-liczbe
```

| Plik | Co to |
| --- | --- |
| `pseudokod.txt` | plan gry do uzupełnienia |
| `gra.py` | szkielet gry z komentarzami `TODO` |
| `bot.py` | bot, który sam zgaduje liczby — na razie bardzo wolno |
| `sedzia.py` | gotowy sędzia: gra z botem o każdą liczbę od 1 do 100 i wypisuje raport (nie zmieniaj go) |

## Część A. Gra dla człowieka

### Krok 1. Najpierw plan: pseudokod

Programista, zanim zacznie pisać, planuje. Otwórz `pseudokod.txt` (`code pseudokod.txt`) i uzupełnij miejsca z kropkami. Pisz zwykłymi zdaniami po polsku, bez składni Pythona. Plan ma odpowiedzieć na pytania:

- co się dzieje, gdy gracz wpisze „siedem” zamiast 7?
- czy taka pomyłka liczy się jako próba?
- kiedy kończy się jedna gra, a kiedy cały program?

### Krok 2. Diagram przepływu na kartce

Narysuj ten sam algorytm jako diagram przepływu. Kształty bloków są opisane na końcu `pseudokod.txt`: owal (start, koniec), równoległobok (wczytaj, wypisz), prostokąt (działanie), romb (pytanie TAK/NIE). Pętla to strzałka, która wraca w górę diagramu. Pokaż diagram koledze z ławki: czy umie według niego zagrać?

### Krok 3. Program

Otwórz `gra.py` i wykonaj po kolei komentarze `TODO 1` … `TODO 6`. Po każdym kroku uruchom grę:

```bash
python3 gra.py
```

Grę przerywasz klawiszami **Ctrl+C**. Gotowa gra wygląda mniej więcej tak:

```text
=== ZGADNIJ LICZBĘ ===
Myślę o liczbie od 1 do 100. Spróbuj ją zgadnąć!
Twoja liczba: 50
Za mało!
Twoja liczba: siedem
To nie jest liczba.
Twoja liczba: 75
Za dużo!
Twoja liczba: 150
Poza zakresem — liczba jest od 1 do 100.
Twoja liczba: 62
Za mało!
Twoja liczba: 68
Za mało!
Twoja liczba: 72
Za dużo!
Twoja liczba: 70
Trafiony! To była liczba 70. Liczba prób: 6.
Jeszcze raz? (t/n): n
Dzięki za grę!
```

Zauważ: „siedem” i 150 nie liczą się jako próby.

<details>
<summary>Podpowiedź 1</summary>

`tekst.isdigit()` zwraca `True`, gdy tekst składa się z samych cyfr. Odwrotny warunek: `if not tekst.isdigit():`. Sprawdzenie musi być **przed** `int(tekst)` — inaczej `int("siedem")` zakończy program błędem `ValueError`.
</details>

<details>
<summary>Podpowiedź 2</summary>

`continue` wraca od razu na początek pętli `while`, więc linijki pod nim się nie wykonają — także `proby += 1`. Dlatego licznik prób zwiększasz dopiero po obu sprawdzeniach (cyfry i zakres). Porównanie z sekretem to `if` / `elif` / `else` z trzema przypadkami, a w ostatnim — `break`.
</details>

<details>
<summary>Podpowiedź 3</summary>

Zewnętrzna pętla (TODO 6): zaznacz w VS Code wszystko od `sekret = …` do końca pliku i naciśnij **Tab** — cały blok przesunie się o jedno wcięcie. Nad nim dopisz `while True:`, a na końcu, już po wewnętrznej pętli (z wcięciem zewnętrznej):

```python
    odpowiedz = input("Jeszcze raz? (t/n): ").strip().lower()
    if odpowiedz != "t":
        break
```

`break` przerywa tylko tę pętlę, w której stoi — ten z wewnętrznej kończy jedną grę, ten z zewnętrznej cały program. `sekret` i `proby` muszą się ustawiać na początku każdej gry, czyli wewnątrz zewnętrznej pętli.
</details>

**Dla chętnych:**

- **rekord:** po każdej grze wypisz najmniejszą liczbę prób ze wszystkich dotychczasowych gier,
- **limit prób:** po 7 nieudanych próbach gra się kończy: „Przegrana! To była liczba …”,
- **poziomy trudności:** na początku gry `match` na wyborze gracza: łatwy (1–10), średni (1–100), trudny (1–1000),
- **ciepło–zimno:** gdy różnica od sekretu jest mniejsza niż 5, zamiast „Za mało!” wypisz „Za mało, ale gorąco!”.

## Część B. Bot, który zgaduje sam

Teraz role się odwracają: liczbę wymyśla sędzia, a zgaduje program — `bot.py`. Bot rozmawia z sędzią dokładnie tak jak gracz z grą w części A, tylko zamiast klawiatury i ekranu jest drugi program:

- bot wypisuje liczbę: `print(strzal)`,
- czyta odpowiedź sędziego: `odpowiedz = input()` — jedno ze słów `wiecej`, `mniej`, `trafiony` (bez polskich znaków),
- po `trafiony` kończy pracę.

Sędzia uruchamia bota osobno dla każdej liczby od 1 do 100 i liczy ruchy.

### Krok 4. Uruchom sędziego

Bot z repozytorium już działa — zgaduje po kolei 1, 2, 3, … Zobacz, jak mu idzie:

```bash
python3 sedzia.py --liczba 37
python3 sedzia.py
```

Pierwsze polecenie to jedna gra o liczbę 37, ruch po ruchu. Drugie — wszystkie liczby od 1 do 100 i raport: ile ruchów najmniej, najwięcej, średnio, i rozkład. Bot wygrywa każdą grę, ale potrzebuje średnio 50,5 ruchu, a najgorzej — 100. Cel to **każda liczba w co najwyżej 7 ruchach**.

Dla porównania sędzia ma też wbudowanego bota, który zgaduje losowo, ale tylko spośród liczb, które jeszcze wchodzą w grę:

```bash
python3 sedzia.py --wbudowany losowy
```

Lepiej niż po kolei, ale do celu daleko.

### Krok 5. Połowienie przedziału

Wykonaj `TODO 1` … `TODO 3` w `bot.py`. Pomysł: bot pamięta przedział, w którym na pewno jest liczba (na początku od 1 do 100), i zawsze strzela w jego środek. Każda odpowiedź „wiecej” albo „mniej” wyrzuca połowę przedziału.

Sprawdzaj bota często, na jednej liczbie:

```bash
python3 sedzia.py --liczba 37
```

Gdy bot łamie zasady (zgaduje liczbę, którą już wykluczył, zgaduje drugi raz to samo, wypisuje coś innego niż liczba, zawiesza się), sędzia przerywa grę i mówi, co poszło nie tak. Możesz też sam być sędzią: `python3 bot.py` i odpowiadaj `wiecej`, `mniej` albo `trafiony`.

Na koniec — wszystkie liczby: `python3 sedzia.py`. Gotowe, gdy raport kończy się linijką `Cel osiągnięty`.

<details>
<summary>Podpowiedź 1</summary>

Zamiast `strzal = 1` na początku programu ustaw `dol = 1` i `gora = 100`. W pętli, przed `print`, licz środek: `strzal = (dol + gora) // 2` — dzielenie całkowite, bo strzał musi być liczbą całkowitą.
</details>

<details>
<summary>Podpowiedź 2</summary>

„wiecej” znaczy: liczba jest większa niż `strzal`, więc najmniejsza możliwa to `strzal + 1` — przesuwasz `dol`. „mniej” — największa możliwa to `strzal - 1`, przesuwasz `gora`. Linijka `strzal = strzal + 1` nie jest już potrzebna.
</details>

<details>
<summary>Podpowiedź 3</summary>

Sędzia mówi, że bot „zgaduje drugi raz” tę samą liczbę? Pewnie przesuwasz granicę na `strzal`, a nie tuż za niego: `dol = strzal` zamiast `dol = strzal + 1`. Wtedy przy przedziale 99–100 bot w kółko strzela w 99. Chcesz podejrzeć, co bot myśli? Wypisz komentarz — linie zaczynające się od `#` sędzia pomija, a pokazuje je w przebiegu gry z `--liczba`:

```python
print("# szukam od", dol, "do", gora)
```
</details>

## Do przemyślenia

1. Dlaczego akurat 7 ruchów? Zapisz, ile liczb zostaje w grze po każdym ruchu bota w najgorszym przypadku: 100 → 50 → … Ile ruchów to za mało?
2. Ile ruchów potrzeba na liczby od 1 do 1000? A od 1 do miliona? Sprawdź swoją odpowiedź: ustaw w bocie `gora = 1000` i uruchom `python3 sedzia.py --do 1000` (to potrwa kilkanaście sekund).
3. Bot średnio potrzebuje 5,8 ruchu. Czy jakiś bot mógłby mieć średnią mniejszą, nie przekraczając 7 ruchów?
4. Gdzie w życiu przydaje się połowienie? Pomyśl o słowniku papierowym, o szukaniu w posortowanej liście albo o `git bisect`, który szuka commita, w którym pojawił się błąd.
