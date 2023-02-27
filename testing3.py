import pygame
from sys import exit
from pygame.locals import *
import random
import math

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

colors = ["blue", "grey"]
station_colors, xy_list, blue_stations = [], [], []

rows = random.randint(7, 12)
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

blue_stations.sort(key=lambda x: x[0])
x = blue_stations[0][0]
n = 0
xy_list2 = [[blue_stations[0]]]

for i in blue_stations[1:]:
    if i[0] == x:
        xy_list2[n].append(i)
    else:
        xy_list2.append([i])
        x = blue_stations[blue_stations.index(i)][0]
        n += 1

path = []

for i in range(longest_sublist(xy_list2)):
    paths = list(product(*xy_list2))
    buh = 0
    d = []

    for e, ii in enumerate(paths):
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
    print(xy_list2)
    print(paths)
    print(path)

def reset():
    for i in range(len(xy_list)):


pygame.init()
screen = pygame.display.set_mode((800, 400), pygame.RESIZABLE)
pygame.display.set_caption("Simulation")
fullscreen = False
clock = pygame.time.Clock()

text = "Smarta bussar"
test_font = pygame.font.SysFont("arial", 100)
text_surface = test_font.render(text, False, "black")
text_width, text_height = test_font.size(text)

bus_length = 50
bus = pygame.surface.Surface((bus_length, 20))
bus.fill("red")
road_thickness = 25
speed = 5
node = 0
path_number = -1

last_station_on = True

start = True

while True:
    screen.fill("lightgrey")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == VIDEORESIZE:
            if not fullscreen:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            start = True
            path_number -= 1
        if event.type == KEYDOWN:
            if event.key == K_f:
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode((800, 400), pygame.RESIZABLE)
                start = True
                path_number -= 1

    if start:
        bus_start = screen.get_height() * int(rows / 2) / rows
        bus_rect = bus.get_rect(center = (0, bus_start)) 
        node = 0
        if path_number != len(path) - 1:
            path_number += 1  
        last_station_on = True  
        if "blue" in station_colors:
            start = False

    # Road building
    for i in range(1, rows):
        pygame.draw.rect(screen, ("black"), pygame.Rect(0, screen.get_height() / rows * i - road_thickness / 2, screen.get_width(), road_thickness))
        pygame.draw.rect(screen, ("black"), pygame.Rect(screen.get_width() / rows * i - road_thickness / 2, 0, road_thickness, screen.get_height()))
    
    for i in range(station_amount):
        pygame.draw.rect(screen, (station_colors[i]), pygame.Rect((screen.get_width() * 1.5 + xy_list[i][0] * screen.get_width()) / rows, screen.get_height() * xy_list[i][1] / rows, 15, 15))
    
    # Bus Movement
    if bus_rect.centerx < screen.get_width() / rows * (path[path_number][node][0] + 1):
        bus_rect.centerx += speed
    elif bus_rect.centery < screen.get_height() / rows * path[path_number][node][1] - speed:
        bus_rect.centery += speed
    elif bus_rect.centery > screen.get_height() / rows * path[path_number][node][1] + speed:
        bus_rect.centery -= speed
    elif node != len(path[path_number]) - 1:
        station_colors[xy_list.index(path[path_number][node])] = "grey"
        node += 1
    elif bus_rect.left < screen.get_width():
        bus_rect.centerx += speed
        if last_station_on:
            station_colors[xy_list.index(path[path_number][node])] = "grey"
            last_station_on = False
    else:
        start = True

    screen.blit(bus, bus_rect)
    screen.blit(text_surface, ((screen.get_width() - text_width)/ 2, (screen.get_height() - text_width) / 10))

    pygame.display.update()
    clock.tick(60)