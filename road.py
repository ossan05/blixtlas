import pygame
import pygame
from sys import exit
from pygame.locals import *
import math

class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("graphics/grass.png"), (screen.get_width(), screen.get_height()))
        self.rect = self.image.get_rect()
        self.rect.topleft = [0, 0]
    def update(self):
        self.image = pygame.transform.scale(self.image, (screen.get_width(), screen.get_height()))
        self.rect = self.image.get_rect()

class RoadHorizontal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("graphics/road2.png"), (213, 60))  # (80, 60)
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

class RoadVertical(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.transform.rotate(pygame.image.load("graphics/road2.png"), 90), (60, 213))  # (60, 80)
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

pygame.init()
screen = pygame.display.set_mode((800, 400), pygame.RESIZABLE)
clock = pygame.time.Clock()

fullscreen = False

while True:
    # screen.fill("chartreuse4")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == VIDEORESIZE:
            if not fullscreen:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            bk_group.update()
        if event.type == KEYDOWN:
            if event.key == K_f:
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode((800, 400), pygame.RESIZABLE)
                bk_group.update()

    bk_group = pygame.sprite.Group()
    bk = Background()
    bk_group.add(bk)

    road_group = pygame.sprite.Group()
    for i in range(math.ceil(screen.get_width()/213)):
        new_h_road = RoadHorizontal(screen.get_width()/213 + 213 * i, 50)
        road_group.add(new_h_road)
    for i in range(math.ceil(screen.get_height()/213)):
        new_v_road = RoadVertical(50, screen.get_height()/213 + 213 * i)
        road_group.add(new_v_road)
    bk_group.draw(screen)
    road_group.draw(screen)
    pygame.display.update()
    clock.tick(60)