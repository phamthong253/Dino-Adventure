# dinosaurs.py
import pygame
from skill import Skill  # Giả sử Skill cũng cần được sử dụng
from utils import load_sprite_sheet
from config import *

class Dinosaur(pygame.sprite.Sprite):
    def __init__(self, image_file, sprite_rows, sprite_cols, sizex=-1, sizey=-1):
        super().__init__()
        self.images, self.rect = load_sprite_sheet(
            image_file, sprite_rows, sprite_cols, sizex, sizey, -1)
        self.rect.bottom = int(0.98 * height)
        self.rect.left = width / 15
        self.image = self.images[0]
        self.index = 0
        self.counter = 0
        self.score = 0
        self.isJumping = False
        self.isDead = False
        self.isDucking = False
        self.isBlinking = False
        self.movement = [0, 0]
        self.jumpSpeed = 11.5
        self.shaking = False
