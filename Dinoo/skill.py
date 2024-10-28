import pygame
from utils import load_image


class Skill:
    def __init__(self, name, cooldown, duration, effect, icon_skill):
        self.icon, self.icon_rect = load_image(icon_skill, 50, 50, -1)
        self.name = name
        self.cooldown = cooldown
        self.duration = duration
        self.effect = effect
        self.last_used = -cooldown
        self.active = False
        self.start_time = None
        self.cooldown_reduction = 0  # Thời gian giảm hồi chiêu ban đầu là 0

    def use(self, current_time):
        if current_time - self.last_used >= self.cooldown:
            self.last_used = current_time
            self.active = True
            self.start_time = current_time
            self.effect()

    def update(self, current_time):
        if self.active and current_time - self.start_time >= self.duration:
            self.active = False

    def get_cooldown_time_left(self, current_time):
        actual_cooldown = self.cooldown - self.cooldown_reduction
        return max(0, actual_cooldown - (current_time - self.last_used))
    
    def reduce_cooldown(self, amount):
        self.cooldown_reduction = min(self.cooldown, amount)


    def draw_icon(self, screen, position, current_time):
        # Vẽ biểu tượng kỹ năng lên màn hình
        screen.blit(self.icon, position)
        # Vẽ lớp màu xám bán trong suốt nếu kỹ năng đang hồi chiêu
        cooldown_time_left = self.get_cooldown_time_left(current_time)
        if cooldown_time_left > 0:
            percentage_left = cooldown_time_left / (self.cooldown - self.cooldown_reduction)
            overlay_height = int(self.icon_rect.height * percentage_left)
            overlay = pygame.Surface((self.icon_rect.width, overlay_height))  # Tạo một bề mặt mới
            overlay.set_alpha(128)  # Đặt độ trong suốt (0-255)
            overlay.fill((128, 128, 128))  # Đặt màu xám
            screen.blit(overlay, (position[0], position[1] + self.icon_rect.height - overlay_height))  # Vẽ lớp màu xám lên trên biểu tượng từ trên xuống dưới
            # Vẽ thời gian hồi chiêu
        font = pygame.font.Font(None, 24)
        cooldown_time_left = self.get_cooldown_time_left(current_time)
        text_surface = font.render(
            f"{cooldown_time_left:.1f}", True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(
            position[0] + self.icon_rect.width // 2, position[1] + self.icon_rect.height // 2))
        screen.blit(text_surface, text_rect)
