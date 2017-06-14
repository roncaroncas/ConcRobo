import pygame
from time import sleep
pygame.init()

pygame.display.set_caption('Robo')

SCREEN = pygame.display.set_mode((200,150))

myfont = pygame.font.SysFont("arial", 15)

pygame.key.set_repeat(100)

class Cliente:
    def __init__(self):

        #definindo a surface
        self.screen = SCREEN
        self.screen.fill([220,220,220])

        pygame.display.update()


    while True:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                print (("You pressed {}").format(event.key))

        #keys = pygame.key.get_pressed() 
        #if keys[pygame.K_w]: 
        #    print ("DOWN")
        #for e in pygame.event.get(): 
        #    pass

Cliente()
