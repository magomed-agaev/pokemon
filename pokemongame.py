import pygame
import sys
from Button import Button
from pygame import mixer
from pokedex.pokedex import Pokedex

SCREEN = pygame.display.set_mode((1200, 700))


def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("PokemonSolid.ttf", size)


def play():
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        PLAY_TEXT = get_font(45).render(
            "This is the New Game screen.", True, "Yellow")
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


def main_menu():
    pygame.init()

    mixer.init()
    mixer.music.load("musicpoke.mp3")
    mixer.music.play(-1)

    # LES DIMENSIONS DE L'ECRAN DU MENU
    SCREEN = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Menu")

    # AJOUT DU FOND D'ECRAN
    BG = pygame.image.load("Pokemons.jpg")

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
                    Pokedex.play()

                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


if __name__ == "__main__":
    main_menu()
