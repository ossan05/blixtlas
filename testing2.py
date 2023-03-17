import pygame
from sys import exit
from pygame.locals import *
import random
import math

class RoadHorizontal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("graphics/road2.png"), (213, 60))  # (80, 60) för road.png
        self.rect = self.image.get_rect()
        self.rect.center = x, y

class RoadVertical(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.transform.rotate(pygame.image.load("graphics/road2.png"), 90), (60, 213))  # (60, 80) för road.png
        self.rect = self.image.get_rect()
        self.rect.center = x, y

class Extrabus(pygame.sprite.Sprite):
    def __init__(self, path, x_pos, y_pos, xnode, last_station):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("graphics\liten-buss.png"), (75, 30))
        self.path = path
        self.rect = self.image.get_rect()
        self.rect.centerx = x_pos
        self.rect.centery = y_pos
        self.xnode = xnode
        self.last_station = last_station


def list_duplicates_of(seq,item):
    start_at = -1
    locs = []
    while True:
        try:
            loc = seq.index(item,start_at+1)
        except ValueError:
            break
        else:
            locs.append(loc)
            start_at = loc
    return locs

def product(*args, repeat=1):
    pools = [tuple(pool) for pool in args] * repeat
    result = [[]]
    for pool in pools:
        result = [x+[y] for x in result for y in pool]
    for prod in result:
        yield tuple(prod)

def empty_list_remove(input_list):
    new_list = []
    for ele in input_list:
        if ele:
            new_list.append(ele)
    return new_list

def longest_sublist(nested_list):
    lp = []
    for i in nested_list:
        lp.append(len(i))
    return max(lp)

rows = random.randint(7, 12)
station_amount = random.randint(2, (rows - 1) * (rows - 2))

pygame.init()
screen = pygame.display.set_mode((800, 400), pygame.RESIZABLE)
pygame.display.set_caption("Simulation")
fullscreen = False
clock = pygame.time.Clock()

bus = pygame.image.load("graphics\stor-buss.png")
bus = pygame.transform.scale(bus, (110, 45))

bk_image = pygame.transform.scale(pygame.image.load("graphics/grass.png"), (screen.get_width(), screen.get_height()))

speed_big = 7
speed_small = 4

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == VIDEORESIZE:
            if not fullscreen:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            start = True
            bk_image = pygame.transform.scale(pygame.image.load("graphics/grass.png"), (screen.get_width(), screen.get_height()))
        if event.type == KEYDOWN:
            if event.key == K_f:
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode((800, 400), pygame.RESIZABLE)
                start = True
                bk_image = pygame.transform.scale(pygame.image.load("graphics/grass.png"), (screen.get_width(), screen.get_height()))

    road_group = pygame.sprite.Group()
    for i in range(1, rows):
        for j in range(math.ceil(screen.get_width()/213)):
            new_h_road = RoadHorizontal(screen.get_width()/213 + 213 * j, screen.get_height() / rows * i)
            road_group.add(new_h_road)
        for j in range(math.ceil(screen.get_height()/213)):
            new_v_road = RoadVertical(screen.get_width() / rows * i, screen.get_height()/213 + 213 * j)
            road_group.add(new_v_road)
        
    screen.blit(bk_image, (0,0))
    road_group.draw(screen)
    
    screen.blit(bus, bus_rect)
    extrabus_group.draw(screen)

    pygame.display.update()
    clock.tick(60)