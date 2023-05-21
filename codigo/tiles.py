import pygame
from configs import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, grupos, tipo, surface = pygame.Surface((tileS, tileS))):
        super().__init__(grupos)
        self.tipo = tipo
        self.image = surface
        if tipo == "corrimao_down":
            self.rect = self.image.get_rect(topleft=(pos[0], pos[1]-5))
            self.hitbox = self.rect.inflate(0, -63)
        elif tipo == "corrimao_up":
            self.rect = self.image.get_rect(topleft=(pos[0], pos[1]-20))
            self.hitbox = self.rect.inflate(0, -63)
        elif tipo == "corrimao_vertical":
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(-63, 0)
        else:
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(0, -10)