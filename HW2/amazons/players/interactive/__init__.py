# from __future__ import print_function
import abstract


class Player(abstract.AbstractPlayer):
	def __init__(self, setup_time, player_color, time_per_k_turns, k):
		abstract.AbstractPlayer.__init__(self, setup_time, player_color, time_per_k_turns, k)

	def get_move(self, board_state, possible_moves):
		# help function.
		def get_input():
			while True:
				r = input('Enter row: ')
				c = input('Enter column: ')
				try:
					r = int(r)
					c = int(c)
					if r not in range(10) or c not in range(10):
						raise ValueError
					return (r,c)
				except ValueError:
					print('Invalid input')
					pass
				
		# get the next move from the user.
		while True:
			print('Select a queen by its position,')
			qu = get_input()
			if board_state.currPlayer == 'black':
				quArray = board_state.blackQ
			else:
				quArray = board_state.whiteQ
			if qu not in quArray:
				print('Invalid position of queen, try again.\n')
				continue
			print('Select a position to move queen,')
			pos = get_input()
			if pos not in board_state.legalPositions(qu):
				print('Invalid position to move queen, try again.\n')
				continue
			print('Select a position to throw the arrow by the queen,')
			aPos = get_input()
			if (qu, pos, aPos) not in possible_moves:
				print('Invalid position to throw arrow, try again.\n')
				continue
			return (qu, pos, aPos)

	def __repr__(self):
		return '{} {}'.format(abstract.AbstractPlayer.__repr__(self), 'interactive')

""" c:\python34\python run_amazons.py 3 3 3 y interactive random_player
"""