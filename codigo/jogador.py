from typing import Any
import pygame
from configs import *
from funcs import importa_imagens

class Jogador(pygame.sprite.Sprite):
    def __init__(self, pos, grupos, solidos):
        super().__init__(grupos)
        self.image = pygame.image.load("./imagens/player.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0,-26)

        self.assets()
        self.estado = "down"
        self.frame = 0
        self.vel_animacao = 0.1

        self.direction = pygame.math.Vector2()
        self.speed = 5
        self.solidos = solidos

    def assets(self):
        path = "./imagens/jogador/"

        self.animacoes = {
            "up":[], "down":[], "left":[], "right":[],
            "up_idle":[], "down_idle":[], "left_idle":[], "right_idle":[]
        }

        for animacao in self.animacoes.keys():
            fpath = path+animacao
            self.animacoes[animacao] = importa_imagens(fpath)

    def get_estado(self):

        if self.direction.x == 0  and self.direction.y == 0:
            if "idle" not in self.estado:
                self.estado += "_idle"


    def animar(self):

        animacao = self.animacoes[self.estado]

        self.frame += self.vel_animacao
        if self.frame >= len(animacao):
            self.frame = 0

        self.image = animacao[int(self.frame)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def input(self):

        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.direction.y = -1
            self.estado = "up"
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.estado = "down"
        else:
            self.direction.y = 0

        if keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.estado = "left"
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.estado = "right"
        else:
            self.direction.x = 0

    def mov(self, speed):

        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.coll("horizontal")
        self.hitbox.y += self.direction.y * speed
        self.coll("vertical")
        self.rect.center = self.hitbox.center

    def coll(self, dir):

        if dir == "horizontal":
            for i in self.solidos:
                if i.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = i.hitbox.left
                    elif self.direction.x < 0:
                        self.hitbox.left = i.hitbox.right

        if dir == "vertical":
            for i in self.solidos:
                if i.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = i.hitbox.top
                    elif self.direction.y < 0:
                        self.hitbox.top = i.hitbox.bottom 

    def update(self):

        self.input()
        self.get_estado()
        self.animar()
        self.mov(self.speed)

