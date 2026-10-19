#!/usr/bin/env python3
"""Strażnik quizu: sprawdza bazę pytań (pytania.py) i po kolei każdą funkcję z quiz.py.

Uruchom po każdej napisanej funkcji:
  python3 sprawdz.py

Strażnik niczego nie zmienia w twoich plikach. Wywołuje każdą funkcję osobno: zamiast klawiatury
podaje jej przygotowane odpowiedzi, a to, co funkcja wypisze, czyta sam.
"""
import ast
import builtins
import contextlib
import io
import random
import signal
import sys
import traceback
from pathlib import Path

TUTAJ = Path(__file__).resolve().parent
PLIK_QUIZU = TUTAJ / "quiz.py"
sys.path.insert(0, str(TUTAJ))
LIMIT_CZASU = 3          # sekundy na jedno wywołanie funkcji
KROKI = {                # nazwa funkcji -> krok w README
    "czy_poprawna": 1, "policz_punkty": 2, "ramka": 3, "pokaz_menu": 4, "wczytaj_wybor": 5,
    "zadaj_pytanie": 6, "rozegraj": 7, "dodaj_wynik": 8, "pokaz_ranking": 8, "main": 9,
}

# Pytania tylko do sprawdzania funkcji — odpowiedzi to słowa, które nie zawierają się w sobie nawzajem.
TESTOWE = [
    {"pytanie": "Pytanie testowe A?", "odpowiedzi": ["jabłko", "gruszka", "śliwka"], "poprawna": 0, "kategoria": "test"},
    {"pytanie": "Pytanie testowe B?", "odpowiedzi": ["czerwony", "zielony"], "poprawna": 1, "kategoria": "test"},
    {"pytanie": "Pytanie testowe C?", "odpowiedzi": ["Wisła", "Odra", "Warta", "Bug"], "poprawna": 3, "kategoria": "test"},
    {"pytanie": "Pytanie testowe D?", "odpowiedzi": ["Kraków", "Lublin"], "poprawna": 0, "kategoria": "test"},
    {"pytanie": "Pytanie testowe E?", "odpowiedzi": ["kot", "pies", "chomik"], "poprawna": 2, "kategoria": "test"},
    {"pytanie": "Pytanie testowe F?", "odpowiedzi": ["lato", "zima"], "poprawna": 0, "kategoria": "test"},
]


class NieDziala(Exception):
    """Funkcja nie działa — treść mówi dlaczego."""


class BrakDanych(Exception):
    pass


class CzasMinal(Exception):
    pass


class Wynik:
    """Co się stało podczas wywołania funkcji."""

    def __init__(self):
        self.wartosc = None
        self.wypisane = ""
        self.zapytania = []      # teksty przekazane do input()
        self.granice = []        # długość wypisanego tekstu przy każdym input()
        self.wyjatek = None
        self.brak_danych = False
        self.czas_minal = False
        self.pozostale = []
        self.dane_wejsciowe = []


def wywolaj(funkcja, *argumenty, wejscie=(), **nazwane):
    """Wywołuje funkcję z podmienionym input() i przechwyconym print()."""
    w = Wynik()
    dane = list(wejscie)
    w.dane_wejsciowe = list(wejscie)
    bufor = io.StringIO()

    def falszywy_input(komunikat=""):
        w.granice.append(len(bufor.getvalue()))
        w.zapytania.append(str(komunikat))
        bufor.write(str(komunikat))
        if not dane:
            raise BrakDanych()
        odpowiedz = dane.pop(0)
        bufor.write(odpowiedz + "\n")          # jak echo w terminalu
        return odpowiedz

    def koniec_czasu(*_):
        raise CzasMinal()

    stary_input = builtins.input
    builtins.input = falszywy_input
    zegar = hasattr(signal, "setitimer")
    if zegar:
        signal.signal(signal.SIGALRM, koniec_czasu)
        signal.setitimer(signal.ITIMER_REAL, LIMIT_CZASU)
    try:
        with contextlib.redirect_stdout(bufor):
            w.wartosc = funkcja(*argumenty, **nazwane)
    except BrakDanych:
        w.brak_danych = True
    except CzasMinal:
        w.czas_minal = True
    except (Exception, SystemExit) as e:
        w.wyjatek = e
    finally:
        if zegar:
            signal.setitimer(signal.ITIMER_REAL, 0)
        builtins.input = stary_input
    w.wypisane = bufor.getvalue()
    w.pozostale = dane
    return w


def opis_wyjatku(e):
    """Np. „NameError: name 'x' is not defined (quiz.py, linia 42)”."""
    if isinstance(e, SystemExit):
        return "wywołuje exit() — funkcja ma się kończyć przez return, a pętla przez break"
    linia = ""
    for ramka_tb in traceback.extract_tb(e.__traceback__):
        if Path(ramka_tb.filename).name == "quiz.py":
            linia = f" (quiz.py, linia {ramka_tb.lineno})"
    return f"kończy się błędem {type(e).__name__}: {e}{linia}"


def wymagaj(w, nazwa, wywolanie, moze_pytac=False, moze_wypisywac=True):
    """Wspólne sprawdzenia po wywołaniu: pusta funkcja, wyjątek, zawieszenie, nadmiarowe input()."""
    if w.czas_minal:
        raise NieDziala(f"{wywolanie} nie kończy się przez {LIMIT_CZASU} s — pętla bez końca?")
    if w.wyjatek is not None:
        raise NieDziala(f"{wywolanie} {opis_wyjatku(w.wyjatek)}")
    if w.brak_danych and not moze_pytac:
        raise NieDziala(f"{nazwa} pyta gracza o dane (input), a nie powinna")
    if w.brak_danych:
        raise NieDziala(f"{wywolanie} pyta o dane więcej razy, niż powinna. Gracz wpisał kolejno: "
                        + ", ".join(repr(z) for z in w.dane_wejsciowe) + " — po dobrej odpowiedzi trzeba skończyć")
    if w.wartosc is None and w.wypisane == "" and not w.zapytania:
        raise NieDziala("jeszcze nic nie robi (w środku jest tylko pass?)")
    if not moze_wypisywac and w.wypisane:
        raise NieDziala(f"{wywolanie} coś wypisuje ({w.wypisane.strip()[:60]!r}) — ta funkcja ma tylko "
                        "zwrócić wynik, bez print")


def wywolaj_i_wymagaj(funkcja, *argumenty, wejscie=(), moze_pytac=False, moze_wypisywac=True, **nazwane):
    w = wywolaj(funkcja, *argumenty, wejscie=wejscie, **nazwane)
    czesci = [repr(a) for a in argumenty] + [f"{k}={v!r}" for k, v in nazwane.items()]
    wywolanie = f"{funkcja.__name__}({', '.join(czesci)})"
    if len(wywolanie) > 70:
        wywolanie = f"{funkcja.__name__}(...)"
    wymagaj(w, funkcja.__name__, wywolanie, moze_pytac, moze_wypisywac)
    return w, wywolanie


def kopia(pytania):
    return [dict(p, odpowiedzi=list(p["odpowiedzi"])) for p in pytania]


# ---------------------------------------------------------------------------------------------
# Sprawdzenia po kolei

def sprawdz_baze():
    import pytania
    baza = getattr(pytania, "PYTANIA", None)
    if not isinstance(baza, list):
        raise NieDziala("w pytania.py nie ma listy PYTANIA")
    if len(baza) < 5:
        raise NieDziala(f"w bazie jest tylko {len(baza)} pytań — dodaj co najmniej 5 (tyle trwa jedna gra)")
    tresci = set()
    kategorie = {}
    for nr, p in enumerate(baza, start=1):
        if not isinstance(p, dict):
            raise NieDziala(f"pytanie {nr} nie jest słownikiem")
        for klucz in ("pytanie", "odpowiedzi", "poprawna", "kategoria"):
            if klucz not in p:
                raise NieDziala(f"pytanie {nr} nie ma klucza \"{klucz}\" (format: zob. opis na górze pytania.py)")
        if not isinstance(p["pytanie"], str) or not p["pytanie"].strip():
            raise NieDziala(f"pytanie {nr}: \"pytanie\" ma być niepustym tekstem")
        if p["pytanie"] in tresci:
            raise NieDziala(f"pytanie {nr} jest w bazie drugi raz: {p['pytanie']!r}")
        tresci.add(p["pytanie"])
        odp = p["odpowiedzi"]
        if not isinstance(odp, list) or not all(isinstance(o, str) and o.strip() for o in odp):
            raise NieDziala(f"pytanie {nr}: \"odpowiedzi\" ma być listą tekstów")
        if len(odp) != 4:
            raise NieDziala(f"pytanie {nr} ma {len(odp)} odpowiedzi, a każde pytanie ma mieć dokładnie 4 "
                            "(format z modułu 2: gracz wpisuje 1–4)")
        if len(set(odp)) != len(odp):
            raise NieDziala(f"pytanie {nr}: odpowiedzi się powtarzają")
        pop = p["poprawna"]
        if isinstance(pop, bool) or not isinstance(pop, int):
            raise NieDziala(f"pytanie {nr}: \"poprawna\" ma być liczbą całkowitą (numer odpowiedzi od 0), "
                            f"a jest {pop!r}")
        if not 0 <= pop < len(odp):
            raise NieDziala(f"pytanie {nr}: \"poprawna\" = {pop}, a odpowiedzi są {len(odp)}, więc numery od 0 "
                            f"do {len(odp) - 1} — pamiętaj, że liczymy od 0")
        if not isinstance(p["kategoria"], str) or not p["kategoria"].strip():
            raise NieDziala(f"pytanie {nr}: \"kategoria\" ma być niepustym tekstem")
        kategorie[p["kategoria"]] = kategorie.get(p["kategoria"], 0) + 1
    opis = ", ".join(f"{k} {n}" for k, n in kategorie.items())
    return f"{len(baza)} pytań ({opis})"


def sprawdz_czy_poprawna(quiz):
    p = TESTOWE[2]                                   # poprawna: 3 (Bug)
    w, wyw = wywolaj_i_wymagaj(quiz.czy_poprawna, p, 3, moze_wypisywac=False)
    if not isinstance(w.wartosc, bool):
        raise NieDziala(f"{wyw} zwraca {w.wartosc!r} — ma zwrócić True albo False")
    if w.wartosc is not True:
        raise NieDziala("dla pytania z \"poprawna\": 3 i wyboru 3 zwraca False. Wybór to numer liczony od 0, "
                        "tak samo jak \"poprawna\" — porównaj je bez dodawania i odejmowania")
    for wybor in (0, 2, 4):
        w, wyw = wywolaj_i_wymagaj(quiz.czy_poprawna, p, wybor, moze_wypisywac=False)
        if w.wartosc is not False:
            raise NieDziala(f"dla pytania z \"poprawna\": 3 i wyboru {wybor} zwraca {w.wartosc!r}, a powinna False")


def sprawdz_policz_punkty(quiz):
    pyt = kopia(TESTOWE[:4])                         # poprawne: 0, 1, 3, 0
    for wybory, oczekiwane in (([0, 1, 3, 0], 4), ([1, 1, 0, 0], 2), ([2, 0, 0, 1], 0), ([0, 0, 0, 0], 2)):
        w, wyw = wywolaj_i_wymagaj(quiz.policz_punkty, pyt, wybory, moze_wypisywac=False)
        if isinstance(w.wartosc, bool) or w.wartosc != oczekiwane:
            raise NieDziala(f"dla 4 pytań (poprawne odpowiedzi: 0, 1, 3, 0) i wyborów {wybory} "
                            f"zwraca {w.wartosc!r}, a powinna {oczekiwane}")
    w = wywolaj(quiz.policz_punkty, [], [])
    if w.wyjatek is not None or w.wartosc != 0:
        raise NieDziala(f"dla pustych list zwraca {w.wartosc!r}"
                        + (f" i {opis_wyjatku(w.wyjatek)}" if w.wyjatek else "") + ", a powinna 0")


def wzor_ramki(*linie, znak="#"):
    szer = max(len(x) for x in linie)
    brzeg = znak * (szer + 4)
    return "\n".join([brzeg] + [f"{znak} {x.ljust(szer)} {znak}" for x in linie] + [brzeg])


def sprawdz_ramka(quiz):
    for linie, nazwane in ((("Quiz",), {}), (("QUIZ", "1) Graj"), {"znak": "="}),
                           (("a", "dłuższa linia", ""), {})):
        w = wywolaj(quiz.ramka, *linie, **nazwane)
        czesci = [repr(x) for x in linie] + [f"{k}={v!r}" for k, v in nazwane.items()]
        wyw = f"ramka({', '.join(czesci)})"
        if w.wartosc is None and w.wypisane and w.wyjatek is None:
            raise NieDziala(f"{wyw} wypisuje ramkę, a ma ją zwrócić (return) — wypisze ją dopiero ten, kto wywoła ramka")
        wymagaj(w, "ramka", wyw, moze_wypisywac=False)
        oczekiwany = wzor_ramki(*linie, **nazwane)
        if not isinstance(w.wartosc, str):
            raise NieDziala(f"{wyw} zwraca {w.wartosc!r} — ma zwrócić tekst")
        if w.wartosc != oczekiwany:
            szczegoly = ("\n      oczekiwany wynik:\n" + "\n".join("        |" + x + "|" for x in oczekiwany.split("\n"))
                         + "\n      twój wynik:\n" + "\n".join("        |" + x + "|" for x in w.wartosc.split("\n")))
            if w.wartosc.endswith("\n"):
                szczegoly += "\n      (na końcu jest zbędny znak nowej linii)"
            raise NieDziala(f"{wyw} zwraca inną ramkę niż trzeba (kreski | pokazują początek i koniec linii):{szczegoly}")


def sprawdz_pokaz_menu(quiz):
    w, wyw = wywolaj_i_wymagaj(quiz.pokaz_menu)
    if w.zapytania:
        raise NieDziala("pokaz_menu ma tylko wypisać menu — o wybór pyta wczytaj_wybor")
    pozycja = -1
    for opcja in ("1) Graj", "2) Ranking", "3) Zasady", "0) Wyjście"):
        if opcja not in w.wypisane:
            raise NieDziala(f"w menu brakuje opcji „{opcja}”")
        if w.wypisane.index(opcja) < pozycja:
            raise NieDziala("opcje menu są w złej kolejności (ma być 1, 2, 3, 0)")
        pozycja = w.wypisane.index(opcja)


def sprawdz_wczytaj_wybor(quiz):
    dozwolone = ["1", "2", "0"]
    w, wyw = wywolaj_i_wymagaj(quiz.wczytaj_wybor, list(dozwolone), wejscie=["2"], moze_pytac=True)
    if not w.zapytania:
        raise NieDziala("nie pyta gracza (input)")
    if w.wartosc == 2:
        raise NieDziala(f"{wyw} zwraca liczbę 2 — ma zwrócić tekst \"2\" (bez int)")
    if w.wartosc != "2":
        raise NieDziala(f"gracz wpisał 2, a {wyw} zwraca {w.wartosc!r}")
    if w.zapytania[0] != "Twój wybór: ":
        raise NieDziala(f"pyta tekstem {w.zapytania[0]!r} zamiast komunikatu — input(komunikat)")
    zle = ["x", "", "5", " 0 "]
    w, wyw = wywolaj_i_wymagaj(quiz.wczytaj_wybor, list(dozwolone), wejscie=zle, moze_pytac=True)
    if w.wartosc != "0":
        raise NieDziala(f"gracz wpisał kolejno 'x', '', '5', ' 0 ', a funkcja zwraca {w.wartosc!r} zamiast '0' "
                        "(spacje usuwa strip; złe odpowiedzi — pytaj jeszcze raz w pętli)")
    if len(w.zapytania) != 4:
        raise NieDziala(f"przy 3 złych odpowiedziach i jednej dobrej pyta {len(w.zapytania)} razy zamiast 4")
    bez_zapytan = w.wypisane
    for z, o in zip(w.zapytania, zle):
        bez_zapytan = bez_zapytan.replace(z + o + "\n", "", 1)
    if not bez_zapytan.strip():
        raise NieDziala("po złej odpowiedzi nic nie wypisuje — powiedz graczowi, co może wpisać")
    w, wyw = wywolaj_i_wymagaj(quiz.wczytaj_wybor, ["1", "2"], "Odpowiedź: ", wejscie=["1"], moze_pytac=True)
    if not w.zapytania or w.zapytania[0] != "Odpowiedź: ":
        raise NieDziala("nie korzysta z parametru komunikat — pytaj przez input(komunikat)")


def sprawdz_zadaj_pytanie(quiz):
    p = kopia([TESTOWE[2]])[0]                       # 4 odpowiedzi, poprawna: 3 (Bug)
    w, wyw = wywolaj_i_wymagaj(quiz.zadaj_pytanie, p, wejscie=["4"], moze_pytac=True)
    if p["pytanie"] not in w.wypisane:
        raise NieDziala("nie wypisuje treści pytania")
    for nr, odp in enumerate(p["odpowiedzi"], start=1):
        if f"{nr}) {odp}" not in w.wypisane:
            raise NieDziala(f"nie wypisuje odpowiedzi w postaci „{nr}) {odp}” (numery od 1)")
    if w.wartosc is True or w.wartosc is False:
        raise NieDziala("zwraca True/False — ma zwrócić numer odpowiedzi gracza liczony od 0 "
                        "(czy to dobra odpowiedź, sprawdza czy_poprawna)")
    if isinstance(w.wartosc, str):
        raise NieDziala(f"gracz wpisał 4, a funkcja zwraca tekst {w.wartosc!r} — zamień go na liczbę (int) i odejmij 1")
    if w.wartosc == 4:
        raise NieDziala("gracz wpisał 4, a funkcja zwraca 4 — ma zwrócić numer liczony od 0, czyli 3 (odejmij 1)")
    if w.wartosc != 3:
        raise NieDziala(f"gracz wpisał 4, a funkcja zwraca {w.wartosc!r} zamiast 3")
    dobrze = w.wypisane
    w, wyw = wywolaj_i_wymagaj(quiz.zadaj_pytanie, p, wejscie=["1"], moze_pytac=True)
    if w.wartosc != 0:
        raise NieDziala(f"gracz wpisał 1, a funkcja zwraca {w.wartosc!r} zamiast 0")
    if w.wypisane.count("Bug") < 2:
        raise NieDziala("po złej odpowiedzi nie wypisuje poprawnej odpowiedzi")
    if dobrze.replace("4\n", "") == w.wypisane.replace("1\n", ""):
        raise NieDziala("po dobrej i złej odpowiedzi wypisuje to samo — powiedz graczowi, czy odpowiedział dobrze")
    w, wyw = wywolaj_i_wymagaj(quiz.zadaj_pytanie, p, wejscie=["7", "abc", "0", "2"], moze_pytac=True)
    if w.wartosc != 1:
        raise NieDziala("gracz wpisał kolejno 7, abc, 0 i 2 — funkcja powinna pytać, aż dostanie numer od 1 do 4, "
                        f"i zwrócić 1, a zwraca {w.wartosc!r} (użyj wczytaj_wybor)")


def zadane(wypisane, baza):
    return [p for p in baza if p["pytanie"] in wypisane]


def uzywa(funkcja_nazwa, wywolywana):
    """Czy w ciele funkcji `funkcja_nazwa` w quiz.py jest wywołanie `wywolywana(...)`."""
    drzewo = ast.parse(PLIK_QUIZU.read_text(encoding="utf-8"))
    for wezel in ast.walk(drzewo):
        if isinstance(wezel, ast.FunctionDef) and wezel.name == funkcja_nazwa:
            for w in ast.walk(wezel):
                if isinstance(w, ast.Call) and isinstance(w.func, ast.Name) and w.func.id == wywolywana:
                    return True
    return False


def sprawdz_rozegraj(quiz):
    baza = kopia(TESTOWE)
    random.seed(3)
    w, wyw = wywolaj_i_wymagaj(quiz.rozegraj, baza, 3, wejscie=["1"] * 50, moze_pytac=True)
    pytane = zadane(w.wypisane, baza)
    for p in pytane:
        if w.wypisane.count(p["pytanie"]) > 1:
            raise NieDziala("to samo pytanie pada w jednej grze dwa razy — losuj bez powtórzeń: random.sample")
    if len(pytane) != 3:
        raise NieDziala(f"rozegraj(baza 6 pytań, 3) zadaje inną liczbę pytań ({len(pytane)}) niż 3")
    oczekiwane = sum(1 for p in pytane if p["poprawna"] == 0)
    if isinstance(w.wartosc, bool) or not isinstance(w.wartosc, int):
        raise NieDziala(f"zwraca {w.wartosc!r} — ma zwrócić liczbę punktów")
    if w.wartosc != oczekiwane:
        raise NieDziala(f"gracz zawsze wybierał odpowiedź 1 i trafił {oczekiwane} razy, a funkcja zwraca {w.wartosc}")
    random.seed(4)
    w, wyw = wywolaj_i_wymagaj(quiz.rozegraj, baza, wejscie=["1"] * 50, moze_pytac=True)
    if len(zadane(w.wypisane, baza)) != 5:
        raise NieDziala(f"bez podanej liczby pytań zadaje {len(zadane(w.wypisane, baza))} pytań zamiast "
                        "5 (parametr domyślny liczba_pytan)")
    mala = kopia(TESTOWE[:3])
    w = wywolaj(quiz.rozegraj, mala, wejscie=["1"] * 50)
    if isinstance(w.wyjatek, ValueError):
        raise NieDziala("przy 3 pytaniach w bazie i liczba_pytan = 5 kończy się błędem ValueError — "
                        "losuj tyle pytań, ile jest w bazie: min(liczba_pytan, len(pytania))")
    wymagaj(w, "rozegraj", "rozegraj(baza 3 pytań)", moze_pytac=True)
    if len(zadane(w.wypisane, mala)) != 3:
        raise NieDziala("przy 3 pytaniach w bazie nie zadaje wszystkich trzech")
    if not uzywa("rozegraj", "zadaj_pytanie"):
        raise NieDziala("nie korzysta z funkcji zadaj_pytanie")
    if not uzywa("rozegraj", "policz_punkty"):
        raise NieDziala("nie korzysta z policz_punkty — zbierz wybory gracza na liście i policz punkty na końcu")


def sprawdz_dodaj_wynik(quiz):
    lista = []
    w = wywolaj(quiz.dodaj_wynik, lista, "Ola", 3)
    if w.wartosc is None and lista and w.wyjatek is None:
        raise NieDziala("dopisuje wynik do listy, ale nic nie zwraca — dodaj return ranking")
    w, wyw = wywolaj_i_wymagaj(quiz.dodaj_wynik, [], "Ola", 3, moze_wypisywac=False)
    if w.wartosc is None:
        raise NieDziala("nic nie zwraca — dodaj return ranking")
    if w.wartosc != [{"imie": "Ola", "punkty": 3}]:
        raise NieDziala(f"{wyw} zwraca {w.wartosc!r}, a powinna [{{'imie': 'Ola', 'punkty': 3}}]")
    w, wyw = wywolaj_i_wymagaj(quiz.dodaj_wynik, [{"imie": "Ola", "punkty": 3}], "Kuba", 5, moze_wypisywac=False)
    if w.wartosc != [{"imie": "Ola", "punkty": 3}, {"imie": "Kuba", "punkty": 5}]:
        raise NieDziala(f"po dodaniu Kuby (5 pkt) do rankingu z Olą zwraca {w.wartosc!r} — nowy wynik ma trafić na koniec")


def sprawdz_pokaz_ranking(quiz):
    w, wyw = wywolaj_i_wymagaj(quiz.pokaz_ranking, [])
    if "pusty" not in w.wypisane.lower():
        raise NieDziala("dla pustego rankingu nie wypisuje „Ranking jest pusty — zagraj pierwszy!”")
    gracze = [("Ola", 3), ("Kuba", 5), ("Zuza", 3), ("Igor", 1), ("Ala", 5), ("Ewa", 4), ("Tomek", 2)]
    ranking = [{"imie": i, "punkty": p} for i, p in gracze]
    kolejnosc = ["Kuba", "Ala", "Ewa", "Ola", "Zuza", "Tomek", "Igor"]
    for argumenty, ile in (((), 5), ((3,), 3)):
        w, wyw = wywolaj_i_wymagaj(quiz.pokaz_ranking, [dict(x) for x in ranking], *argumenty)
        if w.zapytania:
            raise NieDziala("pokaz_ranking ma tylko wypisać ranking, bez pytania gracza")
        linie = w.wypisane.splitlines()
        pokazani = []
        for linia in linie:
            for imie, punkty in gracze:
                if imie in linia.split() or f"{imie}:" in linia or f"{imie}," in linia:
                    if str(punkty) not in linia:
                        raise NieDziala(f"w wierszu z {imie} nie ma jego punktów ({punkty}): {linia.strip()!r}")
                    pokazani.append(imie)
        if pokazani != kolejnosc[:ile]:
            opis = "pokaz_ranking(ranking)" if not argumenty else f"pokaz_ranking(ranking, {ile})"
            raise NieDziala(f"{opis} dla wyników {', '.join(f'{i} {p}' for i, p in gracze)} pokazuje kolejno: "
                            f"{', '.join(pokazani) or 'nikogo'}, a powinien: {', '.join(kolejnosc[:ile])} "
                            "(od najwięcej punktów, przy remisie kto zagrał wcześniej)")


def sprawdz_main(quiz):
    stare = quiz.PYTANIA
    quiz.PYTANIA = kopia([TESTOWE[0], TESTOWE[3], TESTOWE[5]])   # wszystkie: poprawna 0
    scenariusz = ["3", "2", "1", "Ola", "1", "1", "1", "1", "Kuba", "2", "2", "2", "9", "2", "0"]
    try:
        random.seed(5)
        w = wywolaj(quiz.main, wejscie=scenariusz)
    finally:
        quiz.PYTANIA = stare
    opis = ("scenariusz: 3 (zasady), 2 (ranking), 1 (gra: Ola, odpowiedzi 1, 1, 1), 1 (gra: Kuba, "
            "odpowiedzi 2, 2, 2), 9 (zła opcja), 2 (ranking), 0 (wyjście); w bazie 3 pytania")
    if w.brak_danych:
        raise NieDziala(f"main pyta o dane częściej, niż trzeba — {opis}. Zatrzymało się po "
                        f"{len(scenariusz)} odpowiedziach. Czy opcje 1 i 2 są już napisane?")
    wymagaj(w, "main", "main()", moze_pytac=True)
    if w.pozostale:
        raise NieDziala(f"main skończył się, zanim gracz wybrał 0 — {opis}. Zostało: {', '.join(w.pozostale)}")
    granice = w.granice + [len(w.wypisane)]

    def po_odpowiedzi(k):
        return w.wypisane[granice[k]:granice[k + 1]]

    if "ZASADY" not in po_odpowiedzi(0):
        raise NieDziala("po wyborze 3 nie widać zasad")
    if "pusty" not in po_odpowiedzi(1).lower():
        raise NieDziala("po wyborze 2 na początku (bez gier) nie widać „Ranking jest pusty”")
    gra_oli = "".join(po_odpowiedzi(k) for k in range(3, 7))
    if "Pytanie testowe" not in gra_oli:
        raise NieDziala("po wyborze 1 i podaniu imienia nie zaczyna się gra (rozegraj(PYTANIA))")
    ranking = po_odpowiedzi(13)
    linia_oli = [x for x in ranking.splitlines() if "Ola" in x]
    linia_kuby = [x for x in ranking.splitlines() if "Kuba" in x]
    if not linia_oli or not linia_kuby:
        raise NieDziala("w rankingu na końcu scenariusza nie ma Oli i Kuby — czy wynik trafia do rankingu "
                        "(ranking = dodaj_wynik(...)) i czy opcja 2 pokazuje ranking?")
    if "3" not in linia_oli[0] or "0" not in linia_kuby[0]:
        raise NieDziala(f"w rankingu powinno być: Ola 3 pkt, Kuba 0 pkt, a jest: {linia_oli[0].strip()!r}, "
                        f"{linia_kuby[0].strip()!r}")
    if ranking.index("Ola") > ranking.index("Kuba"):
        raise NieDziala("w rankingu Kuba (0 pkt) jest wyżej niż Ola (3 pkt)")
    if "Do zobaczenia" not in po_odpowiedzi(14) and not po_odpowiedzi(14).strip():
        raise NieDziala("po wyborze 0 program nic nie wypisuje")


def sprawdz_bez_global(quiz):
    drzewo = ast.parse(PLIK_QUIZU.read_text(encoding="utf-8"))
    for wezel in ast.walk(drzewo):
        if isinstance(wezel, ast.FunctionDef):
            for w in ast.walk(wezel):
                if isinstance(w, ast.Global):
                    raise NieDziala(f"funkcja {wezel.name} używa global {', '.join(w.names)} — przekaż stan "
                                    "parametrem i zwróć przez return")


# ---------------------------------------------------------------------------------------------

def wczytaj_quiz():
    """Importuje quiz.py. Zwraca (moduł, None) albo (None, opis problemu)."""
    if not PLIK_QUIZU.exists():
        return None, "nie ma pliku quiz.py obok sprawdz.py"
    try:
        drzewo = ast.parse(PLIK_QUIZU.read_text(encoding="utf-8"))
    except SyntaxError as e:
        return None, f"quiz.py ma błąd składni w linii {e.lineno}: {e.msg}"
    ma_warunek = any(isinstance(w, ast.If) and "__name__" in ast.unparse(w.test) for w in drzewo.body)
    w = wywolaj(__import__, "quiz")
    if w.brak_danych or w.zapytania or w.czas_minal:
        return None, ("quiz.py już przy wczytaniu uruchamia menu. Wywołanie main() ma być na końcu pliku "
                      "pod warunkiem: if __name__ == \"__main__\":")
    if w.wyjatek is not None:
        return None, f"quiz.py nie daje się wczytać: {opis_wyjatku(w.wyjatek)}"
    if not ma_warunek:
        return None, "na końcu quiz.py brakuje warunku if __name__ == \"__main__\": przed main()"
    return w.wartosc, None


def main():
    print("Strażnik quizu: sprawdzam pytania.py i funkcje z quiz.py")
    print()
    wyniki = []

    def linia(nazwa, ok, tekst=""):
        wyniki.append((nazwa, ok))
        stan = "działa" if ok else "nie działa, bo"
        print(f"  {nazwa:<15} {stan}{' ' if tekst else ''}{tekst}")

    try:
        opis = sprawdz_baze()
        linia("baza pytań", True, f"— {opis}")
    except NieDziala as e:
        linia("baza pytań", False, str(e))
    except Exception as e:                                   # np. błąd składni w pytania.py
        linia("baza pytań", False, f"pytania.py nie daje się wczytać: {type(e).__name__}: {e}")
        print("\nNajpierw popraw pytania.py.")
        sys.exit(1)

    quiz, problem = wczytaj_quiz()
    if quiz is None:
        print(f"\n  {problem}")
        sys.exit(1)

    sprawdzenia = [
        ("czy_poprawna", sprawdz_czy_poprawna), ("policz_punkty", sprawdz_policz_punkty),
        ("ramka", sprawdz_ramka), ("pokaz_menu", sprawdz_pokaz_menu), ("wczytaj_wybor", sprawdz_wczytaj_wybor),
        ("zadaj_pytanie", sprawdz_zadaj_pytanie), ("rozegraj", sprawdz_rozegraj), ("dodaj_wynik", sprawdz_dodaj_wynik),
        ("pokaz_ranking", sprawdz_pokaz_ranking), ("main", sprawdz_main), ("bez global", sprawdz_bez_global),
    ]
    for nazwa, sprawdzenie in sprawdzenia:
        if nazwa in KROKI and not callable(getattr(quiz, nazwa, None)):
            linia(nazwa, False, f"w quiz.py nie ma funkcji {nazwa}")
            continue
        zle_wyzej = [n for n, ok in wyniki[1:] if not ok]
        if nazwa == "main" and zle_wyzej:
            linia(nazwa, False, f"najpierw muszą działać funkcje wyżej (np. {zle_wyzej[0]})")
            continue
        try:
            sprawdzenie(quiz)
            linia(nazwa, True)
        except NieDziala as e:
            linia(nazwa, False, str(e))
        except Exception as e:                               # błąd w samym sprawdzaniu — pokaż go w całości
            linia(nazwa, False, f"nieoczekiwany błąd: {type(e).__name__}: {e}")

    dzialajace = sum(1 for _, ok in wyniki if ok)
    print()
    print(f"Działa {dzialajace} z {len(wyniki)}.", end=" ")
    zle = [nazwa for nazwa, ok in wyniki if not ok]
    if not zle:
        print("Wszystko gotowe — zagraj: python3 quiz.py")
        sys.exit(0)
    nastepna = zle[0]
    krok = KROKI.get(nastepna)
    print(f"Następna do poprawienia: {nastepna}" + (f" (README, krok {krok})." if krok else "."))
    sys.exit(1)


if __name__ == "__main__":
    main()
