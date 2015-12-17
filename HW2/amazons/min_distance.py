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


def printBoard(board):
    print('\n  ' + '-' * 31)
    for i in range(10):
        print(str(i) + ' |', end='')
        for j in range(10):
            print(board[i][j], end=' |')
        print('\n  ' + '-' * 31)
    print('   0  1  2  3  4  5  6  7  8  9  \n')


def legalPositions(pos, state, board, max_dist):
    a, b = pos
    positions = []
    range_up = range(b - 1, -1, -1)
    range_down = range(b + 1, 10, 1)
    range_left = range(a - 1, -1, -1)
    range_right = range(a + 1, 10, 1)
    # moves are considered legal only if were not visited before
    # line positions.
    for i in range_up:
        if state.board[a][i] != ' ':
            break
        elif board[a][i] == max_dist:
            positions += [(a, i)]
    for i in range_down:
        if state.board[a][i] != ' ':
            break
        elif board[a][i] == max_dist:
            positions += [(a, i)]
    # row positions.
    for j in range_left:
        if state.board[j][b] != ' ':
            break
        elif board[j][b] == max_dist:
            positions += [(j, b)]
    for j in range_right:
        if state.board[j][b] != ' ':
            break
        elif board[j][b] == max_dist:
            positions += [(j, b)]
    # diagonal positions.
    for j, i in zip(range_left, range_up):
        if state.board[j][i] != ' ':
            break
        elif board[j][i] == max_dist:
            positions += [(j, i)]
    for j, i in zip(range_right, range_down):
        if state.board[j][i] != ' ':
            break
        elif board[j][i] == max_dist:
            positions += [(j, i)]
    for j, i in zip(range_left, range_down):
        if state.board[j][i] != ' ':
            break
        elif board[j][i] == max_dist:
            positions += [(j, i)]
    for j, i in zip(range_right, range_up):
        if state.board[j][i] != ' ':
            break
        elif board[j][i] == max_dist:
            positions += [(j, i)]

    return positions


def dist_map(state, color, max_depth=9):
    """
    returns a map of distances to each one of the cells
    :param state: the current game state
    :param color: the player color ('W' for white, 'B' for black)
    :param max_depth: the maximum depth for the search
    :return: a board map with the distance for each cell and max_depth for unreachable cells
    """
    idx = range(10)
    board = [[max_depth for x in idx] for x in idx]

    if color == 'W':
        positions = state.whiteQ
    else:
        positions = state.blackQ

    for qu in positions:
        board[qu[0]][qu[1]] = 0

    for dist in range(1, max_depth):
        if len(positions) == 0:
            break
        new_positions = []
        for pos in positions:
            for move in legalPositions(pos, state, board, max_depth):
                x, y = move
                board[x][y] = dist
                new_positions += [move]
        positions = new_positions

    return board


def cell_owners(state, max_depth):
    """
    Calculates the cell ownership balance. positive if white wins, negative if black wins
    :param state: the current state
    :param max_depth: the maximum depth to search for
    :return: the cell ownership balance
    """
    white_dist_map = dist_map(state, 'W', max_depth)
    black_dist_map = dist_map(state, 'B', max_depth)
    count = 0
    idx = range(10)
    for y in idx:
        for x in idx:
            diff = black_dist_map[x][y] - white_dist_map[x][y]
            count += (diff > 0) - (diff < 0)
    return count


@timed
def test(state):
    count = 0
    max_depth = 9
    for i in range(0, len(state.legalMoves())):
        count = cell_owners(state, max_depth)
    print(count)


state = amazons_board.amazonsBoard()
'''for i in range(0, 10):
    state.board[2][i] = 'a'
state.board[3][1] = 'a'
state.board[4][1] = 'a'
state.board[4][0] = 'a'
state.board[3][8] = 'a'
state.board[4][8] = 'a'
state.board[4][9] = 'a'''''
#state.printBoard()
test(state)

