import os

#Window size
WIDTH = 800
HEIGHT = 437

#Colors
BLACK = [0, 0, 0]

#Game Preferences
GAME_NAME = "Бегун"
OBSTACLE_TICKRATE = 1000

#source
DIR = os.path.dirname(os.path.abspath(__file__))
PLAYER_SCORE_JSON_PATH = f"{DIR}/data/player_score.json"