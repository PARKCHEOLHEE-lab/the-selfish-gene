import random
import pygame
import math
import copy
import shapely
from typing import List, Tuple

from classes.constants import EnvironmentConsts, ColorConsts, DirectionConsts, DisplayConsts
from classes.apple import Apple


class WormHelper:
    
    def _get_color(self) -> Tuple[int]:
        return (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255)
        )
    
    def _get_head(self) -> List[int]:
        height_range = random.randrange(
            DisplayConsts.GAP, (DisplayConsts.HEIGHT // EnvironmentConsts.WORM_SIZE) * EnvironmentConsts.WORM_SIZE - DisplayConsts.GAP, 
            EnvironmentConsts.WORM_SIZE
        )
        
        width_range = random.randrange(
            DisplayConsts.GAP, 
            (DisplayConsts.WIDTH // EnvironmentConsts.WORM_SIZE) * EnvironmentConsts.WORM_SIZE - DisplayConsts.GAP, EnvironmentConsts.WORM_SIZE
        )

        left = [DisplayConsts.GAP, height_range]
        top = [width_range, DisplayConsts.GAP]
        right = [(DisplayConsts.WIDTH - EnvironmentConsts.WORM_SIZE) // EnvironmentConsts.WORM_SIZE * EnvironmentConsts.WORM_SIZE - DisplayConsts.GAP, height_range]
        bottom = [width_range, (DisplayConsts.HEIGHT - EnvironmentConsts.WORM_SIZE) // EnvironmentConsts.WORM_SIZE * EnvironmentConsts.WORM_SIZE - DisplayConsts.GAP]

        boundaries = [left, top, right, bottom]
        head = boundaries[random.randint(0, 3)]
        
        return head
    
    def _get_body(self, head: List[int], length: int, direction: str) -> List[List[int]]:
        body = []
        
        for l in range(length - 1):
            if direction == DirectionConsts.DIRECTION_LEFT:
                b = [head[0] + (l + 1) * EnvironmentConsts.WORM_SIZE, head[1]]
                
            elif direction == DirectionConsts.DIRECTION_UP:
                b = [head[0], head[1] + (l + 1) * EnvironmentConsts.WORM_SIZE]
                
            elif direction == DirectionConsts.DIRECTION_RIGHT:
                b = [head[0] - (l + 1) * EnvironmentConsts.WORM_SIZE, head[1]]
                
            elif direction == DirectionConsts.DIRECTION_DOWN:
                b = [head[0], head[1] - (l + 1) * EnvironmentConsts.WORM_SIZE]
            
            body.append(b)
            
        body = [head] + body
        
        return body
    
    def _draw_body(self, display: pygame.display, body: List[List[int]], color: Tuple[int]) -> None:
        for pos in body:
            pygame.draw.rect(
                display, 
                color,
                pygame.Rect(pos[0], pos[1], EnvironmentConsts.WORM_SIZE, EnvironmentConsts.WORM_SIZE)
            )
    
    def _draw_sense(self, display: pygame.display) -> None:
        circle_center = (
            self.body[-1][0] + EnvironmentConsts.WORM_SIZE/ 2, 
            self.body[-1][1] + EnvironmentConsts.WORM_SIZE/ 2
        )
        circle_radius = self.sense
        num_dashes = 36
        dash_length = 3
        angle_step = 360 / num_dashes

        for i in range(num_dashes):
            angle = math.radians(i * angle_step)
            start_point = (
                circle_center[0] + int(circle_radius * math.cos(angle)),
                circle_center[1] + int(circle_radius * math.sin(angle))
            )
            end_point = (
                circle_center[0] + int((circle_radius + dash_length) * math.cos(angle)),
                circle_center[1] + int((circle_radius + dash_length) * math.sin(angle))
            )
            pygame.draw.line(display, ColorConsts.BRIGHT_GRAY, start_point, end_point)
            
    def _draw_eaten_count(self, display: pygame.display, eaten_count: int, body: List[List[int]]) -> None:
        font = pygame.font.Font(None, 15)
        text_surface = font.render(str(eaten_count), False, ColorConsts.GREEN)
        text_x = (body[-1][0] + EnvironmentConsts.WORM_SIZE / 2) + text_surface.get_width() // 2
        text_y = (body[-1][1] + EnvironmentConsts.WORM_SIZE / 2) + text_surface.get_width() // 2
        display.blit(text_surface, (text_x, text_y))
            
    def _get_random_direction(self, direction: str, switch: float) -> str:
        
        possible_directions = []
        
        for dir in DirectionConsts.DIRECTIONS:
            if dir != direction and direction != DirectionConsts.DIRECTOIN_REVERSE[dir]:
                possible_directions.append(dir)
                
        if random.random() < switch:
            new_direction = random.choice(possible_directions)
            direction = new_direction
            
        return direction
            
    def _get_moved_body(self, body: List[List[int]], direction: str, speed: int) -> List[List[int]]:
        new_head = body[-1].copy()

        body_gaps = copy.deepcopy(body)
        
        for s in range(1, speed + 1):
            
            if direction == DirectionConsts.DIRECTION_UP:
                body_gap = [new_head[0], new_head[1] - EnvironmentConsts.WORM_SIZE * s]
                
            elif direction == DirectionConsts.DIRECTION_DOWN:
                body_gap = [new_head[0], new_head[1] + EnvironmentConsts.WORM_SIZE * s]

            elif direction == DirectionConsts.DIRECTION_LEFT:
                body_gap = [new_head[0] - EnvironmentConsts.WORM_SIZE * s, new_head[1]]

            elif direction == DirectionConsts.DIRECTION_RIGHT:
                body_gap = [new_head[0] + EnvironmentConsts.WORM_SIZE * s, new_head[1]]
                
            body_gaps.append(body_gap)
        
        is_it_out_of_width = 0 > body_gaps[-1][0] or body_gaps[-1][0] > DisplayConsts.WIDTH - EnvironmentConsts.WORM_SIZE
        is_it_out_of_height = 0 > body_gaps[-1][1] or body_gaps[-1][1] > DisplayConsts.HEIGHT - EnvironmentConsts.WORM_SIZE

        if not is_it_out_of_width and not is_it_out_of_height:
            body = body_gaps[speed:]

        return body
    
    def _get_grown_body(self, body: List[List[int]], apples: List[Apple]):
        ate = False
        for apple in apples:
            apple_x = apple.position[0] - EnvironmentConsts.WORM_SIZE / 2
            apple_y = apple.position[1] - EnvironmentConsts.WORM_SIZE / 2
            grown_head = [apple_x, apple_y]
            
            if body[-1] == [apple_x, apple_y]:
                apple.eaten = True
                apples.remove(apple)
                body.append(grown_head)
                ate = True
                break
            
        return body, ate
        

class WormGene:
    def __init__(self, speed: int, sense: float, switch: float) -> None:
        self.speed = speed
        self.sense = sense
        self.switch = switch


class Worm(WormGene, WormHelper):
    def __init__(
        self, 
        speed: int = EnvironmentConsts.WORM_SPEED_ORIGINAL, 
        sense: float = EnvironmentConsts.WORM_SENSE, 
        switch: float = EnvironmentConsts.WORM_DIRECTION_SWITCH_PROBABILITY
    ):
        WormGene.__init__(self, speed, sense, switch)
        self._initialize()

    def _initialize(self):
        self.length: int
        self.length = EnvironmentConsts.WORM_BASIC_LENGTH

        self.direction: str
        self.initial_direction = DirectionConsts.DIRECTIONS[random.randrange(len(DirectionConsts.DIRECTIONS))]
        
        self.color: Tuple[int]
        self.color = self._get_color()

        self.head: List[int]
        self.head = self._get_head()

        self.body: List[List[int]]
        self.body = self._get_body(self.head, self.length, self.initial_direction)
        
        self.direction: str
        self.direction = DirectionConsts.DIRECTOIN_REVERSE[self.initial_direction]
        
        self.eaten_count: int
        self.eaten_count = 0
        
    def drawing(self, display: pygame.display) -> None:
        self._draw_body(display, self.body, self.color)
        self._draw_sense(display)
        # self._draw_eaten_count(display, self.eaten_count, self.body)

    def moving(self) -> None:
        self.direction: str
        self.direction = self._get_random_direction(self.direction, self.switch)

        self.body: List[List[int]]
        self.body = self._get_moved_body(self.body, self.direction, self.speed)
        
    def eating(self, apples: List[Apple]) -> None:
        self.body: List[List[int]]
        self.body, ate = self._get_grown_body(self.body, apples)
        if ate:
            self.eaten_count += 1
            
    def sensing(self):
        pass