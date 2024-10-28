from utils import load_image
import pygame


class Button():
    def __init__(self, image_file, pos, text_input, font, base_color, hovering_color, border_color=(0, 0, 0)):
        self.image, self.rect = load_image(image_file, 70, 50, None)
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_surface = self.font.render(self.text_input, True, self.base_color)
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        self.border_color = border_color  # Add border color

    def update(self, screen):
        # Draw the border
        border_rect = self.rect.inflate(3, 3)  # Inflate to create border space
        pygame.draw.rect(screen, self.border_color, border_rect)  # Draw the border
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text_surface, self.text_rect)
    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(
                self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)
