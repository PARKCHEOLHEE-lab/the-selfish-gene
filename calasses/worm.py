import pygame
import random
import math
from typing import List, Tuple

from constants import EnvironmentConsts, ColorConsts, DirectionConsts, DisplayConsts



class WormHelper:
    
    def _get_color(self) -> Tuple[int]:
        return (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255)
        )
    
    def _get_head(self) -> Tuple[int]:
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
        self.direction = DirectionConsts.DIRECTIONS[random.randrange(len(DirectionConsts.DIRECTIONS))]
        
        self.color: Tuple[int]
        self.color = self._get_color()

        self.head: List[int]
        self.head = self._get_head()

        self.body: List[List[int]]
        self.body = self._get_body(self.head, self.length, self.direction)
        
    def show(self, display: pygame.display) -> None:
        self._draw_body(display, self.body, self.color)
        self._draw_sense(display)

    def move_randomly(self) -> None:
        possible_directions = []
        for dir in DirectionConsts.DIRECTIONS:
            if dir != self.direction and self.direction != DirectionConsts.DIRECTOIN_REVERSE[dir]:
                possible_directions.append(dir)
                
        if random.random() < self.switch:
            new_direction = random.choice(possible_directions)
            self.direction = new_direction
        
        self._move()
            
    def _move(self) -> None:
        new_head = self.body[-1].copy()
        
        if self.direction == DirectionConsts.DIRECTION_UP:
            new_head[1] -= EnvironmentConsts.WORM_SIZE * self.speed
            
        if self.direction == DirectionConsts.DIRECTION_DOWN:
            new_head[1] += EnvironmentConsts.WORM_SIZE * self.speed

        if self.direction == DirectionConsts.DIRECTION_LEFT:
            new_head[0] -= EnvironmentConsts.WORM_SIZE * self.speed

        if self.direction == DirectionConsts.DIRECTION_RIGHT:
            new_head[0] += EnvironmentConsts.WORM_SIZE * self.speed
        
        is_it_out_of_width = 0 > new_head[0] or new_head[0] > DisplayConsts.WIDTH - EnvironmentConsts.WORM_SIZE
        is_it_out_of_height = 0 > new_head[1] or new_head[1] > DisplayConsts.HEIGHT - EnvironmentConsts.WORM_SIZE
        
        if not is_it_out_of_width and not is_it_out_of_height:
            self.body.pop(0)
            self.body.append(new_head)


def draw_grid(display):
    for wi in range(1, int(DisplayConsts.WIDTH // EnvironmentConsts.WORM_SIZE)):
        pygame.draw.line(display, ColorConsts.GRAY, [wi * EnvironmentConsts.WORM_SIZE, 0], [wi * EnvironmentConsts.WORM_SIZE, DisplayConsts.HEIGHT], 1)
        
    for hi in range(1, int(DisplayConsts.HEIGHT // EnvironmentConsts.WORM_SIZE)):
        pygame.draw.line(display, ColorConsts.GRAY, [0, hi * EnvironmentConsts.WORM_SIZE], [DisplayConsts.WIDTH, hi * EnvironmentConsts.WORM_SIZE], 1)


def main():
    random.seed(777)
        
    pygame.init()
    pygame.display.set_caption('The Selfish Gene')

    display = pygame.display.set_mode((DisplayConsts.WIDTH, DisplayConsts.HEIGHT))
    
    generation = 50
    population = 15
    worms = [Worm() for _ in range(population)]
    
    game_over = False
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                    
        display.fill(ColorConsts.BLACK)
        draw_grid(display)
        
        for worm in worms:
            worm.show(display)
            worm.move_randomly()
        
        pygame.display.update()
        
        pygame.time.Clock().tick(DisplayConsts.FRAME_SPEED)

    pygame.quit()
    
if __name__ == "__main__":
    main()