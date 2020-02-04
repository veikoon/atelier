class Bonus:
	def __init__(self, bonusNumber, image, zoom):
		self.bonus = bonusNumber
		self.sprite = self.getSprite(image, zoom)

	def getSprite(image, zoom):
		Tab = []
		for j in range(2):
			for i in range(2):
				imTemp = self.color.subsurface((i*16),(j*16),16,16)
				imTemp = pygame.transform.scale(imTemp,(zoom//2,zoom//2))
				Tab.append(imTemp)
		self.sprite = Tab