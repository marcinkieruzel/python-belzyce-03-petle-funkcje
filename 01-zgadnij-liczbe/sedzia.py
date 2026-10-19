#!/usr/bin/env python3
"""Sędzia gry „Zgadnij liczbę”: gra z botem o każdą liczbę od 1 do 100 i wypisuje raport.

Jak sędzia rozmawia z botem:
  - uruchamia bota jako osobny program (python3 bot.py),
  - czyta od niego jedną linię: liczbę, którą bot zgaduje,
  - odpisuje jednym słowem: wiecej, mniej albo trafiony,
  - po „trafiony” bot ma się zakończyć.
Linie, które bot zaczyna od #, to komentarze: nie liczą się jako ruch, ale widać je
w przebiegu gry (--liczba N).

Użycie (w katalogu z ćwiczeniem):
  python3 sedzia.py                       bot.py gra o każdą liczbę od 1 do 100
  python3 sedzia.py --liczba 37           jedna gra o liczbę 37, ruch po ruchu
  python3 sedzia.py --bot inny_bot.py     inny plik z botem
  python3 sedzia.py --wbudowany losowy    dla porównania: bot wbudowany w sędziego
                                          (losowy albo liniowy)
  python3 sedzia.py --limit 7             gra przegrana, gdy bot nie trafi w 7 ruchach
  python3 sedzia.py --do 1000             liczby od 1 do 1000 (bot musi o tym wiedzieć)

Sędzia działa na Linuksie (także w WSL) i na macOS.
"""
import argparse
import os
import random
import select
import subprocess
import sys
import tempfile
import time
from pathlib import Path

CZAS_NA_START = 5.0      # sekundy na pierwszą liczbę (uruchomienie Pythona chwilę trwa)
CZAS_NA_RUCH = 2.0       # sekundy na każdą następną liczbę
LIMIT_KOMENTARZY = 1000  # tyle linii z # może wypisać bot w jednej grze
LIMIT_BLEDOW = 10        # po tylu grach z błędem sędzia przerywa


class BladBota(Exception):
    """Bot złamał zasady gry. Treść wyjątku mówi, co zrobił źle."""

    def __init__(self, opis, zawieszenie=False):
        super().__init__(opis)
        self.zawieszenie = zawieszenie
        self.przebieg = []
        self.ruch = 0


def odmien(n, jeden, kilka, wiele):
    """Polska odmiana po liczebniku: 1 ruch, 2 ruchy, 5 ruchów, 22 ruchy."""
    if n == 1:
        return jeden
    if n % 10 in (2, 3, 4) and n % 100 not in (12, 13, 14):
        return kilka
    return wiele


def ruchow(n):
    return f"{n} {odmien(n, 'ruch', 'ruchy', 'ruchów')}"


def po_polsku(x):
    """5.8 -> '5,80'."""
    return f"{x:.2f}".replace(".", ",")


# ---------------------------------------------------------------------------------------------
# Bot w osobnym procesie

class ProcesBota:
    """Bot uruchomiony jako osobny program; rozmowa przez jego wejście (stdin) i wyjście (stdout)."""

    def __init__(self, plik):
        self.plik = plik
        self.bledy = tempfile.TemporaryFile()
        srodowisko = dict(os.environ, PYTHONUNBUFFERED="1", PYTHONIOENCODING="utf-8")
        self.proces = subprocess.Popen(
            [sys.executable, "-u", str(plik)],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=self.bledy,
            cwd=str(plik.parent), env=srodowisko)
        self.bufor = b""
        self.limit = CZAS_NA_START

    def czytaj_linie(self):
        """Następna linia od bota albo None, gdy bot zakończył działanie."""
        koniec = time.monotonic() + self.limit
        while b"\n" not in self.bufor:
            zostalo = koniec - time.monotonic()
            gotowe = select.select([self.proces.stdout], [], [], zostalo)[0] if zostalo > 0 else []
            if not gotowe:
                raise BladBota(
                    f"bot nic nie wypisał przez {self.limit:.0f} s — zawiesił się. Pętla bez końca? "
                    "Albo bot czeka na drugie input(), choć sędzia odpowiada tylko raz na ruch?",
                    zawieszenie=True)
            dane = os.read(self.proces.stdout.fileno(), 4096)
            if not dane:                       # koniec wyjścia: bot się zakończył
                if self.bufor:
                    linia, self.bufor = self.bufor, b""
                    return linia.decode("utf-8", "replace")
                return None
            self.bufor += dane
        self.limit = CZAS_NA_RUCH
        linia, _, self.bufor = self.bufor.partition(b"\n")
        return linia.decode("utf-8", "replace").rstrip("\r")

    def wyslij(self, tekst):
        try:
            self.proces.stdin.write((tekst + "\n").encode())
            self.proces.stdin.flush()
        except OSError:
            pass                               # bot już się zakończył; wyjdzie to przy czytaniu

    def ostatni_blad(self):
        """Ostatnia linia z błędem, który bot wypisał (np. ValueError: ...)."""
        self.proces.wait()
        self.bledy.seek(0)
        linie = self.bledy.read().decode("utf-8", "replace").strip().splitlines()
        return linie[-1].strip() if linie else f"kod wyjścia {self.proces.returncode}"

    def koniec_przed_trafieniem(self):
        """Opis sytuacji, w której bot zakończył się, zanim usłyszał „trafiony”."""
        if self.proces.wait() == 0:
            return ("bot zakończył się, zanim usłyszał „trafiony” — poddał się albo ogłosił "
                    "zwycięstwo, którego nie było. Pętla ma się kończyć dopiero po odpowiedzi „trafiony”")
        blad = self.ostatni_blad()
        opis = f"bot zakończył się błędem: {blad}"
        if "invalid literal for int()" in blad:
            opis += (". Odpowiedź sędziego to słowo (wiecej, mniej, trafiony), a nie liczba — "
                     "nie zamieniaj jej na int()")
        else:
            opis += ". Uruchom bota samego (python3 bot.py), żeby zobaczyć cały komunikat"
        return opis

    def zakoncz(self):
        """Po „trafiony”: zamyka wejście bota i czeka, aż się zakończy. Zwraca to, co jeszcze wypisał."""
        try:
            self.proces.stdin.close()
        except OSError:
            pass
        try:
            self.proces.wait(timeout=CZAS_NA_RUCH)
        except subprocess.TimeoutExpired:
            raise BladBota("po „trafiony” bot dalej działa — powinien wyjść z pętli (break) "
                           "i zakończyć się", zawieszenie=True) from None
        reszta = (self.bufor + self.proces.stdout.read()).decode("utf-8", "replace")
        self.bufor = b""
        if self.proces.returncode != 0:
            blad = self.ostatni_blad()
            opis = f"po „trafiony” bot zakończył się błędem: {blad}"
            if "EOFError" in blad:
                opis += (". Bot czyta kolejną odpowiedź, choć gra się skończyła — "
                         "po „trafiony” wyjdź z pętli (break)")
            raise BladBota(opis)
        return reszta

    def zamknij(self):
        if self.proces.poll() is None:
            self.proces.kill()
        self.proces.wait()
        for strumien in (self.proces.stdin, self.proces.stdout, self.bledy):
            try:
                strumien.close()
            except OSError:
                pass


# ---------------------------------------------------------------------------------------------
# Boty wbudowane w sędziego — tylko dla porównania

class BotWbudowany:
    """liniowy: zgaduje po kolei 1, 2, 3, ...; losowy: losuje liczbę z przedziału, który jeszcze zostaje."""

    def __init__(self, rodzaj, gora, los):
        self.rodzaj = rodzaj
        self.dol, self.gora = 1, gora
        self.los = los
        self.strzal = None

    def czytaj_linie(self):
        if self.rodzaj == "liniowy":
            self.strzal = self.dol
        else:
            self.strzal = self.los.randint(self.dol, self.gora)
        return str(self.strzal)

    def wyslij(self, odpowiedz):
        if odpowiedz == "wiecej":
            self.dol = self.strzal + 1
        elif odpowiedz == "mniej":
            self.gora = self.strzal - 1

    def zakoncz(self):
        return ""

    def zamknij(self):
        pass


# ---------------------------------------------------------------------------------------------
# Jedna gra

def odczytaj_strzal(tekst, dol, gora, gora_zakresu, zgadniete):
    """Zamienia linię od bota na liczbę i sprawdza, czy ruch jest zgodny z zasadami."""
    if tekst == "":
        raise BladBota("bot wypisał pustą linię zamiast liczby")
    try:
        strzal = int(tekst)
    except ValueError:
        opis = f"bot wypisał „{tekst}” zamiast samej liczby"
        if any(znak.isdigit() for znak in tekst):
            opis += (". Bot może wypisywać tylko liczbę: print(strzal). Uwaga: input(\"tekst\") "
                     "też wypisuje tekst z nawiasów — w bocie pisz samo input()")
        raise BladBota(opis) from None
    if strzal < 1 or strzal > gora_zakresu:
        raise BladBota(f"bot zgaduje {strzal}, a liczba jest od 1 do {gora_zakresu}")
    if strzal in zgadniete:
        raise BladBota(f"bot zgaduje {strzal} drugi raz — tę liczbę już sprawdził. "
                       "Czy po odpowiedzi przesuwasz granicę tuż za strzał (strzal + 1, strzal - 1)?")
    if strzal < dol or strzal > gora:
        raise BladBota(f"bot zgaduje {strzal}, choć z odpowiedzi sędziego wiadomo już, że liczba "
                       f"jest od {dol} do {gora} — bot nie słucha sędziego. "
                       "Czy nie pomyliły się „wiecej” i „mniej”?")
    return strzal


def rozegraj(bot, sekret, gora_zakresu, limit_ruchow):
    """Jedna gra o liczbę `sekret`. Zwraca (liczba ruchów albo None przy przegranej, przebieg).

    Gdy bot złamie zasady, rzuca BladBota z przebiegiem gry.
    """
    dol, gora = 1, gora_zakresu
    przebieg = []
    zgadniete = set()
    komentarze = 0
    ruch = 0
    try:
        while True:
            linia = bot.czytaj_linie()
            if linia is None:
                raise BladBota(bot.koniec_przed_trafieniem())
            tekst = linia.strip()
            if tekst.startswith("#"):
                komentarze += 1
                if komentarze > LIMIT_KOMENTARZY:
                    raise BladBota("bot wypisuje bez końca komentarze (#) zamiast zgadywać")
                przebieg.append(f"           {tekst}")
                continue
            ruch += 1
            strzal = odczytaj_strzal(tekst, dol, gora, gora_zakresu, zgadniete)
            zgadniete.add(strzal)
            if strzal < sekret:
                odpowiedz = "wiecej"
                dol = strzal + 1
            elif strzal > sekret:
                odpowiedz = "mniej"
                gora = strzal - 1
            else:
                odpowiedz = "trafiony"
            opis = f"ruch {ruch:>2}: bot {strzal:>4} → sędzia: {odpowiedz:<8}"
            if odpowiedz != "trafiony":
                opis += f"  (zostaje {dol}–{gora})" if dol < gora else f"  (zostaje {dol})"
            przebieg.append(opis.rstrip())
            if odpowiedz == "trafiony":
                bot.wyslij(odpowiedz)
                for reszta in bot.zakoncz().splitlines():
                    przebieg.append(f"           {reszta.strip()}")
                return ruch, przebieg
            if ruch >= limit_ruchow:
                przebieg.append(f"limit {ruchow(limit_ruchow)} — gra przegrana")
                return None, przebieg
            bot.wyslij(odpowiedz)
    except BladBota as blad:
        blad.przebieg = przebieg
        blad.ruch = ruch
        raise
    finally:
        bot.zamknij()


# ---------------------------------------------------------------------------------------------
# Raport

def histogram(ruchy):
    """Rozkład liczby ruchów: wiersz na każdą liczbę ruchów albo przedziały po 10, gdy ruchów jest dużo."""
    najwiecej = max(ruchy)
    if najwiecej <= 15:
        przedzialy = [(n, n) for n in range(1, najwiecej + 1)]
    else:
        przedzialy = [(od, od + 9) for od in range(1, najwiecej + 1, 10)]
    wiersze = []
    for od, do in przedzialy:
        ile = sum(1 for r in ruchy if od <= r <= do)
        etykieta = ruchow(od) if od == do else f"{od}–{do} ruchów"
        wiersze.append(f"  {etykieta:<14} {'#' * ile} {ile}")
    return wiersze


def cel_dla(gora_zakresu):
    """Ile ruchów wystarcza metodą połowienia: najmniejsze k, dla którego 2^k − 1 >= liczba liczb."""
    return gora_zakresu.bit_length()


def wypisz_raport(nazwa, wyniki, bledy, przegrane, gora_zakresu, limit_ruchow):
    cel = cel_dla(gora_zakresu)
    gry = len(wyniki) + len(bledy) + len(przegrane)
    print()
    rozegrane = "" if gry == gora_zakresu else " rozegranych"
    print(f"Wygrane gry: {len(wyniki)} na {gry}{rozegrane}")
    if przegrane:
        print(f"Przegrane (limit {ruchow(limit_ruchow)}): {len(przegrane)} — liczby: {skrot(przegrane)}")
    if bledy:
        liczby = sorted(bledy)
        print(f"Gry z błędem bota: {len(bledy)} — liczby: {skrot(liczby)}")
        pierwsza = liczby[0]
        blad = bledy[pierwsza]
        print()
        print(f"Pierwszy błąd — gra o liczbę {pierwsza}, ruch {blad.ruch}:")
        print(f"  {blad}")
        if blad.przebieg:
            print("Przebieg tej gry:")
            for linia in blad.przebieg[-15:]:
                print(f"  {linia}")
        print()
        print(f"Popraw bota i sprawdź tę jedną grę: python3 sedzia.py --liczba {pierwsza}"
              + (f" --bot {nazwa}" if nazwa != "bot.py" else ""))
        return
    if not wyniki:
        return
    ruchy = list(wyniki.values())
    etykieta = "Ruchy w wygranych grach" if przegrane else "Ruchy"
    print(f"{etykieta}: najmniej {min(ruchy)}, najwięcej {max(ruchy)}, "
          f"średnio {po_polsku(sum(ruchy) / len(ruchy))}")
    print("Rozkład liczby ruchów:")
    for wiersz in histogram(ruchy):
        print(wiersz)
    if przegrane:
        return
    powyzej = [liczba for liczba, r in wyniki.items() if r > cel]
    if not powyzej:
        print(f"Cel osiągnięty: każda liczba w co najwyżej {cel} "
              f"{odmien(cel, 'ruchu', 'ruchach', 'ruchach')} "
              f"(2 do potęgi {cel} = {2 ** cel}, więc {cel} połowień wystarcza na {gora_zakresu} liczb).")
    else:
        print(f"Cel nieosiągnięty: {len(powyzej)} z {len(wyniki)} liczb wymagało więcej niż {ruchow(cel)}. "
              f"Metodą połowienia przedziału każda liczba od 1 do {gora_zakresu} "
              f"wymaga co najwyżej {ruchow(cel)}.")


def skrot(liczby, ile=12):
    liczby = sorted(liczby)
    tekst = ", ".join(str(x) for x in liczby[:ile])
    return tekst + (f" i {len(liczby) - ile} innych" if len(liczby) > ile else "")


# ---------------------------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Sędzia gry „Zgadnij liczbę”: gra z botem o liczby od 1 do 100 i wypisuje raport.")
    parser.add_argument("--bot", default=None, help="plik z botem (domyślnie bot.py obok sędziego)")
    parser.add_argument("--liczba", type=int, help="jedna gra o tę liczbę, z przebiegiem ruch po ruchu")
    parser.add_argument("--wbudowany", choices=["losowy", "liniowy"],
                        help="zamiast pliku: bot wbudowany w sędziego (dla porównania)")
    parser.add_argument("--limit", type=int, default=None,
                        help="limit ruchów w jednej grze (domyślnie tyle, ile jest liczb)")
    parser.add_argument("--do", type=int, default=100, dest="gora",
                        help="liczby od 1 do tej wartości (domyślnie 100)")
    parser.add_argument("--ziarno", type=int, default=2026, help="ziarno losowania bota losowego")
    args = parser.parse_args()

    if args.gora < 1:
        parser.error("--do musi być co najmniej 1")
    limit_ruchow = args.limit if args.limit is not None else args.gora
    if limit_ruchow < 1:
        parser.error("--limit musi być co najmniej 1")
    if args.liczba is not None and not 1 <= args.liczba <= args.gora:
        parser.error(f"--liczba musi być od 1 do {args.gora}")

    los = random.Random(args.ziarno)
    if args.wbudowany:
        nazwa = f"wbudowany bot {args.wbudowany}"

        def nowy_bot():
            return BotWbudowany(args.wbudowany, args.gora, los)
    else:
        plik = Path(args.bot) if args.bot else Path(__file__).resolve().parent / "bot.py"
        if not plik.is_file():
            print(f"Nie ma pliku z botem: {plik}")
            sys.exit(2)
        plik = plik.resolve()
        nazwa = args.bot if args.bot else "bot.py"

        def nowy_bot():
            return ProcesBota(plik)

    # --- jedna gra z przebiegiem
    if args.liczba is not None:
        print(f"Gra o liczbę {args.liczba} (od 1 do {args.gora}) — {nazwa}")
        try:
            ruchy, przebieg = rozegraj(nowy_bot(), args.liczba, args.gora, limit_ruchow)
        except BladBota as blad:
            for linia in blad.przebieg:
                print(f"  {linia}")
            print(f"BŁĄD w ruchu {blad.ruch}: {blad}")
            sys.exit(1)
        for linia in przebieg:
            print(f"  {linia}")
        if ruchy is None:
            print("Przegrana: bot nie trafił w limicie ruchów.")
            sys.exit(1)
        print(f"Trafiony w {ruchy} {odmien(ruchy, 'ruchu', 'ruchach', 'ruchach')}.")
        return

    # --- wszystkie liczby
    print(f"Sędzia gry „Zgadnij liczbę” — {nazwa}, liczby od 1 do {args.gora}")
    wyniki, bledy, przegrane = {}, {}, []
    na_ekranie = sys.stdout.isatty()
    for sekret in range(1, args.gora + 1):
        if na_ekranie:
            print(f"\rGram o liczbę {sekret}/{args.gora}...", end="", flush=True)
        try:
            ruchy, _ = rozegraj(nowy_bot(), sekret, args.gora, limit_ruchow)
        except BladBota as blad:
            bledy[sekret] = blad
            if blad.zawieszenie or len(bledy) >= LIMIT_BLEDOW:
                if na_ekranie:
                    print()
                if blad.zawieszenie:
                    print(f"Sędzia przerywa po grze o liczbę {sekret}: bot się zawiesza, "
                          "kolejne gry trwałyby za długo.")
                else:
                    print(f"Sędzia przerywa po grze o liczbę {sekret}: już {LIMIT_BLEDOW} gier z błędem.")
                break
            continue
        if ruchy is None:
            przegrane.append(sekret)
        else:
            wyniki[sekret] = ruchy
    if na_ekranie:
        print("\r" + " " * 40 + "\r", end="")
    wypisz_raport(nazwa, wyniki, bledy, przegrane, args.gora, limit_ruchow)
    sys.exit(0 if not bledy and not przegrane else 1)


if __name__ == "__main__":
    main()
