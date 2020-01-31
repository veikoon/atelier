#################################################################################
#   Class Bombe from Bomberman                                                  #
#   Created by Quentin : 25/01/2020                                             #
#                                                                               #
#   Cette classe permet de definir toutes les propriete d'une Bombe             #
#                                                                               #
#################################################################################
import pygame
from pygame import *
import time

class Bombe:
    def __init__(self,startX, startY, bombes, zoom, times, player):
        self.player = player
        self.explode = False
        self.rayon = player.rayonBombe  # initialize the game_frame counter
        self.x = startX             # Position initiale en x
        self.y = startY             # Position initiale en y
        self.sprite = self.getSprite(bombes, zoom)   # Tableau de sprites en 2D
        self.spriteDir = 0    
        self.timeBomb = times      # Selectionne le tableau de sprite (en 1D) correspondant a la direction du joueur
        self.spriteCount = 0        # Selectionne le sprite du tableau correspondant au mouvement actuel
        self.spriteOffset = 0       # Permet de changer de sprite en fonction du decalage et non a chaque mouvement
        self.caseX = player.x // zoom
        self.caseY = player.y // zoom
        self.exploFin = False
        self.finexplode = False
        self.explX = False
        self.explY = False
        self.explmX = False
        self.explmY = False

# getSpriteBombe(imgBombe):
#   Decoupe l'image imgBombe en sprite
#   Met les sprite a l'echelle de la carte
#   Les rajoute dans un tableau en 2D tel que :
#   Tab = [bombe1,bombe2...]
    def getSprite(self, imgBombe, zoom):
        Tab = []
        tabTemp = []
        for i in range(6):
            imTemp = imgBombe.subsurface((i*20),0,20,26)
            imTemp = pygame.transform.scale(imTemp,(int(zoom * (40/64)),int(zoom * (50/64))))
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
    def getSpriteExplo(self,ImgFire, zoom):
        Tab = []
        for j in range(3):
            tabTemp = []
            for i in range(7):
                imTemp = ImgFire.subsurface((i*48),(j*48),48,48)
                imTemp = pygame.transform.scale(imTemp,((zoom,zoom)))
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

    def drawExplo(self, surface,TAB,listeBombe,i,direction, zoom):

        HAUTEUR = len(TAB)     # Nombre de cases en hauteur
        LARGEUR = len(TAB[0])  # Nombre de cases en largeur
        
        # Declanche le debu de l'explosion (branches)
        if(self.finexplode == True) : # Timer de la bombe est fini
            caseX = self.caseX        
            caseY = self.caseY
            explX = self.explX
            explY = self.explY
            spriteDir = 1 #1 pour dessiner les branches
      # permet de placer correctement la sprite
            testcase =-1

            rotatex=0
            rotatey=270
            
            place = zoom*i+zoom

            if(self.rayon-1 == i):
                spriteDir = 2 # bout du sprite

            if(direction < 0):
                rotatex=180
                rotatey=90
                place = -place
                testcase = 1 
                explX = self.explmX
                explY = self.explmY
            # Reinitialise la case de la bombe
            if(self.exploFin):
                TAB[caseY][caseX] = 0
            
            
            if(self.caseX >= LARGEUR-2 and direction >0):
                b= 2
            else:
                caseTesteX = TAB[caseY][caseX+direction]
                if(self.animStop(TAB,direction,testcase,'x',caseX,caseY) and (caseTesteX == 3 and not explX)):
                        TAB[caseY][caseX+direction]=5
                        if(direction>0):
                            self.explX= True
                        else:
                            self.explmX= True
                if(self.animGo(TAB,direction,testcase,'x',caseX,caseY)): # verifie si c'est une case bombable                    
                    
                    if(TAB[caseY][caseX+direction]==4):
                        self.explMulti(listeBombe,direction,'x') 

                    TAB[caseY][caseX+direction]=5
                    if(self.exploFin):
                        TAB[caseY][caseX+direction]=0
                    rotateXimg =pygame.transform.rotate(self.sprite[spriteDir][self.spriteCount],rotatex)    
                    surface.blit(rotateXimg, (self.x + place - 100 , self.y - 96))
                      
            
            
                    
            if(self.caseY >= HAUTEUR-2 and direction >0):
                a = 3
            else:
                caseTesteY = TAB[caseY+direction][caseX]

                if(self.animStop(TAB,direction,testcase,'y',caseX,caseY) and (caseTesteY == 3 and not explY)):
                    TAB[caseY+direction][caseX]=5
                    if(direction>0):
                        self.explY= True
                    else:
                        self.explmY= True
                
                if(self.animGo(TAB,direction,testcase,'y',caseX,caseY)):
                    if(TAB[caseY+direction][caseX]==4):
                        self.explMulti(listeBombe,direction,'y') 
                    TAB[caseY+direction][caseX] = 5

                    if(self.exploFin):
                        TAB[caseY+direction][caseX] = 0

                    rotateY =pygame.transform.rotate(self.sprite[spriteDir][self.spriteCount],rotatey)    
                    surface.blit(rotateY, (self.x - 100 , self.y + place - 96))   
        
    def animGo(self,TAB,direction,testcase,sens,caseX,caseY):
        if(sens == 'y'):  
            caseTeste = TAB[caseY+direction][caseX]
            caseTesteY = TAB[caseY+direction+testcase][caseX]
            return (((caseTeste == 0 and caseTesteY != 3)  or caseTeste == 5 or caseTeste == 4)and self.animStop(TAB,direction,testcase,sens,caseX,caseY))
        if(sens == 'x'):  
            caseTesteX = TAB[caseY][caseX+direction+testcase]
            caseTeste = TAB[caseY][caseX+direction]
            return (((caseTeste == 0 and caseTesteX != 3) or caseTeste == 5 or caseTeste == 4) and self.animStop(TAB,direction,testcase,sens,caseX,caseY))
    
    def animStop(self,TAB,direction,testcase,sens,caseX,caseY):
        if(sens == 'x'): return TAB[caseY][caseX+direction+testcase]!=2 
        if(sens == 'y'): return TAB[caseY+direction+testcase][caseX]!=2 
    
    def explMulti(self,listeBombe,direction,sens):
        for bombe in listeBombe:
            if(sens =='y'):
                 if(bombe.caseX == self.caseX and bombe.caseY == self.caseY+direction ): bombe.timeBomb = 0  
            if(sens =='x'):
                if(bombe.caseX == self.caseX +direction and bombe.caseY == self.caseY ): bombe.timeBomb = 0  