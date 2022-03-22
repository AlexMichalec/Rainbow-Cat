import pygame
import random
import time


class Kotel:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.wysokosc = 45
        self.szerokosc = 75
        self.ksztalt = pygame.Rect(self.x, self.y, self.szerokosc, self.wysokosc)
        self.grafika = pygame.image.load("kotel.png")

    def rysuj(self):
        screen.blit(self.grafika, (self.x, self.y))

    def ruch(self, vx, vy):
        self.y = self.y + vy
        self.x = self.x + vx
        self.x = max(0, self.x)
        self.x = min(szer - self.szerokosc, self.x)
        self.ksztalt = pygame.Rect(self.x, self.y, self.szerokosc, self.wysokosc)


class Moneta:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.wysokosc = 10
        self.szerokosc = 10
        self.ksztalt = pygame.Rect(self.x, self.y, self.szerokosc, self.wysokosc)
        self.wartosc = random.choice((1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 5))
        if self.wartosc == 1:
            self.grafika = pygame.image.load("moneta1.png")
        elif self.wartosc == 2:
            self.grafika = pygame.image.load("moneta2.png")
        else:
            self.grafika = pygame.image.load("moneta5.png")

    def rysuj(self):
        screen.blit(self.grafika, (self.x, self.y))

    def ruch(self, v):
        self.x = self.x - v
        self.ksztalt = pygame.Rect(self.x, self.y, self.szerokosc, self.wysokosc)

    def kolizja(self, player):
        if self.ksztalt.colliderect(player):
            return True
        else:
            return False


class Przeszkoda:
    def __init__(self, x, szerokosc, wysok=random.randint(10, 290)):
        self.x = x
        self.szerokosc = szerokosc
        self.y_gora = 0
        wysok = min(470 + random.randint(-40, 40), wysok)
        wysok = max(20 + random.randint(-40, 40), wysok)
        self.wys_gora = wysok
        self.odstep = 400
        self.y_dol = self.wys_gora + self.odstep
        self.y_dol = min(self.y_dol, 760 + random.randint(-40, 40))

        self.wys_dol = wys - self.y_dol
        self.kolor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.ksztalt_gora = pygame.Rect(self.x, self.y_gora, self.szerokosc, self.wys_gora)
        self.ksztalt_dol = pygame.Rect(self.x, self.y_dol, self.szerokosc, self.wys_dol)
        self.mb = 0

    def rysuj(self):
        pygame.draw.rect(screen, self.kolor, self.ksztalt_gora, self.mb)
        pygame.draw.rect(screen, self.kolor, self.ksztalt_dol, self.mb)

    def ruch(self, v):
        self.x = self.x - v
        self.ksztalt_gora = pygame.Rect(self.x, self.y_gora, self.szerokosc, self.wys_gora)
        self.ksztalt_dol = pygame.Rect(self.x, self.y_dol, self.szerokosc, self.wys_dol)

    def kolizja(self, player):
        if self.ksztalt_gora.colliderect(player) or self.ksztalt_dol.colliderect(player):
            return True
        else:
            return False

    def recolor(self):
        self.kolor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def recolor2(self, r, g, b):
        self.kolor = (r, g, b)


def napisz(tekst, x, y, rozmiar):
    cz = pygame.font.SysFont("Arial", rozmiar)
    rend = cz.render(tekst, True, (153, 217, 234))
    if x != 60 and x != 1000:
        x = (szer - rend.get_rect().width) / 2
    screen.blit(rend, (x, y))


def rysuj_tlo_koniec():
    for i in range(1, 10):
        screen.blit(pygame.image.load("kotel.png"), (random.randint(10, 1190), random.randint(10, 790)))
    screen.blit(pygame.image.load("moneta1.png"), (random.randint(10, 1190), random.randint(10, 790)))
    screen.blit(pygame.image.load("moneta1.png"), (random.randint(10, 1190), random.randint(10, 790)))
    screen.blit(pygame.image.load("moneta1.png"), (random.randint(10, 1190), random.randint(10, 790)))
    screen.blit(pygame.image.load("moneta2.png"), (random.randint(10, 1190), random.randint(10, 790)))
    screen.blit(pygame.image.load("moneta2.png"), (random.randint(10, 1190), random.randint(10, 790)))
    screen.blit(pygame.image.load("moneta5.png"), (random.randint(10, 1190), random.randint(10, 790)))
    screen.blit(pygame.image.load("moneta1.png"), (random.randint(10, 1190), random.randint(10, 790)))
    screen.blit(pygame.image.load("moneta2.png"), (random.randint(10, 1190), random.randint(10, 790)))
    screen.blit(pygame.image.load("moneta5.png"), (random.randint(10, 1190), random.randint(10, 790)))


pygame.init()
szer = 1200
wys = 800
screen = pygame.display.set_mode((szer, wys))
pygame.display.set_caption("Rainbow Cat")

tryb = "menu"
przeszkody = []
monety = []
punkty = 0
high_score = 0
gracz = Kotel(600, 800)
tempo = 0.7
ruch_gracza_y = 0
ruch_gracza_x = 0

tlo_x = 0
tlo_y = 0

przeszkody.append(Przeszkoda(0, szer / 30))
for i in range(1, 31):
    przeszkody.append(Przeszkoda(i * szer / 30, szer / 40 + random.randint(-4, 4),
                                 przeszkody[-1].wys_gora + random.randint(-40, 40)))

zm = 1  # zmiana wyswietlania przeszkod pelne vs ramka
dom_kol = (random.randint(50, 210), random.randint(50, 210), random.randint(50, 210))
czy_dom_kol = False
czy_bw = False
czy_plynny = False

pygame.mixer.music.load("Night Rider Symphony.mp3")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(start=2)

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w, pygame.K_8):
                ruch_gracza_y = -1.5
            if event.key in (pygame.K_DOWN, pygame.K_s, pygame.K_5):
                ruch_gracza_y = 1.5
            if event.key in (pygame.K_RIGHT, pygame.K_d, pygame.K_6):
                ruch_gracza_x = 1.5
            if event.key in (pygame.K_LEFT, pygame.K_a, pygame.K_4):
                ruch_gracza_x = -1.5

            if event.key == pygame.K_c:
                czy_plynny = False
                czy_dom_kol = False
                for p in przeszkody:
                    p.recolor()
            if event.key == pygame.K_b:
                czy_plynny = False
                czy_dom_kol = False
                if czy_bw:
                    for p in przeszkody:
                        p.recolor()
                    czy_bw = False
                else:
                    czy_bw = True
                    for p in przeszkody:
                        r = random.randint(0, 250)
                        p.recolor2(r, r, r)
            if event.key == pygame.K_m:
                czy_plynny = not czy_plynny
                czy_bw = False
            if event.key == pygame.K_n:
                czy_plynny = False
                czy_bw = False
                r = random.randint(50, 210)
                g = random.randint(50, 210)
                b = random.randint(50, 210)
                dom_kol = (r, g, b)
                czy_dom_kol = True
                for p in przeszkody:
                    p.recolor2(r + random.randint(-40, 40), g + random.randint(-40, 40), b + random.randint(-40, 40))
            if event.key == pygame.K_v:
                zm = (zm + 1) % 6
            if event.key == pygame.K_SPACE:
                if tryb != "rozgrywka":
                    gracz = Kotel(500, (przeszkody[15].wys_gora + przeszkody[15].y_dol) / 2)
                    pygame.mixer.music.stop()
                    pygame.mixer.music.unload()
                    pygame.mixer.music.load("14 - The Police - Canary In A Coalmine.mp3")
                    pygame.mixer.music.set_volume(0.8)
                    pygame.mixer.music.play(loops=-1)
                    punkty = 0
                    ruch_gracza_y = 0
                    tempo = 0.7
                    tryb = "rozgrywka"
                else:
                    for p in przeszkody:
                        p.mb = (p.mb + 2) % 4
            if event.key == pygame.K_x:
                pygame.quit()
        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_UP, pygame.K_w, pygame.K_8, pygame.K_DOWN, pygame.K_s, pygame.K_5):
                ruch_gracza_y = 0
            if event.key in (pygame.K_RIGHT, pygame.K_d, pygame.K_6, pygame.K_LEFT, pygame.K_a, pygame.K_4):
                ruch_gracza_x = 0
    screen.fill((0, 0, 0))
    if tryb == 'menu':
        screen.blit(pygame.image.load("tlo3.png"), (tlo_x, tlo_y))
        tlo_x += random.randint(-4, 0)
        tlo_y += random.randint(-4, 0)
        napisz("Naciśnij spację, aby zacząć", 80, 580, 35)
        napisz("by Alex Michalec", 1000, 700, 20)
        grafika = pygame.image.load('kot.jpg')
        h = (szer - grafika.get_rect().width) / 2
        screen.blit(grafika, (h, 80))

    elif tryb == 'rozgrywka':
        for m in monety:
            m.ruch(tempo)
            m.rysuj()
            if m.kolizja(gracz.ksztalt):
                punkty += m.wartosc
                monety.remove(m)
                tempo += 0.03
        for p in przeszkody:
            p.ruch(tempo)
            p.rysuj()
            if p.kolizja(gracz.ksztalt):
                tryb = "koniec"
                monety = []
        for p in przeszkody:
            if p.x <= -p.szerokosc:
                przeszkody.remove(p)
                przeszkody.append((Przeszkoda(szer, szer / 40 + random.randint(-4, 4),
                                              przeszkody[-1].wys_gora + random.randint(-50, 50))))
                if czy_dom_kol:
                    przeszkody[-1].recolor2(dom_kol[0] + random.randint(-40, 40), dom_kol[1] + random.randint(-40, 40),
                                            dom_kol[2] + random.randint(-40, 40))
                if czy_bw:
                    bw = random.randint(0, 250)
                    przeszkody[-1].recolor2(bw, bw, bw)
                else:
                    if czy_plynny:
                        temp = list(przeszkody[-2].kolor)
                        for i in range(0, 3):
                            temp[i] = temp[i] + random.randint(-30, 30)
                            temp[i] = min(255, temp[i])
                            temp[i] = max(50, temp[i])
                        przeszkody[-1].recolor2(*temp)

                if zm == 1:
                    przeszkody[-1].mb = przeszkody[-2].mb
                elif zm == 2:
                    przeszkody[-1].mb = random.choice((0, 0, 0, 0, 0, 0, 2))
                elif zm == 3:
                    przeszkody[-1].mb = random.choice((0, 0, 0, 0, 0, 0, 1, 2, 3, 4, 5))
                elif zm == 4:
                    przeszkody[-1].mb = random.choice((0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10))
                elif zm == 5:
                    if przeszkody[-3].mb == 0:
                        przeszkody[-1].mb = random.choice((0, 0, 0, 0, 0, 0, 1, 2, 3, 4, 5))

                monety.append(Moneta(szer + 10, random.randint(250, 650)))
                if monety[-1].kolizja(przeszkody[-1].ksztalt_dol) or monety[-1].kolizja(przeszkody[-1].ksztalt_gora):
                    monety.pop()

        for m in monety:
            if m.x <= -m.szerokosc:
                monety.remove(m)
        gracz.rysuj()
        gracz.ruch(ruch_gracza_x, ruch_gracza_y)
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(50, 50, 100, 50), 0)
        napisz(str(punkty), 60, 50, 40)
    elif tryb == "koniec":
        pygame.mixer.music.stop()
        rysuj_tlo_koniec()
        high_score = max(high_score, punkty)
        napisz("Najlepszy wynik: " + str(high_score), 50, 50, 20)
        napisz("Twój wynik: " + str(punkty), 50, 90, 20)
        napisz("x - wyjscie", 50, 750, 20)
        napisz("Kliknij spację by zagrać jeszcze raz ^^", 100, random.randint(100, 700), 30)
        time.sleep(0.7)

    pygame.display.update()
    clock.tick(300)
