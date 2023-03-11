import pygame
from sys import exit
from pygame.locals import *
import random
import math

class Extrabus(pygame.sprite.Sprite):
    def __init__(self, path, x_pos, y_pos, xnode, last_station):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("graphics\liten-buss.png"), (50, 20))
        self.path = path
        self.rect = self.image.get_rect()
        self.rect.center = x_pos, y_pos
        self.xnode = xnode
        self.last_station = last_station
    def update(self):
        global station_colors, re
        for bus in extrabus_group:
            if bus.rect.centerx < screen.get_width() / rows * (bus.path[bus.xnode][0] + 1):
                bus.rect.centerx += 2
            elif bus.rect.centery < screen.get_height() / rows * bus.path[bus.xnode][1] - 2:
                bus.rect.centery += 2
            elif bus.rect.centery > screen.get_height() / rows * bus.path[bus.xnode][1] + 2:
                bus.rect.centery -= 2
            elif bus.xnode != len(bus.path) - 1:
                station_colors[xy_list.index(bus.path[bus.xnode])] = "grey"
                bus.xnode += 1
            elif bus.rect.centerx < screen.get_width():
                bus.rect.centerx += 2
                if bus.last_station:
                    station_colors[xy_list.index(bus.path[bus.xnode])] = "grey"
                    re += 1
                    bus.last_station = False

class Station(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.image = "image" # do this
        self.rect = self.image.get_rect()
        self.rect.centerx = x_pos
        self.rect.centery = y_pos
    def update(self):


station_group = pygame.sprite.Group()
for i in range(7):
    new_station = Station("blalbal")
    station_group.add(new_station)

station_group.draw(screen)