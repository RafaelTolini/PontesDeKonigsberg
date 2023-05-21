from typing import Iterable, Union
import pygame
from pygame.sprite import AbstractGroup
from configs import *
from tiles import Tile
from jogador import Jogador
from funcs import read_csv, importa_imagens

class Mundo:
    def __init__(self):

        self.visiveis = Camera()
        self.solidos = pygame.sprite.Group()
        self.interativos = pygame.sprite.Group()

        self.criar_mundo()
    
    def criar_mundo(self):
        
        #usando arquivos CSV para adicionar sprites ao grupo dos Tiles
        layout = {
            "barreira":read_csv("./CSVs/colisoes.csv"),
            "corrimao_down":read_csv("./CSVs/corrimao_down.csv"),
            "corrimao_up":read_csv("./CSVs/corrimao_up.csv"),
            "corrimao_vertical":read_csv("./CSVs/corrimao_vertical.csv"),
            "corrimao_cornerup_left":read_csv("./CSVs/corrimao_cornerup_left.csv"),
            "corrimao_cornerup_right":read_csv("./CSVs/corrimao_cornerup_right.csv"),
            "corrimao_cornerdown_left":read_csv("./CSVs/corrimao_cornerdown_left.csv"),
            "corrimao_cornerdown_right":read_csv("./CSVs/corrimao_cornerdown_right.csv"),
            #"interativo":read_csv("./CSVs/interativos.csv")
        }
        surfs = {
            "corrimao":importa_imagens("./imagens/corrimao")
        }
        for nome, layout in layout.items():
            for rowi, row in enumerate(layout):
                for coli, col in enumerate(row):
                    if col != "-1":
                        x = coli*tileS
                        y = rowi*tileS
                        if nome == "barreira":
                            Tile((x,y), [self.solidos], "barreira")
                        elif nome == "interativo":
                            Tile((x,y), [self.solidos, self.visiveis, self.interativos], "interativo")
                        elif nome == "corrimao_down":
                            Tile((x,y), [self.solidos, self.visiveis], "corrimao_down", surfs["corrimao"][0])
                        elif nome == "corrimao_up":
                            Tile((x,y), [self.solidos, self.visiveis], "corrimao_up", surfs["corrimao"][0])
                        elif nome == "corrimao_cornerup_left":
                            Tile((x,y), [self.solidos, self.visiveis], "corrimao_up", surfs["corrimao"][1])
                        elif nome == "corrimao_cornerup_right":
                            Tile((x,y), [self.solidos, self.visiveis], "corrimao_up", surfs["corrimao"][2])
                        elif nome == "corrimao_cornerdown_left":
                            Tile((x,y), [self.solidos, self.visiveis], "corrimao_down", surfs["corrimao"][3])
                        elif nome == "corrimao_cornerdown_right":
                            Tile((x,y), [self.solidos, self.visiveis], "corrimao_down", surfs["corrimao"][4])
                        elif nome == "corrimao_vertical":
                            Tile((x,y), [self.solidos, self.visiveis], "corrimao_vertical", surfs["corrimao"][5])
        #criando jogador
        self.jogador = Jogador((70,330), [self.visiveis], self.solidos)

    def run(self):
        #método que desenha tudo o que for visivel
        self.visiveis.desenho(self.jogador)
        self.visiveis.update()

class Camera(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display = pygame.display.get_surface() 
        self.meiowidth = self.display.get_width()//2
        self.meioheight = self.display.get_height()//2
        self.offset = pygame.math.Vector2()

        self.floor = pygame.image.load("./imagens/ground.png").convert()
        self.floorrect = self.floor.get_rect(topleft=(0,0))

    def desenho(self, jogador):
        
        #setup offsets
        self.offset.x = jogador.rect.centerx - self.meiowidth
        self.offset.y = jogador.rect.centery - self.meioheight
        floor_offset = self.floorrect.topleft - self.offset

        #ajustando pos da imagem de fundo de acordo com o offset x
        if self.floorrect.topleft[0] - self.offset.x > 0:
            floor_offset = (0, floor_offset[1])
        elif self.floorrect.topright[0] - self.offset.x < self.display.get_width():
            floor_offset = (self.display.get_width()-self.floor.get_width(),floor_offset[1])

        #ajustando pos da imagem de fundo de acordo com o offset y
        if self.floorrect.topleft[1] - self.offset.y > 0:
            floor_offset = (floor_offset[0], 0)
        elif self.floorrect.bottomleft[1] - self.offset.y < self.display.get_height():
            floor_offset = (floor_offset[0], self.display.get_height()-self.floor.get_height())

        #blit da imagem de fundo
        self.display.blit(self.floor, floor_offset)
        
        #loop que desenha os sprites visiveis
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            
            #ajustando pos x dos sprites de acordo com a pos da imagem de fundo
            offset = []
            if (self.floorrect.topleft[0] - self.offset.x > 0):
                offset.append(sprite.rect.topleft[0])
            elif (self.floorrect.topright[0] - self.offset.x < self.display.get_width()):
                offset.append(sprite.rect.x - self.floor.get_width() + self.display.get_width()) 
            else:
                offset.append(sprite.rect.topleft[0] - self.offset.x)

            #ajustando pos y dos sprites de acordo com a pos da imagem de fundo
            if (self.floorrect.topleft[1] - self.offset.y > 0):
                offset.append(sprite.rect.topleft[1])
            elif (self.floorrect.bottomleft[1] - self.offset.y < self.display.get_height()):
                offset.append(sprite.rect.y - self.floor.get_height() + self.display.get_height()) 
            else:
                offset.append(sprite.rect.topleft[1] - self.offset.y)

            #blit dos sprites
            self.display.blit(sprite.image, (offset[0], offset[1]))
