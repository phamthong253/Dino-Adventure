import pygame
import sys
import random
# from dinosaur.pteranodon import Pteranodon
from dinosaur.dino import Dino
from cactus import Cactus
from ptera import Ptera
from cloud import Cloud
from scoreboard import Scoreboard
from ground import Ground
from effect import shake_screen
from utils import load_image, load_sprite_sheet, disp_gameOver_msg, extractDigits
from config import *

gamePaused = False
def gameplay(dino):
    global high_score, gamePaused
    gamespeed = 4
    startMenu = False
    gameOver = False
    gameQuit = False
    playerDino = dino
    new_ground = Ground(-1 * gamespeed)
    scb = Scoreboard(width * 0.78)
    highsc = Scoreboard(width * 0.78)
    counter = 0

    cacti = pygame.sprite.Group()
    pteras = pygame.sprite.Group()
    clouds = pygame.sprite.Group()
    last_obstacle = pygame.sprite.Group()
    background_music.play(-1)

    Cactus.containers = cacti
    Ptera.containers = pteras
    Cloud.containers = clouds

    retbutton_image, retbutton_rect = load_image(
        'replay_button.png', 35, 31, -1)
    gameover_image, gameover_rect = load_image('game_over.png', 190, 11, -1)

    temp_images, temp_rect = load_sprite_sheet(
        'numbers.png', 12, 1, 11, int(11 * 6 / 5), -1)
    HI_image = pygame.Surface((22, int(11 * 6 / 5)))
    HI_rect = HI_image.get_rect()
    HI_image.fill(background_col)
    HI_image.blit(temp_images[10], temp_rect)
    temp_rect.left += temp_rect.width
    HI_image.blit(temp_images[11], temp_rect)
    HI_rect.top = height * 0.1
    HI_rect.left = width * 0.73

    while not gameQuit:
        while startMenu:
            pass
        while not gameOver:
            if pygame.display.get_surface() is None:
                print("Couldn't load display surface")
                gameQuit = True
                gameOver = True
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        gameQuit = True
                        gameOver = True
                    playerDino.handle_event(event)
                    playerDino.handle_event_pteranodon(event)

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:  # Nhấn P hoặc ESC để tạm dừng
                            gamePaused = not gamePaused  # Đảo trạng thái pause
                            if gamePaused:
                                from interfaces.pause_menu import show_pause_menu
                                show_pause_menu()  # Hiển thị menu pause
                                continue  # Bỏ qua phần game chính nếu game đang bị tạm dừng
            for c in cacti:
                c.movement[0] = -1 * gamespeed
                if pygame.sprite.collide_mask(playerDino, c):
                    if playerDino.invincible:
                        shake_screen(screen, duration=0.3, magnitude=2)
                        playerDino.isDead = False
                        c.kill()
                    else:
                        playerDino.lives -= 1  # Giảm mạng khi va chạm
                        # Gọi hàm để kích hoạt trạng thái bất tử
                        playerDino.make_invincible(5000)
                        if playerDino.lives <= 0:
                            playerDino.isDead = True
                            playerDino.score = 0
                            if pygame.mixer.get_init() is not None:
                                die_sound.play()  # Phát âm thanh khi chết

            for p in pteras:
                p.movement[0] = -1 * gamespeed
                if pygame.sprite.collide_mask(playerDino, p):
                    if playerDino.invincible:
                        shake_screen(screen, duration=0.3, magnitude=2)
                        playerDino.isDead = False
                        p.kill()
                    else:
                        playerDino.lives -= 1  # Giảm mạng khi va chạm
                        # Gọi hàm để kích hoạt trạng thái bất tử
                        playerDino.make_invincible(5000)
                        if playerDino.lives <= 0:
                            playerDino.isDead = True
                            if pygame.mixer.get_init() is not None:
                                die_sound.play()  # Phát âm thanh khi chết

            # Ensure triceratops exists before checking collisions
            # Skill
            if playerDino.triceratops_group:
                playerDino.triceratops_group.update()  # Call update for Triceratops group
                for triceratops in playerDino.triceratops_group:
                    for c in cacti:
                        if pygame.sprite.collide_mask(triceratops, c):
                            shake_screen(screen, duration=0.3, magnitude=2)
                            c.kill()
                            jump_sound.play()

                    for p in pteras:
                        if pygame.sprite.collide_mask(triceratops, p):
                            p.kill()
            # Pteranodon
            if playerDino.pteranodon_group:
                playerDino.pteranodon_group.update()
                for pteranodons in playerDino.pteranodon_group:
                    for c in cacti:
                        if pygame.sprite.collide_mask(pteranodons, c):
                            shake_screen(screen, duration=0.3, magnitude=2)
                            c.kill()
                            jump_sound.play()

                    for p in pteras:
                        if pygame.sprite.collide_mask(pteranodons, p):
                            shake_screen(screen, duration=0.3, magnitude=2)
                            p.kill()
                            jump_sound.play()
            # Fireball
            if playerDino.fireball_group:
                playerDino.fireball_group.update()
                for fireballs in playerDino.fireball_group:
                    for c in cacti:
                        if pygame.sprite.collide_mask(fireballs, c):
                            jump_sound.play()
                            c.kill()
                    for p in pteras:
                        if pygame.sprite.collide_mask(fireballs, p):
                            p.kill()
                            jump_sound.play()

            if len(cacti) < 4:
                if len(cacti) == 0:
                    last_obstacle.empty()
                    last_obstacle.add(Cactus(gamespeed, 40, 40))
                else:
                    for l in last_obstacle:
                        if l.rect.right < width * 0.7 and random.randrange(0, 50) == 10:
                            last_obstacle.empty()
                            last_obstacle.add(Cactus(gamespeed, 40, 40))

            if len(pteras) == 0 and random.randrange(0, 50) == 10 and counter > 500:
                for l in last_obstacle:
                    if l.rect.right < width * 0.8:
                        last_obstacle.empty()
                        last_obstacle.add(Ptera(gamespeed, 56, 50))

            if len(clouds) < 5 and random.randrange(0, 300) == 10:
                Cloud(width, random.randrange(int(height / 5), int(height / 2)))

            playerDino.update()
            cacti.update()
            pteras.update()
            clouds.update()
            new_ground.update()
            scb.update(playerDino.score, background_col)
            highsc.update(high_score, background_col)

            if pygame.display.get_surface() is not None:
                screen.fill(background_col)
                new_ground.draw(screen)
                clouds.draw(screen)
                scb.draw(screen)
                if high_score != 0:
                    highsc.draw(screen)
                    screen.blit(HI_image, HI_rect)
                cacti.draw(screen)
                pteras.draw(screen)
                playerDino.draw(screen)

                pygame.display.update()
            clock.tick(FPS)

            if playerDino.isDead:
                gameOver = True
                if playerDino.score > high_score:
                    high_score = playerDino.score
                background_music.stop()

            if counter % 700 == 699:
                new_ground.speed -= 1
                gamespeed += 1

            counter = (counter + 1)

        if gameQuit:
            break

        while gameOver:
            if pygame.display.get_surface() is None:
                print("Couldn't load display surface")
                gameQuit = True
                gameOver = False
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        gameQuit = True
                        gameOver = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            gameQuit = True
                            gameOver = False
                            background_music.play(-1)
                        if event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                            gameOver = False
                            start_game_with_skin(
                                skins[selected_skin]["ingame"], skins[selected_skin]["ingame_ducking"])
            highsc.update(high_score, background_col)
            if pygame.display.get_surface() is not None:
                disp_gameOver_msg(
                    retbutton_image, gameover_image, screen, width, height)
                if high_score != 0:
                    highsc.draw(screen)
                    screen.blit(HI_image, HI_rect)
                pygame.display.update()
            clock.tick(FPS)

    pygame.quit()
    quit()

def start_game_with_skin(skin_name, skin_name_ducking):
    dino = Dino(44,47)
    dino.images, dino.rect = load_sprite_sheet(skin_name, 5, 1, 44, 47, -1)
    dino.images1, dino.rect1 = load_sprite_sheet(skin_name_ducking, 2, 1, 59, 47, -1)
    dino.rect.left = width / 15
    dino.rect.bottom = int(height * 0.98)
    gameplay(dino)