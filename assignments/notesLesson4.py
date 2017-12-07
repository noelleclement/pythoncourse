"""

eindopdracht
deze dingen moeten op deze manier en niet anders
leren om dingen ECHT realtime te doen, niet afhankelijk van processor snelheid, met de klok van processor
begin van de lus de tijd aanvragen, dus in de lus overal even laat, dus al die statements in de lus gebeuren om die tijd
die manier verschilt per omgeving / taal
python of pyglet methode gebruiken

oldTime = currrentTime ?
currentTime = time() #oid
hierdoor weet je delta tijd/x:
deltaTime = currentTime-oldTime

functiewaarde * deltaTime

als je de verplaatsing wilt weten: afstand / deltaTime oid

houd rekening met een multitasking computer!
geen gemiddelde, differentieren en integreren met deltatijd
kleine delay om niet alle processortijd op te slokken mag wel


ev mogelijk:
simulatie ontkoppelen van visualisatie
niet meer dan 20 fps visueel
meerdere threads (beelden en physics apart)

"""

"""
vb:
github jdeh > lightOn, staat pong in


pyglet.clock.schedule_interval (self.upate, 1/60.) 
update(self, deltaT) is arduino loop functie

plaats is de integraal van de snelheid
"""

"""
tussenstapjes game:

sprite (in pyglet) is iets wat over beeld kan bewegen
- pyglet library installeren
- prog met sprite (bewegend object maken)
- classenstructuur maken (zie pong1)

- iets in die classen stoppen, maar wel geldig (dus stapje voor stapje, en altijd moet t draaien) (pong2)
- veel commenten (altijd weten wat alles doet)

- kijken of er dingen gemeenschappelijk zijn (inheritance gebruiken), zoveel mogelijk code dublicatie vermijden (pong3)
- attributen moeten zoveel mogelijk zelf doen, game zo min mogelijk

- bij update: predict, interact, commit (wat gaat er gebeuren, mag dat gebeuren, doen)

meerder ballen? meerdere paddles? vantevoren vragen? levels?
pong? breakout? mario?


"""

"""
opdracht:
pyglet install
speelveld maken (Field, Ball)
1 sprite maken en die laten bewegen, en die bijv interactief met muren van scherm

nadenken wel objecten nodig zijn, en welk spel maken, hoe ga je objecten benoemen, 
"""


"""
eindopdracht

een realtime game
vb mario kart

vb: asteroid , maanlander, frogger (crossyroad), 3d vliegen
"""
