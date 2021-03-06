from PyQt5.QtCore import QRegExp

host = 'dbs.cjha2rbtxsjk.eu-central-1.rds.amazonaws.com'
database = 'DBS'
user = 'connector'
password = 'sR4kDeXDYtrRQG9g'

formatter = {"identyfikator": "Identyfikator",
             "nazwa": "Nazwa",
             "rodzaj": "Rodzaj",
             "miasto": "Miasto",
             "oznaczenie": "Oznaczenie",
             "liczba_personelu": "Docelowa liczba personelu",
             "rola_budynku": "Rola",
             "id_jednostki": "Identyfikator jednostki",
             "pesel": "PESEL",
             "imie": "Imię",
             "nazwisko": "Nazwisko",
             "data_ur": "Data urodzenia",
             "grupa_krwi": "Grupa krwi",
             "wyznanie": "Wyznanie",
             "budynek": "Budynek",
             "ranga": "Ranga",
             "numer_seryjny": "Numer seryjny",
             "typ": "Typ",
             "producent": "Producent",
             "model": "Model",
             "data_produkcji": "Data produkcji",
             "data_waznosci": "Data ważności",
             "id_zamowienia": "Numer zamówienia",
             "id_pojazdu": "ID pojazdu",
             "masa": "Masa [kg]",
             "liczba_zalogi": "Liczba członków załogi",
             "zasieg": "Zasięg [km]",
             "status": "Status",
             "rok_produkcji": "Rok produkcji",
             "rejestracja": "Rejestracja",
             "data_od": "Data rozpoczęcia",
             "data_do": "Data zakończenia",
             "pesel_oficera": "PESEL oficera",
             "nazwa_rangi": "Nazwa",
             "liczba_przepustek": "Liczba przepustek",
             "poziom_upr": "Poziom uprawnień",
             "zold": "Żołd [zł]",
             "koszt": "Koszt [zł]",
             "data_zam": "Data złożenia zamówienia",
             "deadline": "Maksymalny termin realizacji"
             }

column_names = {"jednostki": ["identyfikator", "nazwa", "rodzaj", "miasto"],
                "oficerowie": ["imie", "nazwisko", "ranga", "pesel", "data_ur", "grupa_krwi", "wyznanie",
                               "id_jednostki", "budynek"],
                "budynki": ["oznaczenie", "rola_budynku", "liczba_personelu", "id_jednostki"],
                "ekwipunek": ["typ", "producent", "model", "numer_seryjny", "data_produkcji", "data_waznosci", "status"],
                "pojazdy": ["rodzaj", "producent", "model", "rok_produkcji", "masa", "liczba_zalogi", "zasieg",
                            "rejestracja", "id_jednostki", "status"],
                "rangi": ["nazwa_rangi", "liczba_przepustek", "poziom_upr", "zold"]}

rx = QRegExp("[\\w\\d .,-:]*")
