import csv
import json
import requests
import sys


def main():


    # Wyszukiwanie tematu
    wyszukiwanie = input("Szukaj tematu: ").lower()
    wynik = wyszukiwarka(wyszukiwanie)
    if len(wynik) < 1:
        print("Nie znaleziono.")
    else:
        for count, item in enumerate(wynik):
            print(f"{count + 1}. {item}")
            

    # Wybór tematu z listy wyników
    wybor = input("Wybierz numer z listy: ")    
    while True:
        try:
            wybor = int(wybor)
            if wybor in range(1, len(wynik) + 2):
                print(wynik[wybor - 1])
                id_zpo = (pobierz_id(wynik[wybor - 1]))
                break
        except ValueError:
            print("Nieprawidłowa wartość.")
            break


    try:
        rok = int(input("Podaj rok: "))
    except ValueError:
        sys.exit("Podaj czterocyfrową liczbę")
            
    zapytanie = requests.get(f"https://api-dbw.stat.gov.pl/api/1.1.0/variable/variable-data-section?id-zmienna={id_zpo[0]}&id-przekroj={id_zpo[1]}&id-rok={rok}&id-okres={id_zpo[2]}&ile-na-stronie=500&numer-strony=0&lang=pl")

    zapytanie = zapytanie.json()
    print(json.dumps(zapytanie, indent=2))
    sys.exit()


    
    
# Wyszukiwarka zmiennych po stringach, pobiera nazwy z API, ale mogłaby też z pliku gus_zmienne.csv
# Obecnie wyniki nie są sortowane, ale mogą być
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


def pobierz_id(nazwa):
    ids = []
    with open("gus_zmienne.csv", "r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row["nazwa-zmienna"] == nazwa:
                ids.append(int(row["id-zmienna"]))
                ids.append(int(row["id-przekroj"]))
                ids.append(int(row["id-okres"]))
                return ids
    

if __name__ == "__main__":
    main()