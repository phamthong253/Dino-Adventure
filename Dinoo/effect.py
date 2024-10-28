import pygame
import random
from config import *


def shake_screen(screen, duration, magnitude):
    """ Rung lắc màn hình trong khoảng thời gian nhất định """
    shake_end_time = pygame.time.get_ticks() + int(duration * 1000)  # Thời gian kết thúc
    # Tạo một bề mặt tạm thời để lưu màn hình hiện tại
    temp_surface = screen.copy()
    while pygame.time.get_ticks() < shake_end_time:
        # Tính toán vị trí mới với rung lắc
        offset_x = random.randint(-magnitude, magnitude)
        offset_y = random.randint(-magnitude, magnitude)

        # Cập nhật vị trí của màn hình
        screen.blit(temp_surface, (offset_x, offset_y))

        pygame.display.update()  # Cập nhật màn hình
        pygame.time.delay(10)  # Đợi một chút trước khi dịch chuyển lại



