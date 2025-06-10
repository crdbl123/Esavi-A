# esavi_tkinter_validado.py

import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk   # Pillow

# --- Configurações de pontuação e classificação ---
FATORES = {
    1: ("Falta de concentração e persistência", [1,3,7,9,12,15,16,19,20,22,23,29]),
    2: ("Controle cognitivo",                 [6,13,18,21,25,26,27,28]),
    3: ("Planejamento futuro",                [2,4,14,17,31]),
    4: ("Audácia e temeridade",               [5,8,10,11,24,30]),
}
ITENS_INVERTIDOS = {2, 14}
CLASSIFICACAO = {
    1: [(0,14,"Extremo Inferior"),(15,20,"Baixo"),(21,30,"Médio"),(31,37,"Alto"),(38,999,"Extremo Superior")],
    2: [(0,22,"Extremo Inferior"),(23,28,"Baixo"),(29,36,"Médio"),(37,39,"Alto"),(40,999,"Extremo Superior")],
    3: [(0,9,"Extremo Inferior"),(10,13,"Baixo"),(14,19,"Médio"),(20,22,"Alto"),(23,999,"Extremo Superior")],
    4: [(0,10,"Extremo Inferior"),(11,13,"Baixo"),(14,19,"Médio"),(20,22,"Alto"),(23,999,"Extremo Superior")],
}

def validar_input(novo):
    return (novo == "") or (novo.isdigit() and 1 <= int(novo) <= 5)

def calcular():
    resp = {}
    for i, entry in entries.items():
        v = entry.get()
        if not (v.isdigit() and 1 <= int(v) <= 5):
            messagebox.showerror("Erro", f"Item {i} inválido (só 1–5).")
            return
        resp[i] = int(v)
    # pontuar
    totais = {}
    for idx, (nome, itens) in FATORES.items():
        soma = 0
        for item in itens:
            val = resp[item]
            if item in ITENS_INVERTIDOS:
                val = 6 - val
            soma += val
        totais[idx] = (nome, soma)
    # classificar e mostrar
    texto = ""
    for idx in sorted(totais):
        nome, soma = totais[idx]
        for inf, sup, rot in CLASSIFICACAO[idx]:
            if inf <= soma <= sup:
                cat = rot
                break
        texto += f"{nome}: {soma} → {cat}\n"
    messagebox.showinfo("Resultados", texto)

def reiniciar():
    for entry in entries.values():
        entry.delete(0, tk.END)

# --- Início da GUI ---
root = tk.Tk()
root.title("EsAvI-A Calculator")

# Carrega e desenha a imagem de fundo
bg = Image.open(r"C:\MeusScripts\Esavi\fundo.jpg")
bg_photo = ImageTk.PhotoImage(bg)
canvas = tk.Canvas(root, width=bg_photo.width(), height=bg_photo.height())
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# Frame com scroll para os itens, sobre o canvas
container = ttk.Frame(canvas)
vsb = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=vsb.set)
vsb.place(relx=1.0, rely=0, relheight=1.0, anchor="ne")
canvas.create_window((0,0), window=container, anchor="nw")

def on_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))
container.bind("<Configure>", on_configure)

# Entradas de 1 a 31
vcmd = (root.register(validar_input), "%P")
entries = {}
for i in range(1, 32):
    ttk.Label(container, text=f"Item {i}", background="#ffffff").grid(row=i-1, column=0, padx=5, pady=2, sticky="e")
    e = ttk.Entry(container, width=5, validate="key", validatecommand=vcmd)
    e.grid(row=i-1, column=1, padx=5, pady=2)
    entries[i] = e

# Botões
btns = ttk.Frame(root)
btns.place(relx=0.5, rely=1.0, anchor="s", y=-10)
ttk.Button(btns, text="Calcular", command=calcular).pack(side="left", padx=5)
ttk.Button(btns, text="Reiniciar", command=reiniciar).pack(side="left", padx=5)
ttk.Button(btns, text="Sair", command=root.destroy).pack(side="left", padx=5)

root.mainloop()
