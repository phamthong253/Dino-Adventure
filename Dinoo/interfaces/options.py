import pygame
import sys
from dinosaur.dino import Dino
from interfaces.button import Button
from interfaces.introscreen import introscreen
from utils import load_image, load_sprite_sheet, disp_gameOver_msg, extractDigits
from config import *
from interfaces.gameplay import *
from interfaces.introscreen import *

def options():
    global selected_skin

    skin_buttons = []
    skin_positions = [(100, 150), (250, 150), (100, 250), (250, 250)]
    skin_names = list(skins.keys())

    # Create a grid of skin buttons
    for i, skin_name in enumerate(skin_names):
        button = Button(
            image_file=skins[skin_name]["avatar"],
            pos=skin_positions[i],
            text_input=None,
            font=font,
            base_color="Black",
            hovering_color="Green",
            border_color=(0, 0, 0)  # Set border color
        )
        skin_buttons.append(button)

    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        screen.fill("white")

        OPTIONS_TEXT = font.render("Choose Your Character", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(450, 60))
        screen.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image_file='B_Button70.png', pos=(
            400, 500), text_input=None, font=font, base_color="Black", hovering_color="Green")
        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(screen)

        START_GAME_BUTTON = Button(image_file='B_Button4.png', pos=(
            600, 500), text_input=None, font=font, base_color="White", hovering_color="Green")
        START_GAME_BUTTON.update(screen)


        for button in skin_buttons:
            button.changeColor(OPTIONS_MOUSE_POS)
            button.update(screen)

        # Display the selected skin
        skin_image, skin_rect = load_image(
            skins[selected_skin]["select"], 100, 100, -1)
        skin_rect.center = (500, 200)
        screen.blit(skin_image, skin_rect)
        # Display the selected skin name
        selected_skin_text = font.render(
            selected_skin.capitalize(), True, "Black")
        selected_skin_rect = selected_skin_text.get_rect(center=(500, 300))
        screen.blit(selected_skin_text, selected_skin_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    from interfaces.introscreen import introscreen
                    introscreen()
                if START_GAME_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    from interfaces.gameplay import start_game_with_skin
                    start_game_with_skin(skins[selected_skin]["ingame"], skins[selected_skin]["ingame_ducking"])
                for i, button in enumerate(skin_buttons):
                    if button.checkForInput(OPTIONS_MOUSE_POS):
                        selected_skin = skin_names[i]

        pygame.display.update()