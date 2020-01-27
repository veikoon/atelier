#################################################################################
#   Class Bombe from Bomberman                                                  #
#   Created by Quentin : 25/01/2020                                             #
#                                                                               #
#   Cette classe permet de definir toutes les propriete d'une Bombe         	#
#                                                                               #
#################################################################################
import pygame
from pygame import *
class Bombe:
    def __init__(self,startX, startY, bombes):
        self.explode = False
        self.game_frame = 0         # initialize the game_frame counter
        self.x = startX             # Position initiale en x
        self.y = startY             # Position initiale en y
        self.sprite = self.getSprite(bombes)     # Tableau de sprites en 2D
        self.spriteDir = 0          # Selectionne le tableau de sprite (en 1D) correspondant a la direction du joueur
        self.spriteCount = 0        # Selectionne le sprite du tableau correspondant au mouvement actuel
        self.spriteOffset = 0       # Permet de changer de sprite en fonction du decalage et non a chaque mouvement
        self.ListBomb =[]


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
    def anim(self):
        if (self.game_frame % 20 == 0):
            self.spriteCount = (self.spriteCount + 1) % 6
            self.spriteOffset = 0

        self.game_frame += 1
        if(self.spriteCount==5):
            self.explode = True



# Accesseur pour l'explosion
    def Explode(self):
        return self.explode

    ##  draw():
    # Permet de dessiner le personnage dont les coordonnees sont au milieu de ses pieds
    # tandis que le jeu dessine les images depuis leur coin superieur gauche:
    # (largeurPerso / 2 = 32 et hauteurPerso = 102)
    def draw(self, surface):
        surface.blit(self.sprite[self.spriteDir][self.spriteCount], (self.x - 32, self.y - 102))
