from enum import Enum

class Directions(Enum):
    UP_LEFT = (-1, -1)
    DOWN_LEFT = (-1, 1)
    UP_RIGHT = (1, -1)
    DOWN_RIGHT = (1, 1)

BG_COLOR = (0, 0, 0) # Black
TEXT_COLOR = (255, 255, 255) # White
BORDER_COLOR = (255, 255, 255) # White
RIGHT_PADDLE_COLOR = (0, 0, 255) # Blue
LEFT_PADDLE_COLOR = (255, 0, 0) # Red

RIGHT_PADDLE_SPEED = 0.3
LEFT_PADDLE_SPEED = 0.18

