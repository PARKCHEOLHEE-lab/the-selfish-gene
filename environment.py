import os
import json
import random
import pygame
import datetime
import argparse

from classes.constants import EnvironmentConsts, ColorConsts, DisplayConsts
from classes.worm import Worm
from classes.apple import Apple
from typing import List, Tuple

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
            
    def _draw_status(
        self, 
        display: pygame.display, 
        gen: int, 
        pop: int, 
        avg_speed: float,
        avg_sense: float,
        avg_switch: float,
    ) -> None:
        
        font_x = DisplayConsts.STATUS_FONT_X_POS
        font_size = DisplayConsts.STATUS_FONT_SIZE
        font = pygame.font.Font(None, font_size)
        
        gen_position = [font_x, font_x]
        gen_string = f"generation: {gen}"
        gen_text_surface = font.render(gen_string, False, ColorConsts.GREEN)
        display.blit(gen_text_surface, gen_position)
        
        pop_position = [font_x, gen_position[1] + font_size]
        pop_string = f"population: {pop}"
        pop_text_surface = font.render(pop_string, False, ColorConsts.GREEN)
        display.blit(pop_text_surface, pop_position)
        
        avg_speed_position = [font_x, pop_position[1] + font_size]
        avg_speed_string = f"avg speed: {avg_speed:.2f}"
        avg_speed_text_surface = font.render(avg_speed_string, False, ColorConsts.BLUE)
        display.blit(avg_speed_text_surface, avg_speed_position)
        
        avg_sense_position = [font_x, avg_speed_position[1] + font_size]
        avg_sense_string = f"avg sense: {avg_sense:.2f}"
        avg_sense_text_surface = font.render(avg_sense_string, False, ColorConsts.BLUE)
        display.blit(avg_sense_text_surface, avg_sense_position)
        
        avg_switch_position = [font_x, avg_sense_position[1] + font_size]
        avg_switch_string = f"avg switch: {avg_switch:.2f}"
        avg_switch_text_surface = font.render(avg_switch_string, False, ColorConsts.BLUE)
        display.blit(avg_switch_text_surface, avg_switch_position)
            
    def _get_apples(self, apple_count: int) -> List[Apple]:
        apples = []
        apples_positions = []
        for _ in range(apple_count):
            apple = Apple(except_positions=apples_positions)
            apples.append(apple)
            apples_positions.append(apple.position)

        return apples
    
    def _get_avg_genes(self, worms: List[Worm]) -> Tuple[float]:
        avg_speed = sum([worm.speed for worm in worms]) / len(worms)
        avg_sense = sum([worm.sense for worm in worms]) / len(worms)
        avg_switch = sum([worm.switch for worm in worms]) / len(worms)
        
        return avg_speed, avg_sense, avg_switch
    
    def _save_result_data(self, collections: dict):
        if not os.path.isdir("data"):
            os.mkdir("data")
            
        current_date_time = datetime.datetime.now()
        formatted_date_time = current_date_time.strftime('%Y-%m-%d %H:%M:%S.%f')
        formatted_date_time_for_filename = formatted_date_time.replace(':', '-')
            
        with open(f"data/result-{formatted_date_time_for_filename}.json", "w") as f:
            json.dump(collections, f, indent=4)
            
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
        seed = self.seed
        
        apple_count = EnvironmentConsts.APPLE_COUNT
        
        worms: List[Worm]
        worms = [Worm() for _ in range(pop)]
        
        collections = {
            "preset": {
                "generation": gen,
                "population": pop,
                "seed": seed,
            },
            "0": {
                "speed": [EnvironmentConsts.WORM_SPEED_ORIGINAL],
                "sense": [EnvironmentConsts.WORM_SENSE_ORIGINAL],
                "switch": [EnvironmentConsts.WORM_SWITCH_ORIGINAL],
            }
        }

        is_pop_1 = False
        for g in range(gen):
            
            if is_pop_1:
                break
            
            apples: List[Apple]
            apples = self._get_apples(apple_count)

            over = False
            while not over:
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        over = True
                        
                avg_speed, avg_sense, avg_switch = self._get_avg_genes(worms)
                            
                self.display.fill(ColorConsts.BLACK)
                self._draw_grid(self.display)
                self._draw_status(
                    self.display, 
                    g, 
                    pop, 
                    avg_speed, 
                    avg_sense, 
                    avg_switch
                )
                
                for apple in apples:
                    apple.draw(self.display)

                for worm in worms:
                    worm.moving(apples)
                    worm.eating(apples)
                    worm.drawing(self.display, apples)
                    
                if len(apples) == 0:
                    over = True
                    
                pygame.display.update()
                pygame.time.Clock().tick(DisplayConsts.FRAME_SPEED)
                
            worms = [worm for worm in worms if worm.eaten_count > 0]
            pop = len(worms)

            gene_per_generation = {
                "speed": [],
                "sense": [],
                "switch": [],
            }

            for worm in worms:
                worm.reset()
                worm.evolving(g + 1)
                
                gene_per_generation["speed"].append(worm.speed)
                gene_per_generation["sense"].append(worm.sense)
                gene_per_generation["switch"].append(worm.switch)
            
            collections[f"{g + 1}"] = gene_per_generation
            
            if g % 2 == 0:
                apple_count -= 2
                
            if apple_count == 0:
                over = True
                
            if pop == 1:
                over = True
                is_pop_1 = True

        pygame.quit()
        
        self._save_result_data(collections)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("generation", type=int)
    parser.add_argument("population", type=int)
    parser.add_argument("seed", type=int)
    
    args = parser.parse_args()
    
    env = Environment(**args.__dict__)
    env.simulate()