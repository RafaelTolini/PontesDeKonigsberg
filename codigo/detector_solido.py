import pygame
from configs import *

class DetectoresSolidos(pygame.sprite.Sprite):
    def __init__(self, pos,grupo, tipo):
        super().__init__(grupo)
        self.tipo = tipo

        if self.tipo == "horizontal":
            self.image = pygame.image.load("../imagens/detector_horizontal.png").convert()
            self.rect = self.image.get_rect(topleft=pos)
        else:
            self.image = pygame.image.load("../imagens/detector_vertical.png").convert()
            self.rect = self.image.get_rect(topleft=(pos[0], pos[1]-tileS*3))