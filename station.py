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

colors = ["blue", "grey"] 
station_colors, xy_list, blue_stations = [], [], []

rows = 4
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

#xy_list = [[0, 4], [1, 3], [1, 6], [1, 2], [2, 6], [2, 2], [2, 5], [3, 3], [3, 4], [3, 6], [4, 2]]
#x = xy_list[0][0]
#n = 0
#xy_list2 = [[xy_list[0]]]
#
#for i in xy_list[1:]:
#    if i[0] == x:
#        xy_list2[n].append(i)
#    else:
#        xy_list2.append([i])
#        x = xy_list[xy_list.index(i)][0]
#        n += 1




def product(*args, repeat=1):
    pools = [tuple(pool) for pool in args] * repeat
    result = [[]]
    for pool in pools:
        result = [x+[y] for x in result for y in pool]
    for prod in result:
        yield tuple(prod)

paths = list(product(*xy_list2))
buh = 0
d = []

for j, i in enumerate(paths):
    for x in range(len(i)-1):
        buh += math.dist(i[x], i[x+1])
    d.append(buh)
    buh = 0

ind = d.index(min(d))
path = [list(paths[ind])]

print(paths)
print(path)
print(xy_list, "\n", xy_list2)

def longest_sublist(nested_list):
    lp = []
    for i in nested_list:
        lp.append(len(i))
    return max(lp)

for i in range(longest_sublist(xy_list2)):
    for i in xy_list2:
        for j in path:
            if j in i:
                del i[i.index(j)]
    paths = list(product(*xy_list2))
    buh = 0
    d = []

    for j, i in enumerate(paths):
        for x in range(len(i)-1):
            buh += math.dist(i[x], i[x+1])
        d.append(buh)
        buh = 0

    print(paths)
    ind = d.index(min(d))
    path.append(list(paths[ind]))

print(xy_list2)
print(path)