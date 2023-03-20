import pygame, math, random
from sys import exit
from pygame.locals import *


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
        self.image_path = image
        self.image = pygame.transform.scale(pygame.image.load(self.image_path), (45, 30)) # 0.662797944631
        self.rect = self.image.get_rect()   
        self.xy = xy   
        self.rect.centerx = (screen.get_width() * 1.5 + xy[0] * screen.get_width()) / rows
        self.rect.centery = screen.get_height() * xy[1] / rows
    def reset(self):
        self.image_path = random.choice(["graphics/station1.png", "graphics/station0.png"])
        self.image = pygame.transform.scale(pygame.image.load(self.image_path), (45, 30))
        

class Bus(pygame.sprite.Sprite):
    def __init__(self, y, image, image_size, dest):
        super().__init__()
        self.y = y
        self.image_path = image
        self.image = pygame.transform.scale(pygame.image.load(self.image_path), (image_size))  # 110, 45; 75, 30
        self.rect = self.image.get_rect()
        self.rect.centerx = 0
        self.rect.centery = screen.get_height() * y / rows
        self.dest = dest
    def update(self):
        global yodafull
        speed = 5
        if self.rect.centerx < self.dest[0] - screen.get_width() / (rows * 2):
            self.rect.centerx += speed
        elif self.rect.centery < self.dest[1] - speed:
            self.rect.centery += speed
        elif self.rect.centery > self.dest[1] + speed:
            self.rect.centery -= speed
        elif self.rect.centerx < self.dest[0]:
            self.rect.centerx += speed
        else:
            yodafull += 1


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

    for bus in bus_group:
        bus.rect.centery = screen.get_height() * bus.y / rows
        bus.rect.centerx = 0
    
    new_destfull()

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
col_blue, col_grey = [], [] 

station_group = pygame.sprite.Group()
blue_station_amount = random.randint(1, station_amount - 1)
grey_station_amount = station_amount - blue_station_amount

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
    while xy_grey in grey_stations or xy_grey in blue_stations:
        xy_grey = [random.randint(0, rows - 3), random.randint(1, rows - 1)]
    new_station = Station(xy_grey, "graphics/station0.png")
    station_group.add(new_station)
    grey_stations.append(xy_grey)
    col_grey.append(xy_grey[0])

big_bus = Bus(int(rows / 2), "graphics\stor-buss.png", (110, 45), [0, 0])
bus_group = pygame.sprite.Group(big_bus)

for i in range(1, number_of_buses(col_blue)):
    new_bus = Bus(i, "graphics/liten-buss.png", (75, 30), [0, 0])
    bus_group.add(new_bus)

def new_destfull():
    global yodafull
    yodafull = 0
    taken = []
    dist = []
    dest = []

    for bus in bus_group:
        dist.clear()
        dest.clear()
        for station in station_group:
            if list(station.rect.center) not in taken and station.rect.centerx - bus.rect.centerx > 10 and station.image_path == "graphics/station1.png":  # having ten is a possible bug
                print(station.rect.center)
                dist.append([math.hypot(station.rect.centerx - bus.rect.centerx, station.rect.centery - bus.rect.centery)])
                dest.append([station.rect.centerx, station.rect.centery])
        try:
            bus.dest = dest[dist.index(min(dist))]
            taken.append(bus.dest)
            # print(bus.dest)
            print(taken)
        except ValueError:
            return



fullscreen = False

yodafull = 0

new_destfull()

# for i in range(len(d[0])):
#     index_values = [lst[i] for lst in d]
#     min_val = min(index_values)
#     min_values.append(min_val)

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

    print(yodafull)
    if yodafull >= len(bus_group):
        new_destfull()

    # reset
    for count, station in enumerate(station_group, start=1):
        if station.image_path == "graphics/station1.png":
            break
        elif count == len(station_group):
            station.reset()

    # Collision between station and bus
    busstation_collision = pygame.sprite.groupcollide(station_group, bus_group, False, False)
    if busstation_collision:
        for station in busstation_collision:
            station.image_path = "graphics/station0.png"
            station.image = pygame.transform.scale(pygame.image.load(station.image_path), (45, 30))

    # Sätt in övre kod i klassen om du har tid

    bus_group.update()
    screen.blit(bk_image, (0, 0))
    road_group.draw(screen)
    station_group.draw(screen)
    bus_group.draw(screen)
    pygame.display.update()
    clock.tick(60)
