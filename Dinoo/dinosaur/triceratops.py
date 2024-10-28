import pygame
from utils import load_image, load_sprite_sheet
from config import height
from dinosaur.dinosaur import *

class Triceratops(Dinosaur):
    def __init__(self, speed=3, sizex=-1, sizey=-1):
        # Initialize the Triceratops specifics
        # Use appropriate image and parameters
        super().__init__('triceratops-stroke.png', 6, 1, sizex, sizey)
        self.rect.left = 0
        self.rect.centery = 0
        self.rect.bottom = int(0.98 * height)
        self.index = 0
        self.counter = 0
        self.speed = speed

    def update(self):
        super().update()
        if self.counter % 10 == 0:
            self.index = (self.index + 1) % 6
        self.image = self.images[self.index]
        self.counter = (self.counter + 1)
        self.rect.x += self.speed
        if self.rect.left > 700:  # Assuming screen width is 800
            self.kill()