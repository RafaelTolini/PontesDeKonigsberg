import pygame

class Dialogo(pygame.sprite.Sprite):
    def __init__(self, groups, surf):

        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=(0,0))
