import pygame
from sys import exit
from pygame.locals import *
import random
# import math

class Station(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, image):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(image), (45, 30)) #0.662797944631
        self.rect = self.image.get_rect()      
        self.rect.centerx = x_pos
        self.rect.centery = y_pos

station_amount = 7
fullscreen = False

pygame.init()
screen = pygame.display.set_mode((800, 400), pygame.RESIZABLE)
clock = pygame.time.Clock()

blue_stations = []
station_group = pygame.sprite.Group()
blue_station_amount = random.randint(1, station_amount)
grey_station_amount = station_amount - blue_station_amount
for i in range(blue_station_amount):
    x, y = random.randint(0, screen.get_width()), random.randint(0, screen.get_height())
    new_station = Station(x, y, "graphics/station1.png")
    station_group.add(new_station)  
    blue_stations.append([x, y])      
for i in range(grey_station_amount):
    new_station = Station(random.randint(0, screen.get_width()), random.randint(0, screen.get_height()), "graphics/station0.png")
    station_group.add(new_station)

while True:
    screen.fill("lawngreen")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == VIDEORESIZE:
            if not fullscreen:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            blue_stations.clear()
            station_group.empty()
            blue_station_amount = random.randint(1, station_amount)
            grey_station_amount = station_amount - blue_station_amount
            for i in range(blue_station_amount):
                x, y = random.randint(0, screen.get_width()), random.randint(0, screen.get_height())
                new_station = Station(x, y, "graphics/station1.png")
                station_group.add(new_station)  
                blue_stations.append([x, y])      
            for i in range(grey_station_amount):
                new_station = Station(random.randint(0, screen.get_width()), random.randint(0, screen.get_height()), "graphics/station0.png")
                station_group.add(new_station)
        if event.type == KEYDOWN:
            if event.key == K_f:
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode((800, 400), pygame.RESIZABLE)
                blue_stations.clear()
                station_group.empty()
                blue_station_amount = random.randint(1, station_amount)
                grey_station_amount = station_amount - blue_station_amount
                for i in range(blue_station_amount):
                    x, y = random.randint(0, screen.get_width()), random.randint(0, screen.get_height())
                    new_station = Station(x, y, "graphics/station1.png")
                    station_group.add(new_station)  
                    blue_stations.append([x, y])      
                for i in range(grey_station_amount):
                    new_station = Station(random.randint(0, screen.get_width()), random.randint(0, screen.get_height()), "graphics/station0.png")
                    station_group.add(new_station)
    
    print(blue_stations)
    station_group.draw(screen)
    pygame.display.update()
    clock.tick(60)