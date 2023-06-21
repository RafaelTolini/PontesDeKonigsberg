import pygame, sys
from configs import *
from mundo import Mundo
from random import randint as r
from random import choice as rc


class Jogo:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.mundo = Mundo()
        self.halfwidth = width//2
        self.halfheight = height//2
        self.floor = pygame.image.load("../imagens/ground.png").convert()
        self.icon = pygame.image.load("../imagens/icon.png")
        self.floorrect = self.floor.get_rect(topleft=(0,0))

        self.offset = pygame.math.Vector2()

        pygame.display.set_caption("Pontes de Königsberg")
        pygame.display.set_icon(self.icon)
        # pygame.mixer.music.load("./musica/musica.wav")
        # pygame.mixer.music.set_volume(0.5)
        # pygame.mixer.music.play()

        #snow setup
        self.snow = []
        for _ in range(2000):
            xsnow = r(0, self.floor.get_width())
            ysnow = r(0, self.floor.get_height())
            snowsize = 4
            self.snow.append([xsnow, ysnow, snowsize, rc([0.6, 0.8, 1])])

    def run(self):
        while True:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill(0)

            if not self.mundo.over:
                self.mundo.run()
            else:
                self.mundo.dialogue()
                self.mundo.cooldown()

            #snow
            if self.mundo.jogador.rect.centerx - self.halfwidth < 0:
                self.offset.x = 0
            elif self.mundo.jogador.rect.centerx + self.halfwidth > self.floorrect.topright[0]:
                self.offset.x = self.floor.get_width() - width
            else:
                self.offset.x = self.mundo.jogador.rect.centerx - self.halfwidth

            if self.mundo.jogador.rect.centery - self.halfheight < 0:
                self.offset.y = 0
            elif self.mundo.jogador.rect.centery + self.halfheight > self.floorrect.bottomleft[1]:
                self.offset.y = self.floor.get_height() - height
            else:
                self.offset.y = self.mundo.jogador.rect.centery - self.halfheight

            for flakeindex, flake in enumerate(self.snow):
                pygame.draw.rect(self.screen, (255,255,255), (flake[0]-self.offset.x, flake[1]-self.offset.y, flake[2],flake[2]))
                self.snow[flakeindex][1] += self.snow[flakeindex][3]
                if self.snow[flakeindex][1] > self.floor.get_height():
                    self.snow[flakeindex][0] = r(0, self.floor.get_width())
                    self.snow[flakeindex][1] = r(-50,-10)

            if not self.mundo.over:
                self.mundo.dialogue()

            pygame.display.update()
            self.clock.tick(fps)

if __name__ == "__main__":
    jogo = Jogo()
    jogo.run()

