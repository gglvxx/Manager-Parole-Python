# manager.py

# Definim parola master (ulterior o vom schimba cu ceva mai complex)
PAROLA_MASTER = "student2024"

def autentificare():
    print("--- Manager de Parole ---")
    incercare = input("Introdu parola master pentru a debloca seiful: ")
    
    if incercare == PAROLA_MASTER:
        print("Acces permis!\n")
        return True
    else:
        print("Parolă incorectă! Acces interzis.")
        return False

# Pornirea programului
if autentificare():
    # Aici va veni meniul principal mai târziu
    print("Bun venit în sistem.")