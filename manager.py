import json # Importăm biblioteca pentru lucrul cu fișiere JSON
import os   # Ne ajută să verificăm dacă fișierul există deja

PAROLA_MASTER = "student2024"
NUME_FISIER = "date_parole.json"
seif_date = []

# --- FUNCȚII NOI PENTRU FIȘIERE ---

def incarca_date():
    global seif_date
    if os.path.exists(NUME_FISIER):
        with open(NUME_FISIER, "r") as f:
            seif_date = json.load(f)
            print("[INFO] Datele vechi au fost încărcate cu succes.")
    else:
        seif_date = []

def salveaza_date():
    with open(NUME_FISIER, "w") as f:
        json.dump(seif_date, f, indent=4)
    print("[INFO] Datele au fost salvate pe disk.")

# ----------------------------------

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
    site = input("Site: ")
    user = input("User: ")
    parola = input("Parola: ")
    seif_date.append({"site": site, "user": user, "parola": parola})
    salveaza_date() # Salvăm imediat ce am adăugat ceva nou!

def vizualizeaza_parole():
    if not seif_date:
        print("\n[!] Seiful este gol.")
    else:
        for element in seif_date:
            print(f"Site: {element['site']} | User: {element['user']} | Parola: {element['parola']}")

if __name__ == "__main__":
    if autentificare():
        incarca_date() # Încărcăm datele imediat după logare!
        while True:
            alegere = afiseaza_meniu()
            if alegere == "1":
                adauga_parola()
            elif alegere == "2":
                vizualizeaza_parole()
            elif alegere == "3":
                print("Se închide seiful...")
                break