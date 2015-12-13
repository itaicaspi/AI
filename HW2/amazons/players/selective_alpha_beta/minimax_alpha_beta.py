# from __future__ import print_function
from threading import Thread
from queue import Queue
import time
import copy
import math
import numpy
from operator import itemgetter

__author__ = 'Orenk'

INFINITY = float(6000)

class SelectiveMiniMaxWithAlphaBetaPruning:

    def __init__(self, utility, my_color, no_more_time, w = 1):
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

    # counts the reachable positions on the board
    def filter_moves(self, state, moves, w):
        sorted_moves = []
        # go over all queen moves
        for move in moves:  # move = ((a,b), (c,d), (e,f))
            board = numpy.empty((8, 8))
            counter = 0
            # for each move, look at the following moves
            queen_moves = state.getMoves(move(1))  # (a,b)
            for qm in queen_moves:
                x, y = qm(1)
                if board[x][y] == 0:
                    counter += 1
                    board[x][y] = 1
            sorted_moves += (move, counter)
        sorted_moves = sorted(sorted_moves, key=itemgetter(1, 2))
        total_moves = len(sorted_moves)
        return sorted_moves(range(0, (w*total_moves)))


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

        filtered_moves = self.filter_moves(next_moves, self.w)

        if maximizing_player:
            selected_move = next_moves[0]
            best_move_utility = -INFINITY
            for move in next_moves:
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
            for move in next_moves:
                new_state = copy.deepcopy(state)
                new_state.doMove(move)
                beta = min(beta, self.search(new_state, depth - 1, alpha, beta, True)[0])
                if beta <= alpha or self.no_more_time():
                    break
            return beta, None
