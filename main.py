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
import copy
import time
from Player import Player
from Bombe import Bombe
#from Sprite import Sprite

#################################################################################
##
##  Variables globales

# TAB est la matrice permettant de former la carte
# 0 vide
# 1 mur exterieur
# 2 mur interieur
# 3 briques destructibles
pygame.init()
TAB = [ [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,2,3,2,0,2,0,2,0,2,0,2,0,2,2,0,2,0,2,0,2,0,2,0,2,0,2,0,1],
        [1,3,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
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
GREEN = [0, 255, 0]
WHITE = [255, 255, 255]
BLACK = [0, 0, 0]
TIME = 0
VIT = 4
LIST_BOMB = []
LIST_IA = []

#################################################################################
##
##  Importation des images :

# de la carte
Block = pygame.image.load("images/blocks/stone.png")
BlockMiddle = pygame.image.load("images/blocks/stone2.png")
Grass = pygame.image.load("images/blocks/grass.png")
Brick = pygame.image.load("images/blocks/brick.png")

# des sprites des differents personnages
Bleu = pygame.image.load("images/ia/Bleu/sprite.png")
Rouge = pygame.image.load("images/ia/Rouge/sprite.png")
Jaune = pygame.image.load("images/ia/Jaune/sprite.png")
Orange = pygame.image.load("images/ia/Orange/sprite.png")
Vert = pygame.image.load("images/ia/Vert/sprite.png")

#du sprite de la bombe
Bombes = pygame.image.load("images/bombe/bomb.png")


#################################################################################
##
##  Importation des musiques :

#importation de la musique du jeu

pygame.mixer.music.load("son/bomberman_stage_theme.mp3")

#################################################################################
##
##  Fonctions principales

# dessine():
#   Parcourt TAB et place les images aux coordonnees idoines
#   en fonction de la valeur des cases du tableau
#   Puis place les joueurs
def draw():
    for i in range(LARGEUR):
        for j in range(HAUTEUR):
            if(TAB[j][i] == 4):
                LIST_BOMB.append(Bombe(i*ZOOM+44,j*ZOOM+100,Bombes, i, j))
                TAB[j][i] = 0
            if(TAB[j][i] == 3):
                screen.blit(Brick,(i*ZOOM,j*ZOOM))
            if(TAB[j][i] == 2):
                screen.blit(BlockMiddle,(i*ZOOM,j*ZOOM))
            if(TAB[j][i] == 1):
                screen.blit(Block,(i*ZOOM,j*ZOOM))
            if(TAB[j][i] == 0):
                screen.blit(Grass,(i*ZOOM,j*ZOOM))
    JoueurBleu.draw(screen)
    JoueurVert.draw(screen)
    JoueurJaune.draw(screen)
    JoueurRouge.draw(screen)
    JoueurOrange.draw(screen)
    screen.blit(font.render(str(TIME // 1), True, WHITE), ((1920 // 2) - 25 , 64*HAUTEUR + 32))

    for bomb in LIST_BOMB : 
        bomb.anim()
        bomb.draw(screen)

    pygame.display.flip() # Rafraichis l'affichage de Pygame

# removeBomb(LIST_BOMB)
# regarde chaque bombe de la liste et si la bombe explose, l'enleve de la liste des bombes
def removeBomb():
    for Bomb in LIST_BOMB:
        if (Bomb.Explode() == True):
            LIST_BOMB.remove(Bomb)

def poseBombe(player):
    caseX = int(player.x/ZOOM)
    caseY = int(player.y/ZOOM)
    if(TAB[caseY][caseX] == 0):
        TAB[caseY][caseX] = 4

def Destroy():
    for bomb in LIST_BOMB:
        if bomb.Explode():
            if TAB[bomb.caseY+1][bomb.caseX] == 3:
                TAB[bomb.caseY+1][bomb.caseX] = 0

            if TAB[bomb.caseY-1][bomb.caseX] == 3:
                TAB[bomb.caseY-1][bomb.caseX] = 0

            if TAB[bomb.caseY][bomb.caseX+1] == 3:
                TAB[bomb.caseY][bomb.caseX+1] = 0

            if TAB[bomb.caseY][bomb.caseX-1] == 3:
                TAB[bomb.caseY][bomb.caseX-1] = 0

def getTabPos(x,y):
    posX = x // ZOOM
    posY = y // ZOOM
    return (posX,posY)

def getPossibleMove(player):
    possibleMove = []
    tab = []

    tab.append(TAB[getTabPos(player.x,player.y+VIT)[1]][getTabPos(player.x,player.y+VIT)[0]])
    tab.append(TAB[getTabPos(player.x,player.y-VIT)[1]][getTabPos(player.x,player.y-VIT)[0]])
    tab.append(TAB[getTabPos(player.x+VIT,player.y)[1]][getTabPos(player.x+VIT,player.y)[0]])
    tab.append(TAB[getTabPos(player.x-VIT,player.y)[1]][getTabPos(player.x-VIT,player.y)[0]])

    if(tab[0]  == 0 or tab[0]  == 5): possibleMove.append((0,1))
    if(tab[1]  == 0 or tab[1]  == 5): possibleMove.append((0,-1))
    if(tab[2]  == 0 or tab[2]  == 5): possibleMove.append((1,0))
    if(tab[3]  == 0 or tab[3]  == 5): possibleMove.append((-1,0))

    return possibleMove


#################################################################################
##
##  Initialisation


police = pygame.font.SysFont("arial", 22)
font = pygame.font.SysFont("arial", 50)
screenInfo = pygame.display.Info()
screeenWidth = screenInfo.current_w
screenHeight = screenInfo.current_h - 100
screen = pygame.display.set_mode((screeenWidth,screenHeight), RESIZABLE)
pygame.display.set_caption("ESIEE - BOMB HERMAN")
done = False
clock = pygame.time.Clock()
pygame.mouse.set_visible(True)
temps = time.time()
pygame.mixer.music.play()#activation de la musique
ZOOM = int((64/1920)*screeenWidth)   # Taille d'une case en pixels
JoueurBleu = Player(ZOOM + ZOOM//2, ZOOM + ZOOM//2, Bleu,int(ZOOM*(102/64)), ZOOM)

#info_ia = [(720,350,Jaune),(1450,102,Rouge),(1450,700,Vert),(96,700,Orange)]

JoueurJaune = Player(720,350,Jaune,int(ZOOM*(102/64)),ZOOM)
JoueurOrange = Player(1450,102,Orange,int(ZOOM*(102/64)),ZOOM)
JoueurRouge = Player(1450,700,Rouge,int(ZOOM*(102/64)),ZOOM)
JoueurVert= Player(96,700,Vert,int(ZOOM*(102/64)),ZOOM)


LIST_IA.append(JoueurJaune)#Jaune
LIST_IA.append(JoueurOrange)#Orange
LIST_IA.append(JoueurRouge)#Rouge
LIST_IA.append(JoueurVert)#Vert

#Deplacement aléatoire des personnages
dep = [(0,4), (0,-4), (4,0),(-4,0)]





#################################################################################
##
##   Boucle principale


# --------  Main -----------
while not done:
    event = pygame.event.Event(pygame.USEREVENT)
    pygame.event.pump()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.VIDEORESIZE:
            screenHeight = event.h
            screeenWidth = event.w
            ZOOM = int((64/1920)*screeenWidth)

            JoueurBleu.getSprite(Bleu,int(ZOOM*(102/64)),ZOOM)
            JoueurJaune.getSprite(Jaune,int(ZOOM*(102/64)),ZOOM)
            JoueurOrange.getSprite(Orange,int(ZOOM*(102/64)),ZOOM)
            JoueurRouge.getSprite(Rouge,int(ZOOM*(102/64)),ZOOM)
            JoueurVert.getSprite(Vert,int(ZOOM*(102/64)),ZOOM)
            Grass = pygame.transform.scale(Grass,(ZOOM,ZOOM))
            Brick = pygame.transform.scale(Brick,(ZOOM,ZOOM))
            Block = pygame.transform.scale(Block,(ZOOM,ZOOM))
            BlockMiddle = pygame.transform.scale(BlockMiddle,(ZOOM,ZOOM))

            pygame.display.flip()
            dessine()

    for ia in LIST_IA:
        deplacement_ia = []
        deplacement_ia = random.randrange(len(dep))
        if deplacement_ia == 0:
            ia.spriteDir = 0
        if deplacement_ia == 1:
            ia.spriteDir = 3
        if deplacement_ia == 2:
            ia.spriteDir = 2
        if deplacement_ia == 3:
            ia.spriteDir = 1
        ia.move(dep[deplacement_ia][0], dep[deplacement_ia][1])
        time.sleep(0.00001)
    keysPressed = pygame.key.get_pressed()  # On retient les touches pressees

    ## Mouvements du Joueur
    #   On choisit la direction du sprite en fonction de sa position dans le tableau des sprites
    #   On fait appelle a la fonction move pour changer les coordonnees et les sprites
    possibleMove = getPossibleMove(JoueurBleu)
    if(keysPressed[pygame.K_DOWN]  and (0,1) in possibleMove):
        JoueurBleu.spriteDir = 0
        JoueurBleu.move(0,VIT)

    if(keysPressed[pygame.K_UP] and (0,-1) in possibleMove):
        JoueurBleu.move(0,-VIT)
        JoueurBleu.spriteDir = 3

    if(keysPressed[pygame.K_RIGHT] and (1,0) in possibleMove):
        JoueurBleu.move(VIT,0)
        JoueurBleu.spriteDir = 2

    if(keysPressed[pygame.K_LEFT] and (-1,0) in possibleMove):
        JoueurBleu.move(-VIT,0)
        JoueurBleu.spriteDir = 1

    if(keysPressed[pygame.K_SPACE]):
        poseBombe(JoueurBleu)

    Destroy()
    removeBomb()

    TIME = time.time() - temps
    screen.fill(BLACK)
    draw()   # On redessine l'affichage et on actualise
    clock.tick(30) # Limite d'image par seconde

    #a mettre quand le personnage est mort : pygame.mixer.music.stop()

pygame.quit() # Ferme la fenetre et quitte.
