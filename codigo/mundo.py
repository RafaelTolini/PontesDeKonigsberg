from typing import Iterable, Union
import pygame
from pygame.sprite import AbstractGroup
from configs import *
from tiles import Tile
from jogador import Jogador
from dialogo import Dialogo
from detector import Detector
from detector_solido import DetectoresSolidos
from funcs import read_csv, importa_imagens

class Mundo:
    def __init__(self):

        self.visiveis = Camera()
        self.solidos = pygame.sprite.Group()
        self.detectores_solidos = pygame.sprite.Group()
        self.interativos = pygame.sprite.Group()
        self.irmaos = pygame.sprite.Group()
        self.detectores = pygame.sprite.Group()
        self.dialogos = []
        self.portraits = []
        self.text = []
        self.irmao_text = []
        self.texto_fim = []
        self.irmao_portrait = None
        self.font = pygame.font.Font("../fontes/Pixellari.ttf", 25)
        # self.font = pygame.font.Font("../fontes/Minecraftia-Regular.ttf", 18)

        self.display = pygame.display.get_surface() 

        self.criar_mundo()

        self.dialoguebox = pygame.image.load("../imagens/dialogo/dialogo1.png").convert_alpha()
        self.opcoesbox = [pygame.image.load("../imagens/dialogo/dialogo2.png").convert_alpha(), pygame.image.load("../imagens/dialogo/dialogo3.png").convert_alpha()]
        self.fim_tela = pygame.image.load("../imagens/fim.png").convert_alpha()
        self.selected = 0
        self.option_lock = False
        self.option_cooldown = 300
        self.option_time = 1

        self.over = False
        self.euler_pt = pygame.image.load("../imagens/euler_retrato.png").convert_alpha()
        self.euler_state = 0
    
    def criar_mundo(self):
        
        #usando arquivos CSV para adicionar sprites ao grupo dos Tiles
        layout = {
            "barreira":read_csv("../CSVs/colisoes.csv"),
            "corrimao_down":read_csv("../CSVs/corrimao_down.csv"),
            "corrimao_up":read_csv("../CSVs/corrimao_up.csv"),
            "corrimao_vertical":read_csv("../CSVs/corrimao_vertical.csv"),
            "corrimao_cornerup_left":read_csv("../CSVs/corrimao_cornerup_left.csv"),
            "corrimao_cornerup_right":read_csv("../CSVs/corrimao_cornerup_right.csv"),
            "corrimao_cornerdown_left":read_csv("../CSVs/corrimao_cornerdown_left.csv"),
            "corrimao_cornerdown_right":read_csv("../CSVs/corrimao_cornerdown_right.csv"),
            "interativo":read_csv("../CSVs/interativos.csv"),
            "irmao":read_csv("../CSVs/irmaos.csv"),
            "detector_vertical":read_csv("../CSVs/detectores_vertical.csv"),
            "detector_horizontal":read_csv("../CSVs/detectores_horizontal.csv")
        }
        surfs = {
            "corrimao":importa_imagens("../imagens/corrimao"),
            "dialogo":importa_imagens("../imagens/dialogo"),
            "portraits":importa_imagens("../imagens/portraits"),
            "irmao":importa_imagens("../imagens/irmao")
        }
        
        i = j = z = 0
        for nome, layout in layout.items():
            for rowi, row in enumerate(layout):
                for coli, col in enumerate(row):
                    if col != "-1":
                        x = coli*tileS
                        y = rowi*tileS
                        if nome == "barreira":
                            Tile((x,y), [self.solidos], "barreira")
                        elif nome == "interativo":
                            Tile((x,y), [self.solidos, self.interativos], "interativo", index=i)
                            i+=1
                        # elif nome == "corrimao_down":
                        #     Tile((x,y), [self.solidos, self.visiveis], "corrimao_down", surfs["corrimao"][0])
                        # elif nome == "corrimao_up":
                        #     Tile((x,y), [self.solidos, self.visiveis], "corrimao_up", surfs["corrimao"][0])
                        # elif nome == "corrimao_cornerup_left":
                        #     Tile((x,y), [self.solidos, self.visiveis], "corrimao_up", surfs["corrimao"][1])
                        # elif nome == "corrimao_cornerup_right":
                        #     Tile((x,y), [self.solidos, self.visiveis], "corrimao_up", surfs["corrimao"][2])
                        # elif nome == "corrimao_cornerdown_left":
                        #     Tile((x,y), [self.solidos, self.visiveis], "corrimao_down", surfs["corrimao"][3])
                        # elif nome == "corrimao_cornerdown_right":
                        #     Tile((x,y), [self.solidos, self.visiveis], "corrimao_down", surfs["corrimao"][4])
                        # elif nome == "corrimao_vertical":
                        #     Tile((x,y), [self.solidos, self.visiveis], "corrimao_vertical", surfs["corrimao"][5])
                        elif nome == "irmao":
                            Tile((x,y), [self.solidos, self.irmaos], "irmao", index=j)
                            j+=1
                        elif nome == "detector_vertical":
                            Detector((x,y), [self.detectores], "detector_vertical", z)
                            z+=1
                        elif nome == "detector_horizontal":
                            Detector((x,y), [self.detectores], "detector_horizontal", z)
                            z+=1


        for d in surfs["portraits"]:
            self.portraits.append(d)

        self.irmao_portrait = surfs["irmao"][0]

        self.text.extend([
            ["Olá, bem-vindo à cidade de Königsberg! Você deve ser\nLeonhard Euler, certo? Sabíamos que você viria para a\ncidade para ouvir sobre o nosso Problema das Sete Pontes!",
             "Converse com os cidadãos para conhecer curiosidades\nsobre a cidade e, quando estiver pronto, fale com o homem\nde chapéu no fim da rua e ele te explicará o Problema (...)",
             "e dará acesso às pontes para que você possa tentar\nencontrar uma solução. Boa sorte!"], 
            ["Oi! Você sabia que cada uma das Sete Pontes tem um\nnome diferente? Elas são:",
             "Schmiedebrucke (Ponte do Ferreiro)",
             "Kottelbrucke (Ponte Conectora)",
             "Grune Brucke (Ponte Verde)",
             "Kramerbrucke (Ponte do Mercado)",
             "Holzbrucke (Ponte de Madeira)",
             "Hohe Brucke (Ponte Alta)",
             "Honigbrucke (Ponte do Mel)",
             "Decorar tudo isso foi bem difícil..."],
            ["Você não é a primeira pessoa importante a pisar na cidade!\nSabia que nasceram aqui o matemático Christian Goldbach e\no filósofo Immanuel Kant?"],
            ["Sei que estamos no século 18. Mas se por acaso, por volta\nde 1933, um regime fascista subir ao poder, você sabia que\nKönigsberg se tornará um importante centro (...)",
             "administrativo e quartel general de um distrito militar?\nIdeia maluca, eu sei. Como se isso fosse acontecer de\nverdade!"],
            ["Já se perguntou o motivo da cidade se chamar Königsberg?\nNão?... bem... vou te dizer mesmo assim. O nome da cidade \ntraduzido para português é algo próximo de (...)",
             "\"Montanha do Rei\". O nome foi dado em homenagem ao Rei\nOtacar II da Boêmia, o líder de uma das campanhas\nTeutônicas. Os membros dessa campanha foram (...)",
             "responsáveis por fundar o que hoje é Königsberg!"],
            ["Já conheceu aquela pessoa estranha que espalha teorias\nmalucas sobre o futuro? 1933, regime fascista?! Quanta\bobagem! Outro dia me falou sobre como, (...)",
             "hipoteticamente, caso a cidade fosse tomada pela Rússia\nno fim de uma suposta guerra, seu nome seria mudado\npara \"Kaliningrad\". Ridículo!"],
            ["Mesmo com a mudança da capital para Berlim no início\ndo século, pelo menos Königsberg continua sendo o local de\ncoroação da monarquia da Prússia!"],
            ["Você sabia que Palmnicken, situada na região de\nKönigsberg, é o maior centro de produção de âmbar do\nmundo?"],
            ["Teste"] 
                          ])
        
        self.irmao_text.extend([
            ["Olá, Leonhard Euler, estávamos esperando por você.\nImagino que deseja saber sobre o Problema das Sete\nPontes, portanto irei explicá-lo para você.", 
             "Pois bem, há um debate entre os cidadãos para saber\nse é possível passar por cada uma das Sete Pontes\nque conectam os quatro distritos da cidade (...)",
             "exatamente uma vez, terminando o trajeto no distrito\nescolhido como ponto de partida. Precisávamos de um\nmatemático como você para definir (...)",
             "de uma vez por todas se tal trajeto é possível ou não.\nAs pontes agora podem ser atravessadas. Caso\nvocê queira reiniciar o caminho a partir (...)",
             "de outro ponto, fale com um dos meus irmãos presentes\nnos outros distritos e eles liberarão as pontes\nnovamente. Fale conosco também caso (...)",
             "você tenha chegado em uma conclusão e queira terminar\nsua busca. Desejo boa sorte!"],
            ["Oi! Gostaria de recomeçar o caminho a partir desse\ndistrito ou já chegou em uma conclusão?"]
        ])

        self.texto_fim.extend([
            ["Isso é um teste"],
            ["Também é um teste"]
        ])

        #criando jogador
        self.jogador = Jogador((70,330), [self.visiveis], self.solidos, self.interativos, self.text, self.irmaos, self.irmao_text, self.detectores)

        for dec in self.detectores:
            DetectoresSolidos((dec.pos[0], dec.pos[1]+tileS), [self.jogador.detectores_solidos], "horizontal") #<---------------------------------------------------------------------!!!!!!!!!!!!
    
    def dialogue(self):
        
        #dialogo dos cidadaos
        if self.jogador.dialogue_state > -1:

            self.display.blit(self.dialoguebox, (self.display.get_width()//2 - self.dialoguebox.get_width()//2, tileS//2))

            self.display.blit(self.portraits[self.jogador.interagindo], (self.display.get_width()//2 - self.dialoguebox.get_width()//2 + 15, tileS//2 + 15))

            tt = self.jogador.texto_atual.split("\n")

            ytexto = tileS//2 + 45

            for linha in tt:
                t = self.font.render(linha, True, (0,0,0))
                self.display.blit(t, (self.display.get_width()//2 - self.dialoguebox.get_width()//2 + 260, ytexto))
                ytexto += 40


        #dialogo dos irmaos que controlam o estado do jogo
        elif self.jogador.irmao_state > -1:

            self.display.blit(self.dialoguebox, (self.display.get_width()//2 - self.dialoguebox.get_width()//2, tileS//2))

            self.display.blit(self.irmao_portrait, (self.display.get_width()//2 - self.dialoguebox.get_width()//2 + 15, tileS//2 + 15))

            tt = self.jogador.texto_atual.split("\n")

            ytexto = tileS//2 + 45

            for linha in tt:
                t = self.font.render(linha, True, (0,0,0))
                self.display.blit(t, (self.display.get_width()//2 - self.dialoguebox.get_width()//2 + 260, ytexto))
                ytexto += 40

            if self.jogador.irmao_tutorial == 1:
    
                if self.selected == 0:
                    self.display.blit(self.opcoesbox[0], (self.display.get_width()//2 - self.dialoguebox.get_width()//2, tileS*8))
                else:
                    self.display.blit(self.opcoesbox[1], (self.display.get_width()//2 - self.dialoguebox.get_width()//2, tileS*8))

                t = self.font.render("Quero reiniciar o caminho a partir desse distrito.", True, (0,0,0))
                self.display.blit(t, (self.display.get_width()//2 - self.dialoguebox.get_width()//2 + 180, tileS*8 + 43))
                t = self.font.render("Já tenho uma conclusão.", True, (0,0,0))
                self.display.blit(t, (self.display.get_width()//2 - self.dialoguebox.get_width()//2 + 330, tileS*9 + 65))

            else:

                self.jogador.detectores_solidos.empty()

        if self.over:
            
            self.display.blit(self.fim_tela, (0,0))
            
            self.display.blit(self.dialoguebox, (self.display.get_width()//2 - self.dialoguebox.get_width()//2, tileS//2))

            self.display.blit(self.euler_pt, (self.display.get_width()//2 - self.dialoguebox.get_width()//2 + 15, tileS//2 + 15))

            tt = self.texto_fim[self.euler_state][0].split("\n")

            ytexto = tileS//2 + 45

            for linha in tt:
                t = self.font.render(linha, True, (0,0,0))
                self.display.blit(t, (self.display.get_width()//2 - self.dialoguebox.get_width()//2 + 260, ytexto))
                ytexto += 40


        self.option_update()

    def option_update(self):

        keys = pygame.key.get_pressed()

        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and not self.option_lock and self.jogador.irmao_state > -1:
            if self.selected == 0:
                self.selected = 1
            else:
                self.selected = 0
            self.option_lock = True
            self.option_time = pygame.time.get_ticks()

        if (keys[pygame.K_UP] or keys[pygame.K_w]) and not self.option_lock and self.jogador.irmao_state > -1:
            if self.selected == 1:
                self.selected = 0
            else:
                self.selected = 1
            self.option_lock = True
            self.option_time = pygame.time.get_ticks()

        if (keys[pygame.K_SPACE]) and not self.option_lock and (self.jogador.irmao_state == -2 or self.over):
            if self.over:
                self.euler_state +=1
            if self.selected == 0:
                self.reinicia_pontes()
            else: 
                self.over = True
                self.display.fill(0)
                pygame.time.wait(2000)
            self.jogador.irmao_state = -1
            self.selected = 0
            self.option_lock = True
            self.option_time = pygame.time.get_ticks()

    def reinicia_pontes(self):

        for dec in self.jogador.detectores:
            dec.lock = False
            dec.ativo =  False

        self.jogador.detectores_solidos.empty()

        self.jogador.ultimo_ativo = -1

    def cooldown(self):

        time = pygame.time.get_ticks()
        if time > self.option_time + self.option_cooldown:
            self.option_lock = False


    def run(self):
        #método que desenha tudo o que for visivel
        if not self.over:
            self.visiveis.desenho(self.jogador)
            self.visiveis.update()
            self.cooldown()
        # self.jogador.detectores_solidos.draw(self.display)

class Camera(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display = pygame.display.get_surface() 
        self.meiowidth = self.display.get_width()//2
        self.meioheight = self.display.get_height()//2
        self.offset = pygame.math.Vector2()

        self.floor = pygame.image.load("../imagens/ground.png").convert()
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
        
        # loop que desenha os sprites visiveis
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
