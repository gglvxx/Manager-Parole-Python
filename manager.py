# manager.py

PAROLA_MASTER = "student2024"
# Aceasta este "memoria" temporară a programului (RAM)
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

# --- FUNCȚII NOI ---

def adauga_parola():
    site = input("Pentru ce site/aplicație? ")
    user = input("Care este numele de utilizator? ")
    parola = input("Care este parola? ")
    
    # Cream un dictionar (o intrare in seif)
    intrare = {
        "site": site,
        "user": user,
        "parola": parola
    }
    
    # Adaugam dictionarul in lista noastra mare
    seif_date.append(intrare)
    print(f"\n[SUCCES] Datele pentru {site} au fost salvate în memorie!")

# -------------------

if __name__ == "__main__":
    if autentificare():
        while True:
            alegere = afiseaza_meniu()
            
            if alegere == "1":
                adauga_parola() # Apelăm funcția nouă
            elif alegere == "2":
                print("\n[Logica pentru VIZUALIZARE urmează...]")
            elif alegere == "3":
                print("Se închide seiful. La revedere!")
                break
            else:
                print("Opțiune invalidă.")