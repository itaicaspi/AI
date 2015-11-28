import ways
from collections import namedtuple
from math import sqrt
from ways import load_map_from_csv
from ways.info import SPEED_RANGES

# define class Node
Node = namedtuple('Node',
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


def astar(roads, init_state, final_state, cost, h, t0):
    hi = h(init_state, final_state)
    open = [Node(init_state, [], 0, hi, hi)]
    close = []
    while open:
        current_node = open.pop(0)
        close = [current_node] + close
        if current_node.state == final_state:
            return build_path(current_node)
        for s in node_succ(roads, current_node.state):
            new_g = current_node.g + cost(roads, current_node.state, s, t0)
            old_node = [n for n in open if n.state == s]
            if old_node:
                old_node = old_node[0]
                if new_g < old_node.g:
                    new_node = Node(old_node.state, current_node, new_g, old_node.h, new_g + old_node.h)
                    open = [n for n in open if n.state is not new_node.state]
                    insert_node(open, new_node)
            else:
                old_node = [n for n in close if n.state == s]
                if old_node:
                    old_node = old_node[0]
                    if new_g < old_node.g:
                        new_node = Node(old_node.state, current_node, new_g, old_node.h, new_g + old_node.h)
                        close = [n for n in close if n.state is not new_node.state]
                        insert_node(open, new_node)
                else:
                    new_node = Node(s, current_node, new_g, h(s, final_state), new_g + h(s, final_state))
                    insert_node(open, new_node)
    return []


def l2_dist(s1, s2):
    return sqrt((s2.lon-s1.lon)**2 + (s2.lat-s1.lat)**2)


def node_cost(roads, s1, s2, t):
    link = [l for l in s1.links if l.target == s2.index]
    speed = sum(SPEED_RANGES[link[0].highway_type])/2  # takes the average speed for the road type
    dist = l2_dist(s1, s2)
    return dist / speed # returns the average time for the road


def node_h(s, final_state):
    dist = l2_dist(final_state, s)
    speed = 70
    return dist / speed


def find_route(roadMap, source, target, start_time):
    return astar(roadMap, roadMap[source], roadMap[target], node_cost, node_h, start_time)


def load_map_and_find_route(source, target, start_time, count):
    roadMap = load_map_from_csv(count=count)
    return astar(roadMap, roadMap[source], roadMap[target], node_cost, node_h, start_time)
