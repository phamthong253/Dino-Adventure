import pygame

# Configuration and shared resources
scr_size = (width, height) = (800, 600)
FPS = 60
gravity = 0.6

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
background_col = (235, 235, 235)

# High score
high_score = 0

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Screen
screen = pygame.display.set_mode(scr_size)
clock = pygame.time.Clock()
clock.tick(FPS)
pygame.display.set_caption("Dino Adventure")

# Load sounds
jump_sound = pygame.mixer.Sound('Dinoo/sprites/jump.wav')
die_sound = pygame.mixer.Sound('Dinoo/sprites/die.wav')
checkPoint_sound = pygame.mixer.Sound('Dinoo/sprites/checkPoint.wav')
background_music = pygame.mixer.Sound('Dinoo/sprites/soundplaygame.mp3')


skins = {
    "default": {"select": "dino_alone.png", "avatar": "dino_avt.png", "ingame": "dino.png", "ingame_ducking": "dino_ducking.png"},
    "rainbow": {"select": "dino_rainbow_alone.png", "avatar": "dino_rainbow_avt.png", "ingame": "dino_rainbow_test.png", "ingame_ducking": "dino_rainbow_ducking.png"},
    "xyz": {"select": "dino_xyz_alone.png", "avatar": "dino_xyz_avt.png", "ingame": "dino_xyz.png", "ingame_ducking": "dino_xyz_ducking.png"},
    "batman": {"select": "dino_batman_alone.png", "avatar": "dino_batman_avt.png", "ingame": "dino_batman.png", "ingame_ducking": "dino_batman_ducking.png"}
}
selected_skin = "default"

font_path = "C:/WINDOWS/FONTS/CALIBRIL.TTF"
# None để sử dụng font mặc định, 36 là kích thước font
font = pygame.font.Font(font_path, 36)
gamePaused = False