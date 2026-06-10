import tkinter as tk
from tkinter import messagebox

from strukture.stek import Stek
from gui.zajednicko import (NARANDZASTA, ZELENA, PLAVA, CRVENA, SIVA, TAMNA,
                            FONT_NASLOV, FONT_BLOK, FONT_OZNAKA, FONT_STATUS,
                            FONT_INFO, zaobljeni_pravougaonik, dugme, legenda)

SIRINA_BLOKA = 190
VISINA_BLOKA = 44
RAZMAK = 10
KORAK = 14        
INTERVAL = 12     
KAPACITET = 6    

class StekPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="white")
        self.stek = Stek()
        self.animacija = False
        self._napravi_interfejs()

    def _napravi_interfejs(self):
        tk.Label(self, text="Vizuelizacija operacija nad stekom (LIFO)",
                 font=FONT_NASLOV, bg="white", fg=TAMNA).pack(pady=(14, 4))
        self.platno = tk.Canvas(self, bg="white", highlightthickness=0,
                                width=560, height=440)
        self.platno.pack(fill=tk.BOTH, expand=True)
        self.platno.bind("<Configure>", lambda e: self.nacrtaj())

        legenda(self, [(NARANDZASTA, "U steku"), (ZELENA, "Push"),
                       (PLAVA, "Vrh / Peek"), (CRVENA, "Pop")]).pack(pady=2)

        kontrole = tk.Frame(self, bg="white")
        kontrole.pack(pady=8)
        self.unos = tk.Entry(kontrole, width=16, font=("Helvetica", 11),
                             relief=tk.SOLID, bd=1)
        self.unos.pack(side=tk.LEFT, padx=(0, 10), ipady=4)
        self.unos.bind("<Return>", lambda e: self.push())
        dugme(kontrole, "Push", ZELENA, self.push).pack(side=tk.LEFT, padx=4)
        dugme(kontrole, "Pop", CRVENA, self.pop).pack(side=tk.LEFT, padx=4)
        dugme(kontrole, "Peek", PLAVA, self.peek).pack(side=tk.LEFT, padx=4)
        dugme(kontrole, "Reset", SIVA, self.reset).pack(side=tk.LEFT, padx=4)

        self.status = tk.Label(self, text="Stek je prazan.", font=FONT_STATUS,
                               bg="white", fg=TAMNA)
        self.status.pack()
        self.info = tk.Label(self, text="Veličina steka: 0", font=FONT_INFO,
                             bg="white", fg="#666666")
        self.info.pack(pady=(0, 10))

    def _kontejner(self):
        sirina = self.platno.winfo_width() or 560
        x0 = (sirina - SIRINA_BLOKA) / 2 - 16
        x1 = (sirina + SIRINA_BLOKA) / 2 + 16
        y1 = (self.platno.winfo_height() or 440) - 28
        y0 = y1 - KAPACITET * (VISINA_BLOKA + RAZMAK) - 10
        return x0, y0, x1, y1

    def _pozicija_bloka(self, indeks_od_dna):
        kx0, _, kx1, ky1 = self._kontejner()
        x0 = (kx0 + kx1) / 2 - SIRINA_BLOKA / 2
        y1 = ky1 - 10 - indeks_od_dna * (VISINA_BLOKA + RAZMAK)
        return x0, y1 - VISINA_BLOKA, x0 + SIRINA_BLOKA, y1

    def nacrtaj(self):
        self.platno.delete("all")
        kx0, ky0, kx1, ky1 = self._kontejner()
        sredina = (kx0 + kx1) / 2
        self.platno.create_line(kx0, ky0, kx0, ky1, fill="#cccccc", width=2)
        self.platno.create_line(kx0, ky1, kx1, ky1, fill="#cccccc", width=2)
        self.platno.create_line(kx1, ky0, kx1, ky1, fill="#cccccc", width=2)
        self.platno.create_text(sredina, ky0 - 12, text="\u2191 TOP",
                                fill="#aaaaaa", font=FONT_OZNAKA)
        self.platno.create_text(sredina, ky1 + 14, text="\u22a5 BOTTOM",
                                fill="#aaaaaa", font=FONT_OZNAKA)

        elementi = list(self.stek)
        for i, element in enumerate(elementi):
            vrh_je = (i == len(elementi) - 1)
            x0, y0, x1, y1 = self._pozicija_bloka(i)
            boja = PLAVA if vrh_je else NARANDZASTA
            zaobljeni_pravougaonik(self.platno, x0, y0, x1, y1, r=10, fill=boja)
            self.platno.create_text((x0+x1)/2, (y0+y1)/2, text=str(element),
                                    fill="white", font=FONT_BLOK)
            if vrh_je:
                self.platno.create_text(sredina, ky0 - 30,
                                        text=f"\u27f6  TOP = {element}",
                                        fill=PLAVA, font=("Helvetica", 11, "bold"))

        self.info.config(text=f"Veličina steka: {len(elementi)}")
    def push(self):
        if self.animacija:
            return
        vrijednost = self.unos.get().strip()
        if not vrijednost:
            messagebox.showwarning("Prazan unos", "Unesite vrijednost za push.")
            return
        if len(self.stek) >= KAPACITET:
            self.status.config(text="Stek je pun (kapacitet prikaza).", fg=CRVENA)
            return
        self.unos.delete(0, tk.END)

        self.stek.push(vrijednost)
        indeks = len(self.stek) - 1
        x0, y0_cilj, x1, _ = self._pozicija_bloka(indeks)
        self.status.config(text=f"Push: element {vrijednost} dodat na vrh.", fg=TAMNA)
        self._animiraj(vrijednost, x0, x1, -VISINA_BLOKA, y0_cilj, ZELENA)

    def pop(self):
        if self.animacija:
            return
        if self.stek.is_empty():
            self.status.config(text="Stek je prazan: Pop nije moguć (underflow).",
                               fg=CRVENA)
            return
        indeks = len(self.stek) - 1
        x0, y0, x1, _ = self._pozicija_bloka(indeks)
        vrijednost = self.stek.pop()
        self.status.config(text=f"Pop: element {vrijednost} skinut sa vrha.", fg=TAMNA)
        self.nacrtaj()
        self._animiraj(vrijednost, x0, x1, y0, -VISINA_BLOKA - 10, CRVENA)

    def peek(self):
        if self.stek.is_empty():
            self.status.config(text="Stek je prazan: Nema vrha.", fg=CRVENA)
            return
        self.status.config(text=f"Peek: na vrhu steka je {self.stek.peek()}.", fg=PLAVA)

    def reset(self):
        self.stek = Stek()
        self.status.config(text="Stek je ispražnjen.", fg=TAMNA)
        self.nacrtaj()
    def _animiraj(self, tekst, x0, x1, y_od, y_do, boja):
        self.animacija = True
        blok = zaobljeni_pravougaonik(self.platno, x0, y_od, x1,
                                      y_od + VISINA_BLOKA, r=10, fill=boja)
        natpis = self.platno.create_text((x0+x1)/2, y_od + VISINA_BLOKA/2,
                                         text=str(tekst), fill="white", font=FONT_BLOK)
        smjer = 1 if y_do > y_od else -1

        def korak(y):
            y_novo = y + smjer * KORAK
            gotovo = (smjer == 1 and y_novo >= y_do) or (smjer == -1 and y_novo <= y_do)
            if gotovo:
                y_novo = y_do
            self.platno.move(blok, 0, y_novo - y)
            self.platno.move(natpis, 0, y_novo - y)
            if gotovo:
                self.platno.delete(blok)
                self.platno.delete(natpis)
                self.animacija = False
                self.nacrtaj()
            else:
                self.platno.after(INTERVAL, korak, y_novo)
        korak(y_od)
