import tkinter as tk
from tkinter import messagebox

from strukture.red import Red
from gui.zajednicko import (NARANDZASTA, ZELENA, PLAVA, CRVENA, SIVA, TAMNA,
                            FONT_NASLOV, FONT_BLOK, FONT_OZNAKA, FONT_STATUS,
                            FONT_INFO, zaobljeni_pravougaonik, dugme, legenda)
SIRINA_BLOKA = 84
VISINA_BLOKA = 52
RAZMAK = 10
KORAK = 16
INTERVAL = 12
KAPACITET = 7

class RedPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="white")
        self.red = Red()
        self.animacija = False
        self._napravi_interfejs()

    def _napravi_interfejs(self):
        tk.Label(self, text="Vizuelizacija operacija nad redom (FIFO)",
                 font=FONT_NASLOV, bg="white", fg=TAMNA).pack(pady=(14, 4))
        self.platno = tk.Canvas(self, bg="white", highlightthickness=0,
                                width=760, height=300)
        self.platno.pack(fill=tk.BOTH, expand=True)
        self.platno.bind("<Configure>", lambda e: self.nacrtaj())

        legenda(self, [(NARANDZASTA, "U redu"), (ZELENA, "Enqueue"),
                       (PLAVA, "Head / Front"), (CRVENA, "Dequeue")]).pack(pady=2)

        kontrole = tk.Frame(self, bg="white")
        kontrole.pack(pady=8)
        self.unos = tk.Entry(kontrole, width=16, font=("Helvetica", 11),
                             relief=tk.SOLID, bd=1)
        self.unos.pack(side=tk.LEFT, padx=(0, 10), ipady=4)
        self.unos.bind("<Return>", lambda e: self.enqueue())
        dugme(kontrole, "Enqueue", ZELENA, self.enqueue).pack(side=tk.LEFT, padx=4)
        dugme(kontrole, "Dequeue", CRVENA, self.dequeue).pack(side=tk.LEFT, padx=4)
        dugme(kontrole, "Front", PLAVA, self.front).pack(side=tk.LEFT, padx=4)
        dugme(kontrole, "Reset", SIVA, self.reset).pack(side=tk.LEFT, padx=4)

        self.status = tk.Label(self, text="Red je prazan.", font=FONT_STATUS,
                               bg="white", fg=TAMNA)
        self.status.pack()
        self.info = tk.Label(self, text="Veličina reda: 0", font=FONT_INFO,
                             bg="white", fg="#666666")
        self.info.pack(pady=(0, 10))

    def _kontejner(self):
        sirina = self.platno.winfo_width() or 760
        ukupno = KAPACITET * (SIRINA_BLOKA + RAZMAK) + 10
        x0 = (sirina - ukupno) / 2
        visina = self.platno.winfo_height() or 300
        y0 = visina / 2 - VISINA_BLOKA / 2 - 10
        return x0, y0, x0 + ukupno, y0 + VISINA_BLOKA + 20

    def _pozicija_bloka(self, index_head):
        kx0, ky0, _, _ = self._kontejner()
        x0 = kx0 + 10 + index_head * (SIRINA_BLOKA + RAZMAK)
        return x0, ky0 + 10, x0 + SIRINA_BLOKA, ky0 + 10 + VISINA_BLOKA
    
    def nacrtaj(self):
        self.platno.delete("all")
        kx0, ky0, kx1, ky1 = self._kontejner()
        self.platno.create_line(kx0, ky0, kx1, ky0, fill="#cccccc", width=2)
        self.platno.create_line(kx0, ky1, kx1, ky1, fill="#cccccc", width=2)
        self.platno.create_text(kx0 - 28, (ky0+ky1)/2, text="IZLAZ\n\u2190",
                                justify=tk.CENTER, fill="#aaaaaa", font=FONT_OZNAKA)
        self.platno.create_text(kx1 + 28, (ky0+ky1)/2, text="ULAZ\n\u2190",
                                justify=tk.CENTER, fill="#aaaaaa", font=FONT_OZNAKA)

        elementi = list(self.red)
        for i, element in enumerate(elementi):
            is_head = (i == 0)
            x0, y0, x1, y1 = self._pozicija_bloka(i)
            boja = PLAVA if is_head else NARANDZASTA
            zaobljeni_pravougaonik(self.platno, x0, y0, x1, y1, r=10, fill=boja)
            self.platno.create_text((x0+x1)/2, (y0+y1)/2, text=str(element),
                                    fill="white", font=FONT_BLOK)
            if is_head:
                self.platno.create_text((x0+x1)/2, y0 - 26,
                                        text=f"FRONT = {element}",
                                        fill=PLAVA, font=("Helvetica", 10, "bold"))
            if i == len(elementi) - 1:
                self.platno.create_text((x0+x1)/2, y1 + 18, text="REAR",
                                        fill="#1E9E6A", font=("Helvetica", 10, "bold"))

        self.info.config(text=f"Veličina reda: {len(elementi)}")
    def enqueue(self):
        if self.animacija:
            return
        vrijednost = self.unos.get().strip()
        if not vrijednost:
            messagebox.showwarning("Prazan unos", "Unesite vrijednost za enqueue.")
            return
        if len(self.red) >= KAPACITET:
            self.status.config(text="Red je pun (kapacitet prikaza).", fg=CRVENA)
            return
        self.unos.delete(0, tk.END)

        self.red.enqueue(vrijednost)
        indeks = len(self.red) - 1
        x0_cilj, _, _, _ = self._pozicija_bloka(indeks)
        sirina = self.platno.winfo_width() or 760
        self.status.config(text=f"Enqueue: element {vrijednost} dodat na tail.",
                           fg=TAMNA)
        self._animiraj(vrijednost, sirina + 10, x0_cilj, ZELENA)

    def dequeue(self):
        if self.animacija:
            return
        if self.red.is_empty():
            self.status.config(text="Red je prazan: Dequeue nije moguć (underflow).",
                               fg=CRVENA)
            return
        x0, _, _, _ = self._pozicija_bloka(0)
        vrijednost = self.red.dequeue()
        self.status.config(text=f"Dequeue: element {vrijednost} skinut sa head.",
                           fg=TAMNA)
        self.nacrtaj()
        self._animiraj(vrijednost, x0, -SIRINA_BLOKA - 10, CRVENA)

    def front(self):
        if self.red.is_empty():
            self.status.config(text="Red je prazan: Nema head.", fg=CRVENA)
            return
        self.status.config(text=f"Front: na head reda je {self.red.head()}.", fg=PLAVA)

    def reset(self):
        self.red = Red()
        self.status.config(text="Red je ispražnjen.", fg=TAMNA)
        self.nacrtaj()

    def _animiraj(self, tekst, x_od, x_do, boja):
        self.animacija = True
        _, ky0, _, _ = self._kontejner()
        y0 = ky0 + 10
        blok = zaobljeni_pravougaonik(self.platno, x_od, y0, x_od + SIRINA_BLOKA,
                                      y0 + VISINA_BLOKA, r=10, fill=boja)
        natpis = self.platno.create_text(x_od + SIRINA_BLOKA/2, y0 + VISINA_BLOKA/2,
                                         text=str(tekst), fill="white", font=FONT_BLOK)
        smjer = 1 if x_do > x_od else -1

        def korak(x):
            x_novo = x + smjer * KORAK
            gotovo = (smjer == 1 and x_novo >= x_do) or (smjer == -1 and x_novo <= x_do)
            if gotovo:
                x_novo = x_do
            self.platno.move(blok, x_novo - x, 0)
            self.platno.move(natpis, x_novo - x, 0)
            if gotovo:
                self.platno.delete(blok)
                self.platno.delete(natpis)
                self.animacija = False
                self.nacrtaj()
            else:
                self.platno.after(INTERVAL, korak, x_novo)
        korak(x_od)
