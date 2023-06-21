import pygame
from configs import *

class Detector(pygame.sprite.Sprite):
    def __init__(self, pos, grupos, tipo, index):
        super().__init__(grupos)
        self.tipo = tipo

        if self.tipo == "detector_horizontal":
            self.image = pygame.image.load("../imagens/detector_horizontal.png").convert()
            self.rect = self.image.get_rect(topleft=pos)
        else:
            self.image = pygame.image.load("../imagens/detector_vertical.png").convert()
            self.rect = self.image.get_rect(topleft=(pos[0], pos[1]-tileS*3))

        self.pos = pos
        self.index = index
        self.lock = False
        self.ativo =  False