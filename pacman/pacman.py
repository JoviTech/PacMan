import pygame

pygame.init()

#CORES
AMARELO = (255,255,0)
PRETO = (0, 0, 0)


#SCREEN
LARGURA = 640
ALTURA = 480

VELOCIDADE = 0.5

x = 10
y= 240
vel_x = VELOCIDADE
vel_y = VELOCIDADE
raio = 30

tela = pygame.display.set_mode((LARGURA, ALTURA), 0)
while True:
    #calcula as regras
    x += vel_x
    y += vel_y

    if x + raio > LARGURA:
        vel_x = -VELOCIDADE
    elif x - raio < 0:
        vel_x = VELOCIDADE
    elif y + raio > ALTURA:
        vel_y = - VELOCIDADE
    elif y - raio < 0:
        vel_y = VELOCIDADE
    #pinta
    tela.fill(PRETO)
    pygame.draw.circle(tela, AMARELO,(int(x),y), raio, 0)
    pygame.display.update()

    #eventos
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            exit()