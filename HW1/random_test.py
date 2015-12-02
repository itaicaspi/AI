import random
from core import find_route
from ways.draw import plot_path
from ways import load_map_from_csv
from core import node_h, get_link
import matplotlib.pyplot as plt

def generate_tests(count):
    paths = []
    times = []
    roadMap = load_map_from_csv()
    total_junctions = len(roadMap)
    for i in range(0, count):
        path = []
        while not path:
            time = random.randint(1, 24*60)
            init_state_idx = random.randint(0, total_junctions-1)
            final_state_idx = random.randint(0, total_junctions-1)
            print('start: ' + str(init_state_idx) + ' end: ' + str(final_state_idx) + ' time: ' + str(time))
            print('start node: ' +str(roadMap[init_state_idx]))
            print('end node: ' + str(roadMap[final_state_idx]))
            result = find_route(roadMap, init_state_idx, final_state_idx, time)
            path = result[1]
        paths.append(path)
        times.append(result[0])
        plot_path(roadMap, paths[-1])
    plt.show()

    f = open('results/AStarRuns.txt', 'w')
    for time in times:
        f.write(str(time) + ', ')

    f.write('\n')
    for path in paths:
        heuristic_time = node_h(roadMap[path[0]], roadMap[path[-1]])
        f.write(str(heuristic_time) + ', ')

    return paths

if __name__ == '__main__':
    paths = generate_tests(10)
