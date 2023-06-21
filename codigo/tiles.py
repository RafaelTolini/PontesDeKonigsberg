import pygame
from configs import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, grupos, tipo, surface = pygame.Surface((tileS, tileS)), index = None):
        super().__init__(grupos)
        self.tipo = tipo
        self.image = surface
        self.index = index
        if tipo == "corrimao_down":
            self.rect = self.image.get_rect(topleft=(pos[0], pos[1]-5))
            self.hitbox = self.rect.inflate(0, -63)
        elif tipo == "corrimao_up":
            self.rect = self.image.get_rect(topleft=(pos[0], pos[1]-20))
            self.hitbox = self.rect.inflate(0, -63)
        elif tipo == "corrimao_vertical":
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(-63, 0)
        elif tipo == "interativo":
            self.rect = self.image.get_rect(topleft=(pos[0], pos[1]-13))
            self.hitbox = self.rect.inflate(0, 13)
            self.ativo = True
        elif tipo == "irmao":
            self.rect = self.image.get_rect(topleft=(pos[0], pos[1]-13))
            self.hitbox = self.rect.inflate(0, 13)
        elif tipo == "barreira":
            self.rect = self.image.get_rect(topleft=(pos[0], pos[1]-16))
            self.hitbox = self.rect.inflate(0, 0)
        else:
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(0, -10)