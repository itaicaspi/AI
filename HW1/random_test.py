import random
from core import find_route

def generate_tests(count, total_junctions):
    paths = []
    for i in range(0, count):
        path = []
        while not path:
            time = random.randint(1, 24*60)
            init_state_idx = random.randint(0, total_junctions-1)
            final_state_idx = random.randint(0, total_junctions-1)
            path = find_route(init_state_idx, final_state_idx, time, total_junctions)
        paths.append(path)
    return paths

paths = generate_tests(20, 100)
print(paths)
