import pygame
from constants import BG_COLOR

class Paddle:
    WIDTH = 10
    HEIGHT = 60
    
    def __init__(self, screen: pygame.Surface, position: (int, int), color: (int, int, int), speed: float):
        self.screen = screen
        self.x = position[0]
        self.y = position[1]
        self.color = color
        self.speed = speed # pixels per millisecond

    def draw(self):
        pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.WIDTH, self.HEIGHT))

    def update(self, new_y: int):
        pygame.draw.rect(self.screen, BG_COLOR, (self.x, self.y, self.WIDTH, self.HEIGHT))
        self.y = new_y
        pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.WIDTH, self.HEIGHT))