import json
import os
import hashlib
import base64
import random
import string
import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# --- CONFIGURARE ---
NUME_FISIER = "date_parole.json"
FISIER_HASH = "master.hash"
CULOARE_FUNDAL = "#1a2a6c" # Albastru inchis regal
CULOARE_BUTON = "#f2a900"  # Galben auriu pentru contrast
seif_date = []
fernet = None

# --- LOGICA DE SECURITATE (NESCHIMBATĂ) ---
def genereaza_cheia(parola_text):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b'sare_pentru_securitate_ac',
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(parola_text.encode()))
    return Fernet(key)

# --- GESTIUNE DATE ---
def incarca_date():
    global seif_date
    if os.path.exists(NUME_FISIER):
        with open(NUME_FISIER, "rb") as f:
            continut = f.read()
            if not continut: return
            try:
                seif_date = json.loads(fernet.decrypt(continut))
            except: seif_date = []

def salveaza_date():
    date_criptate = fernet.encrypt(json.dumps(seif_date).encode())
    with open(NUME_FISIER, "wb") as f:
        f.write(date_criptate)

# --- FUNCTII INTERFATA ---

def login():
    global fernet
    parola = entry_parola.get()
    hash_incercare = hashlib.sha256(parola.encode()).hexdigest()

    if not os.path.exists(FISIER_HASH):
        with open(FISIER_HASH, "w") as f: f.write(hash_incercare)
    else:
        with open(FISIER_HASH, "r") as f:
            if hash_incercare != f.read():
                messagebox.showerror("Eroare", "Parolă Master incorectă!")
                return

    fernet = genereaza_cheia(parola)
    incarca_date()
    fereastra_login.destroy()
    creaza_fereastra_principala()

def adauga_parola_gui():
    site = simpledialog.askstring("Adăugare", "Numele aplicației (ex: Facebook):")
    if not site: return
    user = simpledialog.askstring("Adăugare", "Nume utilizator:")
    
    if messagebox.askyesno("Parolă", "Vrei o parolă generată automat?"):
        caractere = string.ascii_letters + string.digits + "!@#$%^&*"
        parola = ''.join(random.choice(caractere) for _ in range(16))
        messagebox.showinfo("Parolă Generată", f"Parola ta este:\n{parola}")
    else:
        parola = simpledialog.askstring("Adăugare", "Introdu parola manual:", show='*')

    if site and user and parola:
        seif_date.append({"site": site, "user": user, "parola": parola})
        salveaza_date()
        messagebox.showinfo("Succes", "Datele au fost salvate în seif!")

def afiseaza_parole_gui():
    fereastra_lista = tk.Toplevel()
    fereastra_lista.title("Seif - Vizualizare")
    fereastra_lista.geometry("450x400")
    fereastra_lista.configure(bg=CULOARE_FUNDAL)
    
    txt_area = scrolledtext.ScrolledText(fereastra_lista, font=("Consolas", 10))
    txt_area.pack(pady=20, padx=20, expand=True, fill="both")
    
    if not seif_date:
        txt_area.insert(tk.INSERT, "Momentan seiful este gol.")
    else:
        for el in seif_date:
            info = f"APLICAȚIE: {el['site'].upper()}\nUSER: {el['user']}\nPASS: {el['parola']}\n{'_'*40}\n\n"
            txt_area.insert(tk.INSERT, info)
    txt_area.configure(state='disabled')

def creaza_fereastra_principala():
    root = tk.Tk()
    root.title("Seif Digital - Automatizări")
    root.geometry("400x450")
    root.configure(bg=CULOARE_FUNDAL)

    # Titlu mare centrat
    tk.Label(root, text="DASHBOARD SEIF", font=("Helvetica", 18, "bold"), 
             fg="white", bg=CULOARE_FUNDAL).pack(pady=30)
    
    # Stil butoane: mari, centrate, fara cifre
    stil_butoane = {"font": ("Arial", 11, "bold"), "bg": CULOARE_BUTON, "fg": "black", 
                    "width": 25, "pady": 15, "cursor": "hand2", "bd": 0}

    tk.Button(root, text="Adaugă Parolă Nouă", command=adauga_parola_gui, **stil_butoane).pack(pady=10)
    tk.Button(root, text="Vizualizează Seiful", command=afiseaza_parole_gui, **stil_butoane).pack(pady=10)
    
    # Buton iesire rosu
    tk.Button(root, text="Închide Seiful", command=root.quit, font=("Arial", 11, "bold"),
              bg="#d9534f", fg="white", width=25, pady=15, bd=0).pack(pady=30)

    root.mainloop()

# --- START LOGIN ---
fereastra_login = tk.Tk()
fereastra_login.title("Securitate")
fereastra_login.geometry("350x250")
fereastra_login.configure(bg=CULOARE_FUNDAL)

tk.Label(fereastra_login, text="INTRODU PAROLA MASTER", font=("Arial", 10, "bold"),
         fg="white", bg=CULOARE_FUNDAL).pack(pady=(40, 10))

entry_parola = tk.Entry(fereastra_login, show="*", font=("Arial", 14), justify='center')
entry_parola.pack(pady=10, padx=40)

tk.Button(fereastra_login, text="DESCHIDE SEIFUL", command=login, bg=CULOARE_BUTON,
          fg="black", font=("Arial", 10, "bold"), width=20, pady=10, bd=0).pack(pady=20)

fereastra_login.mainloop()