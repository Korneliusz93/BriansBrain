#! /usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import pygame
import sys
import random
from pygame.locals import *  # udostępnienie nazw metod z locals

# inicjacja modułu pygame
pygame.init()

# szerokość i wysokość okna gry
OKNOGRY_SZER = 800
OKNOGRY_WYS = 400

# przygotowanie powierzchni do rysowania, czyli inicjacja okna gry
OKNOGRY = pygame.display.set_mode((OKNOGRY_SZER, OKNOGRY_WYS), 0, 32)
# tytuł okna gry
pygame.display.set_caption('Gra w życie')

# rozmiar komórki
ROZ_KOM = 10
# ilość komórek w poziomie i pionie
KOM_POZIOM = int(OKNOGRY_SZER / ROZ_KOM)
KOM_PION = int(OKNOGRY_WYS / ROZ_KOM)

# wartości oznaczające komórki "martwe" i "żywe"
KOM_MARTWA = 0
KOM_STYGNIE = 1
KOM_ZYWA = 2

# lista opisująca stan pola gry, 0 - komórki martwe, 1 - komórki żywe
# na początku tworzymy listę zawierającą KOM_POZIOM zer
POLE_GRY = [KOM_MARTWA] * KOM_POZIOM
# rozszerzamy listę o listy zagnieżdżone, otrzymujemy więc listę dwuwymiarową
for i in range(KOM_POZIOM):
    POLE_GRY[i] = [KOM_MARTWA] * KOM_PION
    
    # przygotowanie następnej generacji komórek, czyli zaktualizowanego POLA_GRY
def mozg(polegry):
    # na początku tworzymy 2-wymiarową listę wypełnioną zerami
    nast_gen = [KOM_MARTWA] * KOM_POZIOM
    for i in range(KOM_POZIOM):
        nast_gen[i] = [KOM_MARTWA] * KOM_PION
    
    # iterujemy po wszystkich komórkach
    for y in range(KOM_PION):
        for x in range(KOM_POZIOM):
    
            # zlicz populację (żywych komórek) wokół komórki
            populacja = 0
            # wiersz 1
            try:
                if polegry[x - 1][y - 1] == KOM_ZYWA:
                    populacja += 1
            except IndexError:
                pass
            try:
                if polegry[x][y - 1] == KOM_ZYWA:
                    populacja += 1
            except IndexError:
                pass
            try:
                if polegry[x + 1][y - 1] == KOM_ZYWA:
                    populacja += 1
            except IndexError:
                pass
    
            # wiersz 2
            try:
                if polegry[x - 1][y] == KOM_ZYWA:
                    populacja += 1
            except IndexError:
                pass
            try:
                if polegry[x + 1][y] == KOM_ZYWA:
                    populacja += 1
            except IndexError:
                pass
    
            # wiersz 3
            try:
                if polegry[x - 1][y + 1] == KOM_ZYWA:
                    populacja += 1
            except IndexError:
                pass
            try:
                if polegry[x][y + 1] == KOM_ZYWA:
                    populacja += 1
            except IndexError:
                pass
            try:
                if polegry[x + 1][y + 1] == KOM_ZYWA:
                    populacja += 1
            except IndexError:
                pass
    
            # "niedoludnienie" lub przeludnienie = śmierć komórki
            if polegry[x][y] == KOM_MARTWA and (populacja == 2):
                nast_gen[x][y] = KOM_ZYWA
            # życie trwa
            elif polegry[x][y] == KOM_ZYWA:
                nast_gen[x][y] = KOM_STYGNIE
            # nowe życie
            elif polegry[x][y] == KOM_STYGNIE:
                nast_gen[x][y] = KOM_MARTWA
    
    #wywolanie funkcji rysujacej komorki
    rysujMozg(nast_gen) 
    logging.warning('works once')  # will print a message to the console
    # zwróć nowe polegry z następną generacją komórek
    pygame.display.update()
    pygame.time.delay(100)    
    return nast_gen
    
def rysujMozg(pole):
    """Rysowanie komórek (kwadratów) żywych"""
    for y in range(KOM_PION):
        for x in range(KOM_POZIOM):
            if pole[x][y] == KOM_ZYWA:
                logging.warning('works twice')  
                pygame.draw.rect(OKNOGRY, (66, 242, 245), [x * ROZ_KOM, y * ROZ_KOM,ROZ_KOM,ROZ_KOM])
            if pole[x][y] == KOM_STYGNIE:
                logging.warning('works twice')  
                pygame.draw.rect(OKNOGRY, (245, 66, 66), [x * ROZ_KOM, y * ROZ_KOM,ROZ_KOM,ROZ_KOM])
                
# zmienne sterujące wykorzystywane w pętli głównej
zycie_trwa = False
przycisk_wdol = False
                
# pętla główna programu
while True:
    # obsługa zdarzeń generowanych przez gracza
    for event in pygame.event.get():
        # przechwyć zamknięcie okna
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
                
        if event.type == KEYDOWN and event.key == K_RETURN:
            zycie_trwa = True
                
        if zycie_trwa is False:
            if event.type == MOUSEBUTTONDOWN:
                przycisk_wdol = True
                przycisk_typ = event.button
                
            if event.type == MOUSEBUTTONUP:
                przycisk_wdol = False
                
            if przycisk_wdol:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                mouse_x = int(mouse_x / ROZ_KOM)
                mouse_y = int(mouse_y / ROZ_KOM)
                # lewy przycisk myszy ożywia
                if przycisk_typ == 1:
                    POLE_GRY[mouse_x][mouse_y] = KOM_ZYWA
                # prawy przycisk myszy uśmierca
                if przycisk_typ == 3:
                    POLE_GRY[mouse_x][mouse_y] = KOM_MARTWA
 
    OKNOGRY.fill((1, 1, 1))  # ustaw kolor okna gry
    if zycie_trwa is False: 
        rysujMozg(POLE_GRY)
        pygame.display.update()
        pygame.time.delay(100)        
    if zycie_trwa is True:
        POLE_GRY = mozg(POLE_GRY)
