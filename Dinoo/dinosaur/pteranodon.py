import pygame
from dinosaur.dinosaur import Dinosaur
from config import *


class Pteranodon(Dinosaur):
    def __init__(self, speed=3, sizex=-1, sizey=-1):
        # Initialize the Pteranodon specifics
        # Use appropriate image and parameters
        super().__init__('ptetra-complete-test.png', 2, 1, sizex, sizey)
        self.rect.left = 0
        self.rect.centery = height // 2
        self.movement = [0, 0]
        self.index = 0
        self.counter = 0
        self.speed = speed
        self.animation_speed = 20
        self.descending = True  # State to indicate descending
        self.carryDino = False  # State to indicate if carrying Dino
        self.ascending = False  # State to indicate ascending
        self.max_carry_duration = 5000  # Thời gian tối đa mà Pteranodon có thể mang Dino (5000ms = 5 giây)
        self.carry_time = 0  # Khởi tạo carry_time

    def draw(self, screen):
        super.draw(screen)
        # screen.blit(self.image, self.rect)
        # if self.carryDino:  # Chỉ hiển thị thanh thời gian khi đang carry
        #     self.draw_time_bar(screen)

    def update(self):
        if self.counter % self.animation_speed == 0:
            self.index = (self.index + 1) % 2
        self.image = self.images[self.index]
        self.counter += 1
        self.rect.x += self.speed

        if self.rect.left > width // 4:  # xuat hien tu giưa bên trái màn hình
            self.rect.left -= self.speed
        # hạ xuống tới độ cao nhất định
        elif self.descending:
            if self.rect.centery < height * 0.65 - 80:  # Move down until near the ground
                self.rect.centery += 2  # Tăng dần tới giữa màn
                self.carryDino = True
                print(self.rect.centery)
            else:
                # Đặt trạng thái carryDino sau khi hạ xuống đủ
                self.carryDino = True
                self.carry_time = pygame.time.get_ticks() + self.max_carry_duration  # Thiết lập carry_time mới
                self.descending = False  # Ngừng hạ xuống và bắt đầu bay lên

        elif self.carryDino:
            if self.rect.centery > height // 1.3:  # Chỉ bay lên nếu vẫn ở dưới giữa màn
                self.rect.centery -= 5  # Bay lên

            self.rect.centerx = 75  # Bay lên
            # Kiểm tra thời gian còn lại khi carry player
            time_left = self.carry_time - pygame.time.get_ticks()
            if time_left <= 0:
                self.fly_away()  # Kết thúc carry và bay đi

        if not self.carryDino:
            self.rect.centerx += self.speed * 10  # Bay sang phải
            if self.rect.left > 800:  # Nếu Pteranodon ra khỏi màn hình
                self.kill()  # Xóa đối tượng

    def fly_away(self):
        self.carry_time = 0
        self.carryDino = False

    def draw_time_bar(self, screen, position):
        """ Vẽ thanh thời gian dựa trên thời gian còn lại """
        current_time = pygame.time.get_ticks()
        time_left = self.carry_time - current_time
        if time_left < 0:
            time_left = 0

    # Tính tỷ lệ thời gian còn lại
        time_ratio = time_left / self.max_carry_duration

    # Kích thước của thanh bar
        bar_width = 200
        bar_height = 10
        current_bar_width = int(bar_width * time_ratio)

    # Màu thanh bar (từ xanh lá sang đỏ khi hết thời gian)
        bar_color = (int((1 - time_ratio) * 255), int(time_ratio * 255), 0)

        pygame.draw.rect(
            # Viền đen
            screen, (0, 0, 0), (position[0]-10, position[1]-8, bar_width+20, 2))
    # Vẽ viền đen
        pygame.draw.rect(
            # Viền đen
            screen, (0, 0, 0), (position[0], position[1], bar_width, bar_height), border_radius=5)
    # Vẽ thanh thời gian
        # Thanh thời gian
        pygame.draw.rect(
            screen, bar_color, (position[0], position[1], current_bar_width, bar_height), border_radius=5)
