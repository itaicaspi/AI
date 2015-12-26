# from __future__ import print_function
from threading import Thread
from queue import Queue
import time
import copy
import math
import numpy
from operator import itemgetter
import random
from enum import Enum


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

    def count_unblocked_neighbours(self, state, move):
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

    def subset_selection(self, state, w, possible_moves):
        class SelectionMode(Enum):
            Random = 1
            Simple = 2
            Blocked = 3

        # for the first move in the game, the moves of the 2 right queens
        # are exactly the same as the moves of the 2 left queens
        num_possible_moves = len(possible_moves)
        if num_possible_moves == 2176:
            possible_moves = possible_moves[0:int(num_possible_moves/2-1)]

        # get the number of moves in the subset
        subset_size = math.ceil(w * len(possible_moves))

        sorted_moves = []

        if num_possible_moves < 10 or num_possible_moves > 400:
            mode = SelectionMode.Random
        else:
            mode = SelectionMode.Simple

        # insert all moves with their heuristic value into a list and sort it
        if mode == SelectionMode.Random:
            # random selection
            sorted_moves = possible_moves
            random.shuffle(sorted_moves)
            selected_subset = sorted_moves[0:subset_size]
        elif mode == SelectionMode.Blocked:
            # select by number of free neighbours
            for move in possible_moves:
                sorted_moves += [(self.count_unblocked_neighbours(state, move), move)]
            sorted_moves = sorted(sorted_moves, key=lambda m: m[0], reverse=True)

            selected_subset = [m[1] for m in sorted_moves[0:subset_size]]
        elif mode == SelectionMode.Simple:
            # select by simple player heuristic
            for move in possible_moves:
                new_state = copy.deepcopy(state)
                new_state.doMove(move)
                sorted_moves += [(self.utility(new_state), move)]
            sorted_moves = sorted(sorted_moves, key=lambda m: m[0], reverse=True)

            # return only the subset_size top elements
            selected_subset = [m[1] for m in sorted_moves[0:subset_size]]
        else:
            print("Error: Wrong selection mode")
            selected_subset = possible_moves

        return selected_subset

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
