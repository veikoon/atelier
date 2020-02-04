import pygame

class Bonus:
	def __init__(self, startX, startY, bonusNumber, zoom):
		self.caseX = startX
		self.caseY = startY
		self.bonus = bonusNumber
		self.sprite = self.getSprite(pygame.image.load("images/bonus/bonus.png"), zoom)

	def getSprite(self, image, zoom):
		Tab = []
		for j in range(2):
			for i in range(2):
				imTemp = image.subsurface((i*16),(j*16),16,16)
				imTemp = pygame.transform.scale(imTemp,(int(zoom/1.5),int(zoom/1.5)))
				Tab.append(imTemp)
		return Tab

	def draw(self, surface, zoom):
		surface.blit(self.sprite[self.bonus-1], ((self.caseX * zoom) + zoom//5,(self.caseY * zoom) + zoom//5))

	def effect(self, player):
		if(self.bonus == 1 and player.nbBombeMax > 1):
			player.nbBombeMax -= 1
		if(self.bonus == 2 and player.rayonBombe > 1):
			player.rayonBombe -= 1
		if(self.bonus == 3):
			player.nbBombeMax += 1
		if(self.bonus == 4):
			player.rayonBombe += 1
