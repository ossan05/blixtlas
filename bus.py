import pygame

def longest_sublist(nested_list):
    lp = []
    for i in nested_list:
        lp.append(len(i))
    return max(lp)

class Extrabus(pygame.sprite.Sprite):
    def __init__(self, path, y_pos):
        super().__init__()
        self.image = pygame.image.load("graphics\liten-buss.png")
        self.path = path
        self.rect = self.image.get_rect()
        self.rect.center = [0, y_pos]

path = [[[2, 1], [3, 3]], [[2, 6]]]

extrabus_group = pygame.sprite.Group()
for i in path[1:]:
    new_bus = Extrabus(i, i[0][1])
    extrabus_group.add(new_bus)