"""Gra „Zgadnij liczbę”: komputer losuje liczbę od 1 do 100, a gracz ją zgaduje.

Zanim zaczniesz pisać: uzupełnij pseudokod.txt i narysuj diagram przepływu na kartce.
Uruchom: python3 gra.py   (przerwanie gry: Ctrl+C)
"""
import random

print("=== ZGADNIJ LICZBĘ ===")
print("Myślę o liczbie od 1 do 100. Spróbuj ją zgadnąć!")

# TODO 6: na koniec obejmij całą grę (od losowania do trafienia) zewnętrzną pętlą while True.
#         Po każdej grze zapytaj: input("Jeszcze raz? (t/n): ")
#         Gdy gracz nie wpisze t — wyjdź z pętli i wypisz „Dzięki za grę!”.

sekret = random.randint(1, 100)
proby = 0

while True:
    tekst = input("Twoja liczba: ").strip()

    # TODO 1: jeśli tekst nie jest liczbą (tekst.isdigit() zwraca False),
    #         wypisz „To nie jest liczba.” i wróć na początek pętli (continue)

    liczba = int(tekst)

    # TODO 2: jeśli liczba jest spoza zakresu 1–100, wypisz
    #         „Poza zakresem — liczba jest od 1 do 100.” i continue (ta próba się nie liczy)

    # TODO 3: zwiększ licznik prób

    # TODO 4: porównaj liczbę z sekretem: „Za mało!”, „Za dużo!” albo
    #         „Trafiony! To była liczba 37. Liczba prób: 5.”
    # TODO 5: po trafieniu wyjdź z pętli (break)
