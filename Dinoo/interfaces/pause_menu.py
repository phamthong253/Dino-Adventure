import pygame
import sys
# from dinosaur.pteranodon import Pteranodon
from config import font, font_path, gamePaused
# from interfaces.gameplay import *
from interfaces.options import *

def show_pause_menu():
    global gamePaused
    OPTIONS_MOUSE_POS = pygame.mouse.get_pos()  # Lấy vị trí chuột

    # Tạo các button cho giao diện pause
    CONTINUE_BUTTON = Button('B_Button4.png', pos=(width / 2, height / 2 - 100),
                         text_input=None, font=font, base_color="Black", hovering_color="White")
    OPTIONS_BUTTON = Button('B_Button61.png', pos=(width / 2, height / 2),
                              text_input=None, font=font, base_color="Black", hovering_color="White")
    QUIT_BUTTON = Button('B_Button40.png', pos=(width / 2, height / 2 + 100),
                         text_input=None, font=font, base_color="Black", hovering_color="White")

    while True:  # Chạy mã cho đến khi thoát khỏi menu pause
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()  # Cập nhật vị trí chuột mỗi khung hình
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:  # Nhấn P hoặc ESC để tiếp tục
                    gamePaused = False
                    return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if CONTINUE_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    gamePaused = False
                    return  # Trở lại gameplay
                if OPTIONS_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    options()  # Quay lại giao diện options
                if QUIT_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    pygame.quit()
                    sys.exit()  # Thoát game

        # Vẽ giao diện menu pause
        pause_text = font.render("Game Paused", True, "Black")
        pause_rect = pause_text.get_rect(center=(width / 2, height / 2 - 200))
        screen.blit(pause_text, pause_rect)

        # Cập nhật và vẽ các button
        CONTINUE_BUTTON.changeColor(OPTIONS_MOUSE_POS)
        CONTINUE_BUTTON.update(screen)

        OPTIONS_BUTTON.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BUTTON.update(screen)

        QUIT_BUTTON.changeColor(OPTIONS_MOUSE_POS)
        QUIT_BUTTON.update(screen)

        pygame.display.update()