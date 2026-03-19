import json
import os
import hashlib
import base64
import random
import string
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# --- CONFIGURARE ---
NUME_FISIER = "date_parole.json"
FISIER_HASH = "master.hash"
seif_date = []

# --- LOGICA DE SECURITATE ---
def genereaza_cheia(parola_text):
    parola_bytes = parola_text.encode()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b'sare_pentru_securitate_ac',
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
        print("[SUCCES] Parola Master a fost salvată!")
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

# --- FUNCTIE GENERATOR ---
def genereaza_parola_aleatorie(lungime=12):
    # Litere mari, mici, cifre și simboluri
    caractere = string.ascii_letters + string.digits + string.punctuation
    parola = ''.join(random.choice(caractere) for i in range(lungime))
    return parola

# --- GESTIUNE DATE ---
def incarca_date(fernet_obj):
    global seif_date
    if os.path.exists(NUME_FISIER):
        with open(NUME_FISIER, "rb") as f:
            continut_criptat = f.read()
            if len(continut_criptat) == 0: return
            try:
                date_decriptate = fernet_obj.decrypt(continut_criptat)
                seif_date = json.loads(date_decriptate)
            except:
                seif_date = []
    else:
        seif_date = []

def salveaza_date(fernet_obj):
    date_json = json.dumps(seif_date).encode()
    date_criptate = fernet_obj.encrypt(date_json)
    with open(NUME_FISIER, "wb") as f:
        f.write(date_criptate)

# --- ACTIUNI ---
def afiseaza_meniu():
    print("\n--- MENIU ---")
    print("1. Adaugă o parolă nouă")
    print("2. Vizualizează toate parolele")
    print("3. Ieșire")
    return input("Alege o opțiune (1/2/3): ")

def adauga_parola(fernet_obj):
    site = input("Site/Aplicație: ")
    user = input("Username: ")
    
    # Aici este alegerea utilizatorului pentru fiecare parola in parte
    print(f"\nConfigurare parolă pentru {site}:")
    optiune = input("Vrei să generezi o parolă aleatorie sigură? (da/nu): ").lower()
    
    if optiune == 'da' or optiune == 'd':
        parola = genereaza_parola_aleatorie()
        print(f"Parola generată automat este: {parola}")
    else:
        parola = input("Introdu parola dorită de tine: ")
    
    seif_date.append({"site": site, "user": user, "parola": parola})
    salveaza_date(fernet_obj)
    print(f"[OK] Datele pentru {site} au fost criptate și salvate!")

def vizualizeaza_parole():
    if not seif_date:
        print("\n[!] Seiful este gol.")
    else:
        print("\n--- PAROLELE TALE SALVATE ---")
        for el in seif_date:
            print(f"SITE: {el['site']} | USER: {el['user']} | PASS: {el['parola']}")
        print("-----------------------------")

# --- START ---
if __name__ == "__main__":
    parola_master = autentificare_si_setare()
    fernet = genereaza_cheia(parola_master)
    incarca_date(fernet)
    
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