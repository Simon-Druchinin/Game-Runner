import os
import sys
import time
import json
from random import randint

import pygame
import pygame_menu

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
                 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-3,-3,-3,
                 -3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4]

    @staticmethod
    def get_sorted_list_of_players_records(PLAYER_SCORE_JSON_PATH: str) -> list:
        if os.stat(PLAYER_SCORE_JSON_PATH).st_size:
            with open(PLAYER_SCORE_JSON_PATH, 'r', encoding='utf-8') as read_file:
                data = json.load(read_file)
                players_records = sorted(data, key=lambda x: x[list(x.keys())[0]], reverse=True)
        else:
            players_records = []
        
        return players_records
        
    def __init__(self):
        self.x, self.y = [200, 313]
        self.width = 64
        self.height = 64

        self.count = 0
        self.is_dead = False
        self.action = "running"

        self.score = 0
        self.name = "Игрок1"

        self.hitbox = (self.x+4, self.y, self.width-24, self.height-13)
    
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
        self.hitbox = (self.x+4, self.y, self.width-24, self.height-13)

    def draw_jump(self, screen):
        if int(self.count) > 153:
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
    
    def _write_to_json(self):
        if os.stat(PLAYER_SCORE_JSON_PATH).st_size:
            with open(PLAYER_SCORE_JSON_PATH, 'r', encoding='utf-8') as read_file:
                data = json.load(read_file)
                for num, dict in enumerate(data):
                    if next(iter(dict)) == self.name and (int(dict[next(iter(dict))]) < self.score):
                        data.pop(num)
                        data.append({self.name: self.score})
                        break
                for num, dict in enumerate(data):
                    if next(iter(dict)) == self.name:
                        break
                else:
                    data.append({self.name: self.score})
                
        else:
            data = []
            data.append({self.name: self.score})
        
        with open(PLAYER_SCORE_JSON_PATH, 'w', encoding='utf-8') as json_file:
                json.dump(data, json_file, ensure_ascii=False)

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
    
    def collide(self, rect: list) -> bool:
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

    def collide(self, rect: list) -> bool:
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

def redraw_window(player, obstacles: list, points_for_obstacle: int):
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
            player.score += points_for_obstacle
            
    #draw a player action
    draw_player_action = {
        "running": player.draw_run,
        "jumping": player.draw_jump,
        "sliding": player.draw_slide,
        "death": player.draw_death,
    }[player.action](screen)

    draw_score(player)
    
    pygame.display.update()

def set_difficulty():
    pass

def call_menu(screen):
    global menu
    menu = pygame_menu.Menu('Добро пожаловать!', WIDTH-300, HEIGHT - 100,
                        theme=pygame_menu.themes.THEME_BLUE)

    menu.add.text_input('Имя персонажа: ', default='Игрок1', maxchar=12, onchange=set_player_name)
    menu.add.selector('Уровень сложности: ', [('Легко', 1), ('Сложно', 2)], onchange=set_difficulty)
    menu.add.button('Играть', start_the_game)
    menu.add.button('Рекорды', call_record_menu, screen)
    menu.add.button('Выход', pygame_menu.events.EXIT)

    menu.mainloop(screen)

def call_record_menu(screen):
    players_records = Player.get_sorted_list_of_players_records(PLAYER_SCORE_JSON_PATH)
    records_title = ""

    if 0 < len(players_records):
        for num, record in enumerate(players_records):
            if num >= 5:
                break
            for key, value in record.items():
                records_title += f"{num+1}.) {key} - {value}\n"

    record_menu = pygame_menu.Menu('Рекорды:', WIDTH-300, HEIGHT - 100,
                        theme=pygame_menu.themes.THEME_BLUE)

    record_menu.add.label(title=records_title)
    record_menu.add.button("Назад", record_menu.disable)

    record_menu.mainloop(screen)


bg_1 = Background('images/bg.png', [0, 0])
bg_2 = Background('images/bg.png', [bg_1.image.get_width(), 0])

#game variables
obstacles = []
speed = 180
max_speed = 350
points_for_obstacle = 1
player_name = "Игрок1"

def set_player_name(name: str):
    global player_name
    player_name = name

def set_difficulty(value, difficulty: int):
    global speed, max_speed, points_for_obstacle
    if difficulty == 1:
        speed = 180
        max_speed = 350
        points_for_obstacle = 1
        

    elif difficulty == 2:
        speed = 370
        max_speed = 440
        points_for_obstacle = 2

def start_the_game():
    #Class instances
    player = Player()
    player.name = player_name

    #Make timer for events
    speed_event = pygame.USEREVENT + 1
    obstacle_event = pygame.USEREVENT + 2
    pygame.time.set_timer(speed_event , 500)
    pygame.time.set_timer(obstacle_event , OBSTACLE_TICKRATE)

    game(speed, max_speed, player, speed_event, obstacle_event, points_for_obstacle)

def game(speed: int, max_speed: int, player, speed_event, obstacle_event, points_for_obstacle: int):
    obstacles = []
    while not player.is_dead:
        #game events
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

            if speed < max_speed and event.type == speed_event:
                speed += 1
            
            if event.type == obstacle_event:
                obstacle_types = [Saw(), Spike()]
                obstacles.append(obstacle_types[randint(0, 1)])

        #player movements
        keys = pygame.key.get_pressed()

        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and player.action == "running":
            player.count = 0
            player.action = "jumping"
        
        elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and player.action == "running":
            player.count = 0
            player.action = "sliding"

        clock.tick(speed)
        redraw_window(player, obstacles, points_for_obstacle)

    player._write_to_json()
    time.sleep(2)

if __name__ == "__main__":
    call_menu(screen)