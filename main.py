import pygame
import random
import copy

#################################################################
##
##  variables du jeu 
 
# 0 vide
# 1 mur
# 2 maison des fantomes (ils peuvent circuler mais pas pacman)

TAB = [ [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
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

# Define some colors
BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
GREEN = [0, 255, 0]
RED   = [255, 0, 0]
BLUE  = [0 , 0 , 255]
CYAN  = [ 0, 255 ,255]
ORANGE = [255, 165, 0 ]
PINK = [ 255,105,180]
YELLOW = [255,255,0]          

   
ZOOM = 64   # taille d'une case en pixels
HAUTEUR = len(TAB)     # nb de cases en hauteur
LARGEUR = len(TAB[0])  # nb de cases en largeur

Block = pygame.image.load("images/blocks/stone.png")
BlockMiddle = pygame.image.load("images/blocks/stone2.png")
Grass = pygame.image.load("images/blocks/grass.png")

Bleu = pygame.image.load("images/ia/Bleu/sprite.png")
Rouge = pygame.image.load("images/ia/Rouge/sprite.png")
Jaune = pygame.image.load("images/ia/Jaune/sprite.png")
Orange = pygame.image.load("images/ia/Orange/sprite.png")
Vert = pygame.image.load("images/ia/Vert/sprite.png")

BleuSprite = []
RougeSprite = []
JauneSprite = []
OrangeSprite = []
VertSprite = []

def getSprite(Tab, Color):
	for i in range(4):
		imTemp = Color.subsurface((i*29) + (3*i) + 3,0,29,46)
		imTemp = pygame.transform.scale(imTemp,(64,102))
		Tab.append(imTemp)

getSprite(BleuSprite,Bleu)
getSprite(RougeSprite,Rouge)
getSprite(JauneSprite,Jaune)
getSprite(OrangeSprite,Orange)
getSprite(VertSprite,Vert)

#################################################################
##
##  INIT FENETRE 
def Dessine():
	for i in range(LARGEUR):
		for j in range(HAUTEUR):
			if(TAB[j][i] == 2):
				screen.blit(BlockMiddle,(i*ZOOM,j*ZOOM))
			if(TAB[j][i] == 1):
				screen.blit(Block,(i*ZOOM,j*ZOOM))
			if(TAB[j][i] == 0):
				screen.blit(Grass,(i*ZOOM,j*ZOOM))

	screen.blit(BleuSprite[0],(64,0))
	screen.blit(BleuSprite[1],(64,102))
	screen.blit(BleuSprite[2],(64,204))
	screen.blit(BleuSprite[3],(64,306))

	screen.blit(RougeSprite[0],(128,0))
	screen.blit(RougeSprite[1],(128,102))
	screen.blit(RougeSprite[2],(128,204))
	screen.blit(RougeSprite[3],(128,306))

	screen.blit(JauneSprite[0],(192,0))
	screen.blit(JauneSprite[1],(192,102))
	screen.blit(JauneSprite[2],(192,204))
	screen.blit(JauneSprite[3],(192,306))

	screen.blit(OrangeSprite[0],(256,0))
	screen.blit(OrangeSprite[1],(256,102))
	screen.blit(OrangeSprite[2],(256,204))
	screen.blit(OrangeSprite[3],(256,306))

	screen.blit(VertSprite[0],(320,0))
	screen.blit(VertSprite[1],(320,102))
	screen.blit(VertSprite[2],(320,204))
	screen.blit(VertSprite[3],(320,306))

# Setup
pygame.init()
police = pygame.font.SysFont("arial", 22)
screeenWidth = (LARGEUR+1) * ZOOM
screenHeight = (HAUTEUR+2) * ZOOM
screen = pygame.display.set_mode((screeenWidth,screenHeight))
pygame.display.set_caption("ESIEE - BOMBERMAN")
done = False
clock = pygame.time.Clock()   
pygame.mouse.set_visible(True)

#################################################################
##
##   GAME LOOP


# -------- Main Program Loop -----------
while not done:
   event = pygame.event.Event(pygame.USEREVENT)    
   pygame.event.pump()
   for event in pygame.event.get():
      if event.type == pygame.QUIT:
         done = True
     
   pygame.display.flip()
 
   Dessine()
    # Limit frames per second
   clock.tick(20)
 
# Close the window and quit.
pygame.quit()