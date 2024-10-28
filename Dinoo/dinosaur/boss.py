import pygame
from utils import load_image, load_sprite_sheet
from config import *
from dinosaur.dinosaur import Dinosaur

class Boss(Dinosaur):
    def __init__(self, speed=5, sizex=-1, sizey=-1):
        super().__init__('boss.png', 8, 1, 200, 200)
        self.rect.left = 0
        self.rect.centery = 0
        self.rect.bottom = int(0.98 * height)
        self.index = 0
        self.counter = 0
        self.initial_speed = speed  # Lưu tốc độ ban đầu
        self.speed = speed
        self.is_active = False  # Theo dõi nếu boss đang hoạt động
        self.spawn_time = 0     # Theo dõi thời gian boss xuất hiện
        self.reached_dino = False  # Theo dõi nếu boss đã đạt đến 110px sau dino

    def update(self, dino_position):
        if self.is_active:
            super().update()
            if self.counter % 10 == 0:
                self.index = (self.index + 1) % 8
            self.image = self.images[self.index]
            self.counter += 1

            self.rect.x = dino_position - 110
            if not self.reached_dino:
                # Đặt Boss ngay phía sau Dino và cách Dino 110 pixel
                self.reached_dino = True
                self.spawn_time = pygame.time.get_ticks()  # Bắt đầu thời gian thụt lùi
            else:
                # Giảm tốc độ theo thời gian, tăng độ giảm tốc
                elapsed_time = pygame.time.get_ticks() - self.spawn_time
                if elapsed_time <= 10000:
                    time_ratio = elapsed_time / 10000  # Sử dụng 10 giây làm thời gian chuẩn
                    # Giảm tốc độ nhanh hơn bằng cách tăng hệ số giảm tốc
                    self.speed = self.initial_speed * (1 - 2 * time_ratio)  # Tăng tỷ lệ giảm tốc độ

                    # Nếu tốc độ giảm xuống dưới một ngưỡng nhất định, đảm bảo Boss di chuyển về phía trái
                    if self.speed < -self.initial_speed:
                        self.speed = -self.initial_speed
                else:
                    self.speed = -self.initial_speed  # Đảm bảo tốc độ là âm sau 10 giây

                # Di chuyển Boss theo tốc độ hiện tại
                self.rect.x += self.speed  # Di chuyển Boss về bên trái

                # Kiểm tra nếu Boss đã di chuyển ra khỏi màn hình
                if self.rect.right < 0:  # Nếu Boss đã di chuyển ra khỏi màn hình bên trái
                    self.is_active = False
                    self.rect.x = -200  # Di chuyển Boss ra khỏi màn hình để ẩn
                    self.reached_dino = False  # Reset trạng thái reached_dino
                    print("Boss deactivated", self.is_active)

        else:
            # Kiểm tra nếu 5 giây đã trôi qua để hồi sinh Boss
            if pygame.time.get_ticks() - self.spawn_time > 15000:
                self.spawn()

    def draw(self, screen):
        if self.is_active:  # Chỉ vẽ nếu Boss đang hoạt động
            screen.blit(self.image, self.rect)

    def spawn(self):
        self.is_active = True
        self.spawn_time = pygame.time.get_ticks()  # Ghi lại thời gian hồi sinh
        self.reached_dino = False  # Reset trạng thái reached_dino
        self.speed = self.initial_speed  # Reset tốc độ về ban đầu

    def check_collision(self, dino):
        if self.is_active and self.rect.colliderect(dino.rect):
            return True
        return False
