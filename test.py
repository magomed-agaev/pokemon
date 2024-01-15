import pygame
import sys

pygame.init()

screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("My Game")

rect_color = pygame.Color("Yellow")

rect_width, rect_height = 100, 200
rect_x, rect_y = 350, 200
STEP = 10

while True:
    for event in pygame.event.get():
        print(event)
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                rect_y -= STEP
            if event.key == pygame.K_DOWN:
                rect_y += STEP
            if event.key == pygame.K_LEFT:
                rect_x -= STEP
            if event.key == pygame.K_RIGHT:
                rect_x += STEP

    screen.fill((32, 52, 71))
    pygame.draw.rect(screen, rect_color,
                     (rect_x, rect_y, rect_width, rect_height))
    pygame.display.update()
