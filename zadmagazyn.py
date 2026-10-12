import json

class Produkt:
    def __init__(self, nazwa, cena, kategoria, ilosc=0):
        self.nazwa = nazwa
        self.cena = cena
        self.kategoria = kategoria
        self.ilosc = ilosc

    def __str__(self):
        return f"{self.nazwa} | {self.kategoria} | {self.cena:.2f} zł | ilość: {self.ilosc}"

    @property
    def dostepny(self):
        return self.ilosc > 0

# wyswietlenie menu
# 1 wszystkie produkty - nazwa kategoria cena i sztuka
# 2 dostepne produkty - j.w. tylko bez tych co ilosc @ / dla chetnych checkbox obok innych funkcji
# 3 wyszukaj Produkt - lower prosze uzyc
# 4 produkty do podanej ceny - moze byc niedostepny ale spelnia warunek ceny
# 5 kup Produkt - user wpisaze nazwe i jesli istnieje to jego liczba zmniejszy sie o 1
# stan == 0 to print produkt niedostepny
# print nie znaleziono produktu
# podaj produkt: input,
# monit: kupiono mleko
# pozostalo sztuk: x
# 0 zakoncz program - w petli dopoki @
# komunikat że wybrano złą opcje jezeli spoza zbioru 1,2,3,,5,0
#int float, for, bool, while, if elif,else, break , continue, input, lower, try/except


def wczytaj_magazyn(plik="magazyn.json"):
    try:
        with open(plik, "r", encoding="utf-8") as file:
            dane = json.load(file)
        magazyn = [
            Produkt(
                nazwa=produkt["nazwa"],
                cena=float(produkt["cena"]),
                kategoria=produkt["kategoria"],
                ilosc=int(produkt.get("ilosc", 0)),
            )
            for produkt in dane
        ]
        if magazyn:
            return magazyn
    except (FileNotFoundError, json.JSONDecodeError, TypeError, ValueError):
        pass

    return [
        Produkt("mleko", 4.50, "spożywczy", 5),
        Produkt("sól", 2.50, "przyprawa", 3),
        Produkt("chleb", 6.00, "pieczywo", 2),
        Produkt("jajka", 8.00, "nabiał", 0),
    ]



def zapisz_magazyn(magazyn, plik="magazyn.json"):
    dane_do_zapisu = [
        {
            "nazwa": p.nazwa,
            "cena": p.cena,
            "kategoria": p.kategoria,
            "ilosc": p.ilosc,
        }
        for p in magazyn
    ]
    with open(plik, "w", encoding="utf-8") as file:
        json.dump(dane_do_zapisu, file, ensure_ascii=False, indent=4)


def wyswietl_produkt(produkt):
    print(f"Nazwa: {produkt.nazwa}")
    print(f"Kategoria: {produkt.kategoria}")
    print(f"Cena: {produkt.cena:.2f} zł")
    print(f"Ilość: {produkt.ilosc}")
    print("-" * 20)


def wyswietl_wszystkie(magazyn):
    if not magazyn:
        print("Brak produktów w magazynie.")
        return

    print("Wszystkie produkty:")
    for produkt in magazyn:
        wyswietl_produkt(produkt)


def wyswietl_dostepne(magazyn):
    dostepne = [p for p in magazyn if p.dostepny]
    if not dostepne:
        print("Brak dostępnych produktów.")
        return

    print("Dostępne produkty:")
    for produkt in dostepne:
        wyswietl_produkt(produkt)


def znajdz_produkt(magazyn, nazwa):
    nazwa = nazwa.lower()
    for produkt in magazyn:
        if produkt.nazwa.lower() == nazwa:
            return produkt
    return None


def wyszukaj_produkt(magazyn):
    nazwa = input("Podaj nazwę produktu: ").strip().lower()
    produkt = znajdz_produkt(magazyn, nazwa)
    if produkt is None:
        print("Nie znaleziono produktu")
        return

    print("Znaleziono produkt:")
    wyswietl_produkt(produkt)


def produkty_do_ceny(magazyn):
    try:
        cena = float(input("Podaj maksymalną cenę: ").replace(",", "."))
    except ValueError:
        print("Błędna wartość ceny.")
        return

    znaleziono = False
    for produkt in magazyn:
        if produkt.cena <= cena:
            znaleziono = True
            wyswietl_produkt(produkt)

    if not znaleziono:
        print("Brak produktów spełniających warunek ceny.")


def kup_produkt(magazyn):
    nazwa = input("Podaj produkt: ").strip()
    produkt = znajdz_produkt(magazyn, nazwa)

    if produkt is None:
        print("Nie znaleziono produktu")
        return

    if not produkt.dostepny:
        print("Produkt niedostepny")
        return

    produkt.ilosc -= 1
    print(f"Kupiono {produkt.nazwa}")
    print(f"Pozostało sztuk: {produkt.ilosc}")
    zapisz_magazyn(magazyn)


magazyn = wczytaj_magazyn()

while True:
    
    print("\n=== MAGAZYN ===")
    print("1 Wszystkie produkty")
    print("2 Dostępne produkty")
    print("3 Wyszukaj produkt")
    print("4 Produkty do podanej ceny")
    print("5 Kup produkt")
    print("0 Zakończ program")

    try:
        wybor = int(input("Wybierz opcję: "))
    except ValueError:
        print("Wybrano złą opcję")
        continue

    match wybor:
        case 1:
            wyswietl_wszystkie(magazyn)
        case 2:
            wyswietl_dostepne(magazyn)
        case 3:
            wyszukaj_produkt(magazyn)
        case 4:
            produkty_do_ceny(magazyn)
        case 5:
            kup_produkt(magazyn)
        case 0:
            break
        case _:
            print("Wybrano złą opcję")
            continue

    if wybor in (1, 2, 3, 4, 5):
        zapisz_magazyn(magazyn)
