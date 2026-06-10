# Paleta boja 
NARANDZASTA = "#FF8C00"   # element u strukturi
ZELENA      = "#1E9E6A"   # upravo dodat (push / enqueue)
PLAVA       = "#1F5FA8"   # vrh steka / head reda (peek)
CRVENA      = "#E2504C"   # upravo skinut (pop / dequeue)
SIVA        = "#9E9E9E"   # reset dugme
TAMNA       = "#212121"   # naslovi i status
SVIJETLA    = "#F5F5F5"   # pozadina panela

FONT_NASLOV = ("Helvetica", 16, "bold")
FONT_BLOK   = ("Helvetica", 13, "bold")
FONT_OZNAKA = ("Helvetica", 10)
FONT_STATUS = ("Helvetica", 12, "bold")
FONT_INFO   = ("Helvetica", 10)

def zaobljeni_pravougaonik(platno, x0, y0, x1, y1, r=10, **opcije):
    tacke = [x0+r,y0, x1-r,y0, x1,y0, x1,y0+r, x1,y1-r, x1,y1,
             x1-r,y1, x0+r,y1, x0,y1, x0,y1-r, x0,y0+r, x0,y0]
    return platno.create_polygon(tacke, smooth=True, **opcije)

def dugme(parent, tekst, boja, komanda):
    import tkinter as tk
    return tk.Button(parent, text=tekst, command=komanda, bg=boja, fg="white",
                     activebackground=boja, activeforeground="white",
                     font=("Helvetica", 11, "bold"), relief=tk.FLAT,
                     padx=16, pady=4, cursor="hand2")

def legenda(parent, stavke):
    import tkinter as tk
    okvir = tk.Frame(parent, bg="white")
    for boja, tekst in stavke:
        kvadrat = tk.Canvas(okvir, width=14, height=14, bg="white", highlightthickness=0)
        kvadrat.create_rectangle(1, 1, 13, 13, fill=boja, outline="")
        kvadrat.pack(side=tk.LEFT, padx=(10, 3))
        tk.Label(okvir, text=tekst, bg="white", font=FONT_OZNAKA).pack(side=tk.LEFT)
    return okvir
