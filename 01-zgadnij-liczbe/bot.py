"""Bot do gry „Zgadnij liczbę”: sam zgaduje liczbę od 1 do 100, którą wymyślił sędzia.

Bot rozmawia z sędzią tak jak gracz przy klawiaturze:
  print(strzal)          wypisuje liczbę — i nic więcej,
  odpowiedz = input()    czyta odpowiedź sędziego: wiecej, mniej albo trafiony.
Pisz samo input(), bez tekstu w nawiasach: input("Odpowiedź: ") wypisałby ten tekst sędziemu.
Linia zaczynająca się od # to komentarz dla ciebie, sędzia jej nie liczy, np.:
  print("# szukam od", dol, "do", gora)

Sprawdzenie:
  python3 sedzia.py --liczba 37    jedna gra o liczbę 37, ruch po ruchu
  python3 sedzia.py                wszystkie liczby od 1 do 100 i raport
Możesz też sam być sędzią: python3 bot.py i odpowiadaj wiecej, mniej albo trafiony.
"""

# Ten bot już działa, ale jest bardzo cierpliwy: zgaduje po kolei 1, 2, 3, ...
# i w ogóle nie słucha podpowiedzi. Uruchom sędziego i zobacz, ile ruchów potrzebuje.

# TODO 1: zamiast jednej zmiennej strzal zapamiętaj przedział, w którym na pewno jest liczba:
#         dol = 1 i gora = 100
strzal = 1

while True:
    # TODO 2: strzelaj w środek przedziału: (dol + gora) // 2
    print(strzal)
    odpowiedz = input()

    if odpowiedz == "trafiony":
        break
    # TODO 3: „wiecej” — liczba jest większa niż strzal, więc przesuń dol tuż za strzal,
    #         „mniej”  — liczba jest mniejsza niż strzal, więc przesuń gora tuż przed strzal.
    #         Wtedy ta linijka nie będzie już potrzebna:
    strzal = strzal + 1
