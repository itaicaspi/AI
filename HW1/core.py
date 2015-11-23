import ways

def roads_succ(roads, state):
    return [l.target for l in roads.junctions()[state].links]

def astar(init_node, final_node, cost, h, t0):
    hi = h(init_node)
    open = [init_node]
    close = []
    path = []
    while open is not []:
        current_node = open[0]
        close = [current_node] + close
        if current_node.index == final_node.index:
            return path
        for l in current_node.links:
            new_g = current_node.g + cost(current_node.index, l.target)
            old_junction = filter(lambda j: j.index == l.target, open)
            if old_junction is not []:
                if new_g < old_junction.g:
                    old_junction.g = new_g
                    old_junction.parent = current_node
                    old_junction.f = old_junction.g + old_junction.h
                    # remove from open
                    # insert in the sorted position in order
            else:

