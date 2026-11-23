import random
import time
import tkinter as tk

stav = "neaktivny"
pokusy = []
casovac_id = None
cas_startu = None
min_cas = 1000
max_cas = 3000


def zrus_casovac():
    global casovac_id
    if casovac_id is not None:
        root.after_cancel(casovac_id)
        casovac_id = None


def vyhodnot_reakciu():
    global stav, cas_startu
    if stav == "cakam":
        zrus_casovac()
        stav = "neaktivny"
        plocha.config(bg="#f39c12")
        plocha.itemconfig(text_plocha, text="Príliš skoro!")
        lbl_stav.config(text="Klikol si pred zelenou! Skús znova (Štart / Medzerník).")
    elif stav == "zelena" and cas_startu is not None:
        reakcia_ms = round((time.perf_counter() - cas_startu) * 1000)
        pokusy.append(reakcia_ms)
        cas_startu = None

        if len(pokusy) < 5:
            stav = "neaktivny"
            plocha.config(bg="#3498db")
            plocha.itemconfig(text_plocha, text=f"{reakcia_ms} ms")
            lbl_stav.config(text=f"Pokus {len(pokusy)}/5: {reakcia_ms} ms. Stlač Štart alebo Medzerník.")
            lbl_vysledky.config(text=f"Pokusy ({len(pokusy)}/5): {pokusy}")
        else:
            stav = "koniec"
            priemer = round(sum(pokusy) / len(pokusy), 1)
            najlepsi = min(pokusy)
            plocha.config(bg="#9b59b6")
            plocha.itemconfig(text_plocha, text=f"Priemer: {priemer} ms")
            lbl_stav.config(text="Hotovo! Stlač Štart alebo Medzerník pre novú sériu.")
            lbl_vysledky.config(
                text=f"Pokusy: {pokusy}\nPriemer: {priemer} ms | Najlepší čas: {najlepsi} ms"
            )
    elif stav == "koniec":
        lbl_stav.config(text="Test skončil. Stlač Štart, Medzerník alebo Reset.")
    else:
        lbl_stav.config(text="Najprv spusti test (Štart alebo Medzerník).")


# Callback: reaguje na uplynutie náhodného časovača (root.after)
def zmen_na_zelenu():
    global stav, cas_startu, casovac_id
    casovac_id = None
    if stav == "cakam":
        stav = "zelena"
        cas_startu = time.perf_counter()
        plocha.config(bg="#2ecc71")
        plocha.itemconfig(text_plocha, text="KLIKNI TERAZ!")
        lbl_stav.config(text="Zelená! Klikni myšou alebo stlač Medzerník!")


# Callback: reaguje na kliknutie na tlačidlo Štart (command=spusti_test) alebo Medzerník
def spusti_test():
    global stav, casovac_id, cas_startu
    root.focus_set()
    zrus_casovac()
    plocha.delete("klik_bod")
    if len(pokusy) >= 5:
        pokusy.clear()
        lbl_vysledky.config(text="Pokusy: 0/5")
    stav = "cakam"
    cas_startu = None
    plocha.config(bg="#e74c3c")
    plocha.itemconfig(text_plocha, text="Čakaj na zelenú...")
    lbl_stav.config(text=f"Pokus {len(pokusy) + 1}/5 – ešte neklikaj!")
    nahodny_cas = random.randint(min_cas, max_cas)
    casovac_id = root.after(nahodny_cas, zmen_na_zelenu)


# Callback: reaguje na kliknutie na tlačidlo Reset (command=resetuj_test) alebo kláves R
def resetuj_test():
    global stav, cas_startu
    root.focus_set()
    zrus_casovac()
    stav = "neaktivny"
    cas_startu = None
    pokusy.clear()
    plocha.delete("klik_bod")
    plocha.config(bg="#3498db")
    plocha.itemconfig(text_plocha, text="Klikni na Štart")
    lbl_stav.config(text="Návod: Štart / Medzerník = hrať, R = reset, Esc = koniec.")
    lbl_vysledky.config(text="Pokusy: 0/5")
    lbl_info.config(text="Posledná akcia: Reset")


# Callback: reaguje na kliknutie na tlačidlá režimu čakania cez lambda
def nastav_rezim(min_ms, max_ms, nazov):
    global min_cas, max_cas
    root.focus_set()
    min_cas = min_ms
    max_cas = max_ms
    lbl_rezim.config(text=f"Režim čakania: {nazov} ({min_ms // 1000}–{max_ms // 1000} s)")


# Callback: reaguje na kliknutie ľavým tlačidlom myši na plátno (<Button-1>)
def reaguj_na_klik(event):
    plocha.delete("klik_bod")
    r = 5
    plocha.create_oval(
        event.x - r, event.y - r, event.x + r, event.y + r,
        fill="white", outline="black", tags="klik_bod"
    )
    lbl_info.config(text=f"Posledný klik myšou: x={event.x}, y={event.y}")
    vyhodnot_reakciu()


# Callback: reaguje na stlačenie ľubovoľného klávesu na klávesnici (<Key>)
def reaguj_na_klaves(event):
    klaves = event.keysym
    lbl_info.config(text=f"Stlačený kláves: {klaves}")

    if klaves == "space":
        if stav in ("neaktivny", "koniec"):
            spusti_test()
        else:
            vyhodnot_reakciu()
    elif klaves.lower() == "r":
        resetuj_test()
    elif klaves == "Escape":
        ukonci_aplikaciu()


# Callback: reaguje na zatvorenie okna krížikom (WM_DELETE_WINDOW) alebo kláves Esc
def ukonci_aplikaciu():
    zrus_casovac()
    root.destroy()


root = tk.Tk()
root.title("Reakčný test – Téma 3")
root.geometry("520x520")
root.resizable(False, False)
root.protocol("WM_DELETE_WINDOW", ukonci_aplikaciu)

lbl_stav = tk.Label(
    root,
    text="Návod: Štart / Medzerník = hrať, R = reset, Esc = koniec.",
    font=("Arial", 11)
)
lbl_stav.pack(pady=10)

plocha = tk.Canvas(root, width=440, height=220, bg="#3498db", highlightthickness=0)
plocha.pack(pady=10)
text_plocha = plocha.create_text(
    220, 110, text="Klikni na Štart", fill="white", font=("Arial", 18, "bold")
)
plocha.bind("<Button-1>", reaguj_na_klik)
root.bind("<Key>", reaguj_na_klaves)

ram_tlacidla = tk.Frame(root)
ram_tlacidla.pack(pady=6)

btn_start = tk.Button(ram_tlacidla, text="Štart", width=12, takefocus=False, command=spusti_test)
btn_start.pack(side="left", padx=5)

btn_reset = tk.Button(ram_tlacidla, text="Reset", width=12, takefocus=False, command=resetuj_test)
btn_reset.pack(side="left", padx=5)

ram_rezim = tk.Frame(root)
ram_rezim.pack(pady=6)

btn_kratky = tk.Button(
    ram_rezim, text="Krátke čakanie (1–3 s)", takefocus=False,
    command=lambda: nastav_rezim(1000, 3000, "Krátke")
)
btn_kratky.pack(side="left", padx=5)

btn_dlhy = tk.Button(
    ram_rezim, text="Dlhé čakanie (2–5 s)", takefocus=False,
    command=lambda: nastav_rezim(2000, 5000, "Dlhé")
)
btn_dlhy.pack(side="left", padx=5)

lbl_rezim = tk.Label(root, text="Režim čakania: Krátke (1–3 s)", font=("Arial", 10))
lbl_rezim.pack(pady=2)

lbl_vysledky = tk.Label(root, text="Pokusy: 0/5", font=("Arial", 11, "bold"))
lbl_vysledky.pack(pady=8)

lbl_info = tk.Label(root, text="Posledná akcia: –", font=("Arial", 9), fg="gray")
lbl_info.pack(pady=4)

root.mainloop()