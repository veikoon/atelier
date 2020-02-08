#################################################################################
##
## Import

import pygame
from pygame import *
import time
import random
from Bonus import Bonus
#################################################################################
#   Class Bombe from Bomberman                                                  #
#   Created by Quentin : 25/01/2020                                             #
#                                                                               #
#   Cette classe permet de definir toutes les propriete d'une Bombe             #
#                                                                               #
#################################################################################

class Bombe:
    def __init__(self,startX, startY, bombes, zoom, times, player):
        self.player = player                         # Association d'une bombe au joueur
        self.explode = False                         # Explosion de la bombe
        self.rayon = player.rayonBombe               # Initialize the game_frame counter
        self.x = startX                              # Position initiale en x
        self.y = startY                              # Position initiale en y
        self.sprite = self.getSprite(bombes, zoom)   # Tableau de sprites en 2D
        self.spriteDir = 0    
        self.timeBomb = times      # Selectionne le tableau de sprite (en 1D) correspondant a la direction du joueur
        self.spriteCount = 0        # Selectionne le sprite du tableau correspondant au mouvement actuel
        self.spriteOffset = 0       # Permet de changer de sprite en fonction du decalage et non a chaque mouvement
        self.caseX = player.caseY
        self.caseY = player.caseX
        self.exploFin = False
        self.finexplode = False
        self.explX = False
        self.explY = False
        self.explmX = False
        self.explmY = False
        self.stopmX = 10
        self.stopmY =10
        self.stopX = 10
        self.stopY =10

    ## getSpriteBombe(self, imgBombe, zoom):
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


    ## anim(self, time):
    #   Passe au sprite suivant en parcourant le tableau
    def anim(self,TIME):
        finexplode = False
        decompte =1
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


    ## animExplo(self, imgfire, zoom):
    #    Fonction qui affiche l'explosion
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


    ## Explode(self):
    #   Accesseur pour l'explosion
    def Explode(self):
        return self.explode


    ##  dessine(self, surface):
    #   Permet de dessiner le personnage dont les coordonnees sont au milieu de ses pieds
    #   Tandis que le jeu dessine les images depuis leur coin superieur gauche:
    #   (largeurPerso / 2 = 32 et hauteurPerso = 102)
    def dessine(self, surface):
        if(self.finexplode):
            surface.blit(self.sprite[self.spriteDir][self.spriteCount], (self.x - 100, self.y - 96))
        else:
            surface.blit(self.sprite[self.spriteDir][self.spriteCount], (self.x - 90, self.y - 96))


    ## dessineExplo(self, surface, tab, listebombe, i, direction, zoom):
    #   Dessine l'explosion de la bombe
    #   On verifie les cases au alentour pour savoir jusqu'où va l'explosion
    def dessineExplo(self, surface,TAB,listeBombe,i,direction, zoom, listebonus):
        HAUTEUR = len(TAB)          # Nombre de cases en hauteur
        LARGEUR = len(TAB[0])       # Nombre de cases en largeur

        # Declanche le debu de l'explosion (branches)
        if(self.finexplode == True) : # Timer de la bombe est fini
            caseX = self.caseX        
            caseY = self.caseY
            explX = self.explX
            explY = self.explY
            spriteDir = 1   # 1 pour dessiner les branches
            testcase =-1    # Permet de placer correctement la sprite
            rotatex=0       # Rotation de la sprite en x
            rotatey=270     # Rotation de la sprite en y
            place = zoom*i+zoom     # Place correctement la sprite de l'explosion
            stopX1 =self.stopX
            stopY1 =self.stopY
            if(self.rayon-1 == i):
                spriteDir = 2   # Bout de l'explosion

            if(direction < 0):
                rotatex=180
                rotatey=90
                place = -place
                testcase = 1
                explX = self.explmX
                explY = self.explmY
                stopX1 =self.stopmX
                stopY1 =self.stopmY
            if(self.exploFin):     # Reinitialise la case de la bombe
                TAB[caseY][caseX] = 0            
           
            #if( i > LARGEUR-self.caseX-2 and direction >0):
            if(i <= stopX1): 
                if( (self.caseX+direction <0 )or (i > LARGEUR-self.caseX-2 and direction >0)):
                    b= 2
                else:
                    
                    caseTesteX = TAB[caseY][caseX+direction]
                    if(self.animStop(TAB,direction,testcase,'x',caseX,caseY) and ((caseTesteX == 3 or caseTesteX == 6) and not explX)):
                        
                        if(not random.randrange(3) and caseTesteX != 6): 
                            listebonus.append(Bonus(caseX+direction, caseY, random.randrange(8), zoom))
                            TAB[caseY][caseX+direction]=6
                        else:
                            TAB[caseY][caseX+direction]=5
                            for bonus in listebonus:
                                if(bonus.caseY == caseY and bonus.caseX == caseX + direction): listebonus.remove(bonus)

                        if(direction>0):
                            self.explX= True
                            self.stopX=i
                        else:
                            self.explmX= True
                            self.stopmX=i

                
             

                    if(self.animGo(TAB,direction,testcase,'x',caseX,caseY)): # verifie si c'est une case bombable                    
                       

                        if(TAB[caseY][caseX+direction]==4):
                            self.explMulti(listeBombe,direction,'x')
                        if((caseX +direction)>0):
                            TAB[caseY][caseX+direction]=5
                        if(self.exploFin):                     
                            TAB[caseY][caseX+direction]=0

                        rotateXimg =pygame.transform.rotate(self.sprite[spriteDir][self.spriteCount],rotatex)    
                        surface.blit(rotateXimg, (self.x + place- 100 , self.y - 96))
                
            if(i <= stopY1): 
                if((i > HAUTEUR-self.caseY-2 and direction >0) or (self.caseY+direction <0)):
                    a = 3

                else:
                    caseTesteY = TAB[caseY+direction][caseX]

                    if(self.animStop(TAB,direction,testcase,'y',caseX,caseY) and ((caseTesteY == 3 or caseTesteY == 6) and not explY)):
                        tempRand = random.randrange(5)
                        if(not random.randrange(3) and caseTesteY != 6):
                            listebonus.append(Bonus(caseX, caseY+direction, random.randrange(8), zoom))
                            TAB[caseY+direction][caseX]=6
                        else:
                            TAB[caseY+direction][caseX]=5
                            for bonus in listebonus:
                                if(bonus.caseY == caseY + direction and bonus.caseX == caseX): listebonus.remove(bonus)

                        if(direction>0):
                            self.explY= True
                            self.stopY=i
                        else:
                            self.explmY= True
                            self.stopmY=i

                    if(self.animGo(TAB,direction,testcase,'y',caseX,caseY)):
                        
                        if(TAB[caseY+direction][caseX]==4):
                            self.explMulti(listeBombe,direction,'y')
                        TAB[caseY+direction][caseX] = 5

                        if(self.exploFin):
                            TAB[caseY+direction][caseX] = 0

                        rotateY =pygame.transform.rotate(self.sprite[spriteDir][self.spriteCount],rotatey)    
                        surface.blit(rotateY, (self.x - 100 , self.y + place - 96))   
                    


    ## animGo(self, tab, direction, testcase, sens, casex, casey):
    #   Permet de savoir le sens de l'affichage de la sprite de l'explosion
    #   On verifie la coherence avec les murs autour
    def animGo(self,TAB,direction,testcase,sens,caseX,caseY):
        if(sens == 'y'):
            caseTeste = TAB[caseY+direction][caseX]
            caseTesteY = TAB[caseY+direction+testcase][caseX]
            return (((caseTeste == 0 and caseTesteY != 3)  or caseTeste == 5 or caseTeste == 4)and self.animStop(TAB,direction,testcase,sens,caseX,caseY))

        if(sens == 'x'):
            caseTesteX = TAB[caseY][caseX+direction+testcase]
            caseTeste = TAB[caseY][caseX+direction]
            return (((caseTeste == 0 and caseTesteX != 3) or caseTeste == 5 or caseTeste == 4) and self.animStop(TAB,direction,testcase,sens,caseX,caseY))


    ## animStop(self, tab, directio, testcase, sens, casex, casey):
    #   Permet de savoir quand la sprite doit s'arreter
    #   Prend enn compte les murs autour et ce qui a deja ete detruit
    def animStop(self,TAB,direction,testcase,sens,caseX,caseY):
        if(sens == 'x'): return TAB[caseY][caseX+direction+testcase]!=2
        if(sens == 'y'): return TAB[caseY+direction+testcase][caseX]!=2


    ## explMulti(self, listebombe, direction, sens):
    #   Permet de faire exploser une bombe qui est a cote d'une autre
    #   Si une bombe exploser et qu'une autre bombe est dans son rayon d'explosion alors elle explose en meme temps
    def explMulti(self,listeBombe,direction,sens):
        for bombe in listeBombe:
            if(sens =='y'):
                 if(bombe.caseX == self.caseX and bombe.caseY == self.caseY+direction ): bombe.timeBomb = 0
            
            if(sens =='x'):
                if(bombe.caseX == self.caseX +direction and bombe.caseY == self.caseY ): bombe.timeBomb = 0     