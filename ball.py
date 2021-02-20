import pygame
import enum
import random
from typing import Tuple
from constants import BG_COLOR
from constants import Directions

class Ball:
    RADIUS = 5
    COLOR = (255, 255, 255) # White

    def __init__(self, screen: pygame.Surface, position: Tuple[int, int]):
        self.screen = screen
        self.x = position[0]
        self.y = position[1]
        self.speed = 0.2 # Pixels per millisecond
        self.direction = random.choice(list(Directions)) # Direction ball is moving initially

    def draw(self):
        pygame.draw.circle(self.screen, self.COLOR, (self.x, self.y), self.RADIUS)

    def update(self, new_pos: (int, int)):
        pygame.draw.circle(self.screen, BG_COLOR, (self.x, self.y), self.RADIUS)
        self.x = new_pos[0]
        self.y = new_pos[1]
        pygame.draw.circle(self.screen, self.COLOR, (self.x, self.y), self.RADIUS)

    def change_direction(self, direction: enum.auto):
        self.direction = direction

