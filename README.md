# Vizuelna simulacija rada steka i reda

Projektni zadatak iz predmeta _Strukture podataka i algoritmi_: vizuelna
simulacija rada **steka** (LIFO) i **reda** (FIFO) korišćenjem Python GUI
okruženja (Tkinter), uz **uporednu analizu vremenske složenosti** operacija.

Vizuelni stil aplikacije inspirisan je vizuelizacijom sa portala
GeeksforGeeks (_Introduction to Stack Data Structure_),
ali je kompletna implementacija urađena samostalno u Pythonu/Tkinteru i uz pomoću Claude da bih dostigla željeni izgled vizuelne simulacije.

## Pokretanje

```
python main.py                  # pokreće GUI aplikaciju
python -m analiza.benchmark     # generiše grafike uporedne analize u rezultati/
```

Za benchmark je potreban matplotlib: `pip install matplotlib`

## Struktura projekta

```
strukture/
    stek.py          stek nad Python listom (push, pop, peek)
    red.py           obični red (enqueue, dequeue, čelo) + DequeRed za analizu
gui/
    aplikacija.py    glavni prozor sa tabovima
    zajednicko.py    boje, fontovi, zaobljeni blokovi, legenda
    stek_panel.py    vertikalna vizuelizacija steka sa animacijama
    red_panel.py     horizontalna vizuelizacija reda sa animacijama
analiza/
    benchmark.py     empirijsko mjerenje vremena i crtanje grafika
rezultati/           generisani grafici i screenshotovi
main.py              ulazna tačka
```

## Operacije i složenost

| Struktura | Operacija | Složenost                            |
| --------- | --------- | ------------------------------------ |
| Stek      | push      | O(1) amortizovano                    |
| Stek      | pop       | O(1)                                 |
| Stek      | peek      | O(1)                                 |
| Red       | enqueue   | O(1) amortizovano                    |
| Red       | dequeue   | **O(n)** nad listom / O(1) nad deque |
| Red       | front     | O(1)                                 |

Empirijska mjerenja (n = 100.000 operacija): red nad običnom listom
**≈ 12,6 s**, nad `collections.deque` **≈ 13 ms** - razlika od oko tri
reda veličine koja potvrđuje teorijsku analizu (O(n²) naspram O(n)
ukupno za n uzastopnih dequeue operacija).

## Funkcionalnosti GUI-ja

- dva taba: Stek (LIFO) i Red (FIFO)
- animirane operacije: push/pop (vertikalno), enqueue/dequeue (horizontalno)
- boje po legendi: narandžasto = u strukturi, zeleno = dodavanje,
  plavo = vrh/head (peek/front), crveno = skidanje
- oznake TOP/BOTTOM (stek) i FRONT/REAR (red)
- statusne poruke za svaku operaciju, uključujući underflow (prazna struktura)

## Literatura koja su mi pomogla za implementaciju i vremensku složenost

- M. T. Goodrich, R. Tamassia, M. H. Goldwasser, _Data Structures and
  Algorithms in Python_, Wiley, 2013, str. 250 - 268
- B. Baka, _Python Data Structures and Algorithms_, Packt, 2018, str. 161-189
- GeeksforGeeks: _Introduction to Stack Data Structure_, _Introduction to Queue_,
  _Real-time application of Data Structures_.

## Tutorijali koji su mi takođe pomogli za implementaciju vizuelizacije pomoću Python GUI Tkinter

- https://www.pythonguis.com/tutorials/use-tkinter-to-design-gui-layout/
- https://www.geeksforgeeks.org/python/python-gui-tkinter/
