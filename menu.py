import pygame
import time
import os
pygame.init()
pygame.font.init()

RUNNING = True

fenetre = pygame.display.set_mode((1100,875))
jouer = False
myfont = pygame.font.SysFont('Helvetic', 20)
clock = pygame.time.Clock()
arrow_sprite = pygame.image.load("sprite/arrow.png")
fond = pygame.image.load("sprite/menu2.png")
fondx=0
fondy=0
fenetre.blit(fond ,(fondx,fondy))
def gerer_events_principale():
    global RUNNING
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False



def MenuScreen():
    global screen,done,clock, arrow_sprite
    done2 = False
    start = 1
    commandes = 2
    yes = True
    no = False
    arrow = {}
    arrow['x']= 150
    arrow['y']= 430
    arrow['sprite'] = arrow_sprite
    arrow['choice'] = yes

    last_time = 0

    while not done2:

        time = int( pygame.time.get_ticks() / 100 )

        event = pygame.event.Event(pygame.USEREVENT)
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                 done = True
                 done2 = True

        KeysPressed = pygame.key.get_pressed()

        if KeysPressed[pygame.K_DOWN] and time - last_time > 3:
            last_time = time
            if arrow['y'] == 430:
                arrow['y']= 560
                arrow['choice'] = no
            else:
                arrow['y']= 430
                arrow['choice'] = yes

        if KeysPressed[pygame.K_UP] and time - last_time > 3:
            last_time = time
            if arrow['y'] == 430:
                arrow['y']= 560
                arrow['choice'] = no
            else:
                arrow['y']= 430
                arrow['choice'] = yes

        if KeysPressed[pygame.K_RETURN]:

            if arrow['choice'] == yes:
                done2 = True
                jouer = True
                return jouer


            if arrow['choice'] == no:
                done = True
                done2 = True
                jouer = False
                return jouer

        fenetre.blit(fond ,(0,0))
        fenetre.blit(arrow['sprite'],(arrow['x'],arrow['y']))

        pygame.display.flip()
        clock.tick(30)
        
## Affecte la fonction menu

jouer = MenuScreen()
if jouer == True:
    pygame.quit()
    os.system('python3 main.py')
pygame.quit()
