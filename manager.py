import json
import os
import hashlib
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# --- CONFIGURARE ---
NUME_FISIER = "date_parole.json"
FISIER_HASH = "master.hash"
seif_date = []

# --- LOGICA DE SECURITATE (GENERARE CHEIE) ---
def genereaza_cheia(parola_text):
    parola_bytes = parola_text.encode()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b'sare_pentru_securitate_ac', # O "sare" fixa pentru derivare
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(parola_bytes))
    return Fernet(key)

def autentificare_si_setare():
    if not os.path.exists(FISIER_HASH):
        print("\n=== PRIMA RULARE: CONFIGURARE SEIF ===")
        noua_parola = input("Alege o Parolă Master pe care o vei tine minte: ")
        hash_obj = hashlib.sha256(noua_parola.encode())
        with open(FISIER_HASH, "w") as f:
            f.write(hash_obj.hexdigest())
        print("[SUCCES] Parola Master a fost salvată (ca hash)!")
        return noua_parola
    else:
        print("\n=== LOGARE SEIF DIGITAL ===")
        incercare = input("Introdu Parola Master: ")
        hash_incercare = hashlib.sha256(incercare.encode()).hexdigest()
        
        with open(FISIER_HASH, "r") as f:
            hash_salvat = f.read()
            
        if hash_incercare == hash_salvat:
            print("Acces permis!")
            return incercare
        else:
            print("Acces interzis! Parolă greșită.")
            exit()

# --- GESTIUNE DATE (SALVARE / INCARCARE) ---
def incarca_date(fernet_obj):
    global seif_date
    if os.path.exists(NUME_FISIER):
        with open(NUME_FISIER, "rb") as f:
            continut_criptat = f.read()
            if len(continut_criptat) == 0:
                seif_date = []
                return
            try:
                date_decriptate = fernet_obj.decrypt(continut_criptat)
                seif_date = json.loads(date_decriptate)
            except Exception as e:
                print(f"[EROARE] Nu am putut decripta datele: {e}")
                seif_date = []
    else:
        seif_date = []

def salveaza_date(fernet_obj):
    date_json = json.dumps(seif_date).encode()
    date_criptate = fernet_obj.encrypt(date_json)
    with open(NUME_FISIER, "wb") as f:
        f.write(date_criptate)

# --- MENIU SI ACTIUNI ---
def afiseaza_meniu():
    print("\n--- MENIU ---")
    print("1. Adaugă o parolă nouă")
    print("2. Vizualizează toate parolele")
    print("3. Ieșire")
    return input("Alege o opțiune (1/2/3): ")

def adauga_parola(fernet_obj):
    site = input("Site/Aplicație: ")
    user = input("Username: ")
    parola = input("Parola: ")
    seif_date.append({"site": site, "user": user, "parola": parola})
    salveaza_date(fernet_obj)
    print(f"[OK] Datele pentru {site} au fost criptate și salvate!")

def vizualizeaza_parole():
    if not seif_date:
        print("\n[!] Seiful este gol.")
    else:
        print("\n--- PAROLELE TALE ---")
        for el in seif_date:
            print(f"SITE: {el['site']} | USER: {el['user']} | PASS: {el['parola']}")
        print("---------------------")

# --- MOTORUL PROGRAMULUI ---
if __name__ == "__main__":
    # 1. Autentificare
    parola_master = autentificare_si_setare()
    
    # 2. Generare cheie de criptare bazată pe parolă
    fernet = genereaza_cheia(parola_master)
    
    # 3. Încărcare date existente
    incarca_date(fernet)
    
    # 4. Bucla principală
    while True:
        alegere = afiseaza_meniu()
        
        if alegere == "1":
            adauga_parola(fernet)
        elif alegere == "2":
            vizualizeaza_parole()
        elif alegere == "3":
            print("Se închide seiful. La revedere!")
            break
        else:
            print("Opțiune invalidă.")