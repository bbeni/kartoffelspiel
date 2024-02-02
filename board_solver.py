from itertools import product
from copy import deepcopy
from functools import lru_cache


def count_potatos(board):
	return len([c for row in board for c in row if c == 'x'])

def find_moves(board):
	W = len(board[0])
	H = len(board)
	new_boards = []

	# vertical 110, 011
	for i, j in product(range(W), range(H-2)):
		if board[i][j+1] == 'x':
			if board[i][j] == 'x' and board[i][j+2] == 'o':
				nb = deepcopy(board)
				nb[i][j], nb[i][j+1], nb[i][j+2] = 'o', 'o', 'x' 
				new_boards.append(nb)
			elif board[i][j] == 'o' and board[i][j+2] == 'x':
				nb = deepcopy(board)
				nb[i][j], nb[i][j+1], nb[i][j+2] = 'x', 'o', 'o' 
				new_boards.append(nb)

	# horizontal 110, 011
	for i, j in product(range(W-2), range(H)):
		if board[i+1][j] == 'x':
			if board[i][j] == 'x' and board[i+2][j] == 'o':
				nb = deepcopy(board)
				nb[i][j], nb[i+1][j], nb[i+2][j] = 'o', 'o', 'x' 
				new_boards.append(nb)
			if board[i][j] == 'o' and board[i+2][j] == 'x':
				nb = deepcopy(board)
				nb[i][j], nb[i+1][j], nb[i+2][j] = 'x', 'o', 'o' 
				new_boards.append(nb)

	return new_boards


def solve_board(board):

	def solve_rec(board, n_potatoes):
		if n_potatoes == 1:
			return [[board]]
		found = []
		for new_board in find_moves(board):
			prev = solve_rec(new_board, n_potatoes-1)
			for i in range(len(prev)):
				prev[i].append(board)
			found.extend(prev)
		return found

	n_potatoes = count_potatos(board)
	return solve_rec(board, n_potatoes)

def solve_board_greedy(board):
	def solve_rec(board, n_potatoes):
		if n_potatoes == 1:
			return [board]
		for new_board in find_moves(board):
			prev = solve_rec(new_board, n_potatoes-1)
			for i in range(len(prev)):
				return [board] + prev
		return []

	n_potatoes = count_potatos(board)
	return solve_rec(board, n_potatoes)



def display_board(board):	
	for line in board:
		print(''.join(line).replace('x', 'O').replace('o', '.'))
	print('---------')


def solve_all_games(games):

	# try to find solutions to the games
	for i in range(len(games)):
		s = solve_board(games[i])
		print(f'Game nr {i+1} with {count_potatos(games[i])} potatos has {len(s)} solutions.')

	# display all solutions to the last game
	for sol in s:
		for move in sol:
			display_board(move)
		print('############################')
		print('############################')


if __name__ == '__main__':
	from games import games

	print(f'game nr {16} by whoever')
	display_board(games[15])
	sol = solve_board_greedy(games[15])
	for b in sol:
		display_board(b)





