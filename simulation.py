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

def make_path():
    global path, blue_stations
    blue_stations.sort(key=lambda x: x[0])
    x = blue_stations[0][0]
    n = 0
    xy_list2 = [[blue_stations[0]]]
    path = []

    for i in blue_stations[1:]:
        if i[0] == x:
            xy_list2[n].append(i)
        else:
            xy_list2.append([i])
            x = blue_stations[blue_stations.index(i)][0]
            n += 1

    for i in range(longest_sublist(xy_list2)):
        paths = list(product(*xy_list2))
        buh = 0
        d = []

        for e, ii in enumerate(paths):  # tveksam ändring
            for x in range(len(ii)-1):
                buh += math.dist(ii[x], ii[x+1])
            d.append(buh)
            buh = 0

        ind = d.index(min(d))
        path.append(list(paths[ind]))

        for b in range(len(xy_list2)):
            for j in path[i]:   # kan vara annorlunda ?
                if j in xy_list2[b]:
                    xy_list2[b].remove(j)
        xy_list2 = empty_list_remove(xy_list2)
    return path

colors = ["blue", "grey"]
station_colors, xy_list, blue_stations = [], [], []

rows = 7
station_amount = random.randint(2, (rows - 1) * (rows - 2))

for i in range(station_amount):
    station_color = random.choice(colors)
    xy = [random.randint(0, rows - 3), random.randint(1, rows - 1)]

    while xy in xy_list:
        xy = [random.randint(0, rows - 3), random.randint(1, rows - 1)]
        
    xy_list.append(xy)
    station_colors.append(station_color)
    if station_color == "blue":
        blue_stations.append(xy)

if "blue" not in station_colors:
    index = random.randint(0, len(station_colors) - 1)
    station_colors[index] = "blue"
    blue_stations.append(xy_list[index])

path = make_path()

def reset():
    global blue_stations, station_colors, station_color
    blue_stations, station_colors = [], []
    for i in range(station_amount):
        station_color = random.choice(colors)
        station_colors.append(station_color)
        if station_color == "blue":
            blue_stations.append(xy_list[i])
        if "blue" not in station_colors:
            index = random.randint(0, len(station_colors) - 1)
            station_colors[index] = "blue"
            blue_stations.append(xy_list[index])
    return make_path()

pygame.init()
screen = pygame.display.set_mode((800, 400), pygame.RESIZABLE)
pygame.display.set_caption("Simulation")
fullscreen = False
clock = pygame.time.Clock()

bus = pygame.image.load("graphics\stor-buss.png")
bus = pygame.transform.scale(bus, (110, 45))

bk_image = pygame.transform.scale(pygame.image.load("graphics/grass.png"), (screen.get_width(), screen.get_height()))

speed = 7
node = 0


last_station_on = True

start = True

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

    if start:
        bus_start = screen.get_height() * int(rows / 2) / rows
        bus_rect = bus.get_rect(center = (0, bus_start)) 
        extrabus_group = pygame.sprite.Group()
        re = 0
        node = 0
        last_station_on = True  
        if "blue" not in station_colors:
            path = reset()
        for i in path[1:]:
            new_bus = Extrabus(i, 0, screen.get_height() * i[0][1] / rows, 0, True)
            extrabus_group.add(new_bus)
        start = False

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
    
    for i in range(station_amount):
        pygame.draw.rect(screen, (station_colors[i]), pygame.Rect((screen.get_width() * 1.5 + xy_list[i][0] * screen.get_width()) / rows, screen.get_height() * xy_list[i][1] / rows, 15, 15))
    
    # Big Bus Movement
    if bus_rect.centerx < screen.get_width() / rows * (path[0][node][0] + 1):
        bus_rect.centerx += speed
    elif bus_rect.centery < screen.get_height() / rows * path[0][node][1] - speed:
        bus_rect.centery += speed
    elif bus_rect.centery > screen.get_height() / rows * path[0][node][1] + speed:
        bus_rect.centery -= speed
    elif node != len(path[0]) - 1:
        station_colors[xy_list.index(path[0][node])] = "grey"
        node += 1
    elif bus_rect.left < screen.get_width():
        bus_rect.centerx += speed
        if last_station_on:
            station_colors[xy_list.index(path[0][node])] = "grey"
            last_station_on = False
            re += 1
    elif re == len(path):
        start = True

    screen.blit(bus, bus_rect)
    extrabus_group.draw(screen)
    extrabus_group.update()

    pygame.display.update()
    clock.tick(60)