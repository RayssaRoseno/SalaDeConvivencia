# Importações necessárias
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Inicialize o Pygame
pygame.init()
clock = pygame.time.Clock()

# Configurações de exibição
display = (1230, 800)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

# Posição inicial da câmera
camera_x, camera_y, camera_z = 0, 0, -5
camera_rot_x, camera_rot_y = 360, 0  # Orientação vertical ajustada para 360 graus (de cabeça para cima)

# Variável para rastrear o estado da abertura da porta
abertura_porta = 0  # 0 para fechada, 90 para totalmente aberta (ângulo em graus)

# Função para renderizar a casa
def render_house():
    # Parede frontal
    glBegin(GL_QUADS)
    glColor3fv((0.5, 0.5, 0.5))  # Cor da parede
    glVertex3fv((-1, -1, -1))
    glVertex3fv((1, -1, -1))
    glVertex3fv((1, 1, -1))
    glVertex3fv((-1, 1, -1))
    glEnd()

    # Parede traseira
    glBegin(GL_QUADS)
    glColor3fv((0.5, 0.5, 0.5))  # Cor da parede
    glVertex3fv((-1, -1, 1))
    glVertex3fv((1, -1, 1))
    glVertex3fv((1, 1, 1))
    glVertex3fv((-1, 1, 1))
    glEnd()

    # Parede esquerda
    glBegin(GL_QUADS)
    glColor3fv((0.5, 0.5, 0.5))  # Cor da parede
    glVertex3fv((-1, -1, -1))
    glVertex3fv((-1, 1, -1))
    glVertex3fv((-1, 1, 1))
    glVertex3fv((-1, -1, 1))
    glEnd()

    # Parede direita
    glBegin(GL_QUADS)
    glColor3fv((0.5, 0.5, 0.5))  # Cor da parede
    glVertex3fv((1, -1, -1))
    glVertex3fv((1, 1, -1))
    glVertex3fv((1, 1, 1))
    glVertex3fv((1, -1, 1))
    glEnd()

    # Porta
    global abertura_porta  # Declare a variável global
    glPushMatrix()
    glTranslatef(0, 0, -1)  # Posicione a porta na parede
    glTranslatef(0.3, 0, 0)  # Ajuste a posição para a borda direita da porta
    glRotatef(abertura_porta, 0, 1, 0)  # Aplique a rotação da porta em torno da borda
    glColor3fv((1.0, 1.0, 1.0))  # Cor da porta (amarela)
    glBegin(GL_QUADS)
    glVertex3fv((-0.3, -1, 0))
    glVertex3fv((0.3, -1, 0))
    glVertex3fv((0.3, 0, 0))
    glVertex3fv((-0.3, 0, 0))
    glEnd()
    glPopMatrix()

# Loop principal
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEMOTION:
            dx, dy = event.rel
            camera_rot_x += dy
            camera_rot_y += dx

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        camera_z += 0.05
    if keys[pygame.K_s]:
        camera_z -= 0.05
    if keys[pygame.K_a]:
        camera_x += 0.05
    if keys[pygame.K_d]:
        camera_x -= 0.05

    # Verifique se a tecla 'f' é pressionada para abrir a porta gradualmente
    if keys[pygame.K_f] and abertura_porta < 90:
        abertura_porta += 1  # Aumenta o ângulo gradualmente

    # Verifique se a tecla 'g' é pressionada para fechar a porta gradualmente
    if keys[pygame.K_g] and abertura_porta > 0:
        abertura_porta -= 1  # Diminui o ângulo gradualmente

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glPushMatrix()

    glRotatef(camera_rot_x, 1, 0, 0)
    glRotatef(camera_rot_y, 0, 1, 0)

    gluLookAt(camera_x, camera_y, camera_z, camera_x, camera_y, camera_z - 1, 0, 1, 0)

    render_house()

    glPopMatrix()

    pygame.display.flip()
    clock.tick(60)
