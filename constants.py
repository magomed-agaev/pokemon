import pygame


# create the game window
game_width = 800
game_height = 600
size = (game_width, game_height)
game = pygame.display.set_mode(size)
pygame.display.set_caption('Pokemon Battle')

# define colors
black = (0, 0, 0)
gold = (218, 165, 32)
grey = (200, 200, 200)
green = (0, 200, 0)
red = (200, 0, 0)
white = (255, 255, 255)


def display_message(message):
    # draw a white box with black border
    pygame.draw.rect(game, white, (20, 450, 680, 140))
    pygame.draw.rect(game, black, (20, 450, 680, 140), 3)

    # display the message
    font = pygame.font.Font(pygame.font.get_default_font(), 20)
    text = font.render(message, True, black)
    text_rect = text.get_rect()
    text_rect.x = 70
    text_rect.y = 500
    game.blit(text, text_rect)

    pygame.display.update()
