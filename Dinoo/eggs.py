from utils import load_image, load_sprite_sheet
from config import *
from dinosaur.dinosaur import *
class Egg(pygame.sprite.Sprite):
    def __init__(self,speed, x, y):
        super(Egg, self).__init__()
        self.image, self.rect = load_image('eggs.png', 25, 35, -1)
        self.movement = [-1 * speed, 0]
        self.rect.x = x
        self.rect.y = y
    
    def update(self):
        self.rect = self.rect.move(self.movement)
        if self.rect.right < 0:
            self.kill()

    def draw(self, screen):
        screen.blit(self.image, self.rect)