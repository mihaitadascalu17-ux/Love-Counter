def adauga_cheltuiala():
    suma = input("Introdu suma cheltuită: ")
    categorie = input("Categoria (ex: mancare, transport): ")

    with open("cheltuieli.txt", "a", encoding="utf-8") as f:
        f.write(f"{suma},{categorie}\n")

    print("Cheltuiala a fost salvată!\n")


def afiseaza_cheltuieli():
    print("\n=== LISTA CHELTUIELILOR ===")
    try:
        with open("cheltuieli.txt", "r", encoding="utf-8") as f:
            continut = f.readlines()
            if not continut:
                print("Nu există cheltuieli.")
            else:
                for linie in continut:
                    suma, categorie = linie.strip().split(",")
                    print(f"- {suma} lei (categoria: {categorie})")
    except FileNotFoundError:
        print("Nu există fișierul cu cheltuieli.")
    print()


def afiseaza_total():
    total = 0
    try:
        with open("cheltuieli.txt", "r", encoding="utf-8") as f:
            for linie in f:
                suma, _ = linie.strip().split(",")
                total += float(suma)
    except FileNotFoundError:
        pass

    print(f"\nTotal cheltuieli: {total} lei\n")


def meniu():
    while True:
        print("=== TRACKER CHELTUIELI ===")
        print("1. Adaugă cheltuială")
        print("2. Afișează toate cheltuielile")
        print("3. Afișează totalul")
        print("4. Ieșire")

        alegere = input("Alege o opțiune: ")

        if alegere == "1":
            adauga_cheltuiala()
        elif alegere == "2":
            afiseaza_cheltuieli()
        elif alegere == "3":
            afiseaza_total()
        elif alegere == "4":
            print("La revedere!")
            break
        else:
            print("Opțiune invalidă.\n")


meniu()

