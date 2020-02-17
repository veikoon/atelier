#################################################################################
##
## Import

import pygame


#################################################################################
#   Class Bonus from Bomberman                                                  #
#   Created by ? : ?/?/2020   	                         	                    #
#                                                                               #
#   Cette classe permet de definir toutes les propriete des bonus 	            #
#                                                                               #
#################################################################################


class Bonus:
	def __init__(self, startX, startY, bonusNumber, zoom):
		self.caseX = startX
		self.caseY = startY
		self.bonus = bonusNumber
		self.sprite = self.getSprite(pygame.image.load("images/bonus/bonus.png"), zoom)


	## getSprite(self, image, zoom):
	#	Permet d'avoir les sprites des bonus
	def getSprite(self, image, zoom):
		Tab = []
		for j in range(2):
			for i in range(4):
				imTemp = image.subsurface((i*16),(j*16),16,16)
				imTemp = pygame.transform.scale(imTemp,(int(zoom/1.5),int(zoom/1.5)))
				Tab.append(imTemp)
		return Tab


	## dessine(self, surface, zoom):
	#	Dessine le bonus sur la case
	def dessine(self, surface, zoom):
		surface.blit(self.sprite[self.bonus], ((self.caseX * zoom) + zoom//5,(self.caseY * zoom) + zoom//5))


	## effect(self, player):
	#	Permet de definir les effets sur les differents joueurs
	def effect(self, player):
		if(self.bonus == 0 and player.nbBombeMax > 1):
			player.nbBombeMax -= 1
		if(self.bonus == 1 and player.rayonBombe > 1):
			player.rayonBombe -= 1
		if(self.bonus == 2 and player.lives > 1):
			player.lives -= 1
		if(self.bonus == 3 and player.vitesse > 1):
			player.vitesse -= 1
		if(self.bonus == 4):
			player.nbBombeMax += 1
		if(self.bonus == 5):
			player.rayonBombe += 1
		if(self.bonus == 6):
			player.lives += 1
		if(self.bonus == 7):
			player.vitesse += 1
