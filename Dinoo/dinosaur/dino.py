import pygame
import random
from skill import Skill
from fireball import Fireball
from dinosaur.dinosaur import *
from dinosaur.triceratops import *  # Import Triceratops class
from dinosaur.pteranodon import *  # Import Triceratops class
from dinosaur.troodon import *  # Import Triceratops class
from dinosaur.boss import *  # Import Triceratops class
from utils import load_sprite_sheet
from config import *


class Dino(Dinosaur):
    def __init__(self,sizex=-1, sizey=-1):
        super().__init__('dino.png', 5, 1, 44, 47)
        self.images1, self.rect1 = load_sprite_sheet(
            'dino_ducking.png', 2, 1, 59, 47, -1)
        self.heart_image, heart_rect = load_image('heart.png', 25, 25, -1)
        self.stand_pos_width = self.rect.width
        self.duck_pos_width = self.rect1.width
        self.invincible = False
        self.invincible_time = 0
        self.lives = 3
        self.spawn_npc = False
        self.spawn_boss = False
        self.being_chase = False
        # Initialize additional properties and skills for Dino
        self.skills = {
            'call_triceratops': Skill('Call Triceratops', 15, 5, self.call_triceratops_effect, 'icon-skill.png'),
            'fly': Skill('Call Ptera', 25, 5, self.fly_effect, 'icon-skill-ptera.png'),
            'fire': Skill('Fire Ball', 10, 5, self.fire, 'icon-skill-fireball.png')
        }
        self.triceratops_group = pygame.sprite.Group()
        self.pteranodon_group = pygame.sprite.Group()
        self.fireball_group = pygame.sprite.Group()
        self.troodon_group = pygame.sprite.Group()
        self.boss_group = pygame.sprite.Group()

    def call_triceratops_effect(self):
        self.triceratops = Triceratops()
        self.triceratops.left = width
        self.triceratops_group.add(self.triceratops)

    def fly_effect(self):
       # Add logic to handle flying
        self.pteranodon = Pteranodon()
        self.pteranodon.left = width
        self.pteranodon.rect.centery = height // 2
        self.pteranodon.carryDino = True
        self.pteranodon_group.add(self.pteranodon)  # Add to the group

    def fire(self):
        fireball = Fireball()
        fireball.rect.centerx = self.rect.centerx
        fireball.rect.centery = self.rect.centery
        self.fireball_group.add(fireball)

    def has_spawn_boss(self):
        self.boss = Boss()
        self.spawn_boss = True
        self.boss.left = width
        self.boss.spawn()
        self.boss_group.add(self.boss)
        self.being_chase = True
        # Kiểm tra va chạm với Boss
        if pygame.sprite.collide_rect(self, self.boss):
            self.lives -= 1  # Trừ 1 mạng
        # self.reset_position()

        print(f"Dino hit by Boss! Lives left: {self.lives}")

    def reset_position(self):
        self.rect.x = self.stand_pos_width  # Đặt lại vị trí về vị trí ban đầu

    def has_spawn_npc(self):
        self.troodon = Troodon()  # Vị trí xuất hiện của NPC
        self.spawn_npc = True
        self.troodon.left = width
        self.troodon_group.add(self.troodon)

    def check_egg_collision(self):
        for troodon in self.troodon_group:
            eggs = pygame.sprite.spritecollide(self, troodon.egg_group, True)
            for egg in eggs:
                self.handle_egg_reward()
                egg.kill()

    def handle_egg_reward(self):
        reward = random.choice(['invincible', 'reduce_skill_cooldown', 'add_lives'])
        if reward == 'invincible':
            # Kích hoạt trạng thái bất tử trong 5 giây
            self.make_invincible(5000)
            print("Ban dang bat tu")
        elif reward == 'reduce_skill_cooldown':
            self.reduce_skill_cooldown(5)
        elif reward == 'add_lives':
            self.lives += 1
            print("ban dc them 1 mang: ", {self.lives})

    def reduce_skill_cooldown(self, amount):
        for skill in self.skills.values():
            skill.reduce_cooldown(amount)

    def checkbounds(self):
        if self.rect.bottom > int(0.98 * height):
            self.rect.bottom = int(0.98 * height)
            self.isJumping = False

    def update(self):
        current_time = pygame.time.get_ticks() / 1000

        for skill in self.skills.values():
            skill.update(current_time)

        if self.isJumping:
            self.movement[1] = self.movement[1] + gravity

        if self.isJumping:
            self.index = 0
        elif self.isBlinking:
            if self.index == 0:
                if self.counter % 400 == 399:
                    self.index = (self.index + 1) % 2
            else:
                if self.counter % 20 == 19:
                    self.index = (self.index + 1) % 2
        elif self.isDucking:
            if self.counter % 5 == 0:
                self.index = (self.index + 1) % 2
        else:
            if self.counter % 5 == 0:
                self.index = (self.index + 1) % 2 + 2

        if self.isDead:
            self.index = 4

        if not self.isDucking:
            self.image = self.images[self.index]
            self.rect.width = self.stand_pos_width
        else:
            self.image = self.images1[self.index % 2]
            self.rect.width = self.duck_pos_width

        self.rect = self.rect.move(self.movement)
        self.checkbounds()

        # Triceratops
        self.triceratops_group.update()  # Update all triceratops

        # Pteranodon
        self.pteranodon_group.update()  # Update all triceratops
        for pteranodons in self.pteranodon_group:
            if not pteranodons.alive():
                print("pteranodons no longer exists")
                pteranodons.kill()
            if pteranodons.carryDino:
                # Gắp Dino theo vị trí của Ptera
                self.rect.centerx = pteranodons.rect.centerx
                self.rect.centery = pteranodons.rect.centery + 45
                self.pteranodon.carryDino = True
                if self.being_chase:
                    self.rect.x += 80  # Di chuyển Dino lên 100 pixel
                    pteranodons.rect.centerx = self.rect.x
            if current_time * 1000 >= self.pteranodon.carry_time:
                # Set Dino's position to ground level when dropped
                self.rect.centery = height * 0.94  # Set Dino to ground level
                self.pteranodon.carryDino = False
                self.land()

        if not self.isDead and self.counter % 7 == 6 and not self.isBlinking:
            self.score += 1
            if self.score % 100 == 0 and self.score != 0:
                self.has_spawn_npc()
            if self.score == 50:
                self.has_spawn_boss()
                if self.being_chase:
                    self.rect.x += 100
                # self.reset_position()  # Reset vị trí Dino hoặc bất kỳ hành động nào khác khi va chạm
                if pygame.mixer.get_init() is not None:
                    checkPoint_sound.play()
        self.counter = (self.counter + 1)
        # Kiểm tra trạng thái bất tử
        if self.invincible and current_time * 1000 > self.invincible_time:
            self.invincible = False
        # Fireball
        self.fireball_group.update()
        # Troodon
        self.troodon_group.update()
        for troodon in self.troodon_group:
            if not troodon.alive():
                print("Troodon no longer exists")
                troodon.kill()
        # Receive egg
        self.check_egg_collision()
        self.boss_group.update(self.stand_pos_width)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        if self.invincible:
            current_time = pygame.time.get_ticks()
            time_left = self.invincible_time - current_time
        # Hiệu ứng nhấp nháy khi còn ít thời gian
            if time_left <= 2500:  # Nhấp nháy khi còn 2.5 giây
                # Nhấp nháy nhanh
                alpha = 150 if (current_time // 100) % 2 == 0 else 0
            else:
                alpha = 128  # Màu đỏ nhạt khi bất tử
        # Tạo bản sao của hình ảnh
            red_surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        # Bo tròn các góc
            pygame.draw.rect(red_surface, (255, 0, 0, alpha), (0, 0,
                             self.rect.width, self.rect.height), border_radius=10)
            screen.blit(red_surface, self.rect)
        self.triceratops_group.draw(screen)  # Draw all triceratops
        self.pteranodon_group.draw(screen)  # Draw all pteranodon
        self.draw_skills(screen)  # Vẽ các kỹ năng
        for pteranodons in self.pteranodon_group:
            if pteranodons.carryDino:
                pteranodons.draw_time_bar(screen, (width/3, height/5))
        for i in range(self.lives):
            # Tăng khoảng cách giữa các trái tim
            screen.blit(self.heart_image, (10 + i * 30, 20))

        self.fireball_group.draw(screen)
        self.troodon_group.draw(screen)
        self.troodon_group.draw(screen)
        for troodons in self.troodon_group:
            troodons.draw(screen)  # Vẽ Troodon và các trứng của nó
        self.boss_group.draw(screen)

    def draw_skills(self, screen):
        current_time = pygame.time.get_ticks() / 1000
        for index, skill in enumerate(self.skills.values()):
            x = width - 50 * (index + 1)
            y = 10
            skill.draw_icon(screen, (x, y), current_time)

    def handle_event_pteranodon(self, event):
        # Gọi hàm ptera_handle_event của Pteranodon
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.pteranodon.rect.centery -= self.pteranodon.speed * 5
        if keys[pygame.K_s]:
            self.pteranodon.rect.centery += self.pteranodon.speed * 5

    def land(self):
        # Khi player hạ xuống thì Pteranodon bay đi
        if not any(pteranodon.carryDino for pteranodon in self.pteranodon_group):
            self.pteranodon.fly_away()  # Bắt đầu bay đi
            self.make_invincible(5000)  # Kích hoạt trạng thái bất tử
        # Trạng thái bất tử

    def make_invincible(self, duration):
        """ Đặt trạng thái invincible cho dino """
        if not any(pteranodon.carryDino for pteranodon in self.pteranodon_group):
            self.invincible = True
            self.invincible_time = pygame.time.get_ticks() + duration

    def handle_event(self, event):
        current_time = pygame.time.get_ticks() / 1000
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_3:
                self.skills['call_triceratops'].use(current_time)
            if event.key == pygame.K_2:
                self.skills['fly'].use(current_time)
            if event.key == pygame.K_1:
                self.skills['fire'].use(current_time)
            if event.key == pygame.K_DOWN:
                if not self.isJumping and not self.isDead:
                    self.isDucking = True
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                if self.rect.bottom == int(0.98 * height):
                    self.isJumping = True
                    if pygame.mixer.get_init() is not None:
                        jump_sound.play()
                    self.movement[1] = -1 * self.jumpSpeed

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                self.isDucking = False
