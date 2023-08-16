import random
import pygame

from typing import List
from classes.constants import DisplayConsts, EnvironmentConsts, ColorConsts

class AppleHelper:
    def _get_random_position(self, except_positions: List[List[int]]) -> List[float]:
        position_x_range = range(DisplayConsts.GAP, DisplayConsts.WIDTH - DisplayConsts.GAP, EnvironmentConsts.WORM_SIZE)
        position_x_candidates = [candidate for candidate in position_x_range]

        position_y_range = range(DisplayConsts.GAP, DisplayConsts.HEIGHT - DisplayConsts.GAP, EnvironmentConsts.WORM_SIZE)
        position_y_candidates = [candidate for candidate in position_y_range]
        
        random_position_x = random.choice(position_x_candidates) + EnvironmentConsts.WORM_SIZE / 2
        random_position_y = random.choice(position_y_candidates) + EnvironmentConsts.WORM_SIZE / 2
        
        while [random_position_x, random_position_y] in except_positions:
            random_position_x = random.choice(position_x_candidates) + EnvironmentConsts.WORM_SIZE / 2
            random_position_y = random.choice(position_y_candidates) + EnvironmentConsts.WORM_SIZE / 2
        
        return [random_position_x, random_position_y]

class Apple(AppleHelper):
    def __init__(self, except_positions):
        self.eaten = False
        self.except_positions = except_positions
        self.position = self._get_random_position(except_positions)
        
    def draw(self, display: pygame.display) -> None:
        if not self.eaten:
            pygame.draw.circle(
                display, 
                ColorConsts.RED,
                self.position,
                EnvironmentConsts.WORM_SIZE / 2,
            )