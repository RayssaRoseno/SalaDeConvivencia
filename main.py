# Importações necessárias
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math


# Inicialize o Pygame
pygame.init()
clock = pygame.time.Clock()


# Configurações de exibição
display = (1230, 800)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
pygame.display.set_caption("Sala de Convivência")
gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

# Posição inicial da câmera
camera_x, camera_y, camera_z = 0, 0, 5
camera_rot_x, camera_rot_y =  -0, 0  # Orientação vertical ajustada para 360 graus (de cabeça para cima)

# Variável para rastrear o estado da abertura da porta
abertura_porta = 0  # 0 para fechada, 90 para totalmente aberta (ângulo em graus)

# Carregue a textura do piso
floor_texture = pygame.image.load("C:\\Users\\rayss\\Desktop\\CG\\textura\\piso.jpg")
floor_texture_data = pygame.image.tostring(floor_texture, 'RGB', True)
width, height = floor_texture.get_size()

# Textura Chão
glEnable(GL_TEXTURE_2D)
glBindTexture(GL_TEXTURE_2D, 1)
glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
glTexImage2D(GL_TEXTURE_2D, 0, 3, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, floor_texture_data)

# Função para renderizar a sala

def draw_room():
    # Parede frontal com o recorte da porta e a parte de cima
    glBegin(GL_QUADS)
    glColor3fv((0.5, 0.5, 0.5))  # Cor vermelha da parede

    # Parte esquerda da parede
    glVertex3fv((-1, -1, -1))
    glVertex3fv((-0.3, -1, -1))
    glVertex3fv((-0.3, 0, -1))
    glVertex3fv((-1, 0, -1))

    # Parte direita da parede (depois do recorte da porta)
    glVertex3fv((0.3, -1, -1))
    glVertex3fv((1, -1, -1))
    glVertex3fv((1, 0, -1))
    glVertex3fv((0.3, 0, -1))

    # Parte de cima da parede (entrada)
    glVertex3fv((-1, 1, -1))
    glVertex3fv((1, 1, -1))
    glVertex3fv((1, 0, -1))
    glVertex3fv((-1, 0, -1))

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

     # teto
    glBegin(GL_QUADS)
    glColor3fv((0.3, 0.3, 0.3))
    glVertex3fv((-1, 1, -1))
    glVertex3fv((1, 1, -1))
    glVertex3fv((1, 1, 1))
    glVertex3fv((-1, 1, 1))
    glEnd()

    # Porta
    global abertura_porta  # Declare a variável global
    glPushMatrix()
    glTranslatef(0, 0, -1)  # Posicione a porta na parede
    glTranslatef(0.3, 0, 0)  # Mantenha a porta grudada na posição inicial na borda direita
    glRotatef(abertura_porta, 0, 1, 0)  # Aplique a rotação da porta em torno do eixo y
    glTranslatef(-0.3, 0, 0)  # Recoloque a porta na posição correta na borda direita
    glColor3fv((0.3, 0.25, 0.0))  # Cor da porta (branca)
    glBegin(GL_QUADS)
    glVertex3fv((-0.3, -1, 0))
    glVertex3fv((0.3, -1, 0))
    glVertex3fv((0.3, 0, 0))
    glVertex3fv((-0.3, 0, 0))
    glEnd()
    glPopMatrix()

def draw_blackboard():
    glBegin(GL_QUADS)
    glColor3fv((1.0, 1.0, 1.0))  # Cor da lousa (branco)
    glVertex3fv((-1.01, -0.7, -0.7))
    glVertex3fv((-1.01, 0.7, -0.7))
    glVertex3fv((-1.01, 0.7, 0.7))
    glVertex3fv((-1.01, -0.7, 0.7))
    glEnd()

    glColor3fv((0.0, 0.0, 0.0))  # Cor da borda (preto)
    glLineWidth(2.0)  # Espessura da linha
    glBegin(GL_LINE_LOOP)
    glVertex3fv((-1.01, -0.7, -0.7))
    glVertex3fv((-1.01, 0.7, -0.7))
    glVertex3fv((-1.01, 0.7, 0.7))
    glVertex3fv((-1.01, -0.7, 0.7))
    glEnd()



def draw_floor():
    glBindTexture(GL_TEXTURE_2D, 1)  # Use a textura carregada
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3fv((-1, -1, -1))
    glTexCoord2f(1.0, 0.0)
    glVertex3fv((1, -1, -1))
    glTexCoord2f(1.0, 1.0)
    glVertex3fv((1, -1, 1))
    glTexCoord2f(0.0, 1.0)
    glVertex3fv((-1, -1, 1))
    glEnd()


def draw_table():
    # Posição da mesa
    table_x = 0.5  # Ajuste a posição X conforme necessário
    table_width = 1.1  # Ajuste a largura da mesa conforme necessário

    # Tampo da mesa
    glBegin(GL_QUADS)
    glColor3f(0.3, 0.20, 0.0)  # Cor da mesa
    glVertex3f(table_x - table_width / 2, -0.98, -0.3)  # Largura, Altura e Comprimento da mesa
    glVertex3f(table_x + table_width / 2, -0.98, -0.3)
    glVertex3f(table_x + table_width / 2, -0.98, 0.3)
    glVertex3f(table_x - table_width / 2, -0.98, 0.3)
    glEnd()

    # Pernas da mesa
    leg_width = 0.04
    leg_height = 0.5

    glBegin(GL_QUADS)
    glVertex3f(table_x - table_width / 2 + leg_width, -1 - leg_height, -0.28)  # Largura e Altura das pernas da mesa
    glVertex3f(table_x - table_width / 2, -1 - leg_height, -0.28)
    glVertex3f(table_x - table_width / 2, -0.98, -0.28)
    glVertex3f(table_x - table_width / 2 + leg_width, -0.98, -0.28)

    glVertex3f(table_x + table_width / 2 - leg_width, -1 - leg_height, -0.28)  # Largura e Altura das pernas da mesa
    glVertex3f(table_x + table_width / 2, -1 - leg_height, -0.28)
    glVertex3f(table_x + table_width / 2, -0.98, -0.28)
    glVertex3f(table_x + table_width / 2 - leg_width, -0.98, -0.28)

    glVertex3f(table_x + table_width / 2 - leg_width, -1 - leg_height, 0.28)  # Largura e Altura das pernas da mesa
    glVertex3f(table_x + table_width / 2, -1 - leg_height, 0.28)
    glVertex3f(table_x + table_width / 2, -0.98, 0.28)
    glVertex3f(table_x + table_width / 2 - leg_width, -0.98, 0.28)

    glVertex3f(table_x - table_width / 2 + leg_width, -1 - leg_height, 0.28)  # Largura e Altura das pernas da mesa
    glVertex3f(table_x - table_width / 2, -1 - leg_height, 0.28)
    glVertex3f(table_x - table_width / 2, -0.98, 0.28)
    glVertex3f(table_x - table_width / 2 + leg_width, -0.98, 0.28)
    glEnd()
 

def draw_air_conditioner():
    # Cor do ar-condicionado (branco)
    glColor3f(1.0, 1.0, 1.0)


    # Definindo vértices para um retângulo cúbico mais largo e alto
    vertices = [
        (-0.3, 0.6, -0.98),  # V0
        (0.3, 0.6, -0.98),   # V1
        (0.3, 0.8, -0.98),   # V2
        (-0.3, 0.8, -0.98),  # V3
        (-0.3, 0.6, -0.88),  # V4
        (0.3, 0.6, -0.88),   # V5
        (0.3, 0.8, -0.88),   # V6
        (-0.3, 0.8, -0.88)  # V7
    ]

    # Definindo as faces usando os vértices
    faces = [
        (0, 1, 2, 3),  # Parte frontal
        (4, 5, 1, 0),  # Lado esquerdo
        (5, 6, 2, 1),  # Parte superior
        (6, 7, 3, 2),  # Lado direito
        (7, 4, 0, 3),  # Parte inferior
        (4, 7, 6, 5)   # Parte traseira
    ]

    for face in faces:
        glBegin(GL_QUADS)
        for vertex in face:
            glVertex3fv(vertices[vertex])
        glEnd()

# Variável para controlar o estado da luz da lâmpada
lamp_light_on = False

# Função para renderizar a luminária
def draw_lamp():
    global lamp_light_on
    
    # Verificar se a luz da lâmpada está ligada
    if lamp_light_on:
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
    else:
        glDisable(GL_LIGHTING)
        glDisable(GL_LIGHT0)
    
    # Configurar luz direcional para a lâmpada
    lamp_light_position = [0.0, 1.0, 0.0, 1.0]  # Posição da luz (na ponta da lâmpada)
    lamp_light_direction = [0.0, -1.0, 0.0]  # Direção da luz (apontando para baixo)

    glLightfv(GL_LIGHT0, GL_POSITION, lamp_light_position)
    glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, lamp_light_direction)

    # Cubo pequeno amarelo (lâmpada)
    glColor3f(1.0, 1.0, 0.0)  # Cor do cubo (amarelo)

    glBegin(GL_QUADS)
    # Frente do cubo
    glVertex3f(-0.02, 0.7, -0.02)
    glVertex3f(0.02, 0.7, -0.02)
    glVertex3f(0.02, 0.7, 0.02)
    glVertex3f(-0.02, 0.7, 0.02)

    # Lado esquerdo do cubo
    glVertex3f(-0.02, 0.7, -0.02)
    glVertex3f(-0.02, 0.7, 0.02)
    glVertex3f(-0.02, 0.5, 0.02)
    glVertex3f(-0.02, 0.5, -0.02)

    # Lado direito do cubo
    glVertex3f(0.02, 0.7, -0.02)
    glVertex3f(0.02, 0.7, 0.02)
    glVertex3f(0.02, 0.5, 0.02)
    glVertex3f(0.02, 0.5, -0.02)

    # Trás do cubo
    glVertex3f(-0.02, 0.7, -0.02)
    glVertex3f(0.02, 0.7, -0.02)
    glVertex3f(0.02, 0.5, -0.02)
    glVertex3f(-0.02, 0.5, -0.02)

    # Topo do cubo
    glVertex3f(-0.02, 0.7, 0.02)
    glVertex3f(0.02, 0.7, 0.02)
    glVertex3f(0.02, 0.5, 0.02)
    glVertex3f(-0.02, 0.5, 0.02)
    glEnd()

    # Haste da luminária
    glColor3f(0.5, 0.5, 0.5)  # Cor da haste (cinza)
    glBegin(GL_QUADS)
    glVertex3f(-0.005, 0.7, -0.005)  # Largura, Altura e Comprimento da haste da luminária
    glVertex3f(0.005, 0.7, -0.005)
    glVertex3f(0.005, 1.2, -0.005)  # Largura, Altura e Comprimento da haste da luminária
    glVertex3f(-0.005, 1.2, -0.005)
    glEnd()

    # Abajur da luminária
    glColor3f(0.7, 0.7, 0.7)  # Cor do abajur (cinza claro)
    glBegin(GL_QUADS)
    glVertex3f(-0.05, 1.2, -0.05)  # Largura, Altura e Comprimento do abajur da luminária
    glVertex3f(0.05, 1.2, -0.05)
    glVertex3f(0.05, 1.2, 0.05)
    glVertex3f(-0.05, 1.2, 0.05)
    glEnd()

# Verificar se a tecla 'y' foi pressionada para ligar a luz da lâmpada
    if keys[pygame.K_y]:
        lamp_light_on = True

    # Verificar se a tecla 'u' foi pressionada para desligar a luz da lâmpada
    if keys[pygame.K_u]:
        lamp_light_on = False

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

    # Desative a aplicação da textura
    glDisable(GL_TEXTURE_2D)

    # Renderize as partes da cena que não devem ser afetadas pela textura do piso
    
    draw_room()
    draw_lamp()
    draw_air_conditioner()
    

    # Reative a aplicação da textura apenas para o piso
    glEnable(GL_TEXTURE_2D)

    # Renderize o piso
    draw_floor()

    # Desative a aplicação da textura
    glDisable(GL_TEXTURE_2D)

    draw_table()
    draw_blackboard()

    glDisable(GL_TEXTURE_2D)
    
    # Reative a aplicação da textura apenas para o piso
    glPopMatrix()

    pygame.display.flip()
    clock.tick(60)
