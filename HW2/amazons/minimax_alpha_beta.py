# from __future__ import print_function
from threading import Thread
from queue import Queue
import time
import copy
import math
import numpy
from operator import itemgetter
import random

__author__ = 'Orenk'

INFINITY = float(6000)

class SelectiveMiniMaxWithAlphaBetaPruning:

    def __init__(self, utility, my_color, no_more_time, w):
        """Initialize a MiniMax algorithms with alpha-beta pruning.

        :param utility: The utility function. Should have state as parameter.
        :param my_color: The color of the player who runs this MiniMax search.
        :param no_more_time: A function that returns true if there is no more time to run this search, or false if
                             there is still time left.
        """
        self.utility = utility
        self.my_color = my_color
        self.no_more_time = no_more_time
        self.w = w

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

    def subset_selection(self, state, w, possible_moves):
        # get the number of moves in the subset
        subset_size = math.ceil(w * len(possible_moves))

        sorted_moves = []

        do_random = True

        # insert all moves with their heuristic value into a list and sort it
        if do_random:
            sorted_moves = possible_moves
            random.shuffle(sorted_moves)
            return sorted_moves[0:subset_size]
        else:
            for move in possible_moves:
                new_state = copy.deepcopy(state)
                new_state.doMove(move)
                sorted_moves += [(self.utility(new_state), move)]
            sorted(sorted_moves, key=lambda m: m[0], reverse=True)

            # return only the subset_size top elements
            return [m[1] for m in sorted_moves[0:subset_size]]

    def search(self, state, depth, alpha, beta, maximizing_player):
        """Start the MiniMax algorithm.

        :param state: The state to start from.
        :param depth: The maximum allowed depth for the algorithm.
        :param alpha: The alpha of the alpha-beta pruning.
        :param alpha: The beta of the alpha-beta pruning.
        :param maximizing_player: Whether this is a max node (True) or a min node (False).
        :return: A tuple: (The alpha-beta algorithm value, The move in case of max node or None in min mode)
        """
        if depth == 0 or self.no_more_time():
            return self.utility(state), None

        next_moves = state.legalMoves()
        if not next_moves:
            # This player has no moves. So the previous player is the winner.
            return INFINITY if state.currPlayer != self.my_color else -INFINITY, None

        filtered_moves = self.subset_selection(state, self.w, next_moves)

        if maximizing_player:
            selected_move = filtered_moves[0]
            best_move_utility = -INFINITY
            for move in filtered_moves:
                new_state = copy.deepcopy(state)
                new_state.doMove(move)
                minimax_value, _ = self.search(new_state, depth - 1, alpha, beta, False)
                alpha = max(alpha, minimax_value)
                if minimax_value > best_move_utility:
                    best_move_utility = minimax_value
                    selected_move = move
                if beta <= alpha or self.no_more_time():
                    break
            return alpha, selected_move

        else:
            for move in filtered_moves:
                new_state = copy.deepcopy(state)
                new_state.doMove(move)
                beta = min(beta, self.search(new_state, depth - 1, alpha, beta, True)[0])
                if beta <= alpha or self.no_more_time():
                    break
            return beta, None
