"""
Uporedna analiza vremenske složenosti operacija nad stekom i redom.

Empirijski se mjeri ukupno vrijeme n operacija za rastuće n:
  - stek: n x push + n x pop (očekivano linearno ukupno -> O(1) po operaciji)
  - red:  n x enqueue + n x dequeue, poređenje:
        * obična lista (dequeue O(n) -> ukupno O(n^2))
        * collections.deque (dequeue O(1) -> ukupno O(n))
Pokretanje:  python -m analiza.benchmark
"""
import gc
import os
import time

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from strukture.stek import Stek
from strukture.red import Red, DequeRed

VELICINE = [1_000, 2_000, 5_000, 10_000, 20_000, 50_000, 100_000]
BROJ_PONAVLJANJA = 5

def _izmjeri(funkcija):
    najbolje = float("inf")
    for _ in range(BROJ_PONAVLJANJA):
        gc.disable()
        start = time.perf_counter()
        funkcija()
        trajanje = time.perf_counter() - start
        gc.enable()
        najbolje = min(najbolje, trajanje)
    return najbolje

def mjeri_stek(n):
    def posao():
        s = Stek()
        for i in range(n):
            s.push(i)
        for _ in range(n):
            s.pop()
    return _izmjeri(posao)

def mjeri_red(klasa, n):
    def posao():
        r = klasa()
        for i in range(n):
            r.enqueue(i)
        for _ in range(n):
            r.dequeue()
    return _izmjeri(posao)

def _nacrtaj(rezultati, naslov, naziv_fajla, log_skala=False):
    plt.figure(figsize=(8, 5))
    for naziv, vremena in rezultati.items():
        plt.plot(VELICINE, [t * 1000 for t in vremena], marker="o", label=naziv)
    plt.xlabel("Broj operacija (n)")
    plt.ylabel("Ukupno vrijeme (ms)")
    plt.title(naslov)
    if log_skala:
        plt.yscale("log")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    os.makedirs("rezultati", exist_ok=True)
    putanja = f"rezultati/{naziv_fajla}"
    plt.savefig(putanja, dpi=150)
    plt.close()
    print(f"  Snimljen grafik: {putanja}")

def main():
    print("STEK: n x push + n x pop")
    print("****************************")
    stek_rezultati = {"Stek (Python lista)": []}
    for n in VELICINE:
        t = mjeri_stek(n)
        stek_rezultati["Stek (Python lista)"].append(t)
        print(f"  n={n:>7}: {t*1000:8.2f} ms")
    _nacrtaj(stek_rezultati,
             "Stek: ukupno vrijeme raste linearno -> O(1) po operaciji",
             "stek_slozenost.png")

    print("RED: n x enqueue + n x dequeue")
    print("****************************")
    red_rezultati = {
        "Obična lista (dequeue O(n))": [],
        "collections.deque (dequeue O(1))": [],
    }
    for n in VELICINE:
        t_lista = mjeri_red(Red, n)
        t_deque = mjeri_red(DequeRed, n)
        red_rezultati["Obična lista (dequeue O(n))"].append(t_lista)
        red_rezultati["collections.deque (dequeue O(1))"].append(t_deque)
        print(f"  n={n:>7}: lista={t_lista*1000:8.2f} ms   deque={t_deque*1000:8.2f} ms")
    _nacrtaj(red_rezultati, "Red: obična lista (O(n²) ukupno) vs deque (O(n) ukupno)",
             "red_poredjenje.png")
    _nacrtaj(red_rezultati, "Red: poređenje (logaritamska skala)",
             "red_poredjenje_log.png", log_skala=True)
    print("\nGotovo. Grafici iz 'rezultati/' ubačeni su u pisani dio rada.")
    
if __name__ == "__main__":
    main()
