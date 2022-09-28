from ast import Str
import pygame
import random
from pygame.sprite import Sprite
from pygame.locals import K_LEFT, K_RIGHT, K_UP, K_DOWN, K_1


class Player(Sprite):

    def __init__(self):
        # invocar la inicializacion del padre
        super().__init__()
        # crear una superficie
        # self.surf = pygame.image.load("clase_9/bluebird-midflap.png")
        self.mordecai_sheet = pygame.image.load('clase_9/assets/images/mordecai.png').convert_alpha()
        self.scene = 1
        self.width = 39
        self.height = 38
        self.scale = 2
        self.vx = 7
        self.vy = 7
        self.treasures = []
        self.paths = [True, True, True, True]
        self.surf = self.get_image(self.mordecai_sheet, self.scene, self.width, self.height, self.scale, (255,0,255))
        # self.surf.fill((0, 0, 255))
        self.rect = self.surf.get_rect(center=(50, 100))

    def delta_vx(self, new_velocity):
        self.vx = new_velocity
    def delta_vy(self, new_velocity):
        self.vy = new_velocity

    def callback(self, value):
        self.block_path(value)

    def block_path(self, path: int):
        self.paths[path] = False
    
    def free_path(self, path: int):
        self.paths[path] = True

    def free_paths(self):
        self.paths = [True for p in self.paths]

    def update_scene(self):
        self.free_paths()
        if self.scene == 2:
            self.scene = 0
        else:
            self.scene += 1
        self.surf = self.get_image(self.mordecai_sheet, self.scene, self.width, self.height, self.scale, (255,0,255))
    
    
    def update(self, keys):
        if keys[K_LEFT] and self.paths[2]:
            self.update_scene()
            self.rect.move_ip(-self.vx, 0)
        elif keys[K_RIGHT] and self.paths[3]:
            self.update_scene()
            self.rect.move_ip(self.vx, 0)
        elif keys[K_UP] and self.paths[0]:
            self.update_scene()
            self.rect.move_ip(0, -self.vy)
        elif keys[K_DOWN] and self.paths[1]:
            self.update_scene()
            self.rect.move_ip(0, self.vy)
        else:
            self.surf = self.get_image(self.mordecai_sheet, 1, self.width, self.height, self.scale, (255,0,255))
        # print(self.rect[0], self.rect[1])
    
    def get_image(self, sheet, frame, width, height, scale, color):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(sheet, (0,0), (0, (frame * height), width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(color)
        return image


class Enemy(Sprite):
    def __init__(self):
        # invocar la inicializacion del padre
        super().__init__()
        # crear una superficie
        self.rigby_sheet = pygame.image.load('clase_9/assets/images/rigby.png').convert_alpha()
        self.scene = 2
        self.height = 20
        self.width = 40
        self.scale = 2
        self.surf = self.get_image(self.rigby_sheet, self.scene, self.width, self.height, self.scale, (255,0,255))
        
        self.rect = self.surf.get_rect(center=(
            random.randint(1150, 1200),
            random.randint(100, 600)
        ))
    
    def update_scene(self):
        if self.scene == 3:
            self.scene = 0
        else:
            self.scene += 1
        self.surf = self.get_image(self.rigby_sheet, self.scene, self.width, self.height, self.scale, (255,0,255))

    def update(self):
        self.update_scene()
        self.rect.move_ip(-5, 0)
        #print("starting point", (self.scene * self.height) + self.scene)

    def get_image(self, sheet, frame, width, height, scale, color):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(sheet, (0,0), (0, (frame * height) + frame, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(color)
        return image

class Baby(Sprite):
    def __init__(self):
        # invocar la inicializacion del padre
        super().__init__()
        # crear una superficie
        self.baby_sheet = pygame.image.load('clase_9/assets/images/baby.png').convert_alpha()
        self.scene = 0
        self.height = 18
        self.width = 25.5
        self.scale = 2
        self.surf = self.get_image(self.baby_sheet, self.scene, self.width, self.height, self.scale, (255,0,255))
        
        self.rect = self.surf.get_rect(center=(
            random.randint(1150, 1200),
            random.randint(100, 600)
        ))
    
    def update_scene(self):
        if self.scene == 5:
            self.scene = 0
        else:
            self.scene += 1
        self.surf = self.get_image(self.baby_sheet, self.scene, self.width, self.height, self.scale, (255,0,255))

    def update(self):
        self.update_scene()
        self.rect.move_ip(-2, 0)
        #print("starting point", (self.scene * self.height) + self.scene)

    def get_image(self, sheet, frame, width, height, scale, color):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(sheet, (0,0), (8 + width * frame, 24, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(color)
        return image

class Destroyer(Sprite):
    def __init__(self):
        # invocar la inicializacion del padre
        super().__init__()
        # crear una superficie
        self.destroyer_sheet = pygame.image.load('clase_9/assets/images/destroyer.png').convert_alpha()
        self.vx = -7
        self.vy = 1
        self.width = 98
        self.height = 126
        self.surf = self.destroyer_sheet
        
        self.rect = self.surf.get_rect(center=(
            random.randint(1150, 1200),
            random.randint(100, 600)
        ))

    def callback(self, value):
        self.hit_wall()

    def hit_wall(self):
        self.vy = -self.vy
    
    def update(self):
        self.rect.move_ip(self.vx, self.vy)
        #print("starting point", (self.scene * self.height) + self.scene)

    
class Bullet(Sprite):
    def __init__(self, center):
        # invocar la inicializacion del padre
        super().__init__()
        # crear una superficie
        self.scene = 0
        self.height = 16
        self.width = 24
        self.scale = 2
        self.rigby_sheet = pygame.image.load('clase_9/assets/images/bullet.png').convert_alpha()
        self.surf = self.get_image(self.rigby_sheet, self.scene, self.width, self.height, self.scale, (0, 152, 239))
        self.rect = self.surf.get_rect(center=center)

    def update(self):
        self.rect.move_ip(10, 0)

    def get_image(self, sheet, frame, width, height, scale, color):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(sheet, (0,0), (0, (frame * height) + frame, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(color)
        return image
    