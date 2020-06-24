### Author: Łukasz Jaremek
### Date: 11.04.2020

import tkinter as TK
import threading
import win32api
import filecmp
import shutil
import time
import os

# Pobiera sciezki.
# Wyznacza ile jest w nich plikow i jak sie nazywaja.
# Zwraca ilosc i nazwy plikow.
def ilosc_plikow(sciezki):
    suma = 0
    nazwy_plikow = []
    if type(sciezki) != list and type(sciezki) != tuple:
        sciezki = [sciezki]
    for sciezka in sciezki:
        for r, d, p in os.walk(sciezka):
            for plik in p:
                if "." in plik:
                    suma += 1
                    plik = r + "/" + plik
                    nazwy_plikow.append(os.path.join(plik))
    if suma == 0:
        suma = 1
        nazwy_plikow = sciezki
    return suma, nazwy_plikow


# Pobiera sciezke do folderu.
# Wyciaga z niej ostatni folder.
# Zwraca folder.
def oczyszczona_nazwa(sciezka):
    sciezka = list(sciezka)[::-1]
    sciezka = "".join(sciezka[0 : sciezka.index("/")][::-1])
    return sciezka


# Nic nie pobiera.
# Tworzy ciag rok_miesiac_dzien_godzina_minuta_sekunda.
# Zwraca ciag.
def aktualny_czas():
    rok = time.localtime().tm_year
    miesiac = time.localtime().tm_mon
    dzien = time.localtime().tm_mday
    godzina = time.localtime().tm_hour
    minuta = time.localtime().tm_min
    sekunda = time.localtime().tm_sec
    czas = "_".join(map(str, [rok, miesiac, dzien, godzina, minuta, sekunda]))
    return czas


# Pobiera lokalizacje i nazwe folderu.
# Tworzy folder w podanym miejscu o podanej nazwie.
# Zwraca lokalizacje lub blad, gdy tworzenie niepowiedzie sie.
def stworz_folder(lokalizacja, nazwa_folderu):
    lokalizacja = lokalizacja + "/" + nazwa_folderu
    try:
        os.mkdir(lokalizacja)
        return lokalizacja
    except:
        return False


# Pobiera sciezki jako string.
# Zamienia string na format komputerowy.
# Zwraca sciezki w formacie dla komputera.
def przygotuj_sciezki(foldery):
    if type(foldery) != list and type(foldery) != tuple:
        foldery = [foldery]
    gotowe = []
    for folder in foldery:
        folder = zamiana_slashy(folder)
        folder = os.path.join(folder)
        gotowe.append(folder)
##    if len(gotowe) == 1:
##        return gotowe[0]
    return gotowe



# Pobiera sciezke.
# Zamienia wszystkie "\" na "/".
# Zwraca sciezke
def zamiana_slashy(sciezka):
    sciezka = list(sciezka)
    for nr in range(len(sciezka)):
        if sciezka[nr] == "\\":
            sciezka[nr] = "/"
    sciezka = "".join(sciezka)
    return sciezka




class Kopiowanie:
    def __init__(self):
        self.ilosc_plikow_do_przeslania = 1
        self.ilosc_przeslanych_plikow = 0
        self.procent_przeslanych_plikow = 0
        self.aktualizacja_w_toku = False

    def cel(self):
        if not os.path.isfile("cel.txt"):
            plik = open("cel.txt", "w")
            plik.close()
        if not os.path.isfile("zrodla.txt"):
            plik = open("zrodla.txt", "w")
            plik.close()
        plik1 = open("cel.txt")
        plik2 = open("zrodla.txt")
        caly_plik1 = plik1.readlines()
        caly_plik2 = plik2.readlines()
        if caly_plik1 == [] or caly_plik2 == []:
            button_start["state"] = "disable"
            plik1.close()
            plik2.close()
        else:
            button_start["state"] = "normal"
        if caly_plik1 == []:
            self.wyswietl(celelista, "Wprowadz lokalizacje plikow do pliku cel.txt", True)
        if caly_plik2 == []:
            self.wyswietl(zrodlalista, "Wprowadz lokalizacje plikow do pliku zrodla.txt", True)
        if caly_plik1 != []:
            plik = open("cel.txt")
            sciezki = []
            for linia in plik:
                sciezki.append(zamiana_slashy(linia.strip()))
                self.wyswietl(celelista, zamiana_slashy(linia.strip()), True)
            plik.close()
            self.cel = sciezki

    def zrodla(self):
        if not os.path.isfile("cel.txt"):
            plik = open("cel.txt", "w")
            plik.close()
        if not os.path.isfile("zrodla.txt"):
            plik = open("zrodla.txt", "w")
            plik.close()
        plik1 = open("cel.txt")
        plik2 = open("zrodla.txt")
        caly_plik1 = plik1.readlines()
        caly_plik2 = plik2.readlines()
        if caly_plik1 == [] or caly_plik2 == []:
            button_start["state"] = "disable"
            plik1.close()
            plik2.close()
        else:
            button_start["state"] = "normal"
        if caly_plik1 == []:
            self.wyswietl(celelista, "Wprowadz lokalizacje plikow do pliku cel.txt", True)
        if caly_plik2 == []:
            self.wyswietl(zrodlalista, "Wprowadz lokalizacje plikow do pliku zrodla.txt", True)
        if caly_plik2 != []:
            plik = open("zrodla.txt")
            pierwsza = True
            linie = []
            for linia in plik:
                linia = linia.strip()
                linie.append(linia)
                linia += "\n"
                if pierwsza:
                    self.wyswietl(zrodlalista, zamiana_slashy(linia), True)
                    pierwsza = False
                else:
                    self.wyswietl(zrodlalista, zamiana_slashy(linia), False)
            plik.close()
            self.nazwy_folderow = przygotuj_sciezki(linie)
            self.ilosc_plikow_do_przeslania, self.nazwy_plikow_do_przeslania = ilosc_plikow(przygotuj_sciezki(linie))

    def edytuj(self, plik):
        if plik == "zrodla":
            try:
                os.system("zrodla.txt")
            except:
                plik = open("zrodla.txt", "w")
                plik.close()
                os.system("zrodla.txt")
        else:
            try:
                os.system("cel.txt")
            except:
                plik = open("cel.txt", "w")
                plik.close()
                os.system("cel.txt")

    def wyswietl(self, miejsce, tekst, czyszczenie):
        miejsce["state"] = "normal"
        if czyszczenie:
            miejsce.delete(1.0, "end")
        miejsce.insert("insert", tekst)
        miejsce.see("end")
        miejsce["state"] = "disable"

    def uruchom_aplikacje(self):
        self.cel()
        self.zrodla()
        self.procent_przeslanych_plikow = round(self.ilosc_przeslanych_plikow * 100 / self.ilosc_plikow_do_przeslania, 3)
        tekst_procentowy = "Przeslano " + str(aplikacja.ilosc_przeslanych_plikow) + "/" + str(aplikacja.ilosc_plikow_do_przeslania) + " plikow" + " ( " + str(aplikacja.procent_przeslanych_plikow) + "% )"
        tekst_procenty.set(tekst_procentowy)

    def aktualizuj_postep(self):
        while self.aktualizacja_w_toku:
            self.ilosc_przeslanych_plikow = ilosc_plikow(przygotuj_sciezki(self.cel[0] + "/" + self.nazwa_folderu))[0]
            self.przeslane_pliki = ilosc_plikow(przygotuj_sciezki(self.cel[0] + "/" + self.nazwa_folderu))[1]
            self.procent_przeslanych_plikow = round(self.ilosc_przeslanych_plikow * 100 / self.ilosc_plikow_do_przeslania, 3)
            tekst_procentowy = "Przeslano " + str(aplikacja.ilosc_przeslanych_plikow) + "/" + str(aplikacja.ilosc_plikow_do_przeslania) + " plikow" + " ( " + str(aplikacja.procent_przeslanych_plikow) + "% )"
            tekst_procenty.set(tekst_procentowy)
            for plik in self.przeslane_pliki:
                if plik not in self.zaktualizowane_pliki:
                    self.wyswietl(komunikaty, zamiana_slashy(plik) + "\n", False)
                    self.zaktualizowane_pliki.append(plik)
        self.ilosc_przeslanych_plikow = ilosc_plikow(przygotuj_sciezki(self.cel[0] + "/" + self.nazwa_folderu))[0]
        self.przeslane_pliki = ilosc_plikow(przygotuj_sciezki(self.cel[0] + "/" + self.nazwa_folderu))[1]
        self.procent_przeslanych_plikow = round(self.ilosc_przeslanych_plikow * 100 / self.ilosc_plikow_do_przeslania, 3)
        tekst_procentowy = "Przeslano " + str(aplikacja.ilosc_przeslanych_plikow) + "/" + str(aplikacja.ilosc_plikow_do_przeslania) + " plikow" + " ( " + str(aplikacja.procent_przeslanych_plikow) + "% )"
        tekst_procenty.set(tekst_procentowy)
        for plik in self.przeslane_pliki:
            if plik not in self.zaktualizowane_pliki:
                self.wyswietl(komunikaty, zamiana_slashy(plik) + "\n", False)
                self.zaktualizowane_pliki.append(plik)
        self.wyswietl(komunikaty, "...kopiowanie zakonczone." + "\n", False)
        self.wyswietl(komunikaty, "Nieudane przesylania: " + str(len(self.nieudane)) + "\n", False)
        if len(self.nieudane) > 0:
            self.wyswietl(komunikaty, "Nieprzeslane pliki:" + "\n", False)
            for plik in self.nieudane:
                self.wyswietl(komunikaty, zamiana_slashy(plik) + "\n", False)
        button_start["state"] = "normal"
        button_zrodla["state"] = "normal"
        button_cele["state"] = "normal"
            

    def kopiuj(self):
        self.nazwa_folderu = aktualny_czas()
        a = stworz_folder(self.cel[0], self.nazwa_folderu)
        button_start["state"] = "disable"
        button_zrodla["state"] = "disable"
        button_cele["state"] = "disable"
        self.nieudane = []
        for sciezka in self.nazwy_folderow:
            self.cel_aktualny = zamiana_slashy(self.cel[0] + "/" + self.nazwa_folderu + "/" + oczyszczona_nazwa(sciezka))
            try:
                shutil.copytree(sciezka, self.cel_aktualny)
            except:
                try:
                    shutil.copy(sciezka, self.cel_aktualny)
                except:
                    self.nieudane.append(sciezka)
        self.aktualizacja_w_toku = False
        

    def start(self):
        self.przeslane_pliki = []
        self.zaktualizowane_pliki = []
        self.aktualizacja_w_toku = True
        kopiowanie = threading.Thread(target = self.kopiuj)
        aktualizacja_postepu = threading.Thread(target = self.aktualizuj_postep)
        self.wyswietl(komunikaty, "Rozpoczynam kopiowanie..." + "\n", False)
        kopiowanie.start()
        aktualizacja_postepu.start()


aplikacja = Kopiowanie()



# ----- Tworzenie okna -----
szerokosc_ekranu = win32api.GetSystemMetrics(0)
wysokosc_ekranu = win32api.GetSystemMetrics(1)
szerokosc_okna = 400
wysokosc_okna = 530
okno_wymiary = str(szerokosc_okna) + "x" +  str(wysokosc_okna) + "+" + str(int((szerokosc_ekranu - szerokosc_okna)/2)) + "+" + str(int((wysokosc_ekranu - wysokosc_okna)/2))

okno = TK.Tk()
okno.geometry(okno_wymiary)
okno.resizable(0, 0)
okno.title("Just copy.")
#okno.iconbitmap("ikonka.ico")
tekst_procenty = TK.StringVar()

# ----- Zrodla -----

label_zrodla = TK.Label(okno, text = "Zrodla:", font = (None, 14), padx = 10)
label_zrodla.grid(row = 0, column = 0, sticky = "w", pady = (10, 0))

button_edytuj_zrodla = TK.Button(okno, text = "Edytuj", font = (None, 12), command = lambda: aplikacja.edytuj("zrodla"))
button_edytuj_zrodla.grid(row = 0, column = 1, sticky = "e")

button_zrodla = TK.Button(okno, text = "Odswiez", font = (None, 12), command = aplikacja.zrodla)
button_zrodla.grid(row = 0, column = 2, columnspan = 2, sticky = "e")

scroll_zrodlalista = TK.Scrollbar(okno)
scroll_zrodlalista.grid(row = 1, column = 4, sticky = "ns")

zrodlalista = TK.Text(okno, height = 4, width = 46, yscrollcommand = scroll_zrodlalista.set)
zrodlalista.grid(row = 1, column = 0, columnspan = 3, sticky = "w", padx = (10, 0))

sep = TK.Frame(okno, height = 2, width = 400, bd = 1, relief = "sunken")
sep.grid(row = 2, column = 0, columnspan = 5, pady = (20, 0))

# ----- Cele -----

label_cele = TK.Label(okno, text = "Cele:", font = (None, 14), padx = 10)
label_cele.grid(row = 3, column = 0, sticky = "w", pady = (10, 0))

button_edytuj_cele = TK.Button(okno, text = "Edytuj", font = (None, 12), command = lambda: aplikacja.edytuj("cele"))
button_edytuj_cele.grid(row = 3, column = 1, sticky = "e")

button_cele = TK.Button(okno, text = "Odswiez", font = (None, 12), command = aplikacja.cel)
button_cele.grid(row = 3, column = 2, columnspan = 2, sticky = "e")

scroll_celelista = TK.Scrollbar(okno)
scroll_celelista.grid(row = 4, column = 4, sticky = "ns")

celelista = TK.Text(okno, height = 4, width = 46, yscrollcommand = scroll_celelista.set)
celelista.grid(row = 4, column = 0, columnspan = 3, sticky = "w", padx = (10, 0))


sep = TK.Frame(okno, height = 2, width = 400, bd = 1, relief = "sunken")
sep.grid(row = 5, column = 0, columnspan = 5, pady = (20, 10))

# ----- Postep -----

tekst_procentowy = "Przeslano " + str(aplikacja.ilosc_przeslanych_plikow) + "/" + str(aplikacja.ilosc_plikow_do_przeslania) + " plikow" + " ( " + str(aplikacja.procent_przeslanych_plikow) + "% )"
tekst_procenty.set(tekst_procentowy)


label_iloscprocent = TK.Label(okno, textvariable = tekst_procenty, font = (None, 14))
label_iloscprocent.grid(row = 6, column = 0, sticky = "w", columnspan = 10, padx = (10, 0))

label_przeslanepliki = TK.Label(okno, text = "Przeslane pliki:", font = (None, 14))
label_przeslanepliki.grid(row = 7, column = 0, sticky = "w", columnspan = 2, padx = (10, 0))

komunikatyscroll = TK.Scrollbar(okno)
komunikatyscroll.grid(row = 8, column = 4, sticky = "ns")

komunikaty = TK.Text(okno, height = 10, width = 46, state = "disable", yscrollcommand = komunikatyscroll.set)
komunikaty.grid(row = 8, column = 0, columnspan = 3, sticky = "w", padx = (10, 0))


komunikatyscroll.config(command = komunikaty.yview)

# ----- Start -----

button_start = TK.Button(okno, text = "Rozpocznij", font = (None, 14), command = aplikacja.start)
button_start.grid(row = 9, column = 0, columnspan = 4, sticky = "ns")


aplikacja.uruchom_aplikacje()


TK.mainloop()
