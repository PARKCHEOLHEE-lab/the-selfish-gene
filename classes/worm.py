import random
import pygame
import math
import copy
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
    
    def _get_nearest_apple(self, head: List[int], apples: List[Apple]) -> bool:
        sense_origin = [
            head[0] + EnvironmentConsts.WORM_SIZE/ 2, 
            head[1] + EnvironmentConsts.WORM_SIZE/ 2
        ]
        
        nearest_apple = None
        nearest_distance = math.inf
        
        for apple in apples:
            apple_x = apple.position[0] - EnvironmentConsts.WORM_SIZE / 2
            apple_y = apple.position[1] - EnvironmentConsts.WORM_SIZE / 2
            apple_position = [apple_x, apple_y]
            
            haed_to_apple = math.sqrt(
                (apple_position[0] - sense_origin[0])**2 + (apple_position[1] - sense_origin[1])**2
            )
            
            if haed_to_apple <= EnvironmentConsts.WORM_SENSE:
                if nearest_apple is None:
                    nearest_apple = apple
                    nearest_distance = haed_to_apple
                
                elif haed_to_apple < nearest_distance:
                    nearest_apple = apple
                    nearest_distance = haed_to_apple             
        
        return nearest_apple

    def _get_direction_by_sense(self, head: List[int], nearest_apple: Apple, direction: str):
        
        head_x = head[0]
        head_y = head[1]
        apple_x = nearest_apple.position[0] - EnvironmentConsts.WORM_SIZE / 2
        apple_y = nearest_apple.position[1] - EnvironmentConsts.WORM_SIZE / 2 
        
        vector_head_to_apple = [apple_x - head_x, apple_y - head_y]
        vector_head_to_apple_radians = math.atan2(vector_head_to_apple[1], vector_head_to_apple[0])
        vector_head_to_apple_degrees = math.degrees(vector_head_to_apple_radians)

        vector_up = [0, 1]
        vector_down = [0, -1]
        vector_right = [1, 0]
        vector_left = [-1, 0]
        
        unit_vectors = [vector_left, vector_up, vector_right, vector_down]
        unit_vectors_directions = [DirectionConsts.DIRECTION_LEFT, DirectionConsts.DIRECTION_DOWN, DirectionConsts.DIRECTION_RIGHT, DirectionConsts.DIRECTION_UP]
        
        if direction == DirectionConsts.DIRECTION_UP:
            unit_vectors.remove(vector_down) 
            unit_vectors_directions.remove(DirectionConsts.DIRECTION_DOWN)
        elif direction == DirectionConsts.DIRECTION_DOWN:
            unit_vectors.remove(vector_up) 
            unit_vectors_directions.remove(DirectionConsts.DIRECTION_UP)
        elif direction == DirectionConsts.DIRECTION_LEFT:
            unit_vectors.remove(vector_right) 
            unit_vectors_directions.remove(DirectionConsts.DIRECTION_RIGHT)
        elif direction == DirectionConsts.DIRECTION_RIGHT:
            unit_vectors.remove(vector_left)
            unit_vectors_directions.remove(DirectionConsts.DIRECTION_LEFT)
    
        most_similar_direction = direction
        degree_diff = math.inf

        for unit_vector, unit_vector_direction in zip(unit_vectors, unit_vectors_directions):
            unit_vector_radians = math.atan2(unit_vector[1], unit_vector[0])
            unit_vector_degrees = math.degrees(unit_vector_radians)
            
            diff = abs(vector_head_to_apple_degrees - unit_vector_degrees)
            if  diff < degree_diff:
                most_similar_direction = unit_vector_direction
                degree_diff = diff
                            
        return most_similar_direction
    
    def _get_gene(self, speed: int, sense: float, switch: float):

        probability = random.random()
        if probability < EnvironmentConsts.WORM_EVOLVING_PROBABILITY_TRISECT:
            if random.random() < EnvironmentConsts.WORM_EVOLVING_PROBABILITY_BISECT:
                speed += 1
            if random.random() < EnvironmentConsts.WORM_EVOLVING_PROBABILITY_BISECT:
                sense += 10
            if random.random() < EnvironmentConsts.WORM_EVOLVING_PROBABILITY_BISECT:
                switch += 0.03
        
        elif (
            EnvironmentConsts.WORM_EVOLVING_PROBABILITY_TRISECT 
            <= probability 
            < EnvironmentConsts.WORM_EVOLVING_PROBABILITY_TRISECT * 2
        ):
            if random.random() < EnvironmentConsts.WORM_EVOLVING_PROBABILITY_BISECT:
                speed -= 1
            if random.random() < EnvironmentConsts.WORM_EVOLVING_PROBABILITY_BISECT:
                sense -= 10
            if random.random() < EnvironmentConsts.WORM_EVOLVING_PROBABILITY_BISECT:
                switch -= 0.03
          
        return speed, sense, switch
        
        

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

    def moving(self, apples: List[Apple]) -> None:
        self.direction: str
        self.direction = self._get_random_direction(self.direction, self.switch)
        
        nearest_apple = self._get_nearest_apple(self.body[-1], apples)
        if nearest_apple is not None:
            self.direction = self._get_direction_by_sense(self.body[-1], nearest_apple, self.direction)
        
        self.body: List[List[int]]
        self.body = self._get_moved_body(self.body, self.direction, self.speed)
        
    def eating(self, apples: List[Apple]) -> None:
        self.body: List[List[int]]
        ate: bool
        
        self.body, ate = self._get_grown_body(self.body, apples)
        self.eaten_count += bool(ate)
        
    def evolving(self) -> None:
        self.speed: int
        self.sense: float
        self.switch: float
        
        self.speed, self.sense, self.switch = self._get_gene(self.speed, self.sense, self.switch)
        