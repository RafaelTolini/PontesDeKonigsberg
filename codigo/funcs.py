from csv import reader
from os import walk
import pygame

def read_csv(path):
    lista = []
    with open(path) as file:
        mapa = reader(file, delimiter = ",")
        for row in mapa:
            lista.append(list(row))

        return lista
    
def importa_imagens(path):
    lista = []
    for _,__,arquivo in walk(path):
        for imagem in arquivo:
            f_path = path+"/"+imagem
            imagemS = pygame.image.load(f_path).convert_alpha()
            lista.append(imagemS)

    return lista
