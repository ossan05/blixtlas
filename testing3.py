# Releventa bibliotek för programmet

import pygame, math, random
from sys import exit
from pygame.locals import *

# Klass för vägar som går från väst till öst

class RoadHorizontal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("graphics/road2.png"), (213, 60))  # (80, 60)
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

# Klass för vägar som går från norr till syd

class RoadVertical(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.transform.rotate(pygame.image.load("graphics/road2.png"), 90), (60, 213))  # (60, 80)
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

# Klass för stationer

class Station(pygame.sprite.Sprite):
    def __init__(self, xy, image):
        super().__init__()
        self.image_path = image
        self.image = pygame.transform.scale(pygame.image.load(self.image_path), (45, 30)) # 0.662797944631
        self.rect = self.image.get_rect()   
        self.xy = xy   
        self.rect.centerx = (screen.get_width() * 1.5 + xy[0] * screen.get_width()) / rows
        self.rect.centery = screen.get_height() * xy[1] / rows

# Klass för dynamiska bussar

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
        speed = 5
        if self.rect.centerx < self.dest[0] - screen.get_width() / (rows * 2):
            self.rect.centerx += speed
        elif self.rect.centery < self.dest[1] - speed:
            self.rect.centery += speed
        elif self.rect.centery > self.dest[1] + speed:
            self.rect.centery -= speed
        elif self.rect.centerx < self.dest[0]:
            self.rect.centerx += speed

# Klass för vanliga bussar

class Badbus(pygame.sprite.Sprite):
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
        speed = 5
        if self.rect.centerx < self.dest[0] - screen.get_width() / (rows * 2):
            self.rect.centerx += speed
        elif self.rect.centery < self.dest[1] - speed:
            self.rect.centery += speed
        elif self.rect.centery > self.dest[1] + speed:
            self.rect.centery -= speed
        elif self.rect.centerx < self.dest[0]:
            self.rect.centerx += speed

# Funktion som skalar storlek när man ändrar fönsterstorleken

def resize():
    global bk_image, row_badbus, row_bus

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
        bus.dest = [0, screen.get_height() * bus.y / rows]
        print(bus.rect.center, bus.dest)
    
    for bus in badbus_group:
        bus.rect.centery = screen.get_height() * bus.y / rows
        bus.rect.centerx = 0
        bus.dest = [0, screen.get_height() * bus.y / rows]
        print(bus.rect.center, bus.dest)

    row_bus = 0
    row_badbus = 0

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

def new_destfull(row):
    taken = []
    dist = []
    dest = []

    for bus in bus_group:
        dist.clear()
        dest.clear()
        for station in station_group:
            if list(station.rect.center) not in taken and station.xy[0] == row and station.rect.centerx - bus.rect.centerx > 10 and station.image_path == "graphics/station1.png":  # having ten is a possible bug
                dist.append([math.hypot(station.rect.centerx - bus.rect.centerx, station.rect.centery - bus.rect.centery)])
                dest.append([station.rect.centerx, station.rect.centery])
        try:
            bus.dest = dest[dist.index(min(dist))]
            taken.append(bus.dest)
        except ValueError:
            return
        
def new_destempty(row):
    taken = []
    dist = []
    dest = []

    for bus in badbus_group:
        dist.clear()
        dest.clear()
        for station in station_group:
            if list(station.rect.center) not in taken and station.xy[0] == row and station.rect.centerx - bus.rect.centerx > 10:  # having ten is a possible bug
                dist.append([math.hypot(station.rect.centerx - bus.rect.centerx, station.rect.centery - bus.rect.centery)])
                dest.append([station.rect.centerx, station.rect.centery])
        try:
            bus.dest = dest[dist.index(min(dist))]
            taken.append(bus.dest)
        except ValueError:
            return

def reset():
    global blue_station_amount, grey_station_amount, col_blue, col_grey, bus_group, badbus_group, row_badbus, row_bus

    blue_station_amount = random.randint(1, station_amount - 1)
    grey_station_amount = station_amount - blue_station_amount
    col_blue.clear()
    col_grey.clear()

    for station in station_group:
        color = random.choice(["graphics/station1.png", "graphics/station0.png"])
        station.image_path = color
        station.image = pygame.transform.scale(pygame.image.load(station.image_path), (45, 30))
        if color == "graphics/station1.png":
            col_blue.append(station.xy[0])
        else:
            col_grey.append(station.xy[0])
    
    bus_group.empty()
    big_bus = Bus(int(rows / 2), "graphics\stor-buss.png", (110, 45), [0, screen.get_height() * int(rows / 2) / rows])
    bus_group = pygame.sprite.Group(big_bus)

    try:
        for i in range(1, number_of_buses(col_blue)):
            new_bus = Bus(i, "graphics/liten-buss.png", (75, 30), [0, screen.get_height() * i / rows])
            bus_group.add(new_bus)
    except ValueError:
        pass

    badbus_group.empty()
    badbus_group = pygame.sprite.Group()

    for i in range(1, number_of_buses(col_blue + col_grey) + 1):
        new_badbus = Badbus(i, "graphics/liten-spokbuss.png", (75, 30), [0, screen.get_height() * i / rows])
        badbus_group.add(new_badbus)
    row_bus = 0
    row_badbus = 0

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

big_bus = Bus(int(rows / 2), "graphics\stor-buss.png", (110, 45), [0, screen.get_height() * int(rows / 2) / rows])
bus_group = pygame.sprite.Group(big_bus)

for i in range(1, number_of_buses(col_blue)):
    new_bus = Bus(i, "graphics/liten-buss.png", (75, 30), [0, screen.get_height() * i / rows])
    bus_group.add(new_bus)

badbus_group = pygame.sprite.Group()

for i in range(1, number_of_buses(col_blue + col_grey) + 1):
    new_badbus = Badbus(i, "graphics/liten-spokbuss.png", (75, 30), [0, screen.get_height() * i / rows])
    badbus_group.add(new_badbus)


fullscreen = False

new_destfull(0)
new_destempty(0)

row_bus = 0
row_badbus = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == VIDEORESIZE:
            if not fullscreen:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)   
            resize()     
            print(row_badbus, row_bus)
            new_destfull(row_bus)
            new_destempty(row_badbus)
        if event.type == KEYDOWN:
            if event.key == K_f:
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode((800,400), pygame.RESIZABLE)
    if row_badbus >= rows - 2 and row_bus >= rows - 2:
        reset()
        new_destfull(row_bus)
        new_destempty(row_badbus)

    if row_badbus >= rows - 2:
        for bus in badbus_group:
            bus.rect.x += 5
    
    if row_bus >= rows - 2:
        for bus in bus_group:
            bus.rect.x += 5    

    for count, bus in enumerate(bus_group, start=1):
        if bus.dest[0] > bus.rect.centerx:
            break
        elif count == len(bus_group):
            row_bus += 1
            new_destfull(row_bus)

    for count, bus in enumerate(badbus_group, start=1):
        if bus.dest[0] > bus.rect.centerx:
            break
        elif count == len(badbus_group):
            row_badbus += 1
            new_destempty(row_badbus)

    # Collision between station and bus
    busstation_collision = pygame.sprite.groupcollide(station_group, bus_group, False, False)
    if busstation_collision:
        for station in busstation_collision:
            if station.image_path == "graphics/station1.png":
                station.image_path = "graphics/station0.png"
                station.image = pygame.transform.scale(pygame.image.load(station.image_path), (45, 30))

    # Sätt in övre kod i klassen om du har tid

    bus_group.update()
    badbus_group.update()
    screen.blit(bk_image, (0, 0))
    road_group.draw(screen)
    station_group.draw(screen)
    bus_group.draw(screen)
    badbus_group.draw(screen)
    pygame.display.update()
    clock.tick(60)