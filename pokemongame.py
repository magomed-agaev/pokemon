# import pygame_menu
# import pygame

# pygame.init()
# font = pygame.font.Font(None, 36)
# text_surface = font.render("Welcome to Pokemon Game!",
#                            True, (255, 255, 255), (0, 0, 0))
# screen = pygame.display.set_mode((1000, 800))

# screen.blit(text_surface, (50, 50))

# pygame.display.flip()
# font = pygame.font.Font('freesansbold.ttf', 32)
# font.set_bold(True)
# font.set_italic(True)
# text_surface.set_alpha(128)
# new_surface = pygame.transform.scale(text_surface, (300, 70))
# # rotated_surface = pygame.transform.rotate(text_surface, 45)
# text_rect = text_surface.get_rect()
# print(text_rect.width)
# print(text_rect.height)
# text_rect.topleft = (50, 50)
# screen.blit(text_surface, text_rect)
# text_rect.center = (screen.get_width() / 2, screen.get_height() / 2)
# screen.blit(text_surface, text_rect)
# text_surface = font.render("Welcome to Pokemon Game",
#                            True, (255, 0, 0), (0, 0, 0))
# # Compteur
# for i in range(5, -1, -1):
#     text_surface = font.render(
#         f"Get Ready! {i}", True, (255, 255, 255), (0, 0, 0))
#     screen.blit(text_surface, (60, 60))
#     pygame.display.flip()
#     pygame.time.wait(1000)

# surface = pygame.display.set_mode((1000, 800))

# menu = pygame_menu.Menu('Pokemon', 1000, 800,
#                         theme=pygame_menu.themes.THEME_ORANGE)

# surface = pygame.display.set_mode((1000, 800))

# # Create a font object
# font = pygame.font.SysFont('Arial', 36)

# # Render the text
# text = font.render('Hello, World!', True, (255, 255, 255))

# # Blit the text to the screen
# surface.blit(text, (100, 100))

# # Update the display
# pygame.display.update()

# menu.add.button('Play')
# menu.add.button('Pokemons')
# menu.add.button('Quit', pygame_menu.events.EXIT)

# menu.mainloop(surface)

# pygame.quit()
import pygame
import sys
from Button import Button
from pygame import mixer

pygame.init()

mixer.init()
mixer.music.load("musicpoke.mp3")
mixer.music.play(-1)

# LES DIMENSIONS DE L'ECRAN DU MENU

SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")

# AJOUT DU FOND D'ECRAN
BG = pygame.image.load("Pokemons.jpg")


def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("PokemonSolid.ttf", size)


def play():
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        PLAY_TEXT = get_font(45).render(
            "This is the PLAY screen.", True, "Yellow")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        PLAY_BACK = Button(image=None, pos=(640, 460), text_input="BACK", font=get_font(
            75), base_color="White", hovering_color="Green")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()

        pygame.display.update()


def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        OPTIONS_TEXT = get_font(45).render(
            "This is the OPTIONS screen.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(640, 460), text_input="BACK", font=get_font(
            75), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()


def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("Pokemon", True, "Yellow")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("Playrect.png"), pos=(
            640, 250), text_input="NEW GAME", font=get_font(65), base_color="Black", hovering_color="Yellow")
        CONTINUE_BUTTON = Button(image=pygame.image.load("Optionsrect.png"), pos=(
            640, 375), text_input="CONTINUE GAME", font=get_font(65), base_color="Black", hovering_color="Yellow")
        POKEMONS_BUTTON = Button(image=pygame.image.load("Optionsrect.png"), pos=(
            640, 500), text_input="POKEMONS", font=get_font(65), base_color="Black", hovering_color="Yellow")
        QUIT_BUTTON = Button(image=pygame.image.load("Quitrect.png"), pos=(
            640, 650), text_input="QUIT", font=get_font(65), base_color="Black", hovering_color="Yellow")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, CONTINUE_BUTTON, POKEMONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if CONTINUE_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pass
                if POKEMONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


main_menu()
