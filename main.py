#################################################################################
#   Class main from Bomberman                                                   #
#   Created by Vincent : 24/01/2020                                             #
#                                                                               #
#   Cette classe est la classe principale du jeu, elle permet de definir le     #
#   le decor, et contient la boucle du jeu                                      #
#                                                                               #
#################################################################################

#################################################################################
##
## Import

import pygame
from pygame import *
import os
import random
from random import randrange
import copy
from copy import deepcopy
import time
from Player import Player
from Bombe import Bombe
from Player import IA
pygame.init()

#################################################################################
##
##  Importation des images et musiques:

# Decort
BLOCK = pygame.image.load("images/blocks/stone.png")
BLOCK_MIDDLE = pygame.image.load("images/blocks/stone2.png")
GRASS = pygame.image.load("images/blocks/grass.png")
BLOCK_BRICK = pygame.image.load("images/blocks/brick.png")

# Sprites
BLEU = pygame.image.load("images/ia/Bleu/sprite.png")
ROUGE = pygame.image.load("images/ia/Rouge/sprite.png")
JAUNE = pygame.image.load("images/ia/Jaune/sprite.png")
ORANGE = pygame.image.load("images/ia/Orange/sprite.png")
BOMBES = pygame.image.load("images/bombe/bomb.png")
FIRE =pygame.image.load("images/fire/explosion2.png")
# Musique
pygame.mixer.init()
SON_FOND = pygame.mixer.Sound("son/bomberman.wav")
SON_BOMBE = pygame.mixer.Sound("son/bombe.wav")

SON_FOND.play(loops=-1, maxtime = 0, fade_ms=0)
#################################################################################
##
##  Variables globales

# TAB est la matrice permettant de former la carte
# 0 vide
# 1 mur exterieur
# 2 mur interieur
# 3 briques destructibles
# 4 Bombes
# 5 Explosion

TAB = [ [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,2,0,2,0,2,0,2,0,2,0,2,0,2,2,0,2,0,2,0,2,0,2,0,2,0,2,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,2,0,2,0,2,0,2,0,2,0,2,0,2,2,0,2,0,2,0,2,0,2,0,2,0,2,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,2,0,2,0,2,0,2,0,2,0,2,0,2,2,0,2,0,2,0,2,0,2,0,2,0,2,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,2,0,2,0,2,0,2,0,2,0,2,0,2,2,0,2,0,2,0,2,0,2,0,2,0,2,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,2,0,2,0,2,0,2,0,2,0,2,0,2,2,0,2,0,2,0,2,0,2,0,2,0,2,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,2,0,2,0,2,0,2,0,2,0,2,0,2,2,0,2,0,2,0,2,0,2,0,2,0,2,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]


HAUTEUR = len(TAB)     # Nombre de cases en hauteur
LARGEUR = len(TAB[0])  # Nombre de cases en largeur

SCREEN_WIDTH = pygame.display.Info().current_w
SCREEN_HEIGHT = pygame.display.Info().current_h - 100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT), RESIZABLE)

ZOOM = int((64/1920)*SCREEN_WIDTH)   # Taille d'une case en pixels

GREEN = [0, 255, 0]
WHITE = [255, 255, 255]
BLACK = [0, 0, 0]

TIME = 0
VIT = 4

FONT = pygame.font.SysFont("arial", 50)
CLOCK = pygame.time.Clock()
TIME = time.time()
DONE = False

#info_ia = [(720,350,JAUNE),(1450,102,ROUGE),(1450,700,VERT),(96,700,ORANGE)]
LIST_BOMB = []
LIST_IA = []
LIST_JOUEUR = []

JOUEUR_BLEU = Player(1, 1, BLEU,int(ZOOM*(102/64)), ZOOM)
JOUEUR_JAUNE = IA(1, 1, JAUNE,int(ZOOM*(102/64)), ZOOM, (0,1))
JOUEUR_ORANGE = IA(1, 1, ORANGE,int(ZOOM*(102/64)), ZOOM,(1,0))
JOUEUR_ROUGE = IA(1, 1, ROUGE,int(ZOOM*(102/64)), ZOOM,(-1,0))

# grille contenant les distances aux bombes sur la map
GRILLE_BOMBE = None
#################################################################################
##
##  Fonctions principales

# dessine():
#   Parcourt TAB et place les images aux coordonnees idoines
#   en fonction de la valeur des cases du tableau
#   Puis place les JOUEUR_s
def draw():
    for i in range(LARGEUR):
        for j in range(HAUTEUR):
            if(TAB[j][i] == 0 or TAB[j][i] == 4 or TAB[j][i] ==  5): SCREEN.blit(GRASS,(i*ZOOM,j*ZOOM))
            if(TAB[j][i] == 1): SCREEN.blit(BLOCK,(i*ZOOM,j*ZOOM))
            if(TAB[j][i] == 2): SCREEN.blit(BLOCK_MIDDLE,(i*ZOOM,j*ZOOM))
            if(TAB[j][i] == 3): SCREEN.blit(BLOCK_BRICK,(i*ZOOM,j*ZOOM))

    SCREEN.blit(FONT.render(str(TIME // 1), True, WHITE), ((1920 // 2) - 25 , 64*HAUTEUR + 32))

    for bomb in LIST_BOMB:
        bomb.anim(TIME)
        bomb.draw(SCREEN)
        removeBomb()
        for i in range(bomb.rayon):

            bomb.drawExplo(SCREEN,TAB,LIST_BOMB, i,(1+i),ZOOM)
            bomb.drawExplo(SCREEN,TAB, LIST_BOMB, i,-(1+i),ZOOM)



    for joueur in LIST_JOUEUR:

        joueur.draw(SCREEN, ZOOM//2, int(ZOOM*(102/ZOOM)), ZOOM)

    pygame.display.flip() # Rafraichis l'affichage de Pygame

def generate():
    for i in range(LARGEUR):
        for j in range(HAUTEUR):
            if(TAB[j][i] == 0 and random.randrange(2)): TAB[j][i] = 3
    TAB[1][1] = 0; TAB[1][2] = 0; TAB[2][1] = 0
    TAB[HAUTEUR-2][1] = 0; TAB[HAUTEUR-2][2] = 0; TAB[HAUTEUR-3][1] = 0
    TAB[1][LARGEUR-2] = 0; TAB[1][LARGEUR-3] = 0; TAB[2][LARGEUR-2] = 0
    TAB[HAUTEUR-2][LARGEUR-2] = 0; TAB[HAUTEUR-3][LARGEUR-2] = 0; TAB[HAUTEUR-2][LARGEUR-3] = 0

# regarde chaque bombe de la liste et si la bombe explose, l'enleve de la liste des BOMBES
def removeBomb():
    for Bomb in LIST_BOMB:
        if (Bomb.Explode() == True):

            Bomb.spriteCount = 0
            Bomb.spriteDir=0
            Bomb.sprite= Bomb.getSpriteExplo(FIRE, ZOOM)
            #SON_BOMBE.play()
            TAB[Bomb.caseY][Bomb.caseX] = 5
            Bomb.explode = False
            Bomb.player.nbBombe -= 1


        if(Bomb.exploFin):
            TAB[Bomb.caseY][Bomb.caseX] = 0
            LIST_BOMB.remove(Bomb)

def poseBombe(player):
    caseX = player.caseY
    caseY = player.caseX
    if(TAB[caseY][caseX] == 0 and player.nbBombe < player.nbBombeMax):
        LIST_BOMB.append(Bombe(caseX*ZOOM+100,caseY*ZOOM+96,BOMBES, ZOOM, TIME,player))
        TAB[caseY][caseX] = 4
        player.nbBombe += 1

def Meurt(player):
    x = player.caseY
    y = player.caseX
    if(TAB[y][x]==5):
        player.lives -= 1
        if player.lives == 0:
            if(player in LIST_JOUEUR):
                LIST_JOUEUR.remove(player)
            if(player in LIST_IA):
                LIST_IA.remove(player)

def iaDanger(ia): return GRILLE_BOMBE[ia.caseX][ia.caseY] <= 4

def iaFuite(ia) :
    if(ia.x != 0 or ia.y !=0): ia.needToGoCenter = True
    else:ia.needToGoCenter = False

    possibleMove = getPossibleMove(ia)
    posIA = (ia.caseY,ia.caseX)
    max = 0
    caseMax = None  
    for case in possibleMove :
        if GRILLE_BOMBE[posIA[1] + case[1]][posIA[0] + case[0]] > max and GRILLE_BOMBE[posIA[1] + case[1]][posIA[0] + case[0]] < 100:
            max = GRILLE_BOMBE[posIA[1] + case[1]][posIA[0] + case[0]]
            caseMax = case
    if(caseMax != None and not ia.needToGoCenter):
        ia.dir = caseMax
        ia.move(caseMax[0]*VIT, caseMax[1]*VIT,ZOOM)
        ia.setRightDir()
    else:
        ia.move(ia.dir[0]*VIT, ia.dir[1]*VIT,ZOOM)


def moveIA(ia):
    if iaDanger(ia) :  iaFuite(ia)
    else :
        possibleMove = getPossibleMove(ia)
        if (ia.dir in possibleMove):
            ia.move(ia.dir[0]*VIT, ia.dir[1]*VIT,ZOOM)
        else:
            poseBombe(ia)
            if(len(possibleMove) !=0 ):
                deplacement_ia = random.randrange(len(possibleMove))
                ia.dir = possibleMove[deplacement_ia]
                ia.setRightDir()
            else:
                ia.dir = (0,0)



def getPossibleMove(player):
    possibleMove = []
    tab = []

    tab.append(TAB[player.caseX+1][player.caseY])
    tab.append(TAB[player.caseX-1][player.caseY])
    tab.append(TAB[player.caseX][player.caseY+1])
    tab.append(TAB[player.caseX][player.caseY-1])

    if((tab[0]  == 0 or tab[0]  == 5 or player.y != 0) and player.x == 0): possibleMove.append((0,1))
    if((tab[1]  == 0 or tab[1]  == 5 or player.y != 0) and player.x == 0): possibleMove.append((0,-1))
    if((tab[2]  == 0 or tab[2]  == 5 or player.x != 0) and player.y == 0): possibleMove.append((1,0))
    if((tab[3]  == 0 or tab[3]  == 5 or player.x != 0) and player.y == 0): possibleMove.append((-1,0))

    return possibleMove

def grilleBombe():
    global GRILLE_BOMBE
    GRILLE_BOMBE = copy.deepcopy(TAB)
    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            if (TAB[y][x] == 4 or TAB[y][x] == 5): GRILLE_BOMBE[y][x] = 0
            if (TAB[y][x] == 1 or TAB[y][x] == 2 or TAB[y][x] == 3): GRILLE_BOMBE[y][x] = 1000
            if (TAB[y][x] == 0): GRILLE_BOMBE[y][x] = 100

def miseDistance():
    global GRILLE_BOMBE
    done = True
    while done:
        done = False
        for y in range(HAUTEUR):
            for x in range(LARGEUR):
                if (GRILLE_BOMBE[y][x] == 1000): continue
                if (GRILLE_BOMBE[y][x] >= 0):
                    mini = min(GRILLE_BOMBE[y][x+1], GRILLE_BOMBE[y][x-1], GRILLE_BOMBE[y+1][x], GRILLE_BOMBE[y-1][x])
                    if (mini +1 < GRILLE_BOMBE[y][x]):
                        GRILLE_BOMBE[y][x] = mini +1
                        done = True

#################################################################################
##
##  Initialisation

pygame.mouse.set_visible(True)
pygame.display.set_caption("ESIEE - BOMB HERMAN")
#pygame.mixer.music.play()   # Activation de la musique


LIST_IA.append(JOUEUR_JAUNE)#JAUNE
#LIST_IA.append(JOUEUR_ORANGE)#ORANGE
#LIST_IA.append(JOUEUR_ROUGE)#ROUGE

for ia in LIST_IA:
    LIST_JOUEUR.append(ia)
    ia.setRightDir()    # Defini la direction des sprites des ia a l'init

LIST_JOUEUR.append(JOUEUR_BLEU)

generate()
#################################################################################
##
##   Boucle principale


# --------  Main -----------
while not DONE:
    event = pygame.event.Event(pygame.USEREVENT)
    pygame.event.pump()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            DONE = True
            
        if event.type == pygame.VIDEORESIZE:
            SCREEN_HEIGHT = event.h
            SCREEN_WIDTH = event.w
            oldZoom = ZOOM
            ZOOM = int((64/1920)*SCREEN_WIDTH)
            VIT = int(ZOOM / 16)

            for player in LIST_JOUEUR:
                player.x = int(ZOOM * (player.x/oldZoom))
                player.y = int(ZOOM * (player.y/oldZoom))
                player.getSprite(int(ZOOM*(102/64)),ZOOM)

            GRASS = pygame.transform.scale(pygame.image.load("images/blocks/grass.png"),(ZOOM,ZOOM))
            BLOCK_BRICK = pygame.transform.scale(pygame.image.load("images/blocks/brick.png"),(ZOOM,ZOOM))
            BLOCK = pygame.transform.scale(pygame.image.load("images/blocks/stone.png"),(ZOOM,ZOOM))
            BLOCK_MIDDLE = pygame.transform.scale(pygame.image.load("images/blocks/stone2.png"),(ZOOM,ZOOM))
            pygame.display.flip()
            draw()


    grilleBombe()
    miseDistance()

    for ia in LIST_IA:
        moveIA(ia)

    keysPressed = pygame.key.get_pressed()  # On retient les touches pressees

    ## Mouvements du JOUEUR_
    #   On choisit la direction du sprite en fonction de sa position dans le tableau des sprites
    #   On fait appelle a la fonction move pour changer les coordonnees et les sprites

    possibleMove = getPossibleMove(JOUEUR_BLEU)

    if(keysPressed[pygame.K_DOWN]  and (0,1) in possibleMove):
        JOUEUR_BLEU.spriteDir = 0
        JOUEUR_BLEU.move(0,VIT,ZOOM)

    elif(keysPressed[pygame.K_UP] and (0,-1) in possibleMove):
        JOUEUR_BLEU.move(0,-VIT,ZOOM)
        JOUEUR_BLEU.spriteDir = 3

    elif(keysPressed[pygame.K_RIGHT] and (1,0) in possibleMove):
        JOUEUR_BLEU.move(VIT,0,ZOOM)
        JOUEUR_BLEU.spriteDir = 2

    elif(keysPressed[pygame.K_LEFT] and (-1,0) in possibleMove):
        JOUEUR_BLEU.move(-VIT,0,ZOOM)
        JOUEUR_BLEU.spriteDir = 1

    if(keysPressed[pygame.K_SPACE]):
        if JOUEUR_BLEU in LIST_JOUEUR :
            poseBombe(JOUEUR_BLEU)

    for ia in LIST_IA:
        Meurt(ia)

    #print()
    #for i in range(len(TAB)):
    #    print(TAB[i])

    Meurt(JOUEUR_BLEU)

    SCREEN.fill(BLACK)
    TIME = time.time()
    draw()   # On redessine l'affichage et on actualise
    CLOCK.tick(30) # Limite d'image par seconde

    #a mettre quand le personnage est mort : pygame.mixer.music.stop()


pygame.quit() # Ferme la fenetre et quitte.