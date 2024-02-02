from games import games
from board_solver import solve_board_greedy


def tests():
	passed = 0
	failed = 0
	for i, game in enumerate(games):
		res = solve_board_greedy(game)
		if res is []:
			failed += 1
			print(f"TEST: {i+1}/{len(games)}\t \033[31mfailed \033[00m- game {i+1} unsolvable!")
		else:
			passed += 1
			print(f"TEST: {i+1}/{len(games)}\t \033[32mpassed \033[00m- game {i+1} solvable!")

	print(f'{passed}/{len(games)} tests passed.')
	

if __name__ == '__main__':
	tests()