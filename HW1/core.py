import ways
from collections import namedtuple

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
    while current_node is not []:
        path = path + current_node.state
        node = current_node.parent
    return path


def node_succ(roads, state):
    return [roads[l.target] for l in state.links]


def insert_node(l, node):
    l = l.append(node)
    l = sorted(l, key=lambda c: c.f)


def astar(roads, init_state, final_state, cost, h, t0):
    hi = h(init_state)
    open = [Node(init_state, [], 0, hi, hi)]
    close = []
    while open is not []:
        current_node = open[0]
        close = [current_node] + close
        if current_node.state == final_state:
            return build_path(current_node)
        for s in node_succ(roads, current_node.state):
            new_g = current_node.g + cost(current_node.state, s, t0)
            old_node = [n for n in open if n.state == s]
            if old_node is not []:
                old_node = old_node[0]
                if new_g < old_node.g:
                    old_node.g = new_g
                    old_node.parent = current_node
                    old_node.f = old_node.g + old_node.h
                    open = [n for n in open if n.state is not old_node.state]
                    insert_node(open, old_node)
            else:
                old_node = [n for n in close if n.state == s]
                if old_node is not []:
                    old_node = old_node[0]
                    if new_g < old_node.g:
                        old_node.g = new_g
                        old_node.parent = current_node
                        old_node.f = old_node.g + old_node.h
                        close = [n for n in close if n.state is not old_node.state]
                        insert_node(open, old_node)
                else:
                    new_node = Node(s, current_node, new_g, h(s), new_g + h(s))
                    insert_node(open, new_node)
    return []


def node_cost(roads, s1, s2, t):
    link = [l for l in s1.links if l.target == s2.index]
    return roads.link_speed_history(link[0], t)


def node_h(roads, s, final_state):
    return 1
