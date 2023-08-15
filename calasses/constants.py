class EnvironmentConsts:
    
    WORM_SPEED_ORIGINAL = 1
    WORM_SENSE = 20
    WORM_DIRECTION_SWITCH_PROBABILITY = 0.3
    WORM_BASIC_LENGTH = 6
    
    WORM_SIZE = 10
    FOOD_SIZE = 10
    
    
class DisplayConsts:
    WIDTH = 500
    HEIGHT = 500
    FRAME_SPEED = 20

    GAP = EnvironmentConsts.WORM_SIZE * EnvironmentConsts.WORM_BASIC_LENGTH
    
    
class ColorConsts:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    GRAY = (50, 50, 50)
    BRIGHT_GRAY = (100, 100, 100)
    
    
class DirectionConsts:
    DIRECTION_LEFT = "LEFT"
    DIRECTION_UP = "UP"
    DIRECTION_RIGHT = "RIGHT"
    DIRECTION_DOWN = "DOWN"
    
    DIRECTIONS = [DIRECTION_LEFT, DIRECTION_UP, DIRECTION_RIGHT, DIRECTION_DOWN]
    
    DIRECTOIN_REVERSE = {
        DIRECTION_LEFT: DIRECTION_RIGHT,
        DIRECTION_RIGHT: DIRECTION_LEFT,
        DIRECTION_DOWN: DIRECTION_UP,
        DIRECTION_UP: DIRECTION_DOWN,
    }