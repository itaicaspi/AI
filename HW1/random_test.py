import random
from core import find_route, find_route_timed
from ways.draw import plot_path
from ways import load_map_from_csv
from core import node_h, get_link, node_h_timed
import matplotlib.pyplot as plt

def generate_tests(count, finder, h):
    paths = []
    times = []
    roadMap = load_map_from_csv()
    total_junctions = len(roadMap)
    f = open('results/AStarRuns_timed.txt', 'w')
    for i in range(0, count):
        result = []
        while not result:
            time = random.randint(1, 24*60)
            init_state_idx = random.randint(0, total_junctions-1)
            final_state_idx = random.randint(0, total_junctions-1)
            f.write('start: ' + str(init_state_idx) + ' end: ' + str(final_state_idx) + ' time: ' + str(time) + '\n')
            #print('start node: ' + str(roadMap[init_state_idx]))
            #print('end node: ' + str(roadMap[final_state_idx]))
            result = finder(roadMap, init_state_idx, final_state_idx, time)
        f.write('path: ' + str(result[1]) + '\n')
        f.write('actual time: ' + str(result[0]) + '\n')
        f.write('heuristic time: ' + str(h(roadMap[result[1][0]], roadMap[result[1][-1]])) + '\n\n')
        paths.append(result[1])
        times.append(result[0])
        plot_path(roadMap, paths[-1])

    g = open('results/AStarRuns_timed_matlab.txt', 'w')
    for time in times:
        g.write(str(time) + ', ')

    g.write('\n')
    for path in paths:
        heuristic_time = h(roadMap[path[0]], roadMap[path[-1]])
        g.write(str(heuristic_time) + ', ')

    plt.show()
    return paths

if __name__ == '__main__':
    #paths = generate_tests(20, find_route, node_h)
    paths = generate_tests(20, find_route_timed, node_h_timed)

