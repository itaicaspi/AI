from __future__ import division, print_function
import abstract
from utils import MiniMaxWithAlphaBetaPruning, INFINITY
import time


class Player(abstract.AbstractPlayer):
    def __init__(self, setup_time, player_color, time_per_k_turns, k):
        abstract.AbstractPlayer.__init__(self, setup_time, player_color, time_per_k_turns, k)
        self.clock = time.process_time()

        # We are simply providing (remaining time / remaining turns) for each turn in round.
        # Taking a spare 1% time for unfolding the AlphaBeta.
        self.turns_remaining_in_round = self.k
        self.time_remaining_in_round = self.time_per_k_turns
        self.time_for_current_move = self.time_remaining_in_round / self.turns_remaining_in_round - 0.5

    def get_move(self, board_state, possible_moves):

        self.clock = time.process_time()
        self.time_for_current_move = self.time_remaining_in_round / self.turns_remaining_in_round -0.5
        if len(possible_moves) == 1:
            return possible_moves[0]

        current_depth = 1
        prev_alpha = -INFINITY

        # Choosing an arbitrary move:
        best_move = possible_moves[0]

        # Iterative deepening until the time runs out.
        while True:
            print('going to depth: {}, remaining time: {}, prev_alpha: {}, best_move: {}'.format(
                current_depth, self.time_for_current_move - (time.process_time() - self.clock), prev_alpha, best_move))
            minimax = MiniMaxWithAlphaBetaPruning(self.utility, self.color, self.no_more_time)
            alpha, move = minimax.search(board_state, current_depth, -INFINITY, INFINITY, True)

            if self.no_more_time():
                print('no more time')
                break

            prev_alpha = alpha
            best_move = move

            if alpha == INFINITY:
                print('the move: {} will guarantee victory.'.format(best_move))
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
        
        if self.color == 'white':
            myQueens = state.whiteQ
            enQueens = state.blackQ
        else:
            myQueens = state.blackQ
            enQueens = state.whiteQ
        
        checked = set()
        myOld = set()
        enOld = set()
        neutralOld = set() 
        myNew = set()
        enNew = set()
        neutralNew = set()
        
        myBlocks = 0
        enBlocks = 0
        neutralBlocks = 0
        
        checked = checked.union(myQueens).union(enQueens)
        myOld = myOld.union(myQueens)
        enOld = enOld.union(enQueens)
        
        while len(myOld) > 0 or len(enOld) > 0 or len(neutralOld) > 0:
            for pos in myOld:
                myNew = myNew.union(state.legalNeighbours(pos))
            for pos in enOld:
                enNew = enNew.union(state.legalNeighbours(pos))
            for pos in neutralOld:
                neutralNew = neutralNew.union(state.legalNeighbours(pos))
            
            myNew = myNew-checked
            enNew = enNew-checked
            neutralNew = neutralNew-checked
            
            neutralNew = neutralNew.union(myNew.intersection(enNew))
            myNew = myNew-neutralNew
            enNew = enNew-neutralNew
            
            myBlocks += len(myNew)
            enBlocks += len(enNew)
            neutralBlocks += len(neutralNew)
            
            checked = checked.union(myNew).union(enNew).union(neutralNew)
            myOld = myNew
            enOld = enNew
            neutralOld = neutralNew
            myNew = set()
            enNew = set()
            neutralNew = set()
        
        u = 0.1*neutralBlocks + myBlocks - enBlocks
        
        return u

    def no_more_time(self):
        return (time.process_time() - self.clock) >= self.time_for_current_move

    def __repr__(self):
        return '{} {}'.format(abstract.AbstractPlayer.__repr__(self), 'minimal_king_distances')

""" c:\python34\python run_amazons.py 3 3 3 y minimal_king_distances random_player
"""