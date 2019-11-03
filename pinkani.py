#toto je prvni komentar v gitu yadna velka zmena v programu

import pyglet
from pyglet import gl
from pyglet.window import key
import random

# Velikost okna (v pixelech)
SIRKA = 900
VYSKA = 600

VELIKOST_MICE = 20
TLOUSTKA_PALKY = 10
DELKA_PALKY = 100

RYCHLOST = 100  # v pixelech za sekundu
RYCHLOST_PALKY = RYCHLOST * 1.5  # taky v pixelech za sekundu

DELKA_PULICI_CARKY = 20
VELIKOST_FONTU = 42
ODSAZENI_TEXTU = 30

pozice_palek1 = [0, VYSKA // 2]
pozice_palek2 = [SIRKA, VYSKA // 2]  # vertikalni pozice dvou palek
pozice_mice = [0, 0]  # x, y souradnice micku -- nastavene v reset()

rychlost_mice = [0, 0]  # x, y slozky rychlosti micku -- nastavene v reset()
stisknute_klavesy = set()  # sada stisknutych klaves
skore = [0, 0]  # skore dvou hracu

window = pyglet.window.Window(width=SIRKA, height=VYSKA)


def nakresli_text(text, x, y, pozice_x):
    """Nakresli dany text na danou pozici

    Argument ``pozice_x`` muze byt "left" nebo "right", udava na kterou stranu
    bude text zarovnany
    """
    napis = pyglet.text.Label(
        text,
        font_size=VELIKOST_FONTU,
        x=x, y=y, anchor_x=pozice_x
    )
    napis.draw()


def nakresli_obdelnik(x1, y1, x2, y2):

    # Tady pouzijeme volani OpenGL, ktere je pro nas zatim asi nejjednodussi
    # na pouziti
    gl.glBegin(gl.GL_TRIANGLE_FAN)   # zacni kreslit spojene trojuhelniky
    gl.glVertex2f(int(x1), int(y1))  # vrchol A
    gl.glVertex2f(int(x1), int(y2))  # vrchol B
    gl.glVertex2f(int(x2), int(y2))  # vrchol C, nakresli trojuhelnik ABC
    gl.glVertex2f(int(x2), int(y1))  # vrchol D, nakresli trojuhelnik BCD
    # dalsi souradnice E by nakreslila trojuhelnik CDE, atd.
    gl.glEnd()  # ukonci kresleni trojuhelniku

def vykresli():

    gl.glClear(gl.GL_COLOR_BUFFER_BIT)  # smaz obsah okna (vybarvi na cerno)
    gl.glColor3f(1, 1, 1)  # nastav barvu kresleni na bilou

    # Vykresleni micku
    nakresli_obdelnik(
        pozice_mice[0] - VELIKOST_MICE // 2,
        pozice_mice[1] - VELIKOST_MICE // 2,
        pozice_mice[0] + VELIKOST_MICE // 2,
        pozice_mice[1] + VELIKOST_MICE // 2,
        )
    nakresli_text(
        str(skore[0]),
        x = ODSAZENI_TEXTU,
        y = VYSKA - ODSAZENI_TEXTU - VELIKOST_FONTU,
        pozice_x = 'left',
    )

    nakresli_text(
        str(skore[1]),
        x = SIRKA - ODSAZENI_TEXTU,
        y = VYSKA - ODSAZENI_TEXTU - VELIKOST_FONTU,
        pozice_x = 'right',
    )

    # Vykresleni pulici cary
    for y in range(DELKA_PULICI_CARKY // 2, VYSKA, DELKA_PULICI_CARKY * 2):
        nakresli_obdelnik(
            SIRKA // 2 - 1,
            y,
            SIRKA // 2 + 1,
            y + DELKA_PULICI_CARKY
        )
# palky - udelame si seznam souradnic palek a pro kazdou dvojici souradnic
    # v tom seznamu palku vykreslime

        nakresli_obdelnik(
            pozice_palek1[0] - TLOUSTKA_PALKY,
            pozice_palek1[1] - DELKA_PALKY // 2,
            pozice_palek1[0] + TLOUSTKA_PALKY,
            pozice_palek1[1] + DELKA_PALKY // 2,
        )
        nakresli_obdelnik(
            pozice_palek2[0] - TLOUSTKA_PALKY   ,
            pozice_palek2[1] - DELKA_PALKY // 2,
            pozice_palek2[0] + TLOUSTKA_PALKY,
            pozice_palek2[1] + DELKA_PALKY // 2,
)

def reset():
    pozice_mice[0] = SIRKA // 2
    pozice_mice[1] = VYSKA // 2

    # x-ova rychlost - bud vpravo, nebo vlevo
    if random.randint(0, 1):
        rychlost_mice[0] = RYCHLOST
    else:
        rychlost_mice[0] = -RYCHLOST
    # y-ova rychlost - uplne nahodna
    rychlost_mice[1] = random.uniform(-1, 1) * RYCHLOST

# nastavit vychozi stav pro start hry
reset()

def stisk_klavesy(symbol, modifikatory):
    if symbol == key.W:
        stisknute_klavesy.add(('nahoru', 0))
    if symbol == key.S:
        stisknute_klavesy.add(('dolu', 0))
    if symbol == key.UP:
        stisknute_klavesy.add(('nahoru', 1))
    if symbol == key.DOWN:
        stisknute_klavesy.add(('dolu', 1))

def pusteni_klavesy(symbol, modifikatory):
    if symbol == key.W:
        stisknute_klavesy.discard(('nahoru', 0))
    if symbol == key.S:
        stisknute_klavesy.discard(('dolu', 0))
    if symbol == key.UP:
        stisknute_klavesy.discard(('nahoru', 1))
    if symbol == key.DOWN:
        stisknute_klavesy.discard(('dolu', 1))

def obnov_stav(dt):

# pohyb podle klaves (viz funkce `stisk_klavesy`)
    if ('nahoru', 0) in stisknute_klavesy:
        pozice_palek1[1] += RYCHLOST_PALKY * dt
    if ('dolu', 0) in stisknute_klavesy:
        pozice_palek1[1] -= RYCHLOST_PALKY * dt

    if ('nahoru', 1) in stisknute_klavesy:
        pozice_palek2[1] += RYCHLOST_PALKY * dt
    if ('dolu', 1) in stisknute_klavesy:
        pozice_palek2[1] -= RYCHLOST_PALKY * dt

# dolni zarazka - kdyz je palka prilis dole, nastavime ji na minimum
    if pozice_palek1[1] < DELKA_PALKY / 2:
        pozice_palek1[1] = DELKA_PALKY / 2
# horni zarazka - kdyz je palka prilis nahore, nastavime ji na maximum
    if pozice_palek1[1] > VYSKA - DELKA_PALKY / 2:
        pozice_palek1[1] = VYSKA - DELKA_PALKY / 2

    if pozice_palek2[1] < DELKA_PALKY / 2:
        pozice_palek2[1] = DELKA_PALKY / 2
# horni zarazka - kdyz je palka prilis nahore, nastavime ji na maximum
    if pozice_palek2[1] > VYSKA - DELKA_PALKY / 2:
        pozice_palek2[1] = VYSKA - DELKA_PALKY / 2

  # Odraz micku od sten
    if pozice_mice[1] < VELIKOST_MICE // 2:
        rychlost_mice[1] = abs(rychlost_mice[1])
    if pozice_mice[1] > VYSKA - VELIKOST_MICE // 2:
        rychlost_mice[1] = -abs(rychlost_mice[1])

    palka_min = pozice_mice[1] - VELIKOST_MICE / 2 - DELKA_PALKY / 2
    palka_max = pozice_mice[1] + VELIKOST_MICE / 2 + DELKA_PALKY / 2
    pozice_mice[0] += rychlost_mice[0] * dt
    pozice_mice[1] += rychlost_mice[1] * dt

    # odrazeni vlevo
    if pozice_mice[0] < TLOUSTKA_PALKY + VELIKOST_MICE / 2:
        if palka_min < pozice_palek1[1] < palka_max:
            # palka je na spravnem miste, odrazime micek
            rychlost_mice[0] = abs(rychlost_mice[0])
        else:
            # palka je jinde nez ma byt, hrac prohral
            skore[1] += 1
            reset()

    # odrazeni vpravo
    if pozice_mice[0] > SIRKA - (TLOUSTKA_PALKY + VELIKOST_MICE / 2):
        if palka_min < pozice_palek2[1] < palka_max:
            rychlost_mice[0] = -abs(rychlost_mice[0])
        else:
            skore[0] += 1
            reset()

window.push_handlers(
    on_draw=vykresli,
    on_key_press=stisk_klavesy,
    on_key_release=pusteni_klavesy
)

pyglet.clock.schedule(obnov_stav)
pyglet.app.run()  # vse je nastaveno, at zacne hra
