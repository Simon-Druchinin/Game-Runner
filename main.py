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
    slide_animation = [pygame.image.load(os.path.join('images\player_slide', f"{x}.png")) for x in range (1, 2)]
    slide_animation += [pygame.image.load(os.path.join('images\player_slide', f"2.png")) for x in range (7)]
    slide_animation += [pygame.image.load(os.path.join('images\player_slide', f"{x}.png")) for x in range (3, 6)]
    death_animation = pygame.image.load(os.path.join('images', "death.png"))
    jump_list = [1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,0,0,0,0,0,0,0,
                 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,-1,-1,-1,-1,-1,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-3,-3,-3,
                 -3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4]

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.x, self.y = [200, 313]

        self.count = 0
        self.is_dead = False
        self.action = "running"
        
    def draw_run(self):
        if int(self.count) > 95:
            self.count = 0
            self.x, self.y = [200, 313]

        screen.blit(self.run_animation[int(self.count)//12], (self.x,self.y))
        self.count += 1
    
    def draw_jump(self):
        if int(self.count) > 144:
            self.count = 0
            self.action = "running"
        self.y -= self.jump_list[self.count]
        
        
        screen.blit(self.jump_animation[int(self.count)//21], (self.x,self.y))
        self.count += 1

    def draw_slide(self):
        if self.count < 22:
            self.y += 1

        elif self.count == 160:
            self.y -= 21
        
        elif self.count >=  168:
            self.count = 0
            self.action = "running"
        
        screen.blit(self.slide_animation[self.count//18], (self.x, self.y))
        self.count += 1

player = Player(64, 64)

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

def redraw_window(player):
    #Move a background
    screen.fill(BLACK)
    screen.blit(bg_1.image, bg_1.rect)
    screen.blit(bg_2.image, bg_2.rect)
    bg_1.slide()
    bg_2.slide()

    #draw a player actiob
    draw_player_action = {
        "running": player.draw_run,
        "jumping": player.draw_jump,
        "sliding": player.draw_slide,
    }[player.action]()

    pygame.display.update()

while not player.is_dead:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    keys = pygame.key.get_pressed()

    if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and player.action == "running":
        player.count = 0
        player.action = "jumping"
    
    elif keys[pygame.K_DOWN] and player.action == "running":
        player.count = 0
        player.action = "sliding"

    clock.tick(SPEED)
    redraw_window(player)
    