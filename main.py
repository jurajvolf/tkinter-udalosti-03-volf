import tkinter as tk

# Premenné pre stav aplikácie
stav = "neaktivny"
pokusy = []


# Callback: reaguje na kliknutie na tlačidlo Štart (command=spusti_test)
def spusti_test():
    root.focus_set()
    lbl_stav.config(text="Test je pripravený – náhodný časovač doplníme v ďalšom commite.")


# Callback: reaguje na kliknutie na tlačidlo Reset (command=resetuj_test)
def resetuj_test():
    global stav
    root.focus_set()
    stav = "neaktivny"
    pokusy.clear()
    plocha.config(bg="#3498db")
    plocha.itemconfig(text_plocha, text="Klikni na Štart")
    lbl_stav.config(text="Návod: Klikni na Štart a čakaj na zelenú farbu.")
    lbl_vysledky.config(text="Pokusy: 0/5")


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

ram_tlacidla = tk.Frame(root)
ram_tlacidla.pack(pady=8)

btn_start = tk.Button(ram_tlacidla, text="Štart", width=12, takefocus=False, command=spusti_test)
btn_start.pack(side="left", padx=5)

btn_reset = tk.Button(ram_tlacidla, text="Reset", width=12, takefocus=False, command=resetuj_test)
btn_reset.pack(side="left", padx=5)

lbl_vysledky = tk.Label(root, text="Pokusy: 0/5", font=("Arial", 11))
lbl_vysledky.pack(pady=6)

root.mainloop()