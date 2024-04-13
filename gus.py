import json
import requests
import sys


def main():

    wyszukiwanie = input("Szukaj tematu: ").lower()
    wynik = wyszukiwarka(wyszukiwanie)
    if len(wynik) < 1:
        print("Nie znaleziono.")
    else:
        for count, item in enumerate(wynik):
            print(f"{count + 1}. {item}")
    sys.exit()


    try:
        rok = int(input("Podaj rok: "))
    except ValueError:
        sys.exit("Podaj czterocyfrową liczbę")

    # dane roczne id-okres: 282
    id_okres = 282
    id_zmienna = 1115
    
    zapytanie = requests.get(f"https://api-dbw.stat.gov.pl/api/1.1.0/variable/variable-data-section?id-zmienna={id_zmienna}&id-przekroj=933&id-rok={rok}&id-okres={id_okres}&ile-na-stronie=50&numer-strony=0&lang=pl")
    
    
    
# Wyszukiwarka zmiennych po stringach
def wyszukiwarka(string):
    tematy = set()
    znalezione = []
    page = 0
    while page <= 1:
        zmienne = requests.get(f"https://api-dbw.stat.gov.pl/api/1.1.0/variable/variable-section-periods?ile-na-stronie=5000&numer-strony={page}&lang=pl")
        for row in zmienne.json()["data"]:
            nazwa = str(row['nazwa-zmienna'])
            tematy.add(nazwa)
        page += 1

    for temat in tematy:
        check = temat.lower().find(string)
        if check != -1:
            znalezione.append(temat)
    return znalezione
    

if __name__ == "__main__":
    main()