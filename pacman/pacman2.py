import pygame

pygame.init()


LARGURA_TELA = 800
ALTURA_TELA = 600
TELA = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA), 0)

AMARELO = (255, 255, 0)
PRETO = (0, 0, 0)

class PacMan:
    def __init__(self):
        self.coluna = 1
        self.linha = 1
        self.centro_x = 400
        self.centro_y = 300
        self.vel_x = 0
        self.vel_y = 0
        self.tamanho = LARGURA_TELA // 30 #largura / int(numero de colunas do jogo)
        self.raio = self.tamanho//2 # "//" arredonda para inteiro

    def calcula_regras(self):
        self.coluna += self.vel_x
        self.linha += self.vel_y
        self.centro_x  = int(self.coluna * self.tamanho + self.raio)
        self.centro_y = int(self.linha * self.tamanho + self.raio)

    def pintar(self, tela):
        #Desenha o corpo do pacman
        pygame.draw.circle(tela, AMARELO, (self.centro_x, self.centro_y), self.raio, 0)

        #Desenha a boca
        canto_da_boca = (self.centro_x, self.centro_y)
        labio_superior = (self.centro_x + self.raio, self.centro_y - self.raio)
        labio_inferior = (self.centro_x + self.raio, self.centro_y)
        pontos = [canto_da_boca, labio_superior, labio_inferior]
        pygame.draw.polygon(tela, PRETO, pontos, 0)

        #Desenha o olho
        olho_x = int(self.centro_x + self.raio / 3)
        olho_y = int(self.centro_y - self.raio * 0.7)
        olho_raio = int(self.raio / 10)
        pygame.draw.circle(tela, PRETO, (olho_x, olho_y), olho_raio, 0)

    def processar_eventos(self, eventos):
        for e in eventos:

            #Anda para direita
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RIGHT:
                    self.vel_x = 1
            if e.type == pygame.KEYUP:
                if e.key == pygame.K_RIGHT:
                    self.vel_x = 0

            #Anda para esquerda
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_LEFT:
                    self.vel_x = -1
            if e.type == pygame.KEYUP:
                if e.key == pygame.K_LEFT:
                    self.vel_x = 0


            # Anda para baixo
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_DOWN:
                    self.vel_y = 1
            if e.type == pygame.KEYUP:
                if e.key == pygame.K_DOWN:
                    self.vel_y = 0

            # Anda para cima
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP:
                    self.vel_y = -1
            if e.type == pygame.KEYUP:
                if e.key == pygame.K_UP:
                    self.vel_y = 0



if __name__ == "__main__":
    pacman = PacMan()

    while True:
        #Calcula regras
        pacman.calcula_regras()

        #Pintar a tela
        TELA.fill(PRETO)
        pacman.pintar(TELA)
        pygame.display.update()
        pygame.time.delay(100)

        #Captura eventos
        eventos = pygame.event.get()
        for e in eventos:
            if e.type == pygame.QUIT:
                exit()
        pacman.processar_eventos(eventos)