import pygame
import random
from sys import exit
from pygame.locals import *
import math

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

class Station(pygame.sprite.Sprite):
    def __init__(self, xy, image):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(image), (45, 30)) # 0.662797944631
        self.rect = self.image.get_rect()   
        self.xy = xy   
        self.rect.centerx = (screen.get_width() * 1.5 + xy[0] * screen.get_width()) / rows
        self.rect.centery = screen.get_height() * xy[1] / rows

class Bus(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, image, image_size):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(image), (image_size))  # 75, 30
        self.rect = self.image.get_rect()
        self.rect.centerx = x_pos
        self.rect.centery = y_pos

def resize():
    global bk_image

    bk_image = pygame.transform.scale(pygame.image.load("graphics/grass.png"), (screen.get_width(), screen.get_height()))

    road_group.empty()
    for i in range(1, rows):
        for j in range(math.ceil(screen.get_width()/213 + 1)):
            new_h_road = RoadHorizontal(screen.get_width()/213 + 213 * j, screen.get_height() / rows * i)
            road_group.add(new_h_road)
        for j in range(math.ceil(screen.get_height()/213 + 1)):
            new_v_road = RoadVertical(screen.get_width() / rows * i, screen.get_height()/213 + 213 * j)
            road_group.add(new_v_road)

    for station in station_group:
        station.rect.centerx = (screen.get_width() * 1.5 + station.xy[0] * screen.get_width()) / rows
        station.rect.centery = screen.get_height() * station.xy[1] / rows

def number_of_buses(col):
    l = []
    n = 0
    for i in col:
        for j in i:
            for k in i:
                if j == k:
                    n += 1
            l.append(n)
            n = 0
    return max(l)

rows = 5
station_amount = random.randint(2, (rows - 1) * (rows - 2))

pygame.init()
screen = pygame.display.set_mode((800, 400), pygame.RESIZABLE)
clock = pygame.time.Clock()

bk_image = pygame.transform.scale(pygame.image.load("graphics/grass.png"), (screen.get_width(), screen.get_height()))

road_group = pygame.sprite.Group()
for i in range(1, rows):
    for j in range(math.ceil(screen.get_width()/213)):
        new_h_road = RoadHorizontal(screen.get_width()/213 + 213 * j, screen.get_height() / rows * i)
        road_group.add(new_h_road)
    for j in range(math.ceil(screen.get_height()/213)):
        new_v_road = RoadVertical(screen.get_width() / rows * i, screen.get_height()/213 + 213 * j)
        road_group.add(new_v_road)

blue_stations, grey_stations = [], []
station_group = pygame.sprite.Group()
blue_station_amount = random.randint(1, station_amount)
grey_station_amount = station_amount - blue_station_amount
for i in range(blue_station_amount):
    xy_blue = [random.randint(0, rows - 3), random.randint(1, rows - 1)]
    while xy_blue in blue_stations:
        xy_blue = [random.randint(0, rows - 3), random.randint(1, rows - 1)]
    new_station = Station(xy_blue, "graphics/station1.png")
    station_group.add(new_station)  
    blue_stations.append(xy_blue)      
for i in range(grey_station_amount):
    xy_grey = [random.randint(0, rows - 3), random.randint(1, rows - 1)]
    while xy_grey in grey_stations:
        xy_grey = [random.randint(0, rows - 3), random.randint(1, rows - 1)]
    new_station = Station(xy_grey, "graphics/station0.png")
    station_group.add(new_station)
    grey_stations.append(xy_grey)

print(number_of_buses(blue_stations))
print(number_of_buses([blue_stations, grey_stations]))

print()

fullscreen = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == VIDEORESIZE:
            if not fullscreen:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)   
            resize()     
        if event.type == KEYDOWN:
            if event.key == K_f:
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode((800,400), pygame.RESIZABLE)

    screen.blit(bk_image, (0, 0))
    road_group.draw(screen)
    station_group.draw(screen)
    pygame.display.update()
    clock.tick(60)