
from constants import *
from pygame.locals import *
import time
import random
from pokémon import Pokemon
from pokedex.pokedex import Pokedex
from pygame import mixer


def battle():
    pygame.init()
    SCREEN = pygame.display.set_mode((800, 600))

    # Chargement de l'image de fond
    background_image = pygame.image.load("grass.jpg")
    background_image = pygame.transform.scale(
        background_image, (800, 600))  # Adjust the size

    # Affichage de l'image de fond
    game.blit(background_image, (0, 0))

    # Initialisation du module audio de Pygame
    mixer.init()
    mixer.music.load("Battle.mp3")
    mixer.music.play(-1)

    # Fonction pour créer un bouton

    def create_button(width, height, left, top, text_cx, text_cy, label):
        # position of the mouse cursor
        mouse_cursor = pygame.mouse.get_pos()

        button = Rect(left, top, width, height)

        # Mettre en surbrillance le bouton si la souris pointe dessus
        if button.collidepoint(mouse_cursor):
            pygame.draw.rect(game, gold, button)
        else:
            pygame.draw.rect(game, white, button)

        # Ajouter le libellé au bouton
        font = pygame.font.Font(pygame.font.get_default_font(), 16)
        text = font.render(f'{label}', True, black)
        text_rect = text.get_rect(center=(text_cx, text_cy))
        game.blit(text, text_rect)

        return button

    # Création des pokémons de départ
    level = 30
    bulbasaur = Pokemon('Bulbasaur', level, 0, 0)
    charmander = Pokemon('Charmander', level, 200, 0)
    squirtle = Pokemon('Squirtle', level, 400, 0)
    psyduck = Pokemon('Psyduck', level, 600, 0)
    pikachu = Pokemon('Pikachu', level, 0, 200)
    jigglypuff = Pokemon('Jigglypuff', level, 200, 200)
    chikorita = Pokemon('Chikorita', level, 400, 200)
    shuppet = Pokemon('Shuppet', level, 600, 200)
    cyndaquil = Pokemon('Cyndaquil', level, 0, 400)
    gengar = Pokemon('Gengar', level, 200, 400)
    totodile = Pokemon('Totodile', level, 400, 400)
    zapdos = Pokemon('Zapdos', level, 600, 400)

    pokemons = [bulbasaur, charmander, squirtle, pikachu,
                jigglypuff, chikorita, cyndaquil, gengar, totodile, zapdos, shuppet, psyduck]

    # Pokémons sélectionnés par le joueur et son rival
    player_pokemon = None
    rival_pokemon = None

    # Boucle de jeu
    game_status = 'select pokemon'
    while game_status != 'quit':

        for event in pygame.event.get():
            if event.type == QUIT:
                game_status = 'quit'

            # Détection d'une pression de touche
            if event.type == KEYDOWN:

                # Rejouer
                if event.key == K_y:
                    # Réinitialiser les pokémons
                    bulbasaur = Pokemon('Bulbasaur', level, 0, 0)
                    charmander = Pokemon('Charmander', level, 200, 0)
                    squirtle = Pokemon('Squirtle', level, 400, 0)
                    pikachu = Pokemon('Pikachu', level, 0, 200)
                    jigglypuff = Pokemon('Jigglypuff', level, 200, 200)
                    chikorita = Pokemon('Chikorita', level, 400, 200)
                    cyndaquil = Pokemon('Cyndaquil', level, 0, 400)
                    gengar = Pokemon('Gengar', level, 200, 400)
                    totodile = Pokemon('Totodile', level, 400, 400)
                    zapdos = Pokemon('', level, 600, 400)
                    shuppet = Pokemon('Shuppet', level, 600, 200)
                    psyduck = Pokemon('Psyduck', level, 600, 0)

                    pokemons = [bulbasaur, charmander, squirtle, pikachu,
                                jigglypuff, chikorita, cyndaquil, gengar, totodile, zapdos, shuppet, psyduck]
                    game_status = 'select pokemon'

                # Quitter
                elif event.key == K_n:
                    game_status = 'quit'

            # Détection d'un clic de souris
            if event.type == MOUSEBUTTONDOWN:

                # Coordonnées du clic de souris
                mouse_click = event.pos

                # Pour sélectionner un Pokémon
                if game_status == 'select pokemon':

                    # Vérifier quel Pokémon a été cliqué
                    for i in range(len(pokemons)):

                        if pokemons[i].get_rect().collidepoint(mouse_click):
                            # Attribuer le Pokémon du joueur et de son rival
                            player_pokemon = pokemons[i]
                            rival_pokemon = pokemons[(i + 1) % len(pokemons)]

                            # Abaisser le niveau du Pokémon rival pour faciliter le combat
                            rival_pokemon.level = int(
                                rival_pokemon.level * .75)

                            # Définir les coordonnées des barres de points de vie
                            player_pokemon.hp_x = 450
                            player_pokemon.hp_y = 350
                            rival_pokemon.hp_x = 80
                            rival_pokemon.hp_y = 90

                            game_status = 'prebattle'

                # Pour choisir entre attaquer ou utiliser une potion
                elif game_status == 'player turn':

                    if pokedex_button.collidepoint(mouse_click):
                        Pokedex.play()
                        SCREEN = pygame.display.set_mode((800, 600))

                    if main_menu_button.collidepoint(mouse_click):
                        game_status = 'quit'

                    # Vérifier si le bouton Attaquer a été cliqué
                    if fight_button.collidepoint(mouse_click):

                        game_status = 'player move'

                    # Vérifier si le bouton Potion a été cliqué
                    if potion_button.collidepoint(mouse_click):

                        # Forcer à attaquer s'il n'y a plus de potions
                        if player_pokemon.num_potions == 0:
                            display_message('No more potions left')
                            time.sleep(2)
                            game_status = 'player move'
                        else:
                            player_pokemon.use_potion()
                            display_message(
                                f'{player_pokemon.name} used potion')
                            time.sleep(2)
                            game_status = 'rival turn'

                # Pour choisir une attaque
                elif game_status == 'player move':

                    # Vérifier quel bouton de mouvement a été cliqué
                    for i in range(len(move_buttons)):
                        button = move_buttons[i]

                        if button.collidepoint(mouse_click):
                            move = player_pokemon.moves[i]
                            player_pokemon.perform_attack(rival_pokemon, move)

                        # Vérifier si le Pokémon rival est épuisé
                        if rival_pokemon.current_hp == 0:
                            game_status = 'fainted'
                        else:
                            game_status = 'rival turn'

    # Écran de sélection du Pokémon
        if game_status == 'select pokemon':

            game.fill(white)

            # Dessiner les Pokémon de départ
            bulbasaur.draw()
            charmander.draw()
            squirtle.draw()
            pikachu.draw()
            jigglypuff.draw()
            chikorita.draw()
            cyndaquil.draw()
            gengar.draw()
            totodile.draw()
            zapdos.draw()
            shuppet.draw()
            psyduck.draw()

        # Dessiner une boîte autour du Pokémon pointé par la souris
            mouse_cursor = pygame.mouse.get_pos()
            for pokemon in pokemons:

                if pokemon.get_rect().collidepoint(mouse_cursor):
                    pygame.draw.rect(game, black, pokemon.get_rect(), 2)

            pygame.display.update()

    # Obtenir les mouvements de l'API et repositionner les Pokémon
        if game_status == 'prebattle':
            # Dessiner le Pokémon sélectionné
            game.fill(white)
            player_pokemon.draw()
            pygame.display.update()

            player_pokemon.set_moves()
            rival_pokemon.set_moves()

            # Repositionner les Pokémon
            player_pokemon.x = 20
            player_pokemon.y = 190
            rival_pokemon.x = 380
            rival_pokemon.y = 70

            # Redimensionner les sprites
            player_pokemon.size = 430
            rival_pokemon.size = 330
            player_pokemon.set_sprite('back_default')
            rival_pokemon.set_sprite('front_default')

            game_status = 'start battle'

    # Animation de début de combat
        if game_status == 'start battle':

            # Le rival envoie son Pokémon
            alpha = 0
            while alpha < 255:
                game.blit(background_image, (0, 0))
                rival_pokemon.draw(alpha)
                display_message(f'Rival sent out {rival_pokemon.name}!')
                alpha += .4

                pygame.display.update()

            # Pause de 1 seconde
            time.sleep(1)

        # Le joueur envoie son Pokémon
            alpha = 0
            while alpha < 255:
                game.blit(background_image, (0, 0))
                rival_pokemon.draw()
                player_pokemon.draw(alpha)
                display_message(f'Go {player_pokemon.name}!')
                alpha += .4

                pygame.display.update()

            # Dessiner les barres de points de vie
            player_pokemon.draw_hp()
            rival_pokemon.draw_hp()

            # Déterminer qui joue en premier
            if rival_pokemon.speed > player_pokemon.speed:
                game_status = 'rival turn'
            else:
                game_status = 'player turn'

            pygame.display.update()

            # Pause de 1 seconde
            time.sleep(1)

    # Afficher les boutons d'attaque et d'utilisation de potion
        if game_status == 'player turn':
            game.blit(background_image, (0, 0))
            player_pokemon.draw()
            rival_pokemon.draw()
            player_pokemon.draw_hp()
            rival_pokemon.draw_hp()

        # Créer les boutons d'attaque et d'utilisation de potion
            fight_button = create_button(340, 70, 20, 450, 150, 480, 'Fight')
            potion_button = create_button(
                340, 70, 360, 450, 500, 480, f'Use Potion ({player_pokemon.num_potions})')
            pokedex_button = create_button(
                340, 70, 20, 520, 150, 560, 'Pokedex')
            main_menu_button = create_button(
                340, 70, 360, 520, 480, 560, 'Main menu')

            # Dessiner la bordure noire
            pygame.draw.rect(game, black, (20, 450, 680, 140), 3)

            pygame.display.update()

    # Afficher les boutons de mouvement
        if game_status == 'player move':

            game.blit(background_image, (0, 0))
            player_pokemon.draw()
            rival_pokemon.draw()
            player_pokemon.draw_hp()
            rival_pokemon.draw_hp()

            # Créer un bouton pour chaque mouvement
            move_buttons = []
            for i in range(len(player_pokemon.moves)):
                move = player_pokemon.moves[i]
                button_width = 340
                button_height = 70
                left = 20 + i % 2 * button_width
                top = 450 + i // 2 * button_height
                text_center_x = left + 120
                text_center_y = top + 35
                button = create_button(button_width, button_height, left, top, text_center_x, text_center_y,
                                       move.name.capitalize())
                move_buttons.append(button)

            # Dessiner la bordure noire
            pygame.draw.rect(game, black, (20, 450, 680, 140), 3)

            pygame.display.update()

        # Le rival choisit un mouvement aléatoire pour attaquer
        if game_status == 'rival turn':

            game.blit(background_image, (0, 0))
            player_pokemon.draw()
            rival_pokemon.draw()
            player_pokemon.draw_hp()
            rival_pokemon.draw_hp()

            # Vider la boîte d'affichage et faire une pause de 2 secondes avant d'attaquer
            display_message('')
            time.sleep(2)

            # Sélectionner un mouvement aléatoire
            move = random.choice(rival_pokemon.moves)
            rival_pokemon.perform_attack(player_pokemon, move)

            # Vérifier si le Pokémon du joueur est épuisé
            if player_pokemon.current_hp == 0:
                game_status = 'fainted'
            else:
                game_status = 'player turn'

            pygame.display.update()

        # l'un des Pokémon est épuisé
        if game_status == 'fainted':

            alpha = 255
            while alpha > 0:

                game.blit(background_image, (0, 0))
                player_pokemon.draw_hp()
                rival_pokemon.draw_hp()

                # déterminer quel Pokémon est épuisé
                if rival_pokemon.current_hp == 0:
                    player_pokemon.draw()
                    rival_pokemon.draw(alpha)
                    display_message(f'{rival_pokemon.name} fainted!')
                else:
                    player_pokemon.draw(alpha)
                    rival_pokemon.draw()
                    display_message(f'{player_pokemon.name} fainted!')
                alpha -= .4

                pygame.display.update()

            game_status = 'gameover'

        # gameover screen
        if game_status == 'gameover':
            display_message('Play again (Y/N)?')

    # pygame.quit()
    SCREEN = pygame.display.set_mode((1200, 700))
