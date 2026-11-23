import random
import time
import tkinter as tk

stav = "neaktivny"
pokusy = []
casovac_id = None
cas_startu = None
min_cas = 1500
max_cas = 4000


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
        lbl_stav.config(text="Klikol si pred zelenou! Skús znova (Štart).")
    elif stav == "zelena" and cas_startu is not None:
        reakcia_ms = round((time.perf_counter() - cas_startu) * 1000)
        pokusy.append(reakcia_ms)
        cas_startu = None

        if len(pokusy) < 5:
            stav = "neaktivny"
            plocha.config(bg="#3498db")
            plocha.itemconfig(text_plocha, text=f"{reakcia_ms} ms")
            lbl_stav.config(text=f"Pokus {len(pokusy)}/5: {reakcia_ms} ms. Klikni na Štart.")
            lbl_vysledky.config(text=f"Pokusy ({len(pokusy)}/5): {pokusy}")
        else:
            stav = "koniec"
            priemer = round(sum(pokusy) / len(pokusy), 1)
            plocha.config(bg="#9b59b6")
            plocha.itemconfig(text_plocha, text=f"Priemer: {priemer} ms")
            lbl_stav.config(text="Hotovo! Všetkých 5 pokusov dokončených.")
            lbl_vysledky.config(text=f"Pokusy: {pokusy} | Priemer: {priemer} ms")
    elif stav == "koniec":
        lbl_stav.config(text="Test skončil. Klikni na Štart alebo Reset.")
    else:
        lbl_stav.config(text="Najprv spusti test tlačidlom Štart.")


# Callback: reaguje na uplynutie náhodného časovača (root.after)
def zmen_na_zelenu():
    global stav, cas_startu, casovac_id
    casovac_id = None
    if stav == "cakam":
        stav = "zelena"
        cas_startu = time.perf_counter()
        plocha.config(bg="#2ecc71")
        plocha.itemconfig(text_plocha, text="KLIKNI TERAZ!")
        lbl_stav.config(text="Zelená! Klikni na plochu čo najrýchlejšie!")


# Callback: reaguje na kliknutie na tlačidlo Štart (command=spusti_test)
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


# Callback: reaguje na kliknutie na tlačidlo Reset (command=resetuj_test)
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
    lbl_stav.config(text="Návod: Klikni na Štart a čakaj na zelenú farbu.")
    lbl_vysledky.config(text="Pokusy: 0/5")
    lbl_info.config(text="Posledná akcia: Reset")


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


root = tk.Tk()
root.title("Reakčný test – Téma 3")
root.geometry("520x500")
root.resizable(False, False)

lbl_stav = tk.Label(
    root,
    text="Návod: Klikni na Štart a čakaj na zelenú farbu.",
    font=("Arial", 11)
)
lbl_stav.pack(pady=10)

plocha = tk.Canvas(root, width=440, height=220, bg="#3498db", highlightthickness=0)
plocha.pack(pady=10)
text_plocha = plocha.create_text(
    220, 110, text="Klikni na Štart", fill="white", font=("Arial", 18, "bold")
)
plocha.bind("<Button-1>", reaguj_na_klik)

ram_tlacidla = tk.Frame(root)
ram_tlacidla.pack(pady=8)

btn_start = tk.Button(ram_tlacidla, text="Štart", width=12, takefocus=False, command=spusti_test)
btn_start.pack(side="left", padx=5)

btn_reset = tk.Button(ram_tlacidla, text="Reset", width=12, takefocus=False, command=resetuj_test)
btn_reset.pack(side="left", padx=5)

lbl_vysledky = tk.Label(root, text="Pokusy: 0/5", font=("Arial", 11))
lbl_vysledky.pack(pady=6)

lbl_info = tk.Label(root, text="Posledná akcia: –", font=("Arial", 9), fg="gray")
lbl_info.pack(pady=4)

root.mainloop()