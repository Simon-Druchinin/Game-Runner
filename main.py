import os
import sys
from typing import NoReturn
import time

import pygame

from SETTINGS import *


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(GAME_NAME)

clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    run_animation = [pygame.image.load(os.path.join('images\player_run', f"{x}.png")) for x in range (1, 9)]
    jump_animation = [pygame.image.load(os.path.join('images\player_jump', f"{x}.png")) for x in range (1, 8)]
    slide_animation = [pygame.image.load(os.path.join('images\player_slide', f"{x}.png")) for x in range (1, 6)]
    death_animation = pygame.image.load(os.path.join('images', "death.png"))

    def __init__(self, width, height, location):
        self.width = width
        self.height = height
        self.x, self.y = location

        self.runCount = 0
        self.is_dead = False
        
    def draw_run(self):
        if int(self.runCount) > 95:
            self.runCount = 0 

        screen.blit(self.run_animation[int(self.runCount)//12], (self.x,self.y))
        self.runCount += 1
    
    def draw_jump(self):
        pass

    def draw_slide(self):
        pass

player = Player(64, 64, [200, 313])

class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = location

        self.counter = 0

    def slide(self):
        if self.rect.x <= self.image.get_width() * -1:
            self.rect.x = self.image.get_width()
        self.rect.x -= 1



bg_1 = Background('images/bg.png', [0, 0])
bg_2 = Background('images/bg.png', [bg_1.image.get_width(), 0])

def redraw_window():
    #Move a background
    screen.fill(BLACK)
    screen.blit(bg_1.image, bg_1.rect)
    screen.blit(bg_2.image, bg_2.rect)
    bg_1.slide()
    bg_2.slide()

    #draw a player
    player.draw_run()
    pygame.display.update()

while not player.is_dead:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    clock.tick(SPEED)
    redraw_window()
    