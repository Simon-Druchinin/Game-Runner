import os
import sys
import time
from typing import NoReturn
from random import randint

import pygame

from SETTINGS import *


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(GAME_NAME)

clock = pygame.time.Clock()

class Player():
    run_animation = [pygame.image.load(os.path.join('images\player_run', f"{x}.png")) for x in range (1, 9)]
    jump_animation = [pygame.image.load(os.path.join('images\player_jump', f"{x}.png")) for x in range (1, 8)]
    slide_animation = [pygame.image.load(os.path.join('images\player_slide', f"{x}.png")) for x in range (1, 2)]
    slide_animation += [pygame.image.load(os.path.join('images\player_slide', f"2.png")) for x in range (7)]
    slide_animation += [pygame.image.load(os.path.join('images\player_slide', f"{x}.png")) for x in range (3, 6)]
    death_animation = pygame.image.load(os.path.join('images', "death.png"))
    jump_list = [1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,0,0,0,0,0,0,0,
                 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,-1,-1,-1,-1,-1,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-3,-3,-3,
                 -3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4]

    def __init__(self):
        self.x, self.y = [200, 313]
        self.width = 64
        self.height = 64

        self.count = 0
        self.is_dead = False
        self.action = "running"

        self.score = 0
    
    def draw_death(self, screen):
        self.y = 340
        self.is_dead = True
        screen.blit(self.death_animation, (self.x, self.y))

        pygame.draw.rect(screen, (255,255,255), (270, 170, 350, 170))
        pygame.draw.rect(screen, (BLACK), (270, 170, 350, 170), 2)
        text = "Вы проиграли."
        largeFont = pygame.font.SysFont('comicsans', 40)
        message = largeFont.render(text, 1, (255,54,0))
        screen.blit(message, (300, 200))

        text = f"Ваш счёт: {self.score}"
        largeFont = pygame.font.SysFont('comicsans', 40)
        message = largeFont.render(text, 1, (18,173,42))
        screen.blit(message, (330, 240))


    def draw_run(self, screen):
        if int(self.count) > 95:
            self.count = 0
            self.x, self.y = [200, 313]

        screen.blit(self.run_animation[int(self.count)//12], (self.x,self.y))
        self.count += 1
        self.hitbox = (self.x+ 4, self.y, self.width-24, self.height-13)

    def draw_jump(self, screen):
        if int(self.count) > 150:
            self.count = 0
            self.action = "running"
        self.y -= self.jump_list[self.count]
        
        
        screen.blit(self.jump_animation[int(self.count)//22], (self.x,self.y))
        self.count += 1
        self.hitbox = (self.x+4, self.y, self.width-24, self.height-10)

    def draw_slide(self, screen):
        if self.count < 22:
            self.y += 1
            self.hitbox = (self.x+ 4, self.y, self.width-24, self.height-10)

        elif self.count > 22 and self.count < 160:
            self.hitbox = (self.x, self.y+3, self.width-8, self.height-35)

        elif self.count == 160:
            self.y -= 21
        
        elif self.count >=  168:
            self.count = 0
            self.action = "running"
        
        screen.blit(self.slide_animation[self.count//18], (self.x, self.y))
        self.count += 1

class Saw():
    saw_animation = [pygame.image.load(os.path.join('images\saw', f"{x}.png")) for x in range (1, 5)]

    def __init__(self):
        self.x = 810
        self.y = 310
        self.width = 64
        self.height = 64
        self.count = 0
    
    def draw(self, screen):
        self.hitbox = (self.x + 10, self.y + 5, self.width - 20, self.height - 5)
        if self.count >= 8:
            self.count = 0
        screen.blit(pygame.transform.scale(self.saw_animation[self.count//2], (64,64)), (self.x,self.y))
        self.count += 1
        self.x -=1
    
    def collide(self, rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] + rect[3] > self.hitbox[1]:
                return True
        return False

class Spike():
    spike = pygame.image.load(os.path.join('images', 'spike.png'))

    def __init__(self):
        self.x = 810
        self.y = 0

    def draw(self, win):
        self.hitbox = (self.x + 10, self.y, 28, 315)
        win.blit(self.spike, (self.x, self.y))
        self.x -=1

    def collide(self, rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] < self.hitbox[3]:
                return True
        return False


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = location

    def slide(self):
        if self.rect.x <= self.image.get_width() * -1:
            self.rect.x = self.image.get_width()
        self.rect.x -= 1

#Class instances
player = Player()
bg_1 = Background('images/bg.png', [0, 0])
bg_2 = Background('images/bg.png', [bg_1.image.get_width(), 0])

#Make timer for events
speed_event = pygame.USEREVENT + 1
obstacle_event = pygame.USEREVENT + 2
pygame.time.set_timer(speed_event , 500)
pygame.time.set_timer(obstacle_event , OBSTACLE_TICKRATE)

def move_background():
    screen.fill(BLACK)
    screen.blit(bg_1.image, bg_1.rect)
    screen.blit(bg_2.image, bg_2.rect)
    bg_1.slide()
    bg_2.slide()

def draw_score(player):
    largeFont = pygame.font.SysFont('comicsans', 30)
    text = largeFont.render(f"Счёт: {player.score}", 1, (255,255,255))
    screen.blit(text, (600, 10))

def redraw_window(player, obstacles):
    move_background()
    
    #draw obstacles
    for obstacle in obstacles:
        obstacle.draw(screen)
        if obstacle.collide(player.hitbox):
            player.action = "death"

    for num, obstacle in enumerate(obstacles):
        #delete obstacles
        if obstacle.x <= -64:
            obstacles.pop(num)
        
        #add points for passed obstacle
        if obstacle.x + 5 == player.x:
            player.score += 1
            
    #draw a player action
    draw_player_action = {
        "running": player.draw_run,
        "jumping": player.draw_jump,
        "sliding": player.draw_slide,
        "death": player.draw_death,
    }[player.action](screen)

    draw_score(player)
    
    pygame.display.update()

#game variables
obstacles = []

while not player.is_dead:
    #game events
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

        if SPEED < 350 and event.type == speed_event:
            SPEED += 1
        
        if event.type == obstacle_event:
            obstacle_types = [Saw(), Spike()]
            obstacles.append(obstacle_types[randint(0, 1)])

    #player movements
    keys = pygame.key.get_pressed()

    if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and player.action == "running":
        player.count = 0
        player.action = "jumping"
    
    elif keys[pygame.K_DOWN] and player.action == "running":
        player.count = 0
        player.action = "sliding"

    clock.tick(SPEED)
    redraw_window(player, obstacles)

time.sleep(2)