

produse = []
vanzari = []
FISIER_DATE = "magazin_data.txt"

def este_numar_valid(text):
    """
    Verifica manual daca un string poate fi convertit in float.
    Regula: sa contina doar cifre si maxim un punct.
    """
    if len(text) == 0:
        return False


    if text.count('.') > 1:
        return False


    text_curat = text.replace('.', '')
    if text_curat.isdigit():
        return True
    return False


def citeste_numar(mesaj, tip="float"):
    """Cere input pana cand utilizatorul introduce un numar valid."""
    while True:
        val = input(mesaj)
        if este_numar_valid(val):
            numar = float(val)
            if tip == "int":

                if int(numar) == numar:
                    return int(numar)
                else:
                    print("Eroare: Introduceti un numar intreg, fara zecimale.")
            else:
                return numar
        else:
            print("Eroare: Introduceti o valoare numerica valida.")

def incarca_date():
    global produse

    f_create = open(FISIER_DATE, "a")
    f_create.close()

    f = open(FISIER_DATE, "r")
    linii = f.readlines()
    f.close()

    produse = []
    for linie in linii:
        linie = linie.strip()
        if len(linie) > 0:
            parti = linie.split("|")
            if len(parti) >= 6:
                p = {
                    "cod": parti[0],
                    "nume": parti[1],
                    "pret": float(parti[2]),
                    "cantitate": int(parti[3]),
                    "categorie": parti[4],
                    "vandut": int(parti[5])
                }
                produse.append(p)
    print("Date incarcate (sau baza de date noua creata).")


def salveaza_date():
    f = open(FISIER_DATE, "w")
    for p in produse:
        linie = f"{p['cod']}|{p['nume']}|{p['pret']}|{p['cantitate']}|{p['categorie']}|{p['vandut']}\n"
        f.write(linie)
    f.close()
    print("Datele au fost salvate.")

def adauga_produs():
    print("\n=== ADAUGARE PRODUS ===")
    cod = input("Cod produs: ")

    for p in produse:
        if p["cod"] == cod:
            print("Eroare: Acest cod exista deja.")
            return

    nume = input("Nume produs: ")
    pret = citeste_numar("Pret (RON): ", "float")
    cantitate = citeste_numar("Cantitate stoc: ", "int")

    print("Categorii: Alimente, Bauturi, Electronice, Altele")
    categorie = input("Categorie: ")

    produs_nou = {
        "cod": cod,
        "nume": nume,
        "pret": pret,
        "cantitate": cantitate,
        "categorie": categorie,
        "vandut": 0
    }
    produse.append(produs_nou)
    print("Produs adaugat cu succes.")
    salveaza_date()


def afiseaza_inventar():
    print("\n=== INVENTAR ===")
    if len(produse) == 0:
        print("Nu exista produse.")
        return

    print("-" * 70)
    print(f"| {'COD':<5} | {'NUME':<20} | {'PRET':<8} | {'STOC':<6} | {'CATEGORIE':<12} |")
    print("-" * 70)

    for p in produse:
        nume_scurt = p['nume']
        if len(nume_scurt) > 18:
            nume_scurt = nume_scurt[:18] + ".."

        print(f"| {p['cod']:<5} | {nume_scurt:<20} | {p['pret']:<8.2f} | {p['cantitate']:<6} | {p['categorie']:<12} |")

    print("-" * 70)


def cautare_avansata():
    print("\n=== CAUTARE PRODUS ===")
    termen = input("Introduceti nume sau parte din nume: ").lower()

    gasite = []
    for p in produse:
        if termen in p["nume"].lower():
            gasite.append(p)

    if len(gasite) == 0:
        print("Nu s-au gasit produse.")
    else:
        print(f"Rezultate gasite: {len(gasite)}")
        for p in gasite:
            print(f"> {p['nume']} (Cod: {p['cod']}) - Pret: {p['pret']} RON - Stoc: {p['cantitate']}")


def modifica_produs():
    print("\n=== MODIFICARE PRODUS ===")
    cod = input("Cod produs de modificat: ")

    produs = None
    for p in produse:
        if p["cod"] == cod:
            produs = p
            break

    if produs is None:
        print("Produsul nu a fost gasit.")
        return

    print(f"Modificati: {produs['nume']}")
    print("1. Nume\n2. Pret\n3. Cantitate\n4. Categorie")
    opt = input("Optiune: ")

    if opt == "1":
        produs["nume"] = input("Nume nou: ")
    elif opt == "2":
        produs["pret"] = citeste_numar("Pret nou: ", "float")
    elif opt == "3":
        produs["cantitate"] = citeste_numar("Cantitate noua: ", "int")
    elif opt == "4":
        produs["categorie"] = input("Categorie noua: ")

    print("Modificare salvata.")
    salveaza_date()


def sterge_produs():
    print("\n=== STERGERE PRODUS ===")
    cod = input("Cod produs: ")

    index_gasit = -1
    for i in range(len(produse)):
        if produse[i]["cod"] == cod:
            index_gasit = i
            break

    if index_gasit != -1:
        nume = produse[index_gasit]["nume"]
        confirmare = input(f"Sigur stergeti '{nume}'? (da/nu): ")
        if confirmare.lower() == "da":
            produse.pop(index_gasit)
            print("Produs sters.")
            salveaza_date()
    else:
        print("Produsul nu exista.")


def proceseaza_comanda():
    print("\n=== VANZARE NOUA ===")
    if len(produse) == 0:
        print("Inventar gol.")
        return

    cos = []
    total = 0.0

    while True:
        cod = input("Cod produs (sau 'stop' pt finalizare): ")
        if cod == "stop":
            break

        produs_selectat = None
        for p in produse:
            if p["cod"] == cod:
                produs_selectat = p
                break

        if produs_selectat:
            print(f"Produs: {produs_selectat['nume']} | Stoc: {produs_selectat['cantitate']}")
            cant = citeste_numar("Cantitate dorita: ", "int")

            if cant > 0 and cant <= produs_selectat["cantitate"]:
                valoare_linie = produs_selectat["pret"] * cant

                item = {
                    "cod": produs_selectat["cod"],
                    "nume": produs_selectat["nume"],
                    "cantitate": cant,
                    "valoare": valoare_linie
                }
                cos.append(item)
                total += valoare_linie
                print(f"Adaugat in cos. Subtotal curent: {total:.2f} RON")
            else:
                print("Cantitate invalida (sau stoc insuficient).")
        else:
            print("Produsul nu exista.")

    if len(cos) == 0:
        print("Cos gol. Comanda anulata.")
        return

    reducere = 0.0
    if total > 200:
        reducere = total * 0.1
    elif total > 100:
        reducere = total * 0.05

    total_final = total - reducere

    print("\n--- REZUMAT ---")
    print(f"Total brut: {total:.2f} RON")
    print(f"Reducere:  -{reducere:.2f} RON")
    print(f"DE PLATA:   {total_final:.2f} RON")

    conf = input("Confirmati plata? (da/nu): ")
    if conf.lower() == "da":
        for item in cos:
            for p in produse:
                if p["cod"] == item["cod"]:
                    p["cantitate"] -= item["cantitate"]
                    p["vandut"] += item["cantitate"]

        vanzari.append({"total": total_final, "items": len(cos)})

        genereaza_bon(cos, total, reducere, total_final)
        salveaza_date()
    else:
        print("Comanda anulata.")


def genereaza_bon(cos, total, reducere, total_final):
    linii = []
    linii.append("\n==============================")
    linii.append("         BON FISCAL           ")
    linii.append("==============================")
    for item in cos:
        linii.append(f"{item['nume'][:15]:<15} x{item['cantitate']}  {item['valoare']:.2f}")
    linii.append("------------------------------")
    linii.append(f"TOTAL:           {total:.2f}")
    linii.append(f"REDUCERE:       -{reducere:.2f}")
    linii.append(f"FINAL:           {total_final:.2f}")
    linii.append("==============================")

    for l in linii:
        print(l)

    f = open("bon_fiscal.txt", "w")
    for l in linii:
        f.write(l + "\n")
    f.close()
    print("\n[INFO] Bon salvat in 'bon_fiscal.txt'")


def rapoarte():
    print("\n=== RAPOARTE ===")
    print("1. Raport Vanzari")
    print("2. Produse Stoc Critic")
    print("3. Top Produse Vandute")
    opt = input("Alege raport: ")

    if opt == "1":
        total_incasat = 0
        for v in vanzari:
            total_incasat += v["total"]
        print(f"Numar vanzari: {len(vanzari)}")
        print(f"Total incasari: {total_incasat:.2f} RON")

    elif opt == "2":
        gasit = False
        print("Produse cu stoc < 5:")
        for p in produse:
            if p["cantitate"] < 5:
                print(f"- {p['nume']}: {p['cantitate']} buc")
                gasit = True
        if not gasit: print("Niciun produs cu stoc critic.")

    elif opt == "3":
        top = list(produse)  # Copie
        n = len(top)
        for i in range(n):
            for j in range(0, n - i - 1):
                if top[j]["vandut"] < top[j + 1]["vandut"]:
                    aux = top[j]
                    top[j] = top[j + 1]
                    top[j + 1] = aux

        print("Top 3 Produse:")
        for i in range(min(3, len(top))):
            if top[i]["vandut"] > 0:
                print(f"{i + 1}. {top[i]['nume']} - {top[i]['vandut']} vandute")


def meniu():
    incarca_date()
    while True:
        print("\n=== MENIU PRINCIPAL ===")
        print("1. Adauga Produs")
        print("2. Vezi Inventar")
        print("3. Cautare Produs")
        print("4. Modifica Produs")
        print("5. Sterge Produs")
        print("6. Casa de Marcat (Vanzare)")
        print("7. Rapoarte")
        print("0. Iesire")

        opt = input("Optiune: ")

        if opt == "1":
            adauga_produs()
        elif opt == "2":
            afiseaza_inventar()
        elif opt == "3":
            cautare_avansata()
        elif opt == "4":
            modifica_produs()
        elif opt == "5":
            sterge_produs()
        elif opt == "6":
            proceseaza_comanda()
        elif opt == "7":
            rapoarte()
        elif opt == "0":
            salveaza_date()
            print("La revedere!")
            break
        else:
            print("Optiune invalida.")

meniu()
