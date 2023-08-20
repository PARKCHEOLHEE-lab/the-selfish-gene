

### What is natural selection 🦕

[Natural selection](https://www.nhm.ac.uk/discover/what-is-natural-selection.html) is a mechanism of evolution. Organisms that are more adapted to their environment are more likely to survive and pass on the genes that aided their success. This process causes species to change and diverge over time. Natural selection is one of the ways to account for the millions of species that have lived on Earth.  
  
For example, evolving long necks have enabled giraffes to feed on leaves that others can't reach, giving them a competitive advantage. Thanks to a better food source, those with longer necks were able to survive. Those with shorter necks and access to less food would be less likely to survive.

<p align="center">
  <img src="/assets/the-selfish-gene-0.png" width=60%"> <br>
  <a href="https://www.ck12.org/book/ck-12-biology-advanced-concepts/section/10.36/">Giraffes</a> with each other different genes
</p>


  

### Creating environment and defining genes

Let's do a simple simulation based on the basic concepts and understanding of natural selection. First, we need to create an `environment` and `populations` that have the `genes` to do so. The worm will live in the environment that I created in a two-dimensional form, and the worm will have the following genes to survive to eat the feeds:

*   speed: The moving speed of the worm
*   sense: The distance for sensing feeds
*   switch: The direction change probability (when there are no feeds within the distance for sensing)

<br>
  
I defined a class as below. Worms use the `moving` function that interacts with genes to act.
```python
    class WormGene:
        def __init__(self, speed: int, sense: float, switch: float) -> None:
            self.speed = speed
            self.sense = sense
            self.switch = switch


    class Worm(WormGene, WormHelper):
        def __init__(
            self, 
            speed: int = EnvironmentConsts.WORM_SPEED_ORIGINAL, 
            sense: float = EnvironmentConsts.WORM_SENSE_ORIGINAL, 
            switch: float = EnvironmentConsts.WORM_SWITCH_ORIGINAL
        ):
            WormGene.__init__(self, speed, sense, switch)
            self._initialize()
            

        (...)


        def moving(self, apples: List[Apple]) -> None:
            self.direction: str
            self.direction = self._get_random_direction(self.direction, self.switch)
            
            nearest_apple = self._get_nearest_apple(self.body[-1], apples, self.sense)
            if nearest_apple is not None:
                self.direction = self._get_direction_by_sense(self.body[-1], nearest_apple, self.direction)
            
            self.body: List[List[int]]
            self.body = self._get_moved_body(self.body, self.direction, self.speed)
```
  
<br><br>
  
If you want to see the code for `Worm` I defined, you can see it at the following link. And the environment, worms operate like the below Fig.2: An operation of the environment and worms.

*   [https://github.com/PARKCHEOLHEE-lab/the-selfish-gene/blob/main/classes/worm.py](https://github.com/PARKCHEOLHEE-lab/the-selfish-gene/blob/main/classes/worm.py)

<br>

  
Following whether the sensing circle the worm has contains apples, each worm will have a different operation method. If apples are not within the sensing circle, worms determine the direction randomly by the `switch` gene.  
  
Else, calculate the angle between the worm's movement direction vector and the worm-to-apple vector, and calculate the difference between the angles to `select the vector with the highest similarity`. See the [code](https://github.com/PARKCHEOLHEE-lab/the-selfish-gene/blob/4eec1df9e018ea0b87fe6d3fafac892ab32cd80a/classes/worm.py#L217-L265) for detail of the worm's operation method `_get_direction_by_sense()`.  
  
<br>
<p align="center">
  <img src="/assets/the-selfish-gene-1.gif" width="80%"> <br>
  An operation of the environment and worms
</p>


<br>
  
  
### Simulating natural selection

Now all preparations for the simulation are done. You can simulate natural selection as follows Fig.3: A part of the natural selection simulation  
  
Let's fix the `generation`, `population`, and `seed` for the reproducibility of natural selection simulations, and observe which genes survive. Note that worms that do not eat even one `apple` within one generation will die.  
<br>
<p align="center">
  <img src="/assets/the-selfish-gene-2.gif" width="80%"> <br>
  A part of the natural selection simulation
</p>

<br><br>
  
I set the parameters for generation, population and seed as shown below. I then logged and visualized the results to observe how genes evolve and survive.

*   generation: 100
*   population: 50
*   seed: 6

<br>
  
Let's see the visualized results. The x-axis is generation and the y-axis indicates each gene. And in the figure, I drew a line for `average genes` per generation. The set generation is 100, but it stopped at 70 generations. This is because only one worm survived after that generation.  
  
The `Speed` and `Sense` genes tend to increase gradually over generations. Detecting apples and moving quickly to eat it will of course be advantageous to survival.  
  
In the case of the `Switch` gene, it started with 0.5, but the final evolved worm also returned to 0.5. In this environment, turning direction change too much seems to be against survival.  
  

<p align="center">
  <img src="/assets/the-selfish-gene-3.png" width=85%"> <br>
  Speed
</p>

<p align="center">
  <img src="/assets/the-selfish-gene-4.png" width=85%"> <br>
  Sense
</p>

<p align="center">
  <img src="/assets/the-selfish-gene-5.png" width=85%"> <br>
  Switch
</p>
  
<br> 
  

### A birth of the a super worm

Lastly, I will reproduce the data of the super earthworm that survived until the end in the environment and finish the post.  
  

<p align="center">
  <img src="/assets/the-selfish-gene-6.gif" width=80%"> <br>
  Super worm! It's too fast...<br>
  Speed:13 <br>
  Sense: 450 <br>
  Switch: 0.48
</p>
  
  

### References

*   [https://youtu.be/0ZGbIKd0XrM](https://youtu.be/0ZGbIKd0XrM)
*   [https://github.com/kairess/natural-selection](https://github.com/kairess/natural-selection)