import pygame

pygame.init()


AMARELO = (255,255,0)
PRETO = (0, 0, 0)

VELOCIDADE = 1
LARGURA = 640
ALTURA = 480

tela = pygame.display.set_mode((LARGURA, ALTURA), 0)
x = 10
y= 240
vel_x = VELOCIDADE
vel_y = VELOCIDADE
raio = 30
while True:
    #calcula as regras
    x += vel_x
    y += vel_y

    if x > LARGURA:
        vel_x = -VELOCIDADE
    elif x < 0:
        vel_x = VELOCIDADE
    elif y + raio > ALTURA:
        vel_y = - VELOCIDADE
    elif y + raio > 0:
        vel_y = VELOCIDADE
    #pinta
    tela.fill(PRETO)
    pygame.draw.circle(tela, AMARELO,(int(x),y), raio, 0)
    pygame.display.update()

    #eventos
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            exit()