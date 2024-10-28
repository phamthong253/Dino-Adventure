import pygame
from utils import load_image, load_sprite_sheet
from config import *
from dinosaur.dinosaur import *
from eggs import *

# class Egg(pygame.sprite.Sprite):
#     def __init__(self, x, y):
#         super(Egg, self).__init__()
#         self.egg_image, self.rect = load_image('eggs.png', 50, 50, -1)
#         self.rect = self.image.get_rect()  # Tạo rect cho trứng
#         self.rect.x = x
#         self.rect.y = y

class Troodon(Dinosaur):
    def __init__(self, speed=5, sizex=-1, sizey=-1):
        # Initialize the Troodon specifics
        super().__init__('troodon.png', 8, 1, 70, 70)
        
        self.rect.left = 0
        self.rect.centery = 0
        self.rect.bottom = int(0.98 * height)
        self.index = 0
        self.counter = 0
        self.speed = speed
        self.movement = [-1 * speed, 0]
        self.egg_spawn = False
        self.egg_group = pygame.sprite.Group()  # Group for eggs

    def update(self):
        super().update()
        if self.counter % 10 == 0:
            self.index = (self.index + 1) % 8
        self.image = self.images[self.index]
        self.counter += 1
        self.rect.x += self.speed
        if self.rect.right < 0:  # Assuming screen width is 800
            self.rect = self.rect.move(self.movement)
        if self.rect.left > 500 and not self.egg_spawn:
            self.give_item()
            self.egg_spawn = True
        self.egg_group.update()

    def give_item(self):
        # Thả trứng
        self.egg = Egg(5, self.rect.centerx, self.rect.bottom -30)
        self.egg_group.add(self.egg)

    def draw(self, screen):
        # Vẽ Troodon
        screen.blit(self.image, self.rect)
        # Vẽ trứng nếu tồn tại
        self.egg_group.draw(screen)
