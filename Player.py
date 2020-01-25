#################################################################################
#	Class Player from Bomberman													#
#	Created by Vincent : 24/01/2020												#
#																				#
#	Cette classe permet de definir toutes les propriete d'un Joueur				#
#																				#
#################################################################################

class Player:
	def __init__(self,startX, startY, spriteTab):
		self.x = startX				# Positions initiales
		self.y = startY
		self.sprite = spriteTab		# Tableau de sprites en 2D
		self.spriteDir = 0			# Selectionne le tableau de sprite (en 1D) correspondant a la direction du joueur
		self.spriteCount = 0		# Selectionne le sprite du tableau correspondant au mouvement actuel
		self.spriteOffset = 0		# Permet de changer de sprite en fonction du decalage et non a chaque mouvement

	##	draw():
	# Permet de dessiner le personnage dont les coordonnees sont au milieu de ses pieds
	# tandis que le jeu dessine les images depuis leur coin superieur gauche:
	# (largeurPerso / 2 = 32 et hauteurPerso = 102)
	def draw(self, surface):
		surface.blit(self.sprite[self.spriteDir][self.spriteCount], (self.x - 32, self.y - 102))