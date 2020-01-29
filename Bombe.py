#################################################################################
#   Class Bombe from Bomberman                                                  #
#   Created by Quentin : 25/01/2020                                             #
#                                                                               #
#   Cette classe permet de definir toutes les propriete d'une Bombe         	#
#                                                                               #
#################################################################################
import pygame
from pygame import *
import time
class Bombe:
	def __init__(self,startX, startY, bombes, caseX, caseY,times,player):
		self.player = player
		self.explode = False
		self.rayon = player.rayonBombe  # initialize the game_frame counter
		self.x = startX             # Position initiale en x
		self.y = startY             # Position initiale en y
		self.sprite = self.getSprite(bombes)   # Tableau de sprites en 2D
		self.spriteDir = 0    
		self.timeBomb = times      # Selectionne le tableau de sprite (en 1D) correspondant a la direction du joueur
		self.spriteCount = 0        # Selectionne le sprite du tableau correspondant au mouvement actuel
		self.spriteOffset = 0       # Permet de changer de sprite en fonction du decalage et non a chaque mouvement
		self.caseX = caseX
		self.caseY = caseY
		self.exploFin = False
		self.finexplode = False
		self.BorderX=False
		self.BorderY=False

# getSpriteBombe(imgBombe):
#   Decoupe l'image imgBombe en sprite
#   Met les sprite a l'echelle de la carte
#   Les rajoute dans un tableau en 2D tel que :
#   Tab = [bombe1,bombe2...]
	def getSprite(self, imgBombe):
		Tab = []
		tabTemp = []
		for i in range(6):
			imTemp = imgBombe.subsurface((i*20),0,20,26)
			imTemp = pygame.transform.scale(imTemp,(40,50))
			tabTemp.append(imTemp)
		Tab.append(tabTemp)
		return Tab

	
# Passe au sprite suivant en parcourant le tableau
	def anim(self,TIME):
		finexplode = False
		decompte =1
		# print(TIME - self.timeBomb)
		# print("verifi")
		# print(1*self.spriteCount)
		if(self.finexplode):
			decompte = 0.4
		
		if (TIME - self.timeBomb > decompte*self.spriteCount):
			self.spriteCount = (self.spriteCount + 1)
			
		if(self.spriteCount == 4 and self.finexplode):
			self.exploFin = True

		if(self.spriteCount == 5 and not self.finexplode):
			self.finexplode = True
			self.timeBomb = TIME
			self.explode = True
			self.spriteCount = 0


	# def animExplo(self):
	#     TIME2 = time.time()    
	#     if (TIME2 > 1):
	#         self.spriteCountEx = (self.spriteCountEx + 1)
	#         self.game_frame += 1
	def getSpriteExplo(self,ImgFire):
		Tab = []
		for j in range(3):
			tabTemp = []
			for i in range(7):
				imTemp = ImgFire.subsurface((i*48),(j*48),48,48)
				imTemp = pygame.transform.scale(imTemp,((64,64)))
				tabTemp.append(imTemp)
			Tab.append(tabTemp)
		return Tab


# Accesseur pour l'explosion
	def Explode(self):
		return self.explode

	##  draw():
	# Permet de dessiner le personnage dont les coordonnees sont au milieu de ses pieds
	# tandis que le jeu dessine les images depuis leur coin superieur gauche:
	# (largeurPerso / 2 = 32 et hauteurPerso = 102)
	def draw(self, surface):
		surface.blit(self.sprite[self.spriteDir][self.spriteCount], (self.x - 100, self.y - 96))
	def drawExplo(self, surface,TAB,i,direction):
		if(self.finexplode ==True):
			caseX = self.caseX
			caseY = self.caseY
			e = 64*i+64
			testcase =-1

			if(direction <0):
				e = -e
				testcase = 1 
			if(self.exploFin):
				TAB[caseY][caseX]=0
	  
		
			if(self.BorderX==False):
				if(TAB[caseY][caseX+direction]==0 or TAB[caseY][caseX+direction]==3 or TAB[caseY][caseX+direction]==5 or TAB[caseY][caseX+direction]==4):
					if( TAB[caseY][caseX+direction+testcase] !=2):
						TAB[caseY][caseX+direction]=5
						if(self.exploFin):
							TAB[caseY][caseX+direction]=0
						surface.blit(self.sprite[1][self.spriteCount], (self.x+e- 100, self.y - 96))
			if(self.BorderY==False):
				if(TAB[caseY+direction][caseX]==0 or TAB[caseY+direction][caseX]==3 or TAB[caseY+direction][caseX]==5 or TAB[caseY+direction][caseX]==4):
					if( TAB[caseY+direction+testcase][caseX]!=2):         
						TAB[caseY+direction][caseX]=5
						if(self.exploFin):
						   TAB[caseY+direction][caseX]=0
						rotatebas =pygame.transform.rotate(self.sprite[1][self.spriteCount],90)    
						surface.blit(rotatebas, (self.x-100, self.y+e- 96))  

