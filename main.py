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

POS_IA = [(HAUTEUR-2, LARGEUR-2), (HAUTEUR-2, 1), (1, LARGEUR-2)]
JOUEUR_BLEU = Player(ZOOM + ZOOM//2, ZOOM + ZOOM//2, BLEU,int(ZOOM*(102/64)), ZOOM)
JOUEUR_JAUNE = IA(POS_IA[0][1] * ZOOM + ZOOM//2, POS_IA[0][0] * ZOOM + ZOOM//2, JAUNE,int(ZOOM*(102/64)), ZOOM, (0,-1))
JOUEUR_ORANGE = IA(POS_IA[1][1] * ZOOM + ZOOM//2, POS_IA[1][0] * ZOOM + ZOOM//2, ORANGE,int(ZOOM*(102/64)), ZOOM,(1,0))
JOUEUR_ROUGE = IA(POS_IA[2][1] * ZOOM + ZOOM//2, POS_IA[2][0] * ZOOM + ZOOM//2, ROUGE,int(ZOOM*(102/64)), ZOOM,(-1,0))

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

			bomb.drawExplo(SCREEN,TAB,i,(1+i),ZOOM)
			bomb.drawExplo(SCREEN,TAB,i,-(1+i),ZOOM)



	for joueur in LIST_JOUEUR:

		joueur.draw(SCREEN, ZOOM//2, int(ZOOM*(102/ZOOM)))

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
	caseX = int(player.x/ZOOM)
	caseY = int(player.y/ZOOM)
	if(TAB[caseY][caseX] == 0 and player.nbBombe < player.nbBombeMax):
		LIST_BOMB.append(Bombe(caseX*ZOOM+100,caseY*ZOOM+96,BOMBES, ZOOM, TIME,player))
		TAB[caseY][caseX] = 4
		player.nbBombe += 1


# def destroy():
#   for bomb in LIST_BOMB:
#       if bomb.Explode():
#           # if TAB[bomb.caseY][bomb.caseX+2] == 3 and TAB[bomb.caseY][bomb.caseX+1] == 0: TAB[bomb.caseY][bomb.caseX+2] = 0
#           # if TAB[bomb.caseY][bomb.caseX-2] == 3 and TAB[bomb.caseY][bomb.caseX-1] == 0: TAB[bomb.caseY][bomb.caseX-2] = 0
#           # if TAB[bomb.caseY+2][bomb.caseX] == 3 and TAB[bomb.caseY+1][bomb.caseX] == 0: TAB[bomb.caseY+2][bomb.caseX] = 0
#           # if TAB[bomb.caseY-2][bomb.caseX] == 3 and TAB[bomb.caseY-1][bomb.caseX] == 0: TAB[bomb.caseY-2][bomb.caseX] = 0
#           if TAB[bomb.caseY+1][bomb.caseX] == 3: TAB[bomb.caseY+1][bomb.caseX] = 0
#           if TAB[bomb.caseY-1][bomb.caseX] == 3: TAB[bomb.caseY-1][bomb.caseX] = 0
#           if TAB[bomb.caseY][bomb.caseX+1] == 3: TAB[bomb.caseY][bomb.caseX+1] = 0
#           if TAB[bomb.caseY][bomb.caseX-1] == 3: TAB[bomb.caseY][bomb.caseX-1] = 0
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

def iaDanger(ia): return GRILLE_BOMBE[getTabPos(ia.x,ia.y)[1]][getTabPos(ia.x,ia.y)[0]] <= 2

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



def getTabPos(x,y):
	posX = x // ZOOM
	posY = y // ZOOM
	return (posX,posY)

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
LIST_IA.append(JOUEUR_ORANGE)#ORANGE
LIST_IA.append(JOUEUR_ROUGE)#ROUGE

for ia in LIST_IA:
	LIST_JOUEUR.append(ia)
	ia.setRightDir()    # Defini la direction des sprites des ia a l'init

LIST_JOUEUR.append(JOUEUR_BLEU)

#Deplacement aléatoire des personnages
dep = [(0,4), (0,-4), (4,0),(-4,0)]

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
	draw()   # On redessine l'affichage et on actualise
	CLOCK.tick(30) # Limite d'image par seconde

	#a mettre quand le personnage est mort : pygame.mixer.music.stop()


pygame.quit() # Ferme la fenetre et quitte.