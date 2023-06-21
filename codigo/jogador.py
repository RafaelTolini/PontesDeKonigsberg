from typing import Any
import pygame
from configs import *
from funcs import importa_imagens
from detector_solido import DetectoresSolidos

class Jogador(pygame.sprite.Sprite):
    def __init__(self, pos, grupos, solidos, interativos, texto, irmaos, irmao_texto, detectores):
        super().__init__(grupos)
        self.image = pygame.image.load("../imagens/player.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0,-26)

        self.assets()
        self.estado = "down"
        self.frame = 0
        self.vel_animacao = 0.1

        self.direction = pygame.math.Vector2()
        self.speed = 5
        self.solidos = solidos
        self.interativos = interativos

        self.dialogue_state = -1
        self.dialogue_cooldown = 300
        self.dialogue_lock = False
        self.dialogue_time = pygame.time.get_ticks()
        self.conversa_count = 0

        self.text = texto
        self.irmao_text = irmao_texto

        self.irmao_tutorial = 0
        self.irmaos = irmaos
        self.irmao_state = -1

        self.detectores = detectores
        self.ultimo_ativo = -1
        self.detectores_solidos = pygame.sprite.Group()

    def assets(self):
        path = "../imagens/jogador/"

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

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.direction.y = -1
            self.estado = "up"
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.direction.y = 1
            self.estado = "down"
        else:
            self.direction.y = 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1
            self.estado = "left"
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
            self.estado = "right"
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE] and not self.dialogue_lock:
            self.interact()
            self.dialogue_lock = True
            self.dialogue_time = pygame.time.get_ticks()

    def mov(self, speed):

        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.coll("horizontal")
        self.hitbox.y += self.direction.y * speed
        self.coll("vertical")
        self.rect.center = self.hitbox.center
        self.coll("detector")

    def coll(self, dir):

        if dir == "horizontal":
            for i in self.solidos:
                if i.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = i.hitbox.left
                    elif self.direction.x < 0:
                        self.hitbox.left = i.hitbox.right
            
            try:
                for i in self.detectores_solidos:
                    if i.rect.colliderect(self.hitbox):
                        if self.direction.x > 0:
                            self.hitbox.right = i.rect.left
                        elif self.direction.x < 0:
                            self.hitbox.left = i.rect.right
            except:
                pass

        if dir == "vertical":
            for i in self.solidos:
                if i.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = i.hitbox.top
                    elif self.direction.y < 0:
                        self.hitbox.top = i.hitbox.bottom

            try:
                for i in self.detectores_solidos:
                    if i.rect.colliderect(self.hitbox):
                        if self.direction.y > 0:
                            self.hitbox.bottom = i.rect.top
                        elif self.direction.y < 0:
                            self.hitbox.top = i.rect.bottom
            except:
                pass 

        if dir == "detector":
            for dec in self.detectores:
                if dec.rect.colliderect(self.hitbox) and not dec.ativo and not dec.lock:
                    dec.ativo = True
                    self.verifica_ativos(dec)
                    self.ultimo_ativo = dec.index

    def verifica_ativos(self, dec):
        
        found = False
        if (dec.index in [2,5] and self.ultimo_ativo in [2,5]):
            found = True
        elif (dec.index in [3,6] and self.ultimo_ativo in [3,6]):
            found = True
        elif (dec.index in [7,4] and self.ultimo_ativo in [7,4]):
            found = True
        elif (dec.index in [1,0] and self.ultimo_ativo in [1,0]):
            found = True
        elif (dec.index in [8,11] and self.ultimo_ativo in [8,11]):
            found = True
        elif (dec.index in [12,9] and self.ultimo_ativo in [12,9]):
            found = True
        elif (dec.index in [13,10] and self.ultimo_ativo in [13,10]):
            found = True
        else:
            for dec in self.detectores:
                if dec.index == self.ultimo_ativo:
                    dec.ativo = False

        if found:
            dec.lock = True
            for decs in self.detectores:
                if decs.index == self.ultimo_ativo:
                    decs.lock = True
                    if dec.index in [2,3,4,10,9,8]:
                        DetectoresSolidos((dec.pos[0], dec.pos[1]+tileS+40), [self.detectores_solidos], "horizontal")
                        DetectoresSolidos((decs.pos[0], decs.pos[1]-tileS), [self.detectores_solidos], "horizontal")
                    elif dec.index in [5,6,7,13,12,11]:
                        DetectoresSolidos((dec.pos[0], dec.pos[1]-tileS-40), [self.detectores_solidos], "horizontal")
                        DetectoresSolidos((decs.pos[0], decs.pos[1]+tileS), [self.detectores_solidos], "horizontal")
                    elif dec.index == 1:
                        DetectoresSolidos((dec.pos[0]-tileS*2, dec.pos[1]), [self.detectores_solidos], "vertical")
                        DetectoresSolidos((decs.pos[0]+tileS, decs.pos[1]), [self.detectores_solidos], "vertical")
                    else:
                        DetectoresSolidos((dec.pos[0]+tileS*2, dec.pos[1]), [self.detectores_solidos], "vertical")
                        DetectoresSolidos((decs.pos[0]-tileS, decs.pos[1]), [self.detectores_solidos], "vertical")

    def interact(self):

        for interativo in self.interativos:
            if interativo.rect.inflate(10, 23).colliderect(self.hitbox) and interativo.ativo:
                self.dialogue_state += 1
                self.interagindo = interativo.index
                try:
                    self.texto_atual = self.text[self.conversa_count][self.dialogue_state]
                except:
                    self.conversa_count +=1
                    self.dialogue_state = -1
                    interativo.ativo = False

        for irmao in self.irmaos:
            if irmao.rect.inflate(10, 23).colliderect(self.hitbox):
                self.irmao_state += 1
                self.irmão_interagindo = irmao.index
                try:
                    self.texto_atual = self.irmao_text[self.irmao_tutorial][self.irmao_state]
                except:
                    if self.irmao_tutorial == 0:
                        self.irmao_tutorial = 1
                        self.irmao_state = -1
                    else:
                        self.irmao_state = -2
                    # interativo.ativo = False
                

    def cooldown(self):

        time = pygame.time.get_ticks()
        if time > self.dialogue_time + self.dialogue_cooldown:
            self.dialogue_lock = False


    def update(self):
        
        if self.dialogue_state == -1 and self.irmao_state == -1:
            self.cooldown()
            self.input()
            self.get_estado()
            self.animar()
            self.mov(self.speed)
        else:
            self.cooldown()
            self.input()
