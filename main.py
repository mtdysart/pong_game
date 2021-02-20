import time
import random
import pygame
from ball import Ball
from paddle import Paddle
from ai_paddle import AIPaddle
from constants import Directions, RIGHT_PADDLE_COLOR, LEFT_PADDLE_COLOR, BORDER_COLOR, TEXT_COLOR, BG_COLOR, RIGHT_PADDLE_SPEED, LEFT_PADDLE_SPEED


class PongGame:

    # Class Variables
    WIDTH = 1000
    GAME_HEIGHT = 600
    BORDER = 15
    PADDLE_SPACING = 50 # Space between edge of paddle and end of screen
    FPS = 60
    BOTTOM_HEIGHT = 100
    GAME_TEXT_LOC = (WIDTH // 2 - 100, 25)
    SCORE_LOC = (30, GAME_HEIGHT + BORDER + 20)
    
    def __init__(self):
        self.screen = pygame.display.set_mode((self.WIDTH, self.GAME_HEIGHT + self.BOTTOM_HEIGHT))

        self.ball = Ball(self.screen, (self.WIDTH // 2, self.GAME_HEIGHT // 2))

        right_paddle_pos = (self.WIDTH - (self.PADDLE_SPACING + Paddle.WIDTH), self.GAME_HEIGHT // 2 - Paddle.HEIGHT // 2)
        left_paddle_pos = (self.PADDLE_SPACING, self.GAME_HEIGHT // 2 - Paddle.HEIGHT // 2)
        self.right_paddle = Paddle(self.screen, right_paddle_pos, RIGHT_PADDLE_COLOR, RIGHT_PADDLE_SPEED)
        self.left_paddle = AIPaddle(self.screen, left_paddle_pos, LEFT_PADDLE_COLOR, LEFT_PADDLE_SPEED)

        self.score = 0
        pygame.display.set_caption(f"Pong - Level {self.score + 1}")

    def draw_game(self):
        self.right_paddle.draw()
        self.left_paddle.draw()
        self.ball.draw()
        self.draw_border()
        self.display_score()

    def display_score(self):
        """
        Updates score in bottom section.
        """
        pygame.draw.rect(self.screen, BG_COLOR, (self.SCORE_LOC[0], self.SCORE_LOC[1], 200, 40))

        pygame.font.init()
        font = pygame.font.SysFont('calibri', 30)
        score_text_surface = font.render(f"Score: {self.score}", 1, TEXT_COLOR)
        self.screen.blit(score_text_surface, self.SCORE_LOC)

    def draw_border(self):
        pygame.draw.rect(self.screen, BORDER_COLOR, (0, 0, self.WIDTH, self.BORDER))
        pygame.draw.rect(self.screen, BORDER_COLOR, (0, self.GAME_HEIGHT - self.BORDER, self.WIDTH, self.BORDER))

    def move_player(self, dir: str, dt: int):
        if dir == 'up':
            dir_vec = -1
        elif dir == 'down':
            dir_vec = 1
        else:
            dir_vec = 0

        new_y = self.right_paddle.y + round(dir_vec * self.right_paddle.speed * dt)
        if new_y < self.BORDER:
            new_y = self.BORDER
        
        elif new_y > (self.GAME_HEIGHT - self.BORDER - Paddle.HEIGHT):
            new_y = self.GAME_HEIGHT - self.BORDER - Paddle.HEIGHT

        self.right_paddle.update(new_y)

    def move_ai(self, dt: int):
        self.left_paddle.check_fail()

        # If the AI is not failed, paddle moves towards ball
        if self.left_paddle.is_failed == False:

            # Move towards the ball if the ball y coordinate is outside the range of the paddle
            if 0 <= self.ball.x < round(self.WIDTH * (2/5)):
                if self.ball.y - (self.left_paddle.y + Paddle.HEIGHT // 2) < (-1 * Paddle.HEIGHT // 2):
                    dir_vec = -1
                elif self.ball.y - (self.left_paddle.y + Paddle.HEIGHT // 2) > (Paddle.HEIGHT // 2):
                    dir_vec = 1
                else:
                    dir_vec = 0

                new_y = self.left_paddle.y + round(dir_vec * self.left_paddle.speed * dt)
                if new_y < self.BORDER:
                    new_y = self.BORDER
                
                elif new_y > (self.GAME_HEIGHT - self.BORDER - Paddle.HEIGHT):
                    new_y = self.GAME_HEIGHT - self.BORDER - Paddle.HEIGHT

                self.left_paddle.update(new_y)

            # Only move towards the ball if y coordinate is over threshold distance away from paddle center
            elif round(self.WIDTH * (2/5)) <= self.ball.x < self.WIDTH:
                
                threshold = 2 * Paddle.HEIGHT

                if self.ball.y - (self.left_paddle.y + Paddle.HEIGHT // 2) < (-1 * threshold):
                    dir_vec = -1
                elif self.ball.y - (self.left_paddle.y + Paddle.HEIGHT // 2) > (threshold):
                    dir_vec = 1
                else:
                    dir_vec = 0

                new_y = self.left_paddle.y + round(dir_vec * self.left_paddle.speed * dt)
                if new_y < self.BORDER:
                    new_y = self.BORDER
                
                elif new_y > (self.GAME_HEIGHT - self.BORDER - Paddle.HEIGHT):
                    new_y = self.GAME_HEIGHT - self.BORDER - Paddle.HEIGHT

                self.left_paddle.update(new_y)
            

    def move_ball(self, dt: int):
        new_x = self.ball.x + round(self.ball.direction.value[0] * self.ball.speed * dt)
        new_y = self.ball.y + round(self.ball.direction.value[1] * self.ball.speed * dt)

        if new_y <= (self.BORDER + Ball.RADIUS):
            new_y = self.BORDER + Ball.RADIUS
            self.ball_collide('top')

        elif new_y >= (self.GAME_HEIGHT - self.BORDER - Ball.RADIUS):
            new_y = self.GAME_HEIGHT - self.BORDER - Ball.RADIUS
            self.ball_collide('bottom')
        
        elif (self.right_paddle.x - Ball.RADIUS) <= new_x < (self.right_paddle.x + Paddle.WIDTH + Ball.RADIUS):
            if self.right_paddle.y - Ball.RADIUS <= new_y <= self.right_paddle.y + Paddle.HEIGHT + Ball.RADIUS:
                new_x = self.right_paddle.x - Ball.RADIUS
                self.ball_collide('right')

        elif (self.left_paddle.x - Ball.RADIUS) <= new_x < (self.left_paddle.x + Paddle.WIDTH + Ball.RADIUS):
            if self.left_paddle.y - Ball.RADIUS <= new_y <= self.left_paddle.y + Paddle.HEIGHT + Ball.RADIUS:
                new_x = self.left_paddle.x + Paddle.WIDTH + Ball.RADIUS
                self.ball_collide('left')

        self.ball.update((new_x, new_y))

    def ball_collide(self, collision_loc: str):
        """

        """
        if collision_loc == 'top':
            if self.ball.direction == Directions.UP_LEFT:
                self.ball.change_direction(Directions.DOWN_LEFT)
            
            elif self.ball.direction == Directions.UP_RIGHT:
                self.ball.change_direction(Directions.DOWN_RIGHT)

        elif collision_loc == 'bottom':
            if self.ball.direction == Directions.DOWN_LEFT:
                self.ball.change_direction(Directions.UP_LEFT)
            
            elif self.ball.direction == Directions.DOWN_RIGHT:
                self.ball.change_direction(Directions.UP_RIGHT)

        elif collision_loc == 'right':
            if self.ball.direction == Directions.DOWN_RIGHT:
                self.ball.change_direction(Directions.DOWN_LEFT)
            
            elif self.ball.direction == Directions.UP_RIGHT:
                self.ball.change_direction(Directions.UP_LEFT)

        elif collision_loc == 'left':
            if self.ball.direction == Directions.DOWN_LEFT:
                self.ball.change_direction(Directions.DOWN_RIGHT)
            
            elif self.ball.direction == Directions.UP_LEFT:
                self.ball.change_direction(Directions.UP_RIGHT)

        else:
            raise ValueError(f"Invalid direction: {collision_loc}")

    def score_goal(self):
        """
        Updates the score and resets the ball and paddles to the middle.
        """
        self.score += 1
        self.left_paddle.update_prob(self.score)

        # Display Score
        pygame.font.init()
        font = pygame.font.SysFont('calibri', 50)
        score_text_surface = font.render(f"Score: {self.score}", 1, TEXT_COLOR)
        self.screen.blit(score_text_surface, self.GAME_TEXT_LOC)

        self.display_score()

        self.ball.update((self.WIDTH // 2, self.GAME_HEIGHT // 2))
        self.ball.change_direction(random.choice(list(Directions)))

        self.left_paddle.update(self.GAME_HEIGHT // 2 - self.left_paddle.HEIGHT // 2)
        self.right_paddle.update(self.GAME_HEIGHT // 2 - self.right_paddle.HEIGHT //2)
    
    def lose(self):
        """
        Displays 'You Lose' and freezes the game.
        """
        paused = True

        # Display "You Lose!"
        pygame.font.init()
        font = pygame.font.SysFont('calibri', 50)
        lose_text_surface = font.render("You Lose!", 1, TEXT_COLOR)
        score_text_surface = font.render(f"Score: {self.score}", 1, TEXT_COLOR)

        self.screen.blit(lose_text_surface, self.GAME_TEXT_LOC)
        
        x, y = self.GAME_TEXT_LOC
        self.screen.blit(score_text_surface, (x + 15, y + 60))
        pygame.display.update()

        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    paused = False

            #TODO: ask to start new game
        return False

    def run(self):
        clock = pygame.time.Clock()
        running = True
        frozen = False
        frames_frozen = 0
        freeze_length = self.FPS * 4 # frames in 4 seconds

        while running:
            dt = clock.tick(self.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            if not frozen:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_UP]:
                    self.move_player('up', dt)

                elif keys[pygame.K_DOWN]:
                    self.move_player('down', dt)

                self.move_ball(dt)
                self.move_ai(dt)

                if self.ball.x <= 0:
                    frozen = True
                    self.score_goal()

                elif self.ball.x >= self.WIDTH:
                    running = self.lose()
            
            else:
                frames_frozen += 1

                if frames_frozen == freeze_length:
                    frozen = False
                    frames_frozen = 0
                    pygame.draw.rect(self.screen, BG_COLOR, (self.GAME_TEXT_LOC[0], self.GAME_TEXT_LOC[1], 200, 50))

            pygame.display.update()

        pygame.quit()


if __name__ == '__main__':
    game = PongGame()
    game.draw_game()
    game.run()