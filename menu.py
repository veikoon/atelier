import pygame
import time
pygame.init()
pygame.font.init()

RUNNING = True

fenetre = pygame.display.set_mode((1100,875))

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


    # j1 = pygame.image.load("sprite/start.png")
    # j1_x = 262
    # j1_y = 280
    # fenetre.blit(j1 ,(j1_x,j1_y))

   ##   j2 = pygame.image.load("sprite/commandes.png")
    # j2_x = 246
    # j2_y = 380
    # fenetre.blit(j2 ,(j2_x,j2_y))



    # arrow_x = 150
    # arrow_y = 430
    # fenetre.blit(arrow_sprite,(arrow_x,arrow_y))





def gerer_mouse_jeu(rectangle):
    global afficher

    mouse = pygame.mouse.get_pressed()
    if mouse[0]: # UP
        mouse_pos = pygame.mouse.get_pos()

        if rectangle.collidepoint(mouse_pos):
            print('Cliqué sur:', rectangle)
            afficher = menu

def gerer_mouse_menu(rectangle):
    global afficher

    mouse = pygame.mouse.get_pressed()
    if mouse[0]: # UP
        mouse_pos = pygame.mouse.get_pos()

        if rectangle.collidepoint(mouse_pos):
            print('Cliqué sur:', rectangle)
            afficher = jeu
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

        if KeysPressed[pygame.K_SPACE]:
            if arrow['choice'] == yes:
                done2 = True
                pygame.quit()
            if arrow['choice'] == no:
                done = True
                done2 = True

        fenetre.blit(fond ,(0,0))
        fenetre.blit(arrow['sprite'],(arrow['x'],arrow['y']))

        pygame.display.flip()
        clock.tick(30)
## Affecte la fonction menu
    #afficher = menu

def boucle_principale():
    while RUNNING:
        fenetre.fill( (0,0,0) )

        gerer_events_principale()

        ## Exécute la fonction affecté à afficher (menu/jeu)
        #afficher()
        MenuScreen()

        pygame.display.update()

    pygame.quit()



boucle_principale()