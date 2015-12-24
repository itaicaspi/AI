from __future__ import division, print_function
import abstract_selective_player
from utils import MiniMaxWithAlphaBetaPruning, INFINITY, run_with_limited_time, ExceededTimeError
import time
import abstract
import copy
import random

class Player(abstract_selective_player.AbstractSelectivePlayer):
    def __init__(self, setup_time, player_color, time_per_k_turns, k):
        abstract_selective_player.AbstractSelectivePlayer.__init__(self, setup_time, player_color, time_per_k_turns, k)
        self.clock = time.process_time()

        # We are simply providing (remaining time / remaining turns) for each turn in round.
        # Taking a spare time of 0.05 seconds.
        self.turns_remaining_in_round = self.k
        self.time_remaining_in_round = self.time_per_k_turns
        self.time_for_current_move = self.time_remaining_in_round / self.turns_remaining_in_round - 0.05

    def get_w(self):
        return 0.01

    def subset_selection(self, state, w, possible_moves):
        # get the number of moves in the subset
        subset_size = int(w * len(possible_moves))
        print(subset_size)
        '''
        sorted_moves = []

        # insert all moves with their heuristic value into a list and sort it
        for move in possible_moves:
            new_state = copy.deepcopy(state)
            new_state.doMove(move)
            sorted_moves += [(1, move)]
        '''
        sorted_moves = possible_moves
        #random.shuffle(sorted_moves)
        #sorted(sorted_moves, key=random.randint(1, len(possible_moves)), reverse=True)

        # return only the subset_size top elements
        #return [m[1] for m in sorted_moves[0:subset_size]]
        return sorted_moves[0:subset_size]

    def get_move(self, board_state, possible_moves):
        selected_moves = self.subset_selection(board_state, self.w, possible_moves)

        self.clock = time.process_time()
        self.time_for_current_move = self.time_remaining_in_round / self.turns_remaining_in_round - 0.05
        if len(selected_moves) == 1:
            return selected_moves[0]

        current_depth = 1
        prev_alpha = -INFINITY

        # Choosing an arbitrary move:
        best_move = selected_moves[0]

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

    def utility(self, state):
        if not state.legalMoves():
            return INFINITY if state.currPlayer != self.color else -INFINITY

        u = 0
        if self.color == 'white':
            myQueens = state.whiteQ
            enQueens = state.blackQ
        else:
            myQueens = state.blackQ
            enQueens = state.whiteQ

        for mQ in myQueens:
            u += len(state.legalPositions(mQ))
        for eQ in enQueens:
            u -= len(state.legalPositions(eQ))

        return u

    def no_more_time(self):
        return (time.process_time() - self.clock) >= self.time_for_current_move

    def __repr__(self):
        return '{} {}'.format(abstract.AbstractPlayer.__repr__(self), 'selective_simple')

""" c:\python34\python run_amazons.py 3 3 3 y simple_player random_player
"""