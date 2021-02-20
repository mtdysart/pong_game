import random
import math
import pygame
from paddle import Paddle

class AIPaddle(Paddle):
    FAIL_LENGTH = 20 # frames

    def __init__(self, screen: pygame.Surface, position: (int, int), color: (int, int, int), speed: float):
        super().__init__(screen, position, color, speed)

        self.prob_fail = 0.01 # probability that the currently not failed paddle will fail on a given frame
        self.frames_failed = 0 # number of frames the paddle has been failed, reset to 0 once equal to FAIL_LENGTH
        self.is_failed = False # True if paddle is currently in a failed state
        
    def check_fail(self):
        """
        Set is_failed to True if paddle randomly fails. Otherwise increment number of frames paddle has been failed 
        and unfail if necessary.
        """
        if self.is_failed == False:
            rn = random.uniform(0, 1) 

            if rn < self.prob_fail:
                self.is_failed = True
        
        else:
            self.frames_failed += 1

            if self.frames_failed == self.FAIL_LENGTH:
                self.is_failed = False
                self.frames_failed = 0

    def update_prob(self, score):
        """
        Updates the probability of failing if score is a multiple of five. 
        """
        if score % 5 == 0:
            self.prob_fail = 1 / (50 * math.sqrt(score))


