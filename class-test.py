import pygame
from sys import exit
from pygame.locals import *
import random
import math

class Station(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()

station_group = pygame.sprite.Group()
for i in range(7):
    new_station = Station(random.choice(["graphics/empty-station.png", "graphics/full-station.png"]))
    station_group.add(new_station)

print(station_group.image)