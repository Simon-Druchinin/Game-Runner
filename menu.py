import os
import pygame
import pygame_menu
from typing import NoReturn

from SETTINGS import WIDTH, HEIGHT


def set_difficulty(value, difficulty: int):
    print(difficulty)

def start_the_game():
    pass

def call_menu() -> NoReturn:
    menu = pygame_menu.Menu('Добро пожаловать!', WIDTH-300, HEIGHT - 100,
                        theme=pygame_menu.themes.THEME_BLUE)

    menu.add.text_input('Имя персонажа: ', default='Игрок1')
    menu.add.selector('Уровень сложности: ', [('Легко', 1), ('Сложно', 2)], onchange=set_difficulty)
    menu.add.button('Играть', start_the_game)
    menu.add.button('Выход', pygame_menu.events.EXIT)

    menu.mainloop(surface)