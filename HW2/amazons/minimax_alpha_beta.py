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

    def subset_selection2(self, state, w, possible_moves):
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



    def subset_selection(self, state, w, possible_moves):
        class SelectionMode(Enum):
            Random = 1
            Simple = 2
            Blocked = 3

        if self.no_more_time:
            return possible_moves
        # for the first move in the game, the moves of the 2 right queens
        # are exactly the same as the moves of the 2 left queens
        num_possible_moves = len(possible_moves)
        if num_possible_moves == 2176:
            possible_moves = possible_moves[0:int(num_possible_moves/2-1)]

        # get the number of moves in the subset
        subset_size = math.ceil(w * len(possible_moves))

        sorted_moves = []

        if num_possible_moves > 400:
            mode = SelectionMode.Random
        else:
            mode = SelectionMode.Simple
            #return self.subset_selection2(state, w, possible_moves)

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
