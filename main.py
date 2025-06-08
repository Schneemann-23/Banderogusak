import random
import os
import sys

import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

# Функция для правильного пути к ресурсам (работает локально и в вебе)
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Инициализация Pygame
pygame.init()

FPS = pygame.time.Clock()

# Размеры экрана
HEIGHT = 800
WIDTH = 1200

FONT = pygame.font.SysFont('Verdana', 20)

# Цвета
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_GREEN = (0, 255, 0)

# Создание окна игры
main_display = pygame.display.set_mode((WIDTH, HEIGHT))

# Загрузка и масштабирование фона
try:
    bg = pygame.transform.scale(pygame.image.load(resource_path('background.png')), (WIDTH, HEIGHT))
except Exception as e:
    print(f"Error loading background: {e}")
    bg = pygame.Surface((WIDTH, HEIGHT))
bg_X1 = 0
bg_X2 = bg.get_width()
bg_move = 3

# Путь к папке с изображениями игрока
IMAGE_PATH = resource_path("Goose")

# Список файлов в папке, сортируем для стабильного порядка
try:
    PLAYER_IMAGES = sorted(os.listdir(IMAGE_PATH))
except Exception as e:
    print(f"Error listing player images: {e}")
    PLAYER_IMAGES = []

# Загрузка первого изображения игрока
try:
    player = pygame.image.load(os.path.join(IMAGE_PATH, PLAYER_IMAGES[0])).convert_alpha()
except Exception as e:
    print(f"Error loading player image: {e}")
    player = pygame.Surface((20, 20))
    player.fill(COLOR_BLACK)

player_rect = player.get_rect()
player_move_down = [0, 5]
player_move_up = [0, -5]
player_move_left = [-5, 0]
player_move_right = [5, 0]
player_rect.x = 100  
player_rect.y = 200  

def create_bonus():
    bonus_size = (40, 40)
    try:
        bonus = pygame.image.load(resource_path('bonus.png')).convert_alpha()
    except Exception as e:
        print(f"Error loading bonus image: {e}")
        bonus = pygame.Surface(bonus_size)
        bonus.fill(COLOR_GREEN)
    bonus_rect = pygame.Rect(random.randint(100, WIDTH), 0, *bonus_size)
    bonus_move = [0, random.randint(4, 8)]
    return [bonus, bonus_rect, bonus_move]

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 1200)

def create_enemy():
    enemy_size = (30, 30)
    try:
        enemy = pygame.image.load(resource_path('enemy.png')).convert_alpha()
    except Exception as e:
        print(f"Error loading enemy image: {e}")
        enemy = pygame.Surface(enemy_size)
        enemy.fill(COLOR_BLUE)
    enemy_rect = pygame.Rect(WIDTH, random.randint(100, 700), *enemy_size)
    enemy_move = [random.randint(-8, -4), 0]
    return [enemy, enemy_rect, enemy_move]

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)

CHANGE_IMAGE = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMAGE, 200)

enemies = []
bonuses = []

score = 0
image_index = 0
playing = True

while playing:
    FPS.tick(240)

    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())
        if event.type == CHANGE_IMAGE:
            if PLAYER_IMAGES:
                try:
                    player = pygame.image.load(os.path.join(IMAGE_PATH, PLAYER_IMAGES[image_index])).convert_alpha()
                except Exception as e:
                    print(f"Error loading player image at index {image_index}: {e}")
                image_index += 1
                if image_index >= len(PLAYER_IMAGES):
                    image_index = 0

    # Движение фона
    bg_X1 -= bg_move
    bg_X2 -= bg_move

    if bg_X1 < -bg.get_width():
        bg_X1 = bg.get_width()

    if bg_X2 < -bg.get_width():
        bg_X2 = bg.get_width()

    main_display.blit(bg, (bg_X1, 0))
    main_display.blit(bg, (bg_X2, 0))

    keys = pygame.key.get_pressed()

    if keys[K_DOWN] and player_rect.bottom < HEIGHT:
        player_rect = player_rect.move(player_move_down)

    if keys[K_UP] and player_rect.top > 0:
        player_rect = player_rect.move(player_move_up)

    if keys[K_LEFT] and player_rect.left > 0:
        player_rect = player_rect.move(player_move_left)

    if keys[K_RIGHT] and player_rect.right < WIDTH:
        player_rect = player_rect.move(player_move_right)

    for enemy in enemies:
        enemy[1] = enemy[1].move(enemy[2])
        main_display.blit(enemy[0], enemy[1])

        if player_rect.colliderect(enemy[1]):
            playing = False

    for bonus in bonuses:
        bonus[1] = bonus[1].move(bonus[2])
        main_display.blit(bonus[0], bonus[1])

        if player_rect.colliderect(bonus[1]):
            score += 1
            bonuses.pop(bonuses.index(bonus))
      
    main_display.blit(FONT.render(str(score), True, COLOR_BLACK), (WIDTH-50, 20))
    main_display.blit(player, player_rect)

    pygame.display.flip()

    for enemy in enemies:
        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))

    for bonus in bonuses:
        if bonus[1].bottom > HEIGHT:
            bonuses.pop(bonuses.index(bonus))