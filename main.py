#################################################################################
#	Class main from Bomberman													#
#	Created by Vincent : 24/01/2020												#
#																				#
#	Cette classe est la classe principale du jeu, elle permet de definir le 	#
#	le decor, et contient la boucle du jeu 										#
#																				#
#################################################################################

#################################################################################
##
## Import

import pygame
import random
import copy
from Player import Player

#################################################################################
##
##  Variables globales
 
# TAB est la matrice permettant de former la carte
# 0 vide
# 1 mur exterieur
# 2 mur interieur
# 3 briques destructibles

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

   
ZOOM = 64   # Taille d'une case en pixels
HAUTEUR = len(TAB)     # Nombre de cases en hauteur
LARGEUR = len(TAB[0])  # Nombre de cases en largeur

#################################################################################
##
##  Importation des images :

# de la carte
Block = pygame.image.load("images/blocks/stone.png")
BlockMiddle = pygame.image.load("images/blocks/stone2.png")
Grass = pygame.image.load("images/blocks/grass.png")

# des sprites des differents personnages
Bleu = pygame.image.load("images/ia/Bleu/sprite.png")
Rouge = pygame.image.load("images/ia/Rouge/sprite.png")
Jaune = pygame.image.load("images/ia/Jaune/sprite.png")
Orange = pygame.image.load("images/ia/Orange/sprite.png")
Vert = pygame.image.load("images/ia/Vert/sprite.png")

#################################################################################
##
##  Fonctions principales

# getSprite(Color): 
# 	Decoupe l'image Color en sprite
#	Met les sprite a l'echelle de la carte
#	Les rajoute dans un tableau en 2D tel que :
#	Tab = [[SpriteAvant_1, SpriteAvant_2, ...],[SpriteDroit_1, SpriteDroit_2, ...]]
def getSprite(Color):
	Tab = []
	for j in range(4):
		tabTemp = []
		for i in range(4):
			imTemp = Color.subsurface((i*29) + (3*i) + 3,0 + (j*48),29,46)
			imTemp = pygame.transform.scale(imTemp,(64,102))
			tabTemp.append(imTemp)
		Tab.append(tabTemp)
	return Tab

# dessine():
#	Parcourt TAB et place les images aux coordonnees idoines
#	en fonction de la valeur des cases du tableau
#	Puis place les joueurs
def dessine():
	for i in range(LARGEUR):
		for j in range(HAUTEUR):
			if(TAB[j][i] == 2):
				screen.blit(BlockMiddle,(i*ZOOM,j*ZOOM))
			if(TAB[j][i] == 1):
				screen.blit(Block,(i*ZOOM,j*ZOOM))
			if(TAB[j][i] == 0):
				screen.blit(Grass,(i*ZOOM,j*ZOOM))

	JoueurBleu.draw(screen)
	pygame.display.flip() # Rafraichis l'affichage de Pygame

#################################################################################
##
##  Initialisation

pygame.init()
police = pygame.font.SysFont("arial", 22)
screeenWidth = (LARGEUR+1) * ZOOM
screenHeight = (HAUTEUR+2) * ZOOM
screen = pygame.display.set_mode((screeenWidth,screenHeight))
pygame.display.set_caption("ESIEE - BOMBERMAN")
done = False
clock = pygame.time.Clock()   
pygame.mouse.set_visible(True)

JoueurBleu = Player(96,102,getSprite(Bleu))

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

	keysPressed = pygame.key.get_pressed()	# On retient la derniere touche pressee

	## Mouvements du Joueur
	#	Deplacement
	#	On choisit la direction du sprite
	#	On passe a la sprite d'apres modulo le nombre de sprite

	if(keysPressed[pygame.K_DOWN]):
		JoueurBleu.y += 4
		JoueurBleu.spriteDir = 0	
		JoueurBleu.spriteCount = (JoueurBleu.spriteCount + 1) % 4
	if(keysPressed[pygame.K_UP]):
		JoueurBleu.y -= 4
		JoueurBleu.spriteDir = 3
		JoueurBleu.spriteCount = (JoueurBleu.spriteCount + 1) % 4
	if(keysPressed[pygame.K_RIGHT]):
		JoueurBleu.x += 4
		JoueurBleu.spriteDir = 2
		JoueurBleu.spriteCount = (JoueurBleu.spriteCount + 1) % 4
	if(keysPressed[pygame.K_LEFT]):
		JoueurBleu.x -= 4
		JoueurBleu.spriteDir = 1
		JoueurBleu.spriteCount = (JoueurBleu.spriteCount + 1) % 4

	dessine()	# On redessine l'affichage et on actualise
	clock.tick(30) # Limite d'image par seconde
 
pygame.quit() # Ferme la fenetre et quitte.