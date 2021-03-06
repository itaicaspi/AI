from collections import namedtuple
from ways import load_map_from_csv
from ways.tools import compute_distance
from ways.info import SPEED_RANGES
from pqdict import pqdict

# define class Node
Node = namedtuple('Node', [
            'state',    #  Junction: node junction
            'parent',   #  Node: junction parent
            'g',        #  int: cost of the node
            'h',        #  int: heuristic value of the node
            'f'         #  int: total cost - g + h
           ])

# define class TimedNode - a node with the time of arrival
TimedNode = namedtuple('Node', [
                'state',    #  Junction: node junction
                'parent',   #  Node: junction parent
                'g',        #  int: cost of the node
                'h',        #  int: heuristic value of the node
                'f',        #  int: total cost - g + h
                'time'      #  float: last time we visited the node
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


def get_link(roads, s1, s2):
    link = [l for l in s1.links if l.target == s2.index]
    return link[0]


def astar(roads, init_state, final_state, cost, h, t0):
    hi = h(init_state, final_state)
    open = pqdict({init_state.index: Node(init_state, [], 0, hi, hi)}, key=lambda x: x.f)
    close = dict()
    while open:
        current_node = open.popitem()[1]
        close[current_node.state.index] = current_node
        if current_node.state == final_state:
            return current_node.g, build_path(current_node)
        for s in node_succ(roads, current_node.state):
            new_g = current_node.g + cost(roads, current_node.state, s, t0)
            old_node = open.get(s.index)
            if old_node:
                if new_g < old_node.g:
                    # update node in open
                    new_node = Node(old_node.state, current_node, new_g, old_node.h, new_g + old_node.h)
                    del open[old_node.state.index]
                    open[new_node.state.index] = new_node
            else:
                old_node = close.get(s.index)
                if old_node:
                    if new_g < old_node.g:
                        new_node = Node(old_node.state, current_node, new_g, old_node.h, new_g + old_node.h)
                        del close[old_node.state.index]
                        open[new_node.state.index] = new_node
                else:
                    new_node = Node(s, current_node, new_g, h(s, final_state), new_g + h(s, final_state))
                    open[new_node.state.index] = new_node
    return []


def astar_with_time(roads, init_state, final_state, cost, h, t0):
    hi = h(init_state, final_state)
    open = pqdict({init_state.index: TimedNode(init_state, [], 0, hi, hi, 0)}, key=lambda x: x.f)
    close = dict()
    while open:
        current_node = open.popitem()[1]
        close[current_node.state.index] = current_node
        if current_node.state == final_state:
            return current_node.time, build_path(current_node)
        for s in node_succ(roads, current_node.state):
            new_link = get_link(roads, current_node.state, s)
            real_time_speed = kph_to_mpm(roads.realtime_link_speed(new_link, (t0 + current_node.time) % 1440))    # mpm
            drive_time = (current_node.time + new_link.distance / real_time_speed)  # the time from source to next junction in minutes
            real_time = (t0 + drive_time) % 1440    # the time we will arrive at the next junction in minutes
            new_g = current_node.g + cost(roads, current_node.state, s, t0, real_time) # minutes
            old_node = open.get(s.index)
            if old_node:
                if new_g < old_node.g:
                    new_node = TimedNode(old_node.state, current_node, new_g, old_node.h, new_g + old_node.h, drive_time)
                    del open[old_node.state.index]
                    open[new_node.state.index] = new_node
            else:
                old_node = close.get(s.index)
                if old_node:
                    if new_g < old_node.g:
                        new_node = TimedNode(old_node.state, current_node, new_g, old_node.h, new_g + old_node.h, drive_time)
                        del close[old_node.state.index]
                        open[new_node.state.index] = new_node
                else:
                    new_node = TimedNode(s, current_node, new_g, h(s, final_state), new_g + h(s, final_state), drive_time)
                    open[new_node.state.index] = new_node
    return []


# converts KM per hour to meters per minute
def kph_to_mpm(speed):
    return (1000/60)*speed


# cost function for the regular astar - return time in minutes
def node_cost(roads, s1, s2, t = 0):
    link = get_link(roads, s1, s2)
    speed = kph_to_mpm(roads.realtime_link_speed(link, t))  # mpm
    return link.distance / speed    # minutes


# cost function for astar times, using the new equation - returns time in minutes
def node_cost_timed(roads, s1, s2, t0 = 1, current_time = 1):
    link = get_link(roads, s1, s2)
    focus = roads.return_focus(s1.index)
    focus_sum = 0
    t_h_curr = link.distance/kph_to_mpm(roads.link_speed_history(link, current_time)) # minutes
    for l in focus:
        t_r = 1/roads.realtime_link_speed(l, t0)   # 1/kph
        t_h = 1/roads.link_speed_history(l, t0)    # 1/kph
        focus_sum += t_r/t_h    # number
    return (focus_sum*t_h_curr)/len(focus)  # minutes


# computes time in minutes based on speed in mpm and distance in km
def calculate_time(s1, s2, speed):
    dist = compute_distance(s1.lat, s1.lon, s2.lat, s2.lon)*1000 # meters
    return dist / speed # minutes


# returns heuristic value in minutes
def node_h(s, final_state):
    speed = kph_to_mpm(max(max(SPEED_RANGES)))  # mpm
    return calculate_time(s, final_state, speed) # minutes


# returns timed astar heuristic value in minutes
def node_h_timed(s, final_state):
    return node_h(s, final_state)/6


# runs astar without loading the map and return the actual time also (returns [time, path])
def find_route(roadMap, source, target, start_time):
    return astar(roadMap, roadMap[source], roadMap[target], node_cost, node_h, start_time)


# runs astar timed without loading the map and return the actual time also (returns [time, path])
def find_route_timed(roadMap, source, target, start_time):
    return astar_with_time(roadMap, roadMap[source], roadMap[target], node_cost_timed, node_h_timed, start_time)


def run_astar(source, target, cost=node_cost, h=node_h, start_time=1):
    roadMap = load_map_from_csv()
    return astar(roadMap, roadMap[source], roadMap[target], cost, h, start_time)[1]


def run_astar_with_time(source, target, cost=node_cost_timed, h=node_h_timed, start_time=700):
    roadMap = load_map_from_csv()
    return astar_with_time(roadMap, roadMap[source], roadMap[target], cost, h, start_time)[1]

