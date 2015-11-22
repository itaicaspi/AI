import ways

def astar(init_junction, final_junction, cost, h, t0):
    hi = h(init_junction)
    open = [init_junction]
    close = []
    while open != []:
        current_junction = open[0]
        close = [current_junction] + close
        if current_junction.index == final_junction.index:
            return path
        for l in current_junction.links:

