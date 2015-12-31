from __future__ import division, print_function
import abstract_selective_player
from utils import MiniMaxWithAlphaBetaPruning, INFINITY, run_with_limited_time, ExceededTimeError
import time
import abstract
from ..selective_minimax_with_calmness_criteria import SelectiveMiniMaxWithAlphaBetaPruningAndCalmnessCriteria
import math
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

    def get_w(self, k):
        if k == 2:
            return 0.25
        elif k == 10:
            return 0.5
        elif k == 50:
            return 0.75
        else:
            return 1
        return 1

    def get_move(self, board_state, possible_moves):
        self.clock = time.process_time()
        self.time_for_current_move = self.time_remaining_in_round / self.turns_remaining_in_round - 0.05
        if len(possible_moves) == 1:
            return possible_moves[0]

        current_depth = 1
        prev_alpha = -INFINITY

        # Choosing an arbitrary move:
        best_move = possible_moves[0]

        minimax = SelectiveMiniMaxWithAlphaBetaPruningAndCalmnessCriteria(self.utility, self.color, self.no_more_time, self.w, 20)

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
        return '{} {}'.format(abstract.AbstractPlayer.__repr__(self), 'improvedSelectivePlayer')

""" c:\python34\python run_amazons.py 3 3 3 y simple_player random_player
"""