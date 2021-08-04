from time import sleep
import pygame
from random import randrange
from pathlib import Path

GAME_NAME = 'Snake game by Inomoz'
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600
FONTS_PATH = Path('.') / 'TTF'

BLUE = (33, 150, 243)
RED = (255, 87, 34)
WHITE = (250, 250, 250)
GREEN = (76, 175, 80)

OFFSET_SPEED = 10

# Snake dimensions
SNAKE_WIDTH = 20
SNAKE_HEIGHT = 20

# Snake coordinates
pos_x1 = 300
pos_y1 = 300
offset_y1 = 0
offset_x1 = 0

# Score
score = 0


def initialize_display():
    display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    pygame.display.update()
    pygame.display.set_caption(GAME_NAME)
    return display


def close_game():
    sleep(2)
    pygame.quit()
    quit()


def draw_message(msg, color, offset_y=0):
    message_width, message_height = FONT_STYLE_DEFAULT.size(msg)

    message = FONT_STYLE_DEFAULT.render(msg, False, color)
    display.blit(message, [DISPLAY_WIDTH / 2 - message_width / 2,
                           (DISPLAY_HEIGHT / 2 - message_height / 2) + offset_y])


def range_generate(x, y):
    x_start = int(x - SNAKE_WIDTH + 1)
    x_end = int(x + SNAKE_WIDTH - 1)
    x_range = range(x_start, x_end)

    y_start = int(y - SNAKE_WIDTH + 1)
    y_end = int(y + SNAKE_WIDTH - 1)
    y_range = range(y_start, y_end)

    return x_range, y_range


def draw_snake(snake_list):
    snake_head_x, snake_head_y = snake_list[-1]
    pygame.draw.rect(display, RED, [snake_head_x, snake_head_y, SNAKE_WIDTH, SNAKE_HEIGHT])

    for item_x, item_y in snake_list[:-1]:
        pygame.draw.rect(display, BLUE, [item_x, item_y, SNAKE_WIDTH, SNAKE_HEIGHT])


def draw_food(food_x, food_y):
    pygame.draw.rect(display, GREEN, [food_x, food_y, SNAKE_WIDTH, SNAKE_HEIGHT])


if __name__ == '__main__':
    game_end = False
    game_over = False

    pygame.init()

    move_sound = pygame.mixer.Sound(Path('.') / 'hit.ogg')
    FONT_STYLE_DEFAULT = pygame.font.Font(FONTS_PATH / 'VictorMono-Bold.ttf', 30)
    FONT_STYLE_SCORE = pygame.font.Font(FONTS_PATH / 'VictorMono-Oblique.ttf', 30)

    display = initialize_display()
    clock = pygame.time.Clock()

    food_x = int(randrange(0, DISPLAY_WIDTH - SNAKE_WIDTH) / 10)
    food_y = int(randrange(0, DISPLAY_WIDTH - SNAKE_HEIGHT) / 10)

    snake_list = []
    snake_head = (-1, -1)
    length_of_snake = 1

    while not game_end:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_end = True

            if event.type == pygame.KEYDOWN:
                offset_x1 = 0
                offset_y1 = 0
                game_over = False

                if event.key in (pygame.K_LEFT, pygame.K_a):
                    offset_x1 = -OFFSET_SPEED
                if event.key in (pygame.K_RIGHT, pygame.K_d):
                    offset_x1 = OFFSET_SPEED
                elif event.key in (pygame.K_UP, pygame.K_w):
                    offset_y1 = -OFFSET_SPEED
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    offset_y1 = OFFSET_SPEED

        if game_over:
            draw_message("GAME OVER, press any key to continue...", RED)
            pygame.display.update()
            pos_x1 = 400
            pos_y1 = 300
            length_of_snake = 1
            snake_list = []
            score = 0
            continue

        # Boundaries detection
        if any((pos_x1 >= DISPLAY_WIDTH, pos_x1 < 0,
                pos_y1 >= DISPLAY_HEIGHT, pos_y1 < 0)):
            game_over = True
            continue

        for item_x, item_y in snake_list[:-1]:
            if snake_head == (item_x, item_y):
                game_over = True

        # Calculate coordinates
        pos_x1 += offset_x1
        pos_y1 += offset_y1

        # Canvas fill
        display.fill(WHITE)

        draw_food(food_x, food_y)

        # Draw snake
        snake_head = (pos_x1, pos_y1)
        snake_list.append(snake_head)

        if len(snake_list) > length_of_snake:
            del snake_list[0]

        draw_snake(snake_list)
        food_range_x, food_range_y = range_generate(food_x, food_y)

        if all((pos_x1 in food_range_x, pos_y1 in food_range_y)):
            length_of_snake += 1
            draw_food(food_x, food_y)
            food_x = int(randrange(SNAKE_WIDTH * 2, DISPLAY_WIDTH - SNAKE_WIDTH * 2))
            food_y = int(randrange(SNAKE_HEIGHT * 2, DISPLAY_HEIGHT - SNAKE_HEIGHT * 2))
            score += 1
            move_sound.play()

        value = FONT_STYLE_SCORE.render(f'Your score is {score}', True, BLUE)
        display.blit(value, [0, 0])

        pygame.display.update()
        clock.tick(30)

    close_game()


