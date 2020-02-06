#################################################################################
##
## Import

import pygame
import copy
from copy import deepcopy


#################################################################################
#	Class Player from Bomberman													#
#	Created by Vincent : 24/01/2020												#
#																				#
#	Cette classe permet de definir toutes les proprietes d'un Joueur			#
#																				#
#################################################################################

class Player:
	def __init__(self,startX, startY, live, color, hauteur, zoom):
		self.x = 0						# Positions initiales
		self.y = 0
		self.caseX = startX
		self.caseY = startY
		self.color = color				# Couleur du personnage
		self.cartedist = []				# Carte des distance au joueur courant
		self.sprite = []				# Tableau de sprites en 2D
		self.spriteDir = 0				# Selectionne le tableau de sprite (en 1D) correspondant a la direction du joueur
		self.spriteCount = 0			# Selectionne le sprite du tableau correspondant au mouvement actuel
		self.spriteOffset = 0			# Permet de changer de sprite en fonction du decalage et non a chaque mouvement
		self.lives = live				# Nombre de vie du personnage dans une partie de jeu
		self.nbBombe = 0				# Nombre de bombes déjà posé par le personnage
		self.nbBombeMax = 1			# Nombre de bombes maximal que peut poser le personnage en meme temps
		self.rayonBombe = 1			# Rayon d'explosion de la bombe
		self.invincible = -10000         # Rend le player invincible quand il rencontre une bombe et qu'il lui reste encore une vie ou plus
		self.getSprite(hauteur, zoom) 	# Avoir le spoite du personnage de la bonne taille
		self.dir = (0,0)


	## getSprite(self, hauteur, zoom):
	#   Decoupe l'image Color en sprite
	#   Met les sprite a l'echelle de la carte
	#   Les rajoute dans un tableau en 2D tel que :
	#   Tab = [[SpriteAvant_1, SpriteAvant_2, ...],[SpriteDroit_1, SpriteDroit_2, ...]]
	def getSprite(self, hauteur, zoom):
		Tab = []
		for j in range(4):
			tabTemp = []
			for i in range(4):
				imTemp = self.color.subsurface((i*29) + (3*i) + 3,0 + (j*48),29,46)
				imTemp = pygame.transform.scale(imTemp,(zoom,hauteur))
				tabTemp.append(imTemp)
			Tab.append(tabTemp)
		self.sprite = Tab


	##	draw(self, surface, largeurPerso, hauteurPerso):
	#	Permet de dessiner le personnage dont les coordonnees sont au milieu de ses pieds
	#	tandis que le jeu dessine les images depuis leur coin superieur gauche:
	#	(largeurPerso / 2 = 32 et hauteurPerso = 102)
	def draw(self, surface, largeurPerso, hauteurPerso, zoom):
		surface.blit(self.sprite[self.spriteDir][self.spriteCount], ((self.caseY * zoom) + self.x - largeurPerso + zoom//2,(self.caseX * zoom) + self.y - hauteurPerso + zoom//2))


	## move(self, posX, posY):
	#   On change les coordonnees du joueur selon son deplacement
	#   On regarde la retenu de sprite est complete ou non:
	#       * Si oui on change de sprite (+1 %Nombre de sprite pour ne pas sortir du tableau) et et on reset la retenu de sprite
	#       * Si non on augmente la retenu
	#   (permet d'eviter un changement de sprite trop rapide par rapport a sa vitesse)
	def move(self, posX, posY, zoom):
		self.y += posY
		self.x += posX

		if(self.x > zoom//2):
			self.x = - zoom//2
			self.caseY += 1

		if(self.x < -zoom//2):
			self.x = zoom//2
			self.caseY -= 1

		if(self.y > zoom//2):
			self.y = - zoom//2
			self.caseX += 1

		if(self.y < -zoom//2):
			self.y = zoom//2
			self.caseX -= 1

		if(self.spriteOffset == 2):
			self.spriteCount = (self.spriteCount + 1) % 4
			self.spriteOffset = 0
		else:
			self.spriteOffset += 1


	def generateDist(self, tab):
		self.cartedist = [ [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
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
		done = True
		hauteur = len(tab)
		largeur = len(tab[0])
		for x in range(largeur):
			for y in range(hauteur):
				if (tab[y][x] == 1 or tab[y][x] == 2):
					self.cartedist[y][x] = 1000
					continue
				if (tab[y][x] == 0 or tab[y][x] == 3 or tab[y][x] == 4 or tab[y][x] == 5):
					self.cartedist[y][x] = 100
					continue
		while done:
			done = False
			for y in range(hauteur):
				for x in range(largeur):
					self.cartedist[self.caseX][self.caseY] = 0
					if (self.cartedist[y][x] == 1000): continue
					if (self.cartedist[y][x] >= 0):
						mini = min(self.cartedist[y+1][x], self.cartedist[y-1][x], self.cartedist[y][x+1], self.cartedist[y][x-1])
						if (mini +1 < self.cartedist[y][x]):
							self.cartedist[y][x] = mini +1
							done = True



#################################################################################
#	Class Player from Bomberman													#
#	Created by Manon : 27/01/2020												#
#																				#
#	Cette classe permet de definir toutes les propriete d'une IA				#
#	Cette classe herite de la classe player										#
#																				#
#################################################################################

class IA(Player):
	## Variable globale
	GRILLE_BOMBE = None

	def __init__(self,startX, startY, live, color, hauteur, zoom, direction):
		super(IA,self).__init__(startX, startY, live, color, hauteur, zoom) 		# Reutilisation de l'instanciation de Player()
		self.needToGoCenter = False											# Initiation d'un direction par defaut de l'IA


	## setRightDir(self):
	#	Permet de determiner le bon sprite
	#	en fonction de la direction de deplacement de l'IA
	def setRightDir(self):
		if(self.dir == (0,1)): self.spriteDir = 0
		if(self.dir == (0,-1)): self.spriteDir = 3
		if(self.dir == (1,0)): self.spriteDir = 2
		if(self.dir == (-1,0)): self.spriteDir = 1

	def move(self, posX, posY, zoom):
		self.y += posY
		self.x += posX

		if(self.x > zoom//2):
			self.x = - zoom//2
			self.caseY += 1

		if(self.x < -zoom//2):
			self.x = zoom//2
			self.caseY -= 1

		if(self.y > zoom//2):
			self.y = - zoom//2
			self.caseX += 1

		if(self.y < -zoom//2):
			self.y = zoom//2
			self.caseX -= 1

		if(self.spriteOffset == 2):
			if(self.dir != (0,0)): self.spriteCount = (self.spriteCount + 1) % 4
			self.spriteOffset = 0
		else:
			self.spriteOffset += 1
