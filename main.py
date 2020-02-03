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

# Decor
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

TAB = [ [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],      ## TAB est la matrice permettant de former la carte
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],      #   0 vide
        [1,0,2,0,2,0,2,0,2,0,2,0,2,0,2,2,0,2,0,2,0,2,0,2,0,2,0,2,0,1],      #   1 mur exterieur
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],      #   2 mur interieur
        [1,0,2,0,2,0,2,0,2,0,2,0,2,0,2,2,0,2,0,2,0,2,0,2,0,2,0,2,0,1],      #   3 briques destructibles
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],      #   4 Bombes
        [1,0,2,0,2,0,2,0,2,0,2,0,2,0,2,2,0,2,0,2,0,2,0,2,0,2,0,2,0,1],      #   5 Explosion
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

SCREEN_WIDTH = pygame.display.Info().current_w      # L'ecran de jeu s'ajuste à la taille de l'ecran de l'ordinateur
SCREEN_HEIGHT = pygame.display.Info().current_h - 100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT), RESIZABLE)

ZOOM = int((64/1920)*SCREEN_WIDTH)   # Taille d'une case en pixels

GREEN = [0, 255, 0]         # Definition de quelques couleurs en RGB
WHITE = [255, 255, 255]
BLACK = [0, 0, 0]

TIME = 0        # Temps depuis le lancement du jeu
VIT = 4         # Vitesse de deplacement des joueurs

FONT = pygame.font.SysFont("arial", 50)     # Definition de la police d'écriture
CLOCK = pygame.time.Clock()                 # Mise en place de l'horloge interne
TIME = time.time()
DONE = False                                # Variable qui indique si le jeu est terminé

LIST_BOMB = []      # Liste contenant les bombes
LIST_IA = []        # Liste contenant les IA en vie
LIST_JOUEUR = []    # Liste contennat les joueurs en vie

POS_IA = [(HAUTEUR-2, LARGEUR-2), (HAUTEUR-2, 1), (1, LARGEUR-2)]       # Positionnenement des IA à l'initialisation du jeu
JOUEUR_BLEU = Player(ZOOM + ZOOM//2, ZOOM + ZOOM//2, BLEU,int(ZOOM*(102/64)), ZOOM)     # Definition du joueur
JOUEUR_JAUNE = IA(POS_IA[0][1] * ZOOM + ZOOM//2, POS_IA[0][0] * ZOOM + ZOOM//2, JAUNE,int(ZOOM*(102/64)), ZOOM, (0,-1))     # Definition de l'IA
JOUEUR_ORANGE = IA(POS_IA[1][1] * ZOOM + ZOOM//2, POS_IA[1][0] * ZOOM + ZOOM//2, ORANGE,int(ZOOM*(102/64)), ZOOM,(1,0))     # Definition de l'IA
JOUEUR_ROUGE = IA(POS_IA[2][1] * ZOOM + ZOOM//2, POS_IA[2][0] * ZOOM + ZOOM//2, ROUGE,int(ZOOM*(102/64)), ZOOM,(-1,0))      # Definition de l'IA

GRILLE_BOMBE = None     # Grille contenant les distances aux bombes sur la map


#################################################################################
##
##  Fonctions principales

## draw():
#   Parcourt TAB et place les images aux coordonnees donnees
#   en fonction de la valeur des cases du tableau
#   Puis place les joueurs
def draw():
    for i in range(LARGEUR):
        for j in range(HAUTEUR):
            if(TAB[j][i] == 0 or TAB[j][i] == 4 or TAB[j][i] ==  5 or TAB[j][i] == 7): SCREEN.blit(GRASS,(i*ZOOM,j*ZOOM))
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
        joueur.draw(SCREEN, ZOOM//2, int(ZOOM*(102/ZOOM)))

    pygame.display.flip()       # Rafraichis l'affichage de Pygame


## generate():
#   Genere les cases destructibles aleatoirement
#   Les maps changent donc à chaque jeux
def generate():
    for i in range(LARGEUR):
        for j in range(HAUTEUR):
            if(TAB[j][i] == 0 and random.randrange(2)): TAB[j][i] = 3
    TAB[1][1] = 0; TAB[1][2] = 0; TAB[2][1] = 0
    TAB[HAUTEUR-2][1] = 0; TAB[HAUTEUR-2][2] = 0; TAB[HAUTEUR-3][1] = 0
    TAB[1][LARGEUR-2] = 0; TAB[1][LARGEUR-3] = 0; TAB[2][LARGEUR-2] = 0
    TAB[HAUTEUR-2][LARGEUR-2] = 0; TAB[HAUTEUR-3][LARGEUR-2] = 0; TAB[HAUTEUR-2][LARGEUR-3] = 0


## removeBomb():
#   Regarde chaque bombe de la liste
#   On l'enleve de la liste des bombes si elle explose
def removeBomb():
    for Bomb in LIST_BOMB:
        if (Bomb.Explode() == True):
            Bomb.spriteCount = 0
            Bomb.spriteDir=0
            Bomb.sprite= Bomb.getSpriteExplo(FIRE, ZOOM)
            #SON_BOMBE.play()       # Mise en commentaire car ca fais beuguer l'ordi de Quentin
            TAB[Bomb.caseY][Bomb.caseX] = 5
            Bomb.explode = False
            Bomb.player.nbBombe -= 1

        if(Bomb.exploFin):
            TAB[Bomb.caseY][Bomb.caseX] = 0
            LIST_BOMB.remove(Bomb)


## poseBombe(player):
#   Verifie si le joueur peut poser une bombe
#   Pose une bombe sur une case
#   Mise à jour du tableau
def poseBombe(player):
    caseX = int(player.x/ZOOM)
    caseY = int(player.y/ZOOM)
    if(TAB[caseY][caseX] == 0 and player.nbBombe < player.nbBombeMax):
        LIST_BOMB.append(Bombe(caseX*ZOOM+100,caseY*ZOOM+96,BOMBES, ZOOM, TIME,player))
        TAB[caseY][caseX] = 4
        player.nbBombe += 1


## Meurt(player):
#   Regarde si la position du joueur correspond à une cases en explosion
#   Enleve une vie au joueur
#   Si le joueur n'a plus de vie, on enleve le joueur de la liste des joueurs/IA
def Meurt(player):
    x =getTabPos(player.x,player.y)[0]
    y=getTabPos(player.x,player.y)[1]
    if(TAB[y][x]==5):
        player.lives -= 1
        if player.lives == 0:
            if(player in LIST_JOUEUR):
                LIST_JOUEUR.remove(player)
            if(player in LIST_IA):
                LIST_IA.remove(player)


## iaDanger(ia):
#   Regarde la position de l'IA
#   Retourne si elle se trouve dans une zone de danger = le rayon de l'explosion de la bombe
def iaDanger(ia): return GRILLE_BOMBE[getTabPos(ia.x,ia.y)[1]][getTabPos(ia.x,ia.y)[0]] <= 2


## iaFuite(ia):
#   Regarde les deplacement possible de l'IA
#   Se deplace sur la case la plus grande = le plus loin de la bombe
def iaFuite(ia) :
    possibleMove = getPossibleMoveIA(ia)
    posIA = getTabPos(ia.x,ia.y)
    max = 0
    caseMax = None
    for case in possibleMove :
        if GRILLE_BOMBE[posIA[1] + case[1]][posIA[0] + case[0]] > max and GRILLE_BOMBE[posIA[1] + case[1]][posIA[0] + case[0]] < 100:
            max = GRILLE_BOMBE[posIA[1] + case[1]][posIA[0] + case[0]]
            caseMax = case
    if(caseMax != None):
        ia.dir = caseMax
        ia.move(caseMax[0]*VIT, caseMax[1]*VIT)
        ia.setRightDir()


## moveIA(ia):
#   S'occupe du deplacement principal des IA
#   Regarde en premiere si l'IA est en danger = dans le rayon d'explosion de la bombe
#   Si non, elle se dirige dans une direction jusqu'à rencontrer un mur
def moveIA(ia):
    if iaDanger(ia) : iaFuite(ia)
    else :
        possibleMove = getPossibleMoveIA(ia)
        if (ia.dir in possibleMove):
            ia.move(ia.dir[0]*VIT, ia.dir[1]*VIT)
        else:
            poseBombe(ia)
            if(len(possibleMove) !=0 ):
                deplacement_ia = random.randrange(len(possibleMove))
                ia.dir = possibleMove[deplacement_ia]
                ia.setRightDir()
            else:
                ia.dir = (0,0)


## getTabPos(x,y):
#   Prendre la position en pixels du joueur
#   Regarde en fonction du zoom (taille de la fenetre) sur quelle case le joueur se trouve
#   Retourne la case du joueur
def getTabPos(x,y):
    posX = x // ZOOM
    posY = y // ZOOM
    return (posX,posY)


## getPossibleMoveIA(player):
#   En focntion de la position des ia
#   On regarde les cases tout autour pour connaitre leurs valeurs
#   Retourne les deplacements possibles pour l'ia
def getPossibleMoveIA(player):
    possibleMove = []
    tab = []
    dist = ZOOM//2+1
    tab.append(TAB[getTabPos(player.x,player.y+dist)[1]][getTabPos(player.x,player.y+dist)[0]])
    tab.append(TAB[getTabPos(player.x,player.y-dist)[1]][getTabPos(player.x,player.y-dist)[0]])
    tab.append(TAB[getTabPos(player.x+dist,player.y)[1]][getTabPos(player.x+dist,player.y)[0]])
    tab.append(TAB[getTabPos(player.x-dist,player.y)[1]][getTabPos(player.x-dist,player.y)[0]])

    tab.append((getTabPos(player.x,player.y+dist)[0],getTabPos(player.x,player.y+dist)[1]))
    tab.append((getTabPos(player.x,player.y-dist)[0],getTabPos(player.x,player.y-dist)[1]))
    tab.append((getTabPos(player.x+dist,player.y)[0],getTabPos(player.x+dist,player.y)[1]))
    tab.append((getTabPos(player.x-dist,player.y)[0],getTabPos(player.x-dist,player.y)[1]))

    tab.append((getTabPos(player.x,player.y)[0],getTabPos(player.x,player.y)[1]))

    if(tab[0]  == 0 or tab[0]  == 5 or (tab[0]  == 4 and tab[4] == tab[8])): possibleMove.append((0,1))
    if(tab[1]  == 0 or tab[1]  == 5 or (tab[1]  == 4 and tab[5] == tab[8])): possibleMove.append((0,-1))
    if(tab[2]  == 0 or tab[2]  == 5 or (tab[2]  == 4 and tab[6] == tab[8])): possibleMove.append((1,0))
    if(tab[3]  == 0 or tab[3]  == 5 or (tab[3]  == 4 and tab[7] == tab[8])): possibleMove.append((-1,0))

    return possibleMove


## getPossibleMovePlayer(player):
#   En focntion de la position du joueur
#   On regarde les cases tout autour pour connaitre leurs valeurs
#   Retourne les deplacements possibles du joueur
def getPossibleMovePlayer(player):
    possibleMove = []
    tab = []

    tab.append(TAB[getTabPos(player.x,player.y+VIT)[1]][getTabPos(player.x,player.y+VIT)[0]])
    tab.append(TAB[getTabPos(player.x,player.y-VIT)[1]][getTabPos(player.x,player.y-VIT)[0]])
    tab.append(TAB[getTabPos(player.x+VIT,player.y)[1]][getTabPos(player.x+VIT,player.y)[0]])
    tab.append(TAB[getTabPos(player.x-VIT,player.y)[1]][getTabPos(player.x-VIT,player.y)[0]])

    tab.append((getTabPos(player.x,player.y+VIT)[0],getTabPos(player.x,player.y+VIT)[1]))
    tab.append((getTabPos(player.x,player.y-VIT)[0],getTabPos(player.x,player.y-VIT)[1]))
    tab.append((getTabPos(player.x+VIT,player.y)[0],getTabPos(player.x+VIT,player.y)[1]))
    tab.append((getTabPos(player.x-VIT,player.y)[0],getTabPos(player.x-VIT,player.y)[1]))

    tab.append((getTabPos(player.x,player.y)[0],getTabPos(player.x,player.y)[1]))

    if(tab[0]  == 0 or tab[0]  == 5 or (tab[0]  == 4 and tab[4] == tab[8])): possibleMove.append((0,1))
    if(tab[1]  == 0 or tab[1]  == 5 or (tab[1]  == 4 and tab[5] == tab[8])): possibleMove.append((0,-1))
    if(tab[2]  == 0 or tab[2]  == 5 or (tab[2]  == 4 and tab[6] == tab[8])): possibleMove.append((1,0))
    if(tab[3]  == 0 or tab[3]  == 5 or (tab[3]  == 4 and tab[7] == tab[8])): possibleMove.append((-1,0))

    return possibleMove


## grilleBombe():
#   Grille contenantles murs et les bombes
#   Elle permet ensuite de savoir si les ia sont en danger ou non
def grilleBombe():
    global GRILLE_BOMBE
    GRILLE_BOMBE = copy.deepcopy(TAB)
    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            if (TAB[y][x] == 4 or TAB[y][x] == 5): GRILLE_BOMBE[y][x] = 0
            if (TAB[y][x] == 1 or TAB[y][x] == 2 or TAB[y][x] == 3): GRILLE_BOMBE[y][x] = 1000
            if (TAB[y][x] == 0): GRILLE_BOMBE[y][x] = 100


## miseDistance():
#   Fonction qui permet de mettre à distance les cases de la grille bombe
#   Si la case se trouve à cote de la bombe elle sera mise à 1 (etc)
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

pygame.mouse.set_visible(True)      # Souris du clavier visible
pygame.display.set_caption("ESIEE - BOMB HERMAN")       # Titre de la page de jeu
#pygame.mixer.music.play()      # Activation de la musique


LIST_IA.append(JOUEUR_JAUNE)        # Ajout du joueur JAUNE dans la liste IA
LIST_IA.append(JOUEUR_ORANGE)       # Ajout du joueur ORANGE dans la liste IA
LIST_IA.append(JOUEUR_ROUGE)        # Ajout du joueur ROUGE dans la liste IA

for ia in LIST_IA:          # Defini la direction des sprites des ia a l'init
    LIST_JOUEUR.append(ia)  # Ajout des ia dans la liste des joueurs
    ia.setRightDir()

LIST_JOUEUR.append(JOUEUR_BLEU)     # Ajout du joueur BLEU dans la liste des joueurs

generate()      # Genere la map de jeu


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

    ## Mouvements du joueur:
    #   On choisit la direction du sprite en fonction de sa position dans le tableau des sprites
    #   On fait appelle a la fonction move pour changer les coordonnees et les sprites
    possibleMove = getPossibleMovePlayer(JOUEUR_BLEU)
    if(keysPressed[pygame.K_DOWN]  and (0,1) in possibleMove):
        JOUEUR_BLEU.spriteDir = 0
        JOUEUR_BLEU.move(0,VIT)

    if(keysPressed[pygame.K_UP] and (0,-1) in possibleMove):
        JOUEUR_BLEU.move(0,-VIT)
        JOUEUR_BLEU.spriteDir = 3

    if(keysPressed[pygame.K_RIGHT] and (1,0) in possibleMove):
        JOUEUR_BLEU.move(VIT,0)
        JOUEUR_BLEU.spriteDir = 2

    if(keysPressed[pygame.K_LEFT] and (-1,0) in possibleMove):
        JOUEUR_BLEU.move(-VIT,0)
        JOUEUR_BLEU.spriteDir = 1

    if(keysPressed[pygame.K_SPACE]):
        if JOUEUR_BLEU in LIST_JOUEUR :
            poseBombe(JOUEUR_BLEU)

    for ia in LIST_IA:
        Meurt(ia)

    Meurt(JOUEUR_BLEU)

    SCREEN.fill(BLACK)
    TIME = time.time()
    draw()      # On redessine l'affichage et on actualise
    CLOCK.tick(30)   # Limite d'image par seconde

    # A mettre quand le personnage est mort : pygame.mixer.music.stop()


pygame.quit() # Ferme la fenetre et quitte le jeu
