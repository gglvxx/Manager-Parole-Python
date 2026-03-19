# manager.py

PAROLA_MASTER = "student2024"

def autentificare():
    print("\n=== SEIF DIGITAL v1.0 ===")
    incercare = input("Introdu parola master: ")
    return incercare == PAROLA_MASTER

def afiseaza_meniu():
    print("\n--- MENIU ---")
    print("1. Adaugă o parolă nouă")
    print("2. Vizualizează toate parolele")
    print("3. Ieșire")
    optiune = input("Alege o opțiune (1/2/3): ")
    return optiune

# Aici începe "Motorul" programului
if __name__ == "__main__":
    if autentificare():
        print("Acces permis!")
        
        while True:
            alegere = afiseaza_meniu()
            
            if alegere == "1":
                print("\n[Logica pentru ADĂUGARE va fi aici]")
            elif alegere == "2":
                print("\n[Logica pentru VIZUALIZARE va fi aici]")
            elif alegere == "3":
                print("Se închide seiful. La revedere!")
                break # Această comandă oprește bucla while și închide programul
            else:
                print("Opțiune invalidă, mai încearcă.")
    else:
        print("Acces interzis!")