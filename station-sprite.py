import pygame
from sys import exit
from pygame.locals import *
import random
import math

class Station(pygame.sprite.Sprite):
    def __init__(self, xy, image):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(image), (45, 30)) #0.662797944631
        self.rect = self.image.get_rect()   
        self.xy = xy   
        self.rect.centerx = (screen.get_width() * 1.5 + xy[0] * screen.get_width()) / rows
        self.rect.centery = screen.get_height() * xy[1] / rows
    def reset(self):
        self.image_path = random.choice(["graphics/station1.png", "graphics/station0.png"])
        self.image = pygame.transform.scale(pygame.image.load(self.image_path), (45, 30))
        

def number_of_buses(col):
    l = []
    n = 0
    for i in col:
        for j in col:
            if i == j:
                n += 1
        l.append(n)
        n = 0
    return max(l)

rows = 5
station_amount = random.randint(2, (rows - 1) * (rows - 2))
fullscreen = False

pygame.init()
screen = pygame.display.set_mode((800, 400), pygame.RESIZABLE)
clock = pygame.time.Clock()

blue_stations, grey_stations = [], []  # Behövs troligtvis inte
col_blue, col_grey = [], [] 

blue_station_amount = random.randint(1, station_amount)
grey_station_amount = station_amount - blue_station_amount
station_group = pygame.sprite.Group()
for i in range(blue_station_amount):
    xy_blue = [random.randint(0, rows - 3), random.randint(1, rows - 1)]
    while xy_blue in blue_stations:
        xy_blue = [random.randint(0, rows - 3), random.randint(1, rows - 1)]
    new_station = Station(xy_blue, "graphics/station1.png")
    station_group.add(new_station)  
    blue_stations.append(xy_blue) 
    col_blue.append(xy_blue[0])

for i in range(grey_station_amount):
    xy_grey = [random.randint(0, rows - 3), random.randint(1, rows - 1)]
    while xy_grey in grey_stations:
        xy_grey = [random.randint(0, rows - 3), random.randint(1, rows - 1)]
    new_station = Station(xy_grey, "graphics/station0.png")
    station_group.add(new_station)
    grey_stations.append(xy_grey)
    col_grey.append(xy_grey[0])

blue_stations

while True:
    screen.fill("lawngreen")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == VIDEORESIZE:
            if not fullscreen:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            for station in station_group:
                station.rect.centerx = (screen.get_width() * 1.5 + station.xy[0] * screen.get_width()) / rows
                station.rect.centery = screen.get_height() * station.xy[1] / rows
        if event.type == KEYDOWN:
            if event.key == K_f:
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode((800, 400), pygame.RESIZABLE)

    station_group.draw(screen)
    pygame.display.update()
    clock.tick(60)