import amazons_board
from time import clock
import math
import copy

INFINITY = float(6000)

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


@timed
def select_subset(state, possible_moves, w):
    '''
    Implements a three level heuristic algorithm:
    1. Select the best queens to move - the ones with the minimum mobility
    2. Select the best places to move each of the selected queens - the places that will guarantee the highest mobility
    3. Select the best places to shoot the arrow to - the places that will bring the opponent mobility to the minimum

    :param state: the current board state
    :param possible_moves: the list of all possible moves in the current layer
    :param w: the percentage of moves to take
    :return: a list of filtered moves using the given heuristic
    '''
    subset_size = math.ceil(w * len(possible_moves))

    #################################
    # 1st level - select best queen

    # get the current queen locations
    if state.currPlayer == 'white':
        queens_pos = state.whiteQ
    else:
        queens_pos = state.blackQ
    # run heuristic for each queen
    sorted_queens = []
    queen_moves = dict()
    for queen in queens_pos:
        sorted_queens += [(len(state.legalPositions(queen)), queen)]
        queen_moves[queen] = [m for m in possible_moves if m[0] == queen]
    sorted_queens = [q[1] for q in sorted(sorted_queens, key=lambda q: q[0], reverse=True)]

    # filter the possible moves and leave only the selected queens moves
    first_level_moves = []
    for queen in sorted_queens:
        first_level_moves += queen_moves[queen]
        if len(first_level_moves) > subset_size:
            break

    #############################################
    # 2nd level - select where to move the queen

    arrow_moves = dict()
    sorted_queen_moves = []
    # get heuristic value for each queen move
    for move in first_level_moves:
        sorted_queen_moves += [(len(state.legalPositions(move[1])), move)]
        arrow_moves[move] = [m for m in possible_moves if m[1] == move[1]]
    sorted_queen_moves = [m[1] for m in sorted(sorted_queen_moves, key=lambda q: q[0], reverse=True)]

    # filter the possible moves and leave only the selected queens moves
    second_level_moves = []
    for move in sorted_queen_moves:
        second_level_moves += arrow_moves[move]
        if len(second_level_moves) > subset_size:
            break


    #############################################
    # 3rd level - select where to shoot the arrow

    sorted_arrow_moves = []
    # get heuristic value for each arrow move
    for move in second_level_moves:
        new_state = copy.deepcopy(state)
        new_state.doMove(move)
        u = len(new_state.legalMoves())
        sorted_arrow_moves += [(u, move)]
    sorted_arrow_moves = [m[1] for m in sorted(sorted_arrow_moves, key=lambda m: m[0])]

    # take only the necessary number of moves
    third_level_moves = sorted_arrow_moves[0:subset_size]

    return third_level_moves


state = amazons_board.amazonsBoard()
for i in range(0, 10):
    state.board[2][i] = 'a'
state.board[3][1] = 'a'
state.board[4][1] = 'a'
state.board[4][0] = 'a'
state.board[3][8] = 'a'
state.board[4][8] = 'a'
state.board[4][9] = 'a'
'''state.printBoard()'''
selected_moves = select_subset(state, state.legalMoves(), 0.1)
print(selected_moves)
print(len(selected_moves))

