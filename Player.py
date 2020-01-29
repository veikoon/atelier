#################################################################################
#	Class Player from Bomberman													#
#	Created by Vincent : 24/01/2020												#
#																				#
#	Cette classe permet de definir toutes les propriete d'un Joueur				#
#																				#
#################################################################################

import pygame

class Player:
	def __init__(self,startX, startY, color, hauteur, zoom):
		self.x = startX				# Positions initiales
		self.y = startY
		self.sprite = self.getSprite(color, hauteur, zoom)	# Tableau de sprites en 2D
		self.spriteDir = 0			# Selectionne le tableau de sprite (en 1D) correspondant a la direction du joueur
		self.spriteCount = 0		# Selectionne le sprite du tableau correspondant au mouvement actuel
		self.spriteOffset = 0		# Permet de changer de sprite en fonction du decalage et non a chaque mouvement
		self.lives = 1
		self.nbBombe = 1

	##	draw():
	# Permet de dessiner le personnage dont les coordonnees sont au milieu de ses pieds
	# tandis que le jeu dessine les images depuis leur coin superieur gauche:
	# (largeurPerso / 2 = 32 et hauteurPerso = 102)
	def draw(self, surface):
		surface.blit(self.sprite[self.spriteDir][self.spriteCount], (self.x - 32, self.y - 102))

	# getSprite(Color):
	#   Decoupe l'image Color en sprite
	#   Met les sprite a l'echelle de la carte
	#   Les rajoute dans un tableau en 2D tel que :
	#   Tab = [[SpriteAvant_1, SpriteAvant_2, ...],[SpriteDroit_1, SpriteDroit_2, ...]]
	def getSprite(self, Color, hauteur, zoom):
		Tab = []
		for j in range(4):
			tabTemp = []
			for i in range(4):
				imTemp = Color.subsurface((i*29) + (3*i) + 3,0 + (j*48),29,46)
				imTemp = pygame.transform.scale(imTemp,(zoom,hauteur))
				tabTemp.append(imTemp)
			Tab.append(tabTemp)
		return Tab

	## move():
	#   On change les coordonnees du joueur selon son deplacement
	#   On regarde la retenu de sprite est complete ou non:
	#       * Si oui on change de sprite (+1 %Nombre de sprite pour ne pas sortir du tableau) et et on reset la retenu de sprite
	#       * Si non on augmente la retenu
	#   (permet d'eviter un changement de sprite trop rapide par rapport a sa vitesse)
	def move(self, posX, posY):
		self.y += posY
		self.x += posX
		if(self.spriteOffset == 2):
			self.spriteCount = (self.spriteCount + 1) % 4
			self.spriteOffset = 0
		else:
			self.spriteOffset += 1



#################################################################################
#	Class Player from Bomberman													#
#	Created by Manon : 27/01/2020												#
#																				#
#	Cette classe permet de definir toutes les propriete d'une IA				#
#	Cette classe herite de la classe player										#
#																				#
#################################################################################


class IA(Player):

	def __init__(self,startX, startY, color, hauteur, zoom, direction):
		super(IA,self).__init__(startX, startY, color, hauteur, zoom)
		self.dir = direction

	def setRightDir(self):
		if(self.dir == (0,1)): self.spriteDir = 0
		if(self.dir == (0,-1)): self.spriteDir = 3
		if(self.dir == (1,0)): self.spriteDir = 2
		if(self.dir == (-1,0)): self.spriteDir = 1
