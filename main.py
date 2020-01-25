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
import time	
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

   
ZOOM = 64   # Taille d'une case en pixels
HAUTEUR = len(TAB)     # Nombre de cases en hauteur
LARGEUR = len(TAB[0])  # Nombre de cases en largeur
GREEN = [0, 255, 0]
WHITE = [255, 255, 255]
BLACK = [0, 0, 0]

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
			if(TAB[j][i] == 3):
				screen.blit(Brick,(i*ZOOM,j*ZOOM))
			if(TAB[j][i] == 2):
				screen.blit(BlockMiddle,(i*ZOOM,j*ZOOM))
			if(TAB[j][i] == 1):
				screen.blit(Block,(i*ZOOM,j*ZOOM))
			if(TAB[j][i] == 0):
				screen.blit(Grass,(i*ZOOM,j*ZOOM))

	JoueurBleu.draw(screen)
	screen.blit(font.render(str(actualTime // 1), True, WHITE), ((1920 // 2) - 25 , 64*HAUTEUR + 32))
	pygame.display.flip() # Rafraichis l'affichage de Pygame

## move():
#	On change les coordonnees du joueur selon son deplacement
#	On regarde la retenu de sprite est complete ou non:
#		* Si oui on change de sprite (+1 %Nombre de sprite pour ne pas sortir du tableau) et et on reset la retenu de sprite
#		* Si non on augmente la retenu
#	(permet d'eviter un changement de sprite trop rapide par rapport a sa vitesse)
def move(player, posX, posY):
	player.y += posY
	player.x += posX
	if(player.spriteOffset == 2):
		player.spriteCount = (JoueurBleu.spriteCount + 1) % 4
		player.spriteOffset = 0
	else:
		player.spriteOffset += 1

#################################################################################
##
##  Initialisation

pygame.init()
police = pygame.font.SysFont("arial", 22)
font = pygame.font.SysFont("arial", 50)
screeenWidth = (LARGEUR+1) * ZOOM
screenHeight = (HAUTEUR+2) * ZOOM
screen = pygame.display.set_mode((screeenWidth,screenHeight))
pygame.display.set_caption("ESIEE - BOMBERMAN")
done = False
clock = pygame.time.Clock()   
pygame.mouse.set_visible(True)
temps = time.time()
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

	keysPressed = pygame.key.get_pressed()	# On retient les touches pressees

	## Mouvements du Joueur
	#	On choisit la direction du sprite en fonction de sa position dans le tableau des sprites
	#	On fait appelle a la fonction move pour changer les coordonnees et les sprites
	print(keysPressed)
	if(keysPressed[pygame.K_DOWN]):
		JoueurBleu.spriteDir = 0
		move(JoueurBleu,0,4)
	if(keysPressed[pygame.K_UP]):
		move(JoueurBleu,0,-4)
		JoueurBleu.spriteDir = 3
	if(keysPressed[pygame.K_RIGHT]):
		move(JoueurBleu,4,0)
		JoueurBleu.spriteDir = 2
	if(keysPressed[pygame.K_LEFT]):
		move(JoueurBleu,-4,0)
		JoueurBleu.spriteDir = 1

	actualTime = time.time() - temps
	screen.fill(BLACK)
	dessine()	# On redessine l'affichage et on actualise
	clock.tick(30) # Limite d'image par seconde
 
pygame.quit() # Ferme la fenetre et quitte.