import random
from core import find_route
from ways.draw import plot_path
from ways import load_map_from_csv
from core import node_h, get_link
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
        plot_path(roadMap, path)
    plt.show()

    f = open('results/AStarRuns.txt', 'w')
    for path in paths:
        actual_time = 0
        for i in range(0,len(path)-1):
            actual_time += roadMap.realtime_link_speed(get_link(roadMap, path[i], path[i+1]))
        f.write(str(actual_time) + ', ')

    f.write('\n')
    for path in paths:
        heuristic_time = node_h(roadMap[path[0]], roadMap[path[-1]])
        f.write(str(heuristic_time) + ', ')

    return paths

if __name__ == '__main__':
    paths = generate_tests(20, 1000)
