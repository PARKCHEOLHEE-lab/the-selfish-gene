import json
import os
import matplotlib.pyplot as plt

class VisualizerHelper:
    def _to_dict(self, data_path):

        with open(data_path, "r") as f:
            collections = json.load(f) 

        return collections

class Visualizer(VisualizerHelper):
    def __init__(self, data):
        self.data = data
        
        self.visualize_result()
        
    def visualize_result(self):
        collections = self._to_dict(self.data)
        
        results_dir_path = os.path.abspath(os.path.join(__file__, "..", "results"))
        if not os.path.isdir(results_dir_path):
            os.mkdir(results_dir_path)
        
        dir_name = os.path.abspath(self.data).split("\\")[-1]
        save_path = os.path.join(results_dir_path, f"{dir_name}")
        if not os.path.isdir(save_path):
            os.mkdir(save_path)
        
        generation = list(range(len(collections) - 1))
        
        flattened_speed = [speed for collection in list(collections.values())[1:] for speed in collection["speed"]]
        min_speed = min(flattened_speed)
        max_speed = max(flattened_speed)

        fig_speed, ax_speed = plt.subplots(1, 1, figsize=(10 + max(generation) / 8, 10))
        ax_speed.set_yticks(range(min_speed - 1, max_speed + 1))
        ax_speed.set_ylim([min_speed - 1, max_speed + 1])
        ax_speed.set_xticks([g for g in generation if g % 2 == 0])
        ax_speed.set_xlabel("generation")
        ax_speed.set_ylabel("speed")

        flattened_sense = [sense for collection in list(collections.values())[1:] for sense in collection["sense"]]
        min_sense = min(flattened_sense)
        max_sense = max(flattened_sense)

        fig_sense, ax_sense = plt.subplots(1, 1, figsize=(10 + max(generation) / 8, 10))
        ax_sense.set_yticks(range(min_sense - 1, max_sense + 1, 20))
        ax_sense.set_ylim([min_sense - 15, max_sense + 15])
        ax_sense.set_xticks([g for g in generation if g % 2 == 0])
        ax_sense.set_xlabel("generation")
        ax_sense.set_ylabel("sense")

        fig_switch, ax_switch = plt.subplots(1, 1, figsize=(10 + max(generation) / 8, 10))

        ax_switch.set_yticks([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])
        ax_switch.set_ylim([-0.1, 1.1])
        ax_switch.set_xticks([g for g in generation if g % 2 == 0])
        ax_switch.set_xlabel("generation")
        ax_switch.set_ylabel("switch")

        all_avg_speed = []
        all_avg_sense = []
        all_avg_switch = []
        for g, collection in collections.items():
            if g == "preset":
                continue
            
            population_speed = collection["speed"]
            avg_speed = sum(population_speed) / len(population_speed)
            ax_speed.scatter([g] * len(population_speed), population_speed, color='red')
            ax_speed.scatter(g, avg_speed, color="red", marker="x")
            all_avg_speed.append(avg_speed)

            population_sense = collection["sense"]
            avg_sense = sum(population_sense) / len(population_sense)
            ax_sense.scatter([g] * len(population_sense), population_sense, color='green')  
            ax_sense.scatter(g, avg_sense, color="green", marker="x")
            all_avg_sense.append(avg_sense)

            population_switch = collection["switch"]
            avg_switch = sum(population_switch) / len(population_switch)
            ax_switch.scatter([g] * len(population_switch), population_switch, color='blue')  
            ax_switch.scatter(g, avg_switch, color="blue", marker="x")
            all_avg_switch.append(avg_switch)

        ax_speed.plot(generation, all_avg_speed, color="red")
        ax_sense.plot(generation, all_avg_sense, color="green")
        ax_switch.plot(generation, all_avg_switch, color="blue")

        fig_speed.savefig(os.path.join(save_path, "speed.png"))
        fig_sense.savefig(os.path.join(save_path, "sense.png"))
        fig_switch.savefig(os.path.join(save_path, "switch.png"))
        
if __name__ == "__main__":
    Visualizer("data/result-2023-08-19 19-54-56.402991.json")