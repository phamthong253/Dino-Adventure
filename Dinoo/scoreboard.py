import os
from utils import load_sprite_sheet, extractDigits
import pygame

class Scoreboard:
    def __init__(self, x=-1, y=-1, width=800, height=600):
        self.score = 0
        self.high_score = self.load_high_score()  # Tải điểm cao nhất từ file
        self.tempimages, self.temprect = load_sprite_sheet('numbers.png', 12, 1, 11, int(11 * 6 / 5), -1)
        self.image = pygame.Surface((220, int(11 * 6 / 5)))  # Mở rộng bề rộng để hiển thị cả hai điểm
        self.rect = self.image.get_rect()
        if x == -1:
            self.rect.left = width * 0.85  # Dịch sang phải theo yêu cầu
        else:
            self.rect.left = x
        if y == -1:
            self.rect.top = height * 0.1
        else:
            self.rect.top = y

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self, score, background_col):
        self.score = score
        self.image.fill(background_col)

        # Cập nhật điểm cao nhất nếu cần
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()  # Lưu điểm cao nhất vào file

        # Chuyển đổi cả điểm hiện tại và điểm cao nhất thành danh sách chữ số
        score_digits = extractDigits(self.score)
        high_score_digits = extractDigits(self.high_score)

        # Đảm bảo cả hai điểm đều có tối đa 5 chữ số
        score_digits = [0] * (5 - len(score_digits)) + score_digits  # Thêm số 0 vào đầu
        high_score_digits = [0] * (5 - len(high_score_digits)) + high_score_digits  # Thêm số 0 vào đầu
        margin = 10
        # Vẽ điểm cao nhất
        offset_x = margin  # Bắt đầu từ vị trí này để tạo khoảng cách
        for hs in high_score_digits:
            self.image.blit(self.tempimages[hs], (offset_x + 15, 0))
            offset_x += self.temprect.width

        # Thêm khoảng cách giữa điểm cao nhất và điểm hiện tại
        offset_x += 25 + margin  # Tăng khoảng cách thêm một chút

        # Vẽ điểm hiện tại
        for s in score_digits:
            self.image.blit(self.tempimages[s], (offset_x + 15, 0))
            offset_x += self.temprect.width

    def load_high_score(self):
        # Đọc điểm cao nhất từ file
        if os.path.exists('high_score.txt'):
            with open('high_score.txt', 'r') as f:
                try:
                    return int(f.read().strip())
                except ValueError:
                    return 0  # Nếu file có lỗi, trả về 0
        return 0  # Nếu file không tồn tại, trả về 0

    def save_high_score(self):
        # Lưu điểm cao nhất vào file
        with open('high_score.txt', 'w') as f:
            f.write(str(self.high_score))
