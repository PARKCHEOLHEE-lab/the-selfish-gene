import random
import pygame

from typing import List
from classes.constants import DisplayConsts, EnvironmentConsts, ColorConsts


class AppleHelper:
    def _get_random_position(self, except_positions: List[List[int]]) -> List[float]:
        position_x_range = range(DisplayConsts.GAP, DisplayConsts.WIDTH - DisplayConsts.GAP, EnvironmentConsts.WORM_SIZE)
        position_y_range = range(DisplayConsts.GAP, DisplayConsts.HEIGHT - DisplayConsts.GAP, EnvironmentConsts.WORM_SIZE)
        
        available_positions = []
        for x in position_x_range:
            for y in position_y_range:
                position = [x + EnvironmentConsts.WORM_SIZE / 2, y + EnvironmentConsts.WORM_SIZE / 2]
                if position not in except_positions:
                    available_positions.append(position)
        
        if not available_positions:
            raise ValueError("No valid positions available")
        
        random_position = random.choice(available_positions)
        return random_position


class Apple(AppleHelper):
    def __init__(self, except_positions: List[List[int]]):
        self.except_positions = except_positions
        self.position = self._get_random_position(except_positions)
        
    def draw(self, display: pygame.display) -> None:
        pygame.draw.circle(
            display, 
            ColorConsts.RED,
            self.position,
            EnvironmentConsts.WORM_SIZE / 2,
        )