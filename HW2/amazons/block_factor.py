import amazons_board
from time import clock

def timed(f):
    '''decorator for printing the timing of functions
    usage:
    @timed
    def some_funcion(args...):'''

    def wrap(*x, **d):
        start = clock()
        res = f(*x, **d)
        print(f.__name__, ':', clock() - start)
        return res
    return wrap

def count_unblocked_neighbours(state, move):
    qx, qy = move[1]
    ax, ay = move[2]
    count = 0
    # check if the arrow is shoot on one of the neighbour cells
    if abs(qx - ax) <= 1 and abs(qy - ay) <= 1:
        count -= 1

    # count free neighbour cells
    if qx > 0:
        if state.board[qx-1][qy] == ' ':
            count += 1
        if qy > 0:
            if state.board[qx-1][qy-1] == ' ':
                count += 1
        if qy < 9:
            if state.board[qx-1][qy+1] == ' ':
                count += 1
    if qx < 9:
        if state.board[qx+1][qy] == ' ':
            count += 1
        if qy > 0:
            if state.board[qx+1][qy-1] == ' ':
                count += 1
        if qy < 9:
            if state.board[qx+1][qy+1] == ' ':
                count += 1
    if qy > 0:
        if state.board[qx][qy-1] == ' ':
            count += 1
    if qy < 9:
        if state.board[qx][qy+1] == ' ':
            count += 1

    return count


@timed
def test(state):
    count = 0
    sorted_moves = []
    for move in state.legalMoves():
        u = count_unblocked_neighbours(state, move)
        sorted_moves += [(u, move)]

    sorted_moves = sorted(sorted_moves, key=lambda m: m[0], reverse=True)

    return sorted_moves[0:20]


state = amazons_board.amazonsBoard()
'''for i in range(0, 10):
    state.board[2][i] = 'a'
state.board[3][1] = 'a'
state.board[4][1] = 'a'
state.board[4][0] = 'a'
state.board[3][8] = 'a'
state.board[4][8] = 'a'
state.board[4][9] = 'a'
state.printBoard()'''
print(test(state))

