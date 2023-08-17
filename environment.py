import random
import pygame

from classes.constants import EnvironmentConsts, ColorConsts, DisplayConsts
from classes.worm import Worm
from classes.apple import Apple

class EnvironmentHelper:
    def _draw_grid(self, display: pygame.display) -> None:
        for wi in range(1, int(DisplayConsts.WIDTH // EnvironmentConsts.WORM_SIZE)):
            pygame.draw.line(
                display, 
                ColorConsts.GRAY, 
                [wi * EnvironmentConsts.WORM_SIZE, 0], 
                [wi * EnvironmentConsts.WORM_SIZE, DisplayConsts.HEIGHT], 
                1
            )
            
        for hi in range(1, int(DisplayConsts.HEIGHT // EnvironmentConsts.WORM_SIZE)):
            pygame.draw.line(
                display, 
                ColorConsts.GRAY, 
                [0, hi * EnvironmentConsts.WORM_SIZE], 
                [DisplayConsts.WIDTH, hi * EnvironmentConsts.WORM_SIZE], 
                1
            )
    

class Environment(EnvironmentHelper):
    def __init__(
        self, 
        seed=EnvironmentConsts.INIT_SEED, 
        generation=EnvironmentConsts.INIT_GENERATION, 
        population=EnvironmentConsts.INIT_POPULATION
    ):
        random.seed(seed)
        pygame.init()
        pygame.display.set_caption('The Selfish Gene')

        self.seed = seed
        self.generation = generation
        self.population = population

        self.display = pygame.display.set_mode((DisplayConsts.WIDTH, DisplayConsts.HEIGHT))
        
    def simulate(self) -> None:
        
        gen = self.generation
        pop = self.population 
        
        for _ in range(gen):
        
            worms = [Worm() for _ in range(pop)]
            apples = []
            apples_positions = []
            for _ in range(EnvironmentConsts.APPLE_COUNT):
                apple = Apple(except_positions=apples_positions)
                apples.append(apple)
                apples_positions.append(apple.position)

            over = False
            while not over:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        over = True
                            
                self.display.fill(ColorConsts.BLACK)
                self._draw_grid(self.display)
                
                for apple in apples:
                    apple.draw(self.display)

                for worm in worms:
                    worm.drawing(self.display)
                    worm.moving(apples)
                    worm.eating(apples)
                    
                if len(apples) == 0:
                    over = True
                    
                pygame.display.update()
                pygame.time.Clock().tick(DisplayConsts.FRAME_SPEED)

        pygame.quit()

if __name__ == "__main__":
    env = Environment()
    env.simulate()