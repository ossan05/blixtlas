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

def longest_sublist(nested_list):
    lp = []
    for i in nested_list:
        lp.append(len(i))
    return max(lp)

def empty_list_remove(input_list):
    new_list = []
    for ele in input_list:
        if ele:
            new_list.append(ele)
    return new_list

colors = ["blue", "grey"] 
station_colors, xy_list, blue_stations = [], [], []

rows = random.randint(3, 8)
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

print(xy_list2)
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