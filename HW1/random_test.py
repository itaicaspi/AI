import random
from core import find_route
from ways.draw import plot_path
from ways import load_map_from_csv
import matplotlib.pyplot as plt

def generate_tests(count, total_junctions):
    paths = []
    roadMap = load_map_from_csv(count=total_junctions)
    for i in range(0, count):
        path = []
        while not path:
            time = random.randint(1, 24*60)
            init_state_idx = random.randint(0, total_junctions-1)
            final_state_idx = random.randint(0, total_junctions-1)
            path = find_route(roadMap, init_state_idx, final_state_idx, time)
        paths.append(path)
        #plot_path(roadMap, path)
    #plt.show()
    return paths

paths = generate_tests(100, 1000)
print(paths)
