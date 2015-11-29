import ways
from collections import namedtuple
from math import sqrt
from ways import load_map_from_csv
from ways.info import SPEED_RANGES

# define class TimedNode
TimedNode = namedtuple('Node',
           ['state',    #  Junction: node junction
            'parent',   #  Node: junction parent
            'g',        #  int: cost of the node
            'h',        #  int: heuristic value of the node
            'f'         #  int: total cost - g + h
           ])


def build_path(node):
    """
    Build the path from the initial node to the final node by traversing up the tree
    :param node: the final node
    :return: the path from the initial node to the final node
    """
    path = []
    current_node = node
    while current_node:
        path.append(current_node.state)
        current_node = current_node.parent
    path.reverse()
    return [s.index for s in path]


def node_succ(roads, state):
    return [roads[l.target] for l in state.links]


def insert_node(l, node):
    l.append(node)
    l = sorted(l, key=lambda c: c.f)


def astar_with_time(roads, init_state, final_state, cost, h, t0):
    hi = h(init_state, final_state)
    current_time = t0
    open = [TimedNode(init_state, [], 0, hi, hi)]
    close = []
    while open:
        current_node = open.pop(0)
        close = [current_node] + close
        if current_node.state == final_state:
            return build_path(current_node)
        for s in node_succ(roads, current_node.state):
            new_g = current_node.g + cost(roads, current_node.state, s, t0, t0 + current_node.g) # g is the current time
            old_node = [n for n in open if n.state == s]
            if old_node:
                old_node = old_node[0]
                if new_g < old_node.g:
                    new_node = TimedNode(old_node.state, current_node, new_g, old_node.h, new_g + old_node.h)
                    open = [n for n in open if n.state is not new_node.state]
                    insert_node(open, new_node)
            else:
                old_node = [n for n in close if n.state == s]
                if old_node:
                    old_node = old_node[0]
                    if new_g < old_node.g:
                        new_node = TimedNode(old_node.state, current_node, new_g, old_node.h, new_g + old_node.h)
                        close = [n for n in close if n.state is not new_node.state]
                        insert_node(open, new_node)
                else:
                    new_node = TimedNode(s, current_node, new_g, h(s, final_state), new_g + h(s, final_state))
                    insert_node(open, new_node)
    return []


def l2_dist(s1, s2):
    mul = 107000
    return mul*sqrt((s2.lon-s1.lon)**2 + (s2.lat-s1.lat)**2)


def calculate_time(s1, s2, speed):
    dist = l2_dist(s1, s2)
    return dist / speed


def node_cost_timed(roads, s1, s2, t0 = 1, current_time = 1):
    link = [l for l in s1.links if l.target == s2.index]
    focus = roads.return_focus(s1.index)
    focus_sum = 0
    t_h_curr = calculate_time(s1, s2, (1000/60)*roads.link_speed_history(link[0], current_time))
    for l in focus:
        t_r = calculate_time(s1, s2, (1000/60)*roads.realtime_link_speed(l, t0))
        t_h = calculate_time(s1, s2, (1000/60)*roads.link_speed_history(l, t0))
        focus_sum += t_r/t_h

    return (focus_sum*t_h_curr)/len(focus)



def node_h(s, final_state):
    speed = (1000/60)*110 # convert to meters per minute
    return calculate_time(s, final_state, speed)


roadMap = load_map_from_csv(count=100)
print('result: ' + str(node_cost_timed(roadMap, roadMap[0], roadMap[1])))
print('go')