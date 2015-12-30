
import copy
import utils
import random
from enum import Enum
import math

INFINITY = float(6000)

class SelectiveMiniMaxWithAlphaBetaPruningAndCalmnessCriteria:

    def __init__(self, utility, my_color, no_more_time, w, calmness_factor):
        """Initialize a MiniMax algorithms with alpha-beta pruning.

        :param utility: The utility function. Should have state as parameter.
        :param my_color: The color of the player who runs this MiniMax search.
        :param no_more_time: A function that returns true if there is no more time to run this search, or false if
                             there is still time left.
        """
        self.utility = utility
        self.my_color = my_color
        self.no_more_time = no_more_time
        self.calmness_factor = calmness_factor
        self.w = w

    def simple_player_utility(self, state):
        if not state.legalMoves():
            return INFINITY if state.currPlayer != self.my_color else -INFINITY

        u = 0
        if self.my_color == 'white':
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
        """
        Counts the number of free neighbours the queen will have after doing the move
        :param state: the current state
        :param move: the move we are checking
        :return: number of free neighbours
        """
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

    def legal_positions(self, pos, state, board, max_dist):
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
                for move in self.legal_positions(pos, state, board, max_depth):
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

    def min_queen_distance(self, state):
        if not state.legalMoves():
            return INFINITY if state.currPlayer != self.my_color else -INFINITY

        u = self.cell_owners(state, 9)
        if self.my_color != 'white':
            u = -u

        return u

    def tree_selection(self, state, w, possible_moves):
        """
        Implements a three level heuristic algorithm:
        1. Select the best queens to move - the ones with the minimum mobility
        2. Select the best places to move each of the selected queens - the places that will guarantee the highest mobility
        3. Select the best places to shoot the arrow to - the places that will bring the opponent mobility to the minimum

        :param state: the current board state
        :param possible_moves: the list of all possible moves in the current layer
        :param w: the percentage of moves to take
        :return: a list of filtered moves using the given heuristic
        """
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
            Queen = 4
            Tree = 5

        # for the first move in the game, the moves of the 2 right queens
        # are exactly the same as the moves of the 2 left queens
        num_possible_moves = len(possible_moves)
        if num_possible_moves == 2176:
            possible_moves = possible_moves[0:int(num_possible_moves/2-1)]

        # get the number of moves in the subset
        subset_size = math.ceil(w * len(possible_moves))

        # if w ~ 1 then don't waste time on the rest of the function
        if self.no_more_time() or num_possible_moves == subset_size:
            return possible_moves

        # if the number of possible moves is low, subset size can be 0 and then we will get error afterwards
        if subset_size == 0:
            subset_size = 1

        sorted_moves = []

        # user can define a threshold where game stage with a lot of moves will be evaluated with faster heuristics
        fast_utility_threshold = 3000
        if num_possible_moves > fast_utility_threshold:
            mode = SelectionMode.Random
        else:
            mode = SelectionMode.Queen

        # insert all moves with their heuristic value into a list and sort it
        if mode == SelectionMode.Tree:
            return self.tree_selection(state, w, possible_moves)
        elif mode == SelectionMode.Random:
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
            for i in range(0, len(possible_moves)):
                if (i == 0) or (i > 0 and (possible_moves[i][0] != possible_moves[i-1][0] or possible_moves[i][1] != possible_moves[i-1][1])):
                    new_state = copy.deepcopy(state)
                    new_state.doMove(possible_moves[i])
                    sorted_moves += [(self.simple_player_utility(new_state), possible_moves[i])]
                else:
                    sorted_moves += [(sorted_moves[-1][0], possible_moves[i])]
                if self.no_more_time():
                    return possible_moves
            sorted_moves = sorted(sorted_moves, key=lambda m: m[0], reverse=True)
            if len(sorted_moves) == 0:
                return possible_moves
            # return only the subset_size top elements
            selected_subset = [m[1] for m in sorted_moves[0:subset_size]]
        elif mode == SelectionMode.Queen:
            # select by simple player heuristic
            for i in range(0, len(possible_moves)):
                if (i == 0) or (i > 0 and (possible_moves[i][0] != possible_moves[i-1][0] or possible_moves[i][1] != possible_moves[i-1][1])):
                    new_state = copy.deepcopy(state)
                    new_state.doMove(possible_moves[i])
                    sorted_moves += [(self.min_queen_distance(new_state), possible_moves[i])]
                else:
                    sorted_moves += [(sorted_moves[-1][0], possible_moves[i])]
                if self.no_more_time():
                    return possible_moves
            sorted_moves = sorted(sorted_moves, key=lambda m: m[0], reverse=True)
            if len(sorted_moves) == 0:
                return possible_moves
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
        u = self.utility(state)
        if self.no_more_time() or depth == 0:
            return u, None

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
                minimax_value, _ = self.search_helper(new_state, depth - 1, alpha, beta, False, u)
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
                beta = min(beta, self.search_helper(new_state, depth - 1, alpha, beta, True, u)[0])
                if beta <= alpha or self.no_more_time():
                    break
            return beta, None

    def search_helper(self, state, depth, alpha, beta, maximizing_player, last_utility):
        """Start the MiniMax algorithm.

        :param state: The state to start from.
        :param depth: The maximum allowed depth for the algorithm.
        :param alpha: The alpha of the alpha-beta pruning.
        :param alpha: The beta of the alpha-beta pruning.
        :param maximizing_player: Whether this is a max node (True) or a min node (False).
        :return: A tuple: (The alpha-beta algorithm value, The move in case of max node or None in min mode)
        """
        u = self.utility(state)
        if  self.no_more_time() or (depth == 0 and self.is_calm(u, last_utility)):
            return u, None

        next_moves = state.legalMoves()
        if not next_moves:
            # This player has no moves. So the previous player is the winner.
            return INFINITY if state.currPlayer != self.my_color else -INFINITY, None
        new_depth = depth - 1
        if depth == 0:
            new_depth = 0

        filtered_moves = self.subset_selection(state, self.w, next_moves)

        if maximizing_player:
            selected_move = filtered_moves[0]
            best_move_utility = -INFINITY
            for move in filtered_moves:
                new_state = copy.deepcopy(state)
                new_state.doMove(move)
                minimax_value, _ = self.search_helper(new_state, new_depth, alpha, beta, False, u)
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
                beta = min(beta, self.search_helper(new_state, new_depth, alpha, beta, True, u)[0])
                if beta <= alpha or self.no_more_time():
                    break
            return beta, None

    def is_calm(self, u, last_value):
        if abs(u - last_value) < self.calmness_factor:
            return True
        return False
