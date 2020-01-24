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
		self.spriteDir = 0
		self.spriteCount = 0

	def draw(self, surface):
		surface.blit(self.sprite[self.spriteDir][self.spriteCount], (self.x - 32, self.y - 102))