import pygame
import sys
import math
from pygame.locals import *

pygame.init()

size = width, height = 1400, 750
screen = pygame.display.set_mode(size)
pygame.display.set_caption("binary")
myfont = pygame.font.Font(None, 165)
clock = pygame.time.Clock()

pos_e = pos_mm = []

roll_e = roll_m = 0
roll_2 = roll_3 = roll_4 = roll_5 = roll_6 = roll_7 = roll_8 = 0

pygame.mixer.music.load(r'audio/人间星光.mp3')
pygame.mixer.music.play(loops=-1)
pygame.mixer.music.set_volume(0.5)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()

    background = pygame.image.load(r"img/backimg.jpg")
    screen.blit(background, (0, 0))

    sun = pygame.image.load(r"img\太阳.png")
    screen.blit(pygame.transform.scale(sun, (170, 170)), (700 - 60, 375 - 60))

    roll_3 += 0.077
    pos_3_x = int(size[0] // 2 + size[1] // 8 * math.sin(roll_3))
    pos_3_y = int(size[1] // 2 + size[1] // 8 * math.cos(roll_3))
    mercury = pygame.image.load(r"img\月球.png")
    screen.blit(pygame.transform.scale(mercury, (8, 8)), (pos_3_x, pos_3_y))

    roll_2 += 0.069
    pos_2_x = int(size[0] // 2 + size[1] // 7 * math.sin(roll_2))
    pos_2_y = int(size[1] // 2 + size[1] // 7 * math.cos(roll_2))
    venus = pygame.image.load(r"img\金星.png")
    screen.blit(pygame.transform.scale(venus, (10, 10)), (pos_2_x, pos_2_y))

    roll_e += 0.060
    pos_e_x = int(size[0] // 2 + size[1] // 6 * math.sin(roll_e))
    pos_e_y = int(size[1] // 2 + size[1] // 6 * math.cos(roll_e))
    earth = pygame.image.load(r"img\地球.png")
    screen.blit(pygame.transform.scale(earth, (15, 15)), (pos_e_x, pos_e_y))

    roll_4 += 0.053
    pos_4_x = int(size[0] // 2 + size[1] // 5 * math.sin(roll_4))
    pos_4_y = int(size[1] // 2 + size[1] // 5 * math.cos(roll_4))
    venus = pygame.image.load(r"img\火星.png")
    screen.blit(pygame.transform.scale(venus, (13, 13)), (pos_4_x, pos_4_y))

    roll_5 += 0.045
    pos_5_x = int(size[0] // 2 + size[1] // 4 * math.sin(roll_5))
    pos_5_y = int(size[1] // 2 + size[1] // 4 * math.cos(roll_5))
    mouth = pygame.image.load(r"img\木星.png")
    screen.blit(pygame.transform.scale(mouth, (70, 70)), (pos_5_x, pos_5_y))

    roll_6 += 0.037
    pos_6_x = int(size[0] // 2 + size[1] // 3.5 * math.sin(roll_6))
    pos_6_y = int(size[1] // 2 + size[1] // 3.5 * math.cos(roll_6))
    saturn = pygame.image.load(r"img\土星.png")
    screen.blit(pygame.transform.scale(saturn, (50, 50)), (pos_6_x, pos_6_y))

    roll_7 += 0.031
    pos_7_x = int(size[0] // 2 + size[1] // 2.7 * math.sin(roll_7))
    pos_7_y = int(size[1] // 2 + size[1] // 2.7 * math.cos(roll_7))
    uranus = pygame.image.load(r"img\天王星.png")
    screen.blit(pygame.transform.scale(uranus, (45, 45)), (pos_7_x, pos_7_y))

    roll_8 += 0.025
    pos_8_x = int(size[0] // 2 + size[1] // 2 * math.sin(roll_8))
    pos_8_y = int(size[1] // 2 + size[1] // 2 * math.cos(roll_8))
    neptune = pygame.image.load(r"img\海王星.png")
    screen.blit(pygame.transform.scale(neptune, (37, 37)), (pos_8_x, pos_8_y))

    roll_m += 0.2
    pos_m_x = int(pos_e_x + size[1] // 50 * math.sin(roll_m))
    pos_m_y = int(pos_e_y + size[1] // 50 * math.cos(roll_m))
    mouth = pygame.image.load(r"img\月球.png")
    screen.blit(pygame.transform.scale(mouth, (6, 6)), (pos_m_x, pos_m_y))

    pygame.display.flip()
    clock.tick(50)
