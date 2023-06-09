import pygame
import random
from abc import ABCMeta, abstractmethod

pygame.init()
font = pygame.font.SysFont("arial", 24, True, False)

LARGURA_TELA = 800
ALTURA_TELA = 600
TELA = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA), 0)

AMARELO = (255, 255, 0)
PRETO = (0, 0, 0)
AZUL = (0, 0, 255)
ROSA = (255, 0, 255)
VERMELHO = (255, 0, 0)
BRANCO = (255, 255, 255)
LARANJA = (255, 140, 0)
CIANO = (0, 255, 255)

VELOCIDADE = 1

JOGANDO = 0
PAUSADO = 1
GAME_OVER = 2
VITORIA = 3
START = 4

CIMA = 1
BAIXO = 2
DIREITA = 3
ESQUERDA  = 4

class ElementoJogo(metaclass=ABCMeta):
    @abstractmethod
    def pintar(self, tela):
        pass

    @abstractmethod
    def calcula_regras(self):
        pass

    @abstractmethod
    def processar_eventos(self, eventos):
        pass

class Movivel(metaclass= ABCMeta):
    @abstractmethod
    def aceitar_movimento(self):
        pass
    @abstractmethod
    def recusar_movimento(self, direcoes):
        pass
    @abstractmethod
    def esquina(self, direcoes):
        pass
class Cenario(ElementoJogo):
    def __init__(self, tamanho, pac):
        self.pacman = pac
        self.moviveis = []
        self.tamanho = tamanho
        # Estados possíveis => 0 Jogando, 1 Pausado, 2 GameOver, 3 Vitória, 4 Start
        self.estado = JOGANDO
        self.pontos = 0
        self.vidas = 5
        self.matriz = [
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 0, 0, 0, 0, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 0, 0, 0, 0, 0, 0, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 2, 0, 0, 0, 0, 0, 0, 2, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 0, 0, 0, 0, 0, 0, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]

        ]
    def adicionar_movivel(self, obj):
        self.moviveis.append(obj)
    def pintar_score(self, tela):
        pontos_x = 30 * self.tamanho
        img_pontos = font.render("Score: {}".format(self.pontos), True, AMARELO)
        img_vidas = font.render("Vidas: {}".format(self.vidas), True, AMARELO)
        tela.blit(img_pontos, (pontos_x, 50))
        tela.blit(img_vidas, (pontos_x, 80))
    def pintar_linha(self, tela, numero_linha, linha):
        for numero_coluna, coluna in enumerate(linha):
            x= numero_coluna * self.tamanho
            y = numero_linha * self.tamanho
            cor = PRETO
            half = self.tamanho // 2

            #Pinta paredes
            if coluna == 2:
                cor= AZUL
            pygame.draw.rect(tela, cor, (x, y, self.tamanho, self.tamanho), 0)

            #Pinta Pastilhas
            if coluna == 1:
                pygame.draw.circle(tela, AMARELO, (x + half,y + half),
                                   self.tamanho//10, 0)


    def pintar(self, tela):
        if self.estado == JOGANDO:
            self.pintar_jogando(tela)
        elif self.estado == PAUSADO:
            self.pintar_jogando(tela)
            self.pintar_pausado(tela)
        elif self.estado == GAME_OVER:
            self.pintar_jogando(tela)
            self.pintar_gameover(tela)
        elif self.estado == VITORIA:
            self.pintar_jogando(tela)
            self.pintar_vitoria(tela)
        # elif self.estado == START:
        #     self.pintar_jogando(tela)
        #     self.pintar_start(tela)

    def pintar_texto_centro(self, tela, texto):
        img_texto = font.render(texto, True, AMARELO)
        texto_x = (tela.get_width() - img_texto.get_width()) // 2
        texto_y = (tela.get_height() - img_texto.get_height()) // 2
        tela.blit(img_texto, (texto_x, texto_y))

    def pintar_vitoria(self, tela):
        self.pintar_texto_centro(tela, "Y O U   W I N")
    def pintar_gameover(self, tela):
        self.pintar_texto_centro(tela, "G A M E   O V E R")
    def pintar_pausado(self, tela):
        self.pintar_texto_centro(tela,"P A U S A D O")
    def pintar_start(self, tela):
        self.pintar_texto_centro(tela, "S T A R T")

    def pintar_jogando(self, tela):
        for numero_linha, linha in enumerate(self.matriz):
            self.pintar_linha(tela, numero_linha, linha)
        self.pintar_score(tela)

    def get_direcoes(self, linha, coluna):
        direcoes = []
        if self.matriz[int(linha - 1)][int(coluna)] != 2:
            direcoes.append(CIMA)
        if self.matriz[int(linha + 1)][int(coluna)] != 2:
            direcoes.append(BAIXO)
        if self.matriz[int(linha)][int(coluna - 1)] != 2:
            direcoes.append(ESQUERDA)
        if self.matriz[int(linha)][int(coluna + 1)] != 2:
            direcoes.append(DIREITA)
        return direcoes

    def calcula_regras(self):
        if self.estado == JOGANDO:
            self.calcula_regras_jogando()
        elif self.estado == PAUSADO:
            self.calcula_regras_pausado()
        elif self.estado == GAME_OVER:
            self.calcula_regras_gameover()

    def calcula_regras_gameover(self):
        pass
    def calcula_regras_pausado(self):
        pass
    def calcula_regras_jogando(self):
        for movivel in self.moviveis:
            lin = int(movivel.linha)
            col = int(movivel.coluna)
            lin_intencao = int(movivel.linha_intencao)
            col_intencao = int(movivel.coluna_intencao)

            direcoes = self.get_direcoes(lin, col)

            if len(direcoes) >= 3:
                movivel.esquina(direcoes)
            if isinstance(movivel, Fantasma) and movivel.linha == self.pacman.linha and \
                    movivel.coluna == self.pacman.coluna:

                    self.pacman.linha = 1
                    self.pacman.coluna = 1

                    if self.vidas > 0:
                        if self.vidas == 5:
                            self.vidas = 4
                            break
                        elif self.vidas == 4:
                            self.vidas = 3
                            break
                        elif self.vidas == 3:
                            self.vidas = 2
                            break
                        if self.vidas == 2:
                            self.vidas = 1
                            break
                        if self.vidas == 1:
                            self.vidas = 0
                    elif self.vidas <= 0:
                        self.estado = GAME_OVER

            else:
                if 0 <= lin_intencao < 28 and 0 <= col_intencao < 29 and self.matriz[lin_intencao][col_intencao] != 2:
                    movivel.aceitar_movimento()
                    if isinstance(movivel, PacMan) and self.matriz[lin][col] == 1:
                        self.pontos += 1
                        self.matriz[lin][col] = 0
                        if self.pontos >= 306:
                            self.estado = VITORIA

                else:
                    movivel.recusar_movimento(direcoes)

    def processar_eventos(self, evts):
        for e in evts:
            if e.type == pygame.QUIT:
                exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    if self.estado == JOGANDO:
                        self.estado = PAUSADO
                    else:
                        self.estado = JOGANDO

class Fantasma(ElementoJogo, Movivel):
    def __init__(self, cor, tamanho):
        self.cor = cor
        self.tamanho = tamanho
        self.velocidade = 1
        self.direcao = BAIXO
        self.coluna = 13.0
        self.linha = 15.0
        self.linha_intencao = self.linha
        self.coluna_intencao = self.coluna

    def pintar(self, tela):
        fatia = self.tamanho // 8
        px = int(self.coluna * self.tamanho)
        py = int(self.linha * self.tamanho)

        #Marcação do perimetro do corpo do fantasma
        contorno = [(px, py + self.tamanho), # ponto 1
                    (px + fatia, py + fatia*3), #ponto 2
                    (px + fatia * 2, py + fatia //2), #ponto 3
                    (px + fatia * 3, py), # ponto 4
                    # Acima é referente ao lado esquerdo do fantasma
                    # Abaixo começa o lado direito do fantasma
                    (px + fatia * 5, py), # ponto 5
                    (px + fatia * 6, py + fatia // 2), #ponto 6
                    (px + fatia * 7, py + fatia * 3), #ponto 7
                    (px + self.tamanho, py + self.tamanho)] #ponto 8

        #DESENHA O CORPO DO FANTASMA
        pygame.draw.polygon(tela, self.cor, contorno, 0)

        olho_raio_interno = fatia //2
        olho_raio_externo = fatia

        olho_e_x = int(px + fatia * 2.5)
        olho_e_y = int(py + fatia * 2.5)

        olho_d_x = int(px + fatia * 5.5)
        olho_d_y = int(py + fatia * 2.5)

        #DESENHA A PARTE BRANCA DOS OLHOS
        pygame.draw.circle(tela, BRANCO, (olho_e_x, olho_e_y), olho_raio_externo, 0)
        pygame.draw.circle(tela, BRANCO, (olho_d_x, olho_d_y), olho_raio_externo, 0)

        #DESENHA A PUPILA DOS OLHOS
        pygame.draw.circle(tela, PRETO, (olho_e_x, olho_e_y), olho_raio_interno, 0)
        pygame.draw.circle(tela, PRETO, (olho_d_x, olho_d_y), olho_raio_interno, 0)

    def calcula_regras(self):
        if self.direcao == CIMA:
            self.linha_intencao -= self.velocidade
        if self.direcao == BAIXO:
            self.linha_intencao += self.velocidade
        if self.direcao == ESQUERDA:
            self.coluna_intencao -= self.velocidade
        if self.direcao == DIREITA:
            self.coluna_intencao += self.velocidade
    def processar_eventos(self, evts):
        pass
    def mudar_direcao(self, direcoes):
        self.direcao = random.choice(direcoes)
    def esquina(self, direcoes):
        self.mudar_direcao(direcoes)
    def recusar_movimento(self, direcoes):
        self.linha_intencao = self.linha
        self.coluna_intencao = self.coluna
        self.mudar_direcao(direcoes)
    def aceitar_movimento(self):
        self.linha = self.linha_intencao
        self.coluna = self.coluna_intencao



class PacMan (ElementoJogo, Movivel):
    def __init__(self, tamanho):
        self.coluna = 1
        self.linha = 1
        self.centro_x = 400
        self.centro_y = 300
        self.vel_x = 0
        self.vel_y = 0
        self.tamanho = tamanho
        self.raio = self.tamanho//2 # "//" arredonda para inteiro
        self.coluna_intencao = self.coluna
        self.linha_intencao = self.linha
        self.abertura_boca = 0
        self.velocidade_abertura = 1

    def calcula_regras(self):
        self.coluna_intencao = self.coluna + self.vel_x
        self.linha_intencao = self.linha + self.vel_y
        self.centro_x  = int(self.coluna * self.tamanho + self.raio)
        self.centro_y = int(self.linha * self.tamanho + self.raio)


    def pintar(self, tela):
        #Desenha o corpo do pacman
        pygame.draw.circle(tela, AMARELO, (self.centro_x, self.centro_y), self.raio, 0)

        self.abertura_boca += self.velocidade_abertura
        if self.abertura_boca > self.raio - 3.5:
            self.velocidade_abertura = -2
        elif self.abertura_boca <= 0:
            self.velocidade_abertura = 2

        #Desenha a boca
        canto_da_boca = (self.centro_x, self.centro_y)
        labio_superior = (self.centro_x + self.raio, self.centro_y - self.abertura_boca)
        labio_inferior = (self.centro_x + self.raio, self.centro_y + self.abertura_boca)
        pontos = [canto_da_boca, labio_superior, labio_inferior]
        pygame.draw.polygon(tela, PRETO, pontos, 0)

        #Desenha o olho
        olho_x = int(self.centro_x + self.raio / 3)
        olho_y = int(self.centro_y - self.raio * 0.7)
        olho_raio = int(self.raio / 5)
        pygame.draw.circle(tela, PRETO, (olho_x, olho_y), olho_raio, 0)

    def processar_eventos(self, eventos):
        for e in eventos:

            #Quando aperta a tecla
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RIGHT:
                    self.vel_x = VELOCIDADE
                if e.key == pygame.K_LEFT:
                    self.vel_x = - VELOCIDADE
                if e.key == pygame.K_DOWN:
                    self.vel_y = VELOCIDADE
                if e.key == pygame.K_UP:
                    self.vel_y = -VELOCIDADE

            #Quando solta a tecla
            if e.type == pygame.KEYUP:
                if e.key == pygame.K_RIGHT:
                    self.vel_x = 0
                if e.key == pygame.K_LEFT:
                    self.vel_x = 0
                if e.key == pygame.K_DOWN:
                    self.vel_y = 0
                if e.key == pygame.K_UP:
                    self.vel_y = 0

    def aceitar_movimento(self):
        self.linha = self.linha_intencao
        self.coluna = self.coluna_intencao

    def recusar_movimento(self, direcoes):
        self.linha_intencao = self.linha
        self.coluna_intencao = self.coluna

    def esquina(self, direcoes):
        pass

if __name__ == "__main__":
    size = 600 // 30
    pacman = PacMan(size)
    blinky = Fantasma(VERMELHO, size)
    inky = Fantasma(CIANO, size)
    clyde = Fantasma(LARANJA, size)
    pinky = Fantasma(ROSA, size)
    cenario = Cenario(size, pacman)



    while True:
        #Calcula regras
        pacman.calcula_regras()
        cenario.calcula_regras()
        blinky.calcula_regras()
        inky.calcula_regras()
        clyde.calcula_regras()
        pinky.calcula_regras()

        cenario.adicionar_movivel(pacman)
        cenario.adicionar_movivel(blinky)
        cenario.adicionar_movivel(inky)
        cenario.adicionar_movivel(clyde)
        cenario.adicionar_movivel(pinky)



        #Pintar a tela
        TELA.fill(PRETO)
        cenario.pintar(TELA)
        pacman.pintar(TELA)
        blinky.pintar(TELA)
        inky.pintar(TELA)
        clyde.pintar(TELA)
        pinky.pintar(TELA)


        pygame.display.update()
        pygame.time.delay(100)

        #Captura eventos
        eventos = pygame.event.get()
        pacman.processar_eventos(eventos)
        cenario.processar_eventos(eventos)

