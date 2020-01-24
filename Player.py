#################################################################################
#	Class Player from Bomberman													#
#	Created by Vincent : 24/01/2020												#
#																				#
#	Cette classe permet de definir toutes les propriete d'un Joueur				#
#																				#
#################################################################################

class Player:
	def __init__(self,startX, startY, spriteTab):
		self.x = startX
		self.y = startY
		self.sprite = spriteTab

	def draw(self, surface):
		surface.blit(self.sprite[0][0], (self.x, self.y))