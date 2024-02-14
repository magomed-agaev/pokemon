from pygame.locals import *
from constants import *
import time
import math
import random
import requests
import io
from urllib.request import urlopen
from move import Move

# base url of the API
base_url = 'https://pokeapi.co/api/v2'


def display_message(message):
    # Dessiner une boîte blanche avec une bordure noire
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


class Pokemon(pygame.sprite.Sprite):

    def __init__(self, name, level, x, y):

        pygame.sprite.Sprite.__init__(self)

        # call the pokemon API endpoint
        req = requests.get(f'{base_url}/pokemon/{name.lower()}')
        self.json = req.json()

        # set the pokemon's name and level
        self.name = name
        self.level = level

        # set the sprite position on the screen
        self.x = x
        self.y = y

        # number of potions left
        self.num_potions = 3

        # get the pokemon's stats from the API
        stats = self.json['stats']
        for stat in stats:
            if stat['stat']['name'] == 'hp':
                self.current_hp = stat['base_stat'] + self.level
                self.max_hp = stat['base_stat'] + self.level
            elif stat['stat']['name'] == 'attack':
                self.attack = stat['base_stat']
            elif stat['stat']['name'] == 'defense':
                self.defense = stat['base_stat']
            elif stat['stat']['name'] == 'speed':
                self.speed = stat['base_stat']

        # set the pokemon's types
        self.types = []
        for i in range(len(self.json['types'])):
            type = self.json['types'][i]
            self.types.append(type['type']['name'])

        # set the sprite's width
        self.size = 150

        # set the sprite to the front facing sprite
        self.set_sprite('front_default')

    def perform_attack(self, other, move):

        display_message(f'{self.name} used {move.name}')

        # pause for 2 seconds
        time.sleep(2)

        # calculate the damage
        damage = (2 * self.level + 10) / 250 * \
            self.attack / other.defense * move.power

        # same type attack bonus (STAB)
        if move.type in self.types:
            damage *= 1.5

        # critical hit (6.25% chance)
        random_num = random.randint(1, 10000)
        if random_num <= 625:
            damage *= 1.5

        # round down the damage
        damage = math.floor(damage)

        other.take_damage(damage)

    def take_damage(self, damage):

        self.current_hp -= damage

        # hp should not go below 0
        if self.current_hp < 0:
            self.current_hp = 0

    def use_potion(self):

        # check if there are potions left
        if self.num_potions > 0:

            # add 30 hp (but don't go over the max hp)
            self.current_hp += 30
            if self.current_hp > self.max_hp:
                self.current_hp = self.max_hp

            # decrease the number of potions left
            self.num_potions -= 1

    def set_sprite(self, side):

        # set the pokemon's sprite
        image = self.json['sprites'][side]
        image_stream = urlopen(image).read()
        image_file = io.BytesIO(image_stream)
        self.image = pygame.image.load(image_file).convert_alpha()

        # scale the image
        scale = self.size / self.image.get_width()
        new_width = self.image.get_width() * scale
        new_height = self.image.get_height() * scale
        self.image = pygame.transform.scale(
            self.image, (new_width, new_height))

    def set_moves(self):

        self.moves = []

        # go through all moves from the api
        for i in range(len(self.json['moves'])):

            # get the move from different game versions
            versions = self.json['moves'][i]['version_group_details']
            for j in range(len(versions)):

                version = versions[j]

                # only get moves from red-blue version
                if version['version_group']['name'] != 'platinum':
                    continue

                # only get moves that can be learned from leveling up (ie. exclude TM moves)
                learn_method = version['move_learn_method']['name']
                if learn_method != 'level-up':
                    continue

                # add move if pokemon level is high enough
                level_learned = version['level_learned_at']
                if self.level >= level_learned:
                    move = Move(self.json['moves'][i]['move']['url'])

                    # only include attack moves
                    if move.power is not None:
                        self.moves.append(move)

        # select up to 4 random moves
        if len(self.moves) > 4:
            self.moves = random.sample(self.moves, 4)

    def draw(self, alpha=255):

        sprite = self.image.copy()
        transparency = (255, 255, 255, alpha)
        sprite.fill(transparency, None, pygame.BLEND_RGBA_MULT)
        game.blit(sprite, (self.x, self.y))

    def draw_hp(self):

        # display the health bar
        bar_scale = 300 // self.max_hp
        for i in range(self.max_hp):
            bar = (self.hp_x + bar_scale * i, self.hp_y, bar_scale, 30)
            pygame.draw.rect(game, red, bar)

        for i in range(self.current_hp):
            bar = (self.hp_x + bar_scale * i, self.hp_y, bar_scale, 30)
            pygame.draw.rect(game, green, bar)

        # display "HP" text
        font = pygame.font.Font(pygame.font.get_default_font(), 16)
        text = font.render(
            f'HP: {self.current_hp} / {self.max_hp}', True, black)
        text_rect = text.get_rect()
        text_rect.x = self.hp_x
        text_rect.y = self.hp_y + 30
        game.blit(text, text_rect)

    def get_rect(self):

        return Rect(self.x, self.y, self.image.get_width(), self.image.get_height())
