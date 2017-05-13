##################################################################
##                                                              ##
##      CODIGO CRIADO PELO GRUPO TURING - POLI USP 2016         ##
##      https://www.facebook.com/grupoturing.poliusp            ##
##      Todos podem usar este codigo livremente                 ##
##                                                              ##
##################################################################

import pygame
from time import sleep
pygame.init()

pygame.display.set_caption('Robo')

SCREEN      = pygame.display.set_mode((800,600))

myfont = pygame.font.SysFont("arial", 15)


class MovePad(pygame.sprite.Sprite):
    def __init__(self,num,update=False):

        cox = 670   #centerOcuppyX
        coy = 140   #centerOcuppyY

        dPad = 43  #distancia do center do Pad

        if num == 1:
            self.imgName, self.center = "move_down"  , (cox,        coy+dPad)
        elif num == 2:
            self.imgName, self.center = "move_right" , (cox+dPad,  coy      )
        elif num == 3:
            self.imgName, self.center = "move_up"    , (cox,        coy-dPad)
        elif num == 4:
            self.imgName, self.center = "move_left"  , (cox-dPad,  coy      )


        #self.img = IMAGES_BUTTONS[self.imgName]
        #self.rect = self.img.get_rect(center=self.center)
        #SCREEN.blit(self.img,self.rect)

        if update:
            pygame.display.update()

# Mostra o display o valor de algum 
class Value1(pygame.sprite.Sprite):
    pass


class Cliente:
    def __init__(self):

        SCREEN.fill([220,220,220])

        #definindo a surface
        self.screen = SCREEN

        #definindo as acoes
        self.acoes = [MovePad(i) for i in range(1,5)]
        pygame.display.update()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    print (("You pressed {}").format(event.key))
                elif event.type == pygame.KEYUP:
                    print (("You released {}").format(event.key))





Cliente().run()
