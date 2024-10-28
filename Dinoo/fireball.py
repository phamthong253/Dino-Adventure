import pygame
from utils import *
class Fireball(pygame.sprite.Sprite):
    def __init__(self, speed=5, sizex=-1, sizey=-1, width=800, height=600):
        super().__init__()
        self.images, self.rect = load_sprite_sheet(
            'fireball.png', 10, 1, 50, 50, -1)
        
        self.rect.left = 0
        self.rect.centery = 0
        self.image = self.images[0]
        self.index = 0
        self.counter = 0
        self.speed = speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        if self.counter % 10 == 0:
            self.index = (self.index + 1) % 10
        self.image = self.images[self.index]
        self.counter = (self.counter + 1)
        self.rect.x += self.speed
        if self.rect.left > 700:  # Assuming screen width is 800
            self.kill()
