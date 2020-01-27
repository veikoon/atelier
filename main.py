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
VERT = pygame.image.load("images/ia/Vert/sprite.png")
BOMBES = pygame.image.load("images/bombe/bomb.png")

# Musique
pygame.mixer.music.load("son/bomberman_stage_theme.mp3")

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

JOUEUR_BLEU = Player(ZOOM + ZOOM//2, ZOOM + ZOOM//2, BLEU,int(ZOOM*(102/64)), ZOOM)
JOUEUR_JAUNE = Player(720,350,JAUNE,int(ZOOM*(102/64)),ZOOM)
JOUEUR_ORANGE = Player(1450,102,ORANGE,int(ZOOM*(102/64)),ZOOM)
JOUEUR_ROUGE = Player(1450,700,ROUGE,int(ZOOM*(102/64)),ZOOM)
JOUEUR_VERT= Player(96,700,VERT,int(ZOOM*(102/64)),ZOOM)

#################################################################################
##
##  Initialisation

pygame.mouse.set_visible(True)
pygame.display.set_caption("ESIEE - BOMB HERMAN")
pygame.mixer.music.play()   # Activation de la musique


LIST_IA.append(JOUEUR_JAUNE)#JAUNE
LIST_IA.append(JOUEUR_ORANGE)#ORANGE
LIST_IA.append(JOUEUR_ROUGE)#ROUGE
LIST_IA.append(JOUEUR_VERT)#VERT

for ia in LIST_IA: LIST_JOUEUR.append(ia)
LIST_JOUEUR.append(JOUEUR_BLEU)

#Deplacement aléatoire des personnages
dep = [(0,4), (0,-4), (4,0),(-4,0)]

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
			if(TAB[j][i] == 4):
				LIST_BOMB.append(Bombe(i*ZOOM+44,j*ZOOM+100,BOMBES, i, j))
				TAB[j][i] = 0
			if(TAB[j][i] == 0): SCREEN.blit(GRASS,(i*ZOOM,j*ZOOM))
			if(TAB[j][i] == 1): SCREEN.blit(BLOCK,(i*ZOOM,j*ZOOM))
			if(TAB[j][i] == 2): SCREEN.blit(BLOCK_MIDDLE,(i*ZOOM,j*ZOOM))
			if(TAB[j][i] == 3): SCREEN.blit(BLOCK_BRICK,(i*ZOOM,j*ZOOM))

	SCREEN.blit(FONT.render(str(TIME // 1), True, WHITE), ((1920 // 2) - 25 , 64*HAUTEUR + 32))

	for bomb in LIST_BOMB : 
		bomb.anim()
		bomb.draw(SCREEN)
		
	for j in LIST_JOUEUR: j.draw(SCREEN)

	pygame.display.flip() # Rafraichis l'affichage de Pygame


def mort(Player):
    Player.lives -= 1
    if Player.lives == 0:
        LIST_JOUEUR.remove(Player)
    

# removeBomb(LIST_BOMB)
# regarde chaque bombe de la liste et si la bombe explose, l'enleve de la liste des BOMBES
def removeBomb():
	for Bomb in LIST_BOMB:
		if (Bomb.Explode() == True):
			LIST_BOMB.remove(Bomb)

def poseBombe(player):
	caseX = int(player.x/ZOOM)
	caseY = int(player.y/ZOOM)
	if(TAB[caseY][caseX] == 0):
		TAB[caseY][caseX] = 4

def destroy():
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
			ZOOM = int((64/1920)*SCREEN_WIDTH)

			JOUEUR_BLEU.getSprite(BLEU,int(ZOOM*(102/64)),ZOOM)
			JOUEUR_JAUNE.getSprite(JAUNE,int(ZOOM*(102/64)),ZOOM)
			JOUEUR_ORANGE.getSprite(ORANGE,int(ZOOM*(102/64)),ZOOM)
			JOUEUR_ROUGE.getSprite(ROUGE,int(ZOOM*(102/64)),ZOOM)
			JOUEUR_VERT.getSprite(VERT,int(ZOOM*(102/64)),ZOOM)


			GRASS = pygame.transform.scale(GRASS,(ZOOM,ZOOM))
			BLOCK_BRICK = pygame.transform.scale(BLOCK_BRICK,(ZOOM,ZOOM))
			BLOCK = pygame.transform.scale(BLOCK,(ZOOM,ZOOM))
			BLOCK_MIDDLE = pygame.transform.scale(BLOCK_MIDDLE,(ZOOM,ZOOM))

			pygame.display.flip()
			draw()

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

	## Mouvements du JOUEUR_
	#   On choisit la direction du sprite en fonction de sa position dans le tableau des sprites
	#   On fait appelle a la fonction move pour changer les coordonnees et les sprites
	possibleMove = getPossibleMove(JOUEUR_BLEU)
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
		poseBombe(JOUEUR_BLEU)

	destroy()
	removeBomb()
	SCREEN.fill(BLACK)
	TIME = time.time() - TIME
	draw()   # On redessine l'affichage et on actualise
	CLOCK.tick(30) # Limite d'image par seconde

	#a mettre quand le personnage est mort : pygame.mixer.music.stop()

pygame.quit() # Ferme la fenetre et quitte.