# manager.py

PAROLA_MASTER = "student2024"
seif_date = [] 

def autentificare():
    print("\n=== SEIF DIGITAL v1.0 ===")
    incercare = input("Introdu parola master: ")
    return incercare == PAROLA_MASTER

def afiseaza_meniu():
    print("\n--- MENIU ---")
    print("1. Adaugă o parolă nouă")
    print("2. Vizualizează toate parolele")
    print("3. Ieșire")
    return input("Alege o opțiune (1/2/3): ")

def adauga_parola():
    site = input("Pentru ce site/aplicație? ")
    user = input("Care este numele de utilizator? ")
    parola = input("Care este parola? ")
    
    intrare = {"site": site, "user": user, "parola": parola}
    seif_date.append(intrare)
    print(f"\n[SUCCES] Datele pentru {site} au fost salvate!")

# --- FUNCȚIA NOUĂ ---

def vizualizeaza_parole():
    if not seif_date: # Verificăm dacă lista este goală
        print("\n[!] Seiful este gol. Nu ai nicio parolă salvată.")
    else:
        print("\n--- DATELE TALE SALVATE ---")
        # Folosim o buclă 'for' pentru a trece prin fiecare dicționar din listă
        for element in seif_date:
            print(f"Site: {element['site']} | User: {element['user']} | Parola: {element['parola']}")
        print("---------------------------")

# --------------------

if __name__ == "__main__":
    if autentificare():
        while True:
            alegere = afiseaza_meniu()
            if alegere == "1":
                adauga_parola()
            elif alegere == "2":
                vizualizeaza_parole() # Apelăm funcția nouă
            elif alegere == "3":
                print("Se închide seiful. La revedere!")
                break
            else:
                print("Opțiune invalidă.")