from __future__ import division, print_function
import abstract
from utils import MiniMaxWithAlphaBetaPruning, INFINITY, run_with_limited_time, ExceededTimeError
import time


class Player(abstract.AbstractPlayer):
    def __init__(self, setup_time, player_color, time_per_k_turns, k):
        abstract.AbstractPlayer.__init__(self, setup_time, player_color, time_per_k_turns, k)
        self.clock = time.process_time()

        # We are simply providing (remaining time / remaining turns) for each turn in round.
        # Taking a spare time of 0.05 seconds.
        self.turns_remaining_in_round = self.k
        self.time_remaining_in_round = self.time_per_k_turns
        self.time_for_current_move = self.time_remaining_in_round / self.turns_remaining_in_round - 0.05

    def get_move(self, board_state, possible_moves):
        self.clock = time.process_time()
        self.time_for_current_move = self.time_remaining_in_round / self.turns_remaining_in_round - 0.05
        if len(possible_moves) == 1:
            return possible_moves[0]

        current_depth = 1
        prev_alpha = -INFINITY

        # Choosing an arbitrary move:
        best_move = possible_moves[0]

        minimax = MiniMaxWithAlphaBetaPruning(self.utility, self.color, self.no_more_time)

        # Iterative deepening until the time runs out.
        while True:
            if self.no_more_time():
                print('no more time')
                break

            print('going to depth: {}, remaining time: {}, prev_alpha: {}, best_move: {}'.format(
                current_depth, self.time_for_current_move - (time.process_time() - self.clock), prev_alpha, best_move))

            try:
                (alpha, move), run_time = run_with_limited_time(
                    minimax.search, (board_state, current_depth, -INFINITY, INFINITY, True), {},
                    self.time_for_current_move - (time.process_time() - self.clock))
            except (ExceededTimeError, MemoryError):
                print('no more time')
                break

            prev_alpha = alpha
            best_move = move

            if alpha == INFINITY:
                print('the move: {} will guarantee victory.'.format(best_move))
                break

            if alpha == -INFINITY:
                print('all is lost')
                break

            current_depth += 1

        if self.turns_remaining_in_round == 1:
            self.turns_remaining_in_round = self.k
            self.time_remaining_in_round = self.time_per_k_turns
        else:
            self.turns_remaining_in_round -= 1
            self.time_remaining_in_round -= (time.process_time() - self.clock)
        return best_move


    def legalPositions(self, pos, state, board, max_dist):
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


    def dist_map(self, state, color, max_depth=9):
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
                for move in self.legalPositions(pos, state, board, max_depth):
                    x, y = move
                    board[x][y] = dist
                    new_positions += [move]
            positions = new_positions

        return board


    def cell_owners(self, state, max_depth):
        """
        Calculates the cell ownership balance. positive if white wins, negative if black wins
        :param state: the current state
        :param max_depth: the maximum depth to search for
        :return: the cell ownership balance
        """
        white_dist_map = self.dist_map(state, 'W', max_depth)
        black_dist_map = self.dist_map(state, 'B', max_depth)
        count = 0
        idx = range(10)
        for y in idx:
            for x in idx:
                diff = black_dist_map[x][y] - white_dist_map[x][y]
                count += (diff > 0) - (diff < 0)
        return count

    def utility(self, state):
        if not state.legalMoves():
            return INFINITY if state.currPlayer != self.color else -INFINITY

        u = self.cell_owners(state, 9)
        if self.color != 'white':
            u = -u

        return u

    def no_more_time(self):
        return (time.process_time() - self.clock) >= self.time_for_current_move

    def __repr__(self):
        return '{} {}'.format(abstract.AbstractPlayer.__repr__(self), 'min_queen_distances')

""" c:\python34\python run_amazons.py 3 3 3 y simple_player random_player
"""