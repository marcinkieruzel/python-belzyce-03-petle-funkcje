"""Quiz wiedzy: menu tekstowe i główna pętla zbudowane z funkcji (moduł 3, ćwiczenie 04).

Sprawdź swoje funkcje:  python3 sprawdz.py
Zagraj:                 python3 quiz.py

Funkcje piszesz po kolei, od góry. Każda ma gotowy nagłówek (def) i opis w potrójnym cudzysłowie
(docstring). Zostaw opis, a zamiast `pass` napisz ciało funkcji.

Zasada: funkcje nie zmieniają zmiennych globalnych. Wszystko, czego potrzebują, dostają w parametrach,
a wynik oddają przez return.
"""
import random

from pytania import PYTANIA

LICZBA_PYTAN = 5


# ---------------------------------------------------------------------------------------------
# Funkcje „czyste”: niczego nie wypisują i o nic nie pytają, tylko liczą i zwracają wynik.

def czy_poprawna(pytanie, wybor):
    """Zwraca True, gdy `wybor` jest poprawną odpowiedzią na `pytanie`, w przeciwnym razie False.

    `wybor` to numer odpowiedzi liczony od 0 — tak samo jak "poprawna" w słowniku pytania.
    Przykład: dla pytania z "poprawna": 1 czy_poprawna(pytanie, 1) zwraca True, a czy_poprawna(pytanie, 0) — False.
    """
    pass


def policz_punkty(pytania, wybory):
    """Zwraca liczbę poprawnych odpowiedzi.

    `pytania` to lista pytań, a `wybory` — lista odpowiedzi gracza (numery od 0) w tej samej kolejności:
    wybory[0] to odpowiedź na pytania[0], wybory[1] na pytania[1] itd. Użyj funkcji czy_poprawna.
    """
    pass


def ramka(*linie, znak="#"):
    """Zwraca tekst: podane linie w ramce ze znaku `znak`. Niczego nie wypisuje — zwraca.

    Ramka jest tak szeroka, żeby zmieściła najdłuższą linię. Między znakiem ramki a tekstem jest
    jedna spacja z każdej strony. Linie ramki są połączone znakiem nowej linii, bez nowej linii na końcu.
    Przykłady (tak wyglądają po wypisaniu przez print):

    ramka("Quiz")                         ramka("QUIZ", "1) Graj", znak="=")
        ########                              ===========
        # Quiz #                              = QUIZ    =
        ########                              = 1) Graj =
                                              ===========
    """
    pass


# ---------------------------------------------------------------------------------------------
# Funkcje, które rozmawiają z graczem: wypisują (print) i pytają (input).

def pokaz_menu():
    """Wypisuje menu główne w ramce (użyj funkcji ramka). Menu ma cztery opcje, w tej kolejności:

    1) Graj
    2) Ranking
    3) Zasady
    0) Wyjście
    """
    pass


def wczytaj_wybor(dozwolone, komunikat="Twój wybór: "):
    """Pyta gracza, dopóki nie wpisze jednej z opcji z listy `dozwolone`, i zwraca tę opcję jako tekst.

    Pyta przez input(komunikat). Spacje na początku i na końcu odpowiedzi pomija (strip).
    Po złej odpowiedzi wypisuje, co można wpisać, i pyta jeszcze raz.
    Przykład: wczytaj_wybor(["1", "2", "0"]) — gracz wpisuje "x", potem "2" — funkcja zwraca "2".
    """
    pass


def zadaj_pytanie(pytanie):
    """Zadaje jedno pytanie z bazy i zwraca numer odpowiedzi gracza liczony od 0.

    1. Wypisuje kategorię i treść pytania, np. [Linux] Jakim poleceniem...
    2. Wypisuje odpowiedzi ponumerowane od 1, każdą w osobnej linii: "1) pwd", "2) ls", ...
    3. Wczytuje numer odpowiedzi funkcją wczytaj_wybor (dozwolone: "1", "2", ... — tyle, ile jest odpowiedzi).
    4. Sprawdza odpowiedź funkcją czy_poprawna i wypisuje „Dobrze!” albo „Źle. Poprawna odpowiedź: …”.
    5. Zwraca numer odpowiedzi gracza liczony od 0 (gracz wpisał "2" — funkcja zwraca 1).
    """
    pass


def rozegraj(pytania, liczba_pytan=LICZBA_PYTAN):
    """Rozgrywa jedną grę i zwraca liczbę zdobytych punktów.

    1. Losuje liczba_pytan różnych pytań: random.sample(pytania, ile). Jeśli w bazie jest mniej pytań
       niż liczba_pytan, zadaje wszystkie (losuje tyle, ile jest).
    2. Zadaje je po kolei funkcją zadaj_pytanie, przed każdym wypisuje numer, np. „Pytanie 2/5”,
       i zbiera odpowiedzi gracza na liście wybory.
    3. Na końcu liczy punkty funkcją policz_punkty i je zwraca.
    """
    pass


def dodaj_wynik(ranking, imie, punkty):
    """Dodaje wynik gracza na koniec rankingu i zwraca ranking.

    Ranking to lista słowników, np. [{"imie": "Ola", "punkty": 4}, {"imie": "Kuba", "punkty": 5}].
    """
    pass


def pokaz_ranking(ranking, ile=5):
    """Wypisuje `ile` najlepszych wyników: miejsce, imię i punkty, od największej liczby punktów.

    Sortuj funkcją sorted z key=lambda ... Przy remisie wyżej jest ten, kto zagrał wcześniej
    (sorted tak działa sam z siebie). Gdy ranking jest pusty, wypisuje „Ranking jest pusty — zagraj pierwszy!”.
    """
    pass


def pokaz_zasady():
    """Wypisuje zasady gry. Ta funkcja jest gotowa."""
    print()
    print("ZASADY")
    print(f"- W każdej grze dostajesz {LICZBA_PYTAN} pytań wylosowanych z bazy, bez powtórzeń.")
    print("- Odpowiadasz, wpisując numer odpowiedzi.")
    print("- Za każdą dobrą odpowiedź dostajesz 1 punkt.")
    print("- Wyniki trafiają do rankingu, który trwa do wyjścia z programu.")


# ---------------------------------------------------------------------------------------------
# Główna pętla programu

def main():
    """Menu, wybór, akcja — i tak w kółko, aż gracz wybierze 0."""
    ranking = []
    while True:
        pokaz_menu()
        wybor = wczytaj_wybor(["1", "2", "3", "0"])
        match wybor:
            case "1":
                # TODO: zapytaj o imię: input("Twoje imię: ")
                #       rozegraj grę: punkty = rozegraj(PYTANIA)
                #       wypisz wynik, np. „Ola: 4/5 pkt” (ile było pytań: min(LICZBA_PYTAN, len(PYTANIA)))
                #       dodaj wynik do rankingu: ranking = dodaj_wynik(ranking, imie, punkty)
                pass
            case "2":
                # TODO: pokaż ranking
                pass
            case "3":
                pokaz_zasady()
            case "0":
                print("Do zobaczenia!")
                break
            case _:
                # Tu program trafia tylko wtedy, gdy wczytaj_wybor jeszcze nie działa.
                print("Najpierw napisz funkcje pokaz_menu i wczytaj_wybor. Sprawdź je: python3 sprawdz.py")
                break


# Dzięki temu warunkowi sprawdz.py może zaimportować funkcje z tego pliku bez uruchamiania menu.
if __name__ == "__main__":
    main()
