# games board and board movement.


class amazonsBoard:
	# setting board (10 by 10, 2d board) and queen positions.
	def __init__(self):
		self.board = [[' ' for x in range(10)] for x in range(10)]
		self.board[0][3] = self.board[0][6] = self.board[3][0] = self.board[3][9] = 'B'
		self.board[6][0] = self.board[6][9] = self.board[9][3] = self.board[9][6] = 'W'

		self.blackQ = [(0, 3), (0, 6), (3, 0), (3, 9)]
		self.whiteQ = [(6, 0), (6, 9), (9, 3), (9, 6)]

		self.currPlayer = 'white'

	# move is a vector with: a - position to move from, b - move to, c - shoot arrow
	def doMove(self, move):
		a, b, c = move
		if self.board[a[0]][a[1]] == 'B':
			self.blackQ.remove(a)
			self.blackQ.append(b)
			self.currPlayer = 'white'
		else:
			self.whiteQ.remove(a)
			self.whiteQ.append(b)
			self.currPlayer = 'black'
		self.board[b[0]][b[1]] = self.board[a[0]][a[1]]
		self.board[a[0]][a[1]] = ' '
		self.board[c[0]][c[1]] = 'a'

	# print board in current state.
	def printBoard(self):
		print('\n  ' + '-' * 31)
		for i in range(10):
			print(str(i) + ' |', end='')
			for j in range(10):
				print(self.board[i][j], end=' |')
			print('\n  ' + '-' * 31)
		print('   0  1  2  3  4  5  6  7  8  9  \n')

	# returns all legal position to move on board from pos, for queen or arrow.
	def legalPositions(self, pos):
		a, b = pos
		positions = []
		# line positions.
		for i in range(b - 1, -1, -1):
			if self.board[a][i] != ' ':
				break
			else:
				positions += [(a, i)]
		for i in range(b + 1, 10, 1):
			if self.board[a][i] != ' ':
				break
			else:
				positions += [(a, i)]
		# row positions.
		for j in range(a - 1, -1, -1):
			if self.board[j][b] != ' ':
				break
			else:
				positions += [(j, b)]
		for j in range(a + 1, 10, 1):
			if self.board[j][b] != ' ':
				break
			else:
				positions += [(j, b)]
		# diagonal positions.
		for j, i in zip(range(a - 1, -1, -1), range(b - 1, -1, -1)):
			if self.board[j][i] != ' ':
				break
			else:
				positions += [(j, i)]
		for j, i in zip(range(a + 1, 10, 1), range(b + 1, 10, 1)):
			if self.board[j][i] != ' ':
				break
			else:
				positions += [(j, i)]
		for j, i in zip(range(a - 1, -1, -1), range(b + 1, 10, 1)):
			if self.board[j][i] != ' ':
				break
			else:
				positions += [(j, i)]
		for j, i in zip(range(a + 1, 10, 1), range(b - 1, -1, -1)):
			if self.board[j][i] != ' ':
				break
			else:
				positions += [(j, i)]

		return positions

	def __hash__(self):
		"""This object can be inserted into a set or as dict key. NOTICE: Changing the object after it has been inserted
		into a set or dict (as key) may have unpredicted results!!!
		"""
		str_board = ','.join(','.join(e) for e in self.board)
		return hash(str_board + self.currPlayer)

	def __eq__(self, other):
		return isinstance(other, amazonsBoard) and self.board == other.board and self.curr_player == other.curr_player

	# returns all moves the queen in position qu can make. uses legalPositions.
	def getMoves(self, qu):
		a, b = qu
		moves = []
		t = self.board[a][b]
		self.board[a][b] = ' '
		qMoves = self.legalPositions(qu)
		for qm in qMoves:
			aMoves = self.legalPositions(qm)
			for am in aMoves:
				moves += [(qu, qm, am)]
		self.board[a][b] = t
		return moves

	# returns all legal moves a current player can make. uses getMoves.
	def legalMoves(self):
		moves = []
		if self.currPlayer == 'black':
			quArray = self.blackQ
		else:
			quArray = self.whiteQ
		for qu in quArray:
			moves += self.getMoves(qu)
		return moves

	# return all legal neighbours to move on board from pos.
	def legalNeighbours(self, pos):
		a, b = pos
		neighbours = []

		if b > 0:
			if self.board[a][b - 1] == ' ':
				neighbours += [(a, b - 1)]
			if a > 0:
				if self.board[a - 1][b - 1] == ' ':
					neighbours += [(a - 1, b - 1)]
			if a < 9:
				if self.board[a + 1][b - 1] == ' ':
					neighbours += [(a + 1, b - 1)]

		if b < 9:
			if self.board[a][b + 1] == ' ':
				neighbours += [(a, b + 1)]
			if a > 0:
				if self.board[a - 1][b + 1] == ' ':
					neighbours += [(a - 1, b + 1)]
			if a < 9:
				if self.board[a + 1][b + 1] == ' ':
					neighbours += [(a + 1, b + 1)]

		if a > 0 and self.board[a - 1][b] == ' ':
			neighbours += [(a - 1, b)]

		if a < 9 and self.board[a + 1][b] == ' ':
			neighbours += [(a + 1, b)]

		return neighbours

