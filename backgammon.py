import rotem_helpers
from tqdm import tqdm
import os.path
import time
from random import randint, choices
import csv

dict = {}

def main():
	global dict

	if os.path.isfile('board_stats.pkl'):
		dict = rotem_helpers.load_obj('board_stats.pkl')
	else:
		create_dict()

	# board1 = (2,0,0,0,0,0)
	# board2 = (2,0,0,0,0,1)
	# print(dict[board1])
	# print(dict[board2])
	# print(two_boards_game_stats(board1,board2,num_games=10000))

	add_to_dataset()

def add_to_dataset(num=94):
	batch = []
	for i in tqdm(range(num)):
		b1, b2, board1_moves, board2_moves, game_stats = random_game()
		batch.append([board1_moves,board2_moves,game_stats,b1[0],b1[1],b1[2],b1[3],b1[4],b1[5],b2[0],b2[1],b2[2],b2[3],b2[4],b2[5]])

		if i % 100 == 0:
			with open('moves_dataset.csv', 'a', newline='') as graphFile:
				graphFileWriter = csv.writer(graphFile)
				for x in batch:
					graphFileWriter.writerow(x)
			batch = []
	with open('moves_dataset.csv', 'a', newline='') as graphFile:
		graphFileWriter = csv.writer(graphFile)
		for x in batch:
			graphFileWriter.writerow(x)

def random_game():
	board1 = random_board()
	board2 = random_board()
	board1_moves = round(dict[tuple(board1)],5)
	board2_moves = round(dict[tuple(board2)],5)
	game_stats = two_boards_game_stats(board1,board2)
	return board1,board2,board1_moves,board2_moves,game_stats

def random_board():
	board = [0, 0, 0, 0, 0, 0]
	num_checkers = choices(range(1,16),range(1,16))
	for _ in range(num_checkers[0]):
		board[randint(0,5)] += 1
	return board

def two_boards_game_stats(board1,board2,num_games=10000):
	board1,board2 = list(board1),list(board2)
	win1, win2 = 0,0
	for i in range(num_games):
		if i % 2 == 0:
			winner = two_boards_single_game(board1,board2)
			if winner == 1:
				win1+=1
			else:
				win2+=1
		else:
			winner = two_boards_single_game(board2, board1)
			if winner == 2:
				win1 += 1
			else:
				win2 += 1
	return win1/(win1+win2)

def two_boards_single_game(board1,board2):
	while True:
		board1 = random_two_dice_move(board1)
		if board1 == [0,0,0,0,0,0]:
			return 1
		board2 = random_two_dice_move(board2)
		if board2 == [0, 0, 0, 0, 0, 0]:
			return 2




def random_two_dice_move(board):
	dice1,dice2 = randint(1,6), randint(1,6)
	if dice1 == dice2:
		board = single_move(board, dice1)
		board = single_move(board, dice1)
		board = single_move(board, dice1)
		board = single_move(board, dice1)
		return board
	else:
		board1 = single_move(board, dice1)
		board1 = single_move(board1, dice2)
		board2 = single_move(board, dice2)
		board2 = single_move(board2,dice1)
		if dict[tuple(board1)] < dict[tuple(board2)]:
			return board1
		return board2

def two_dice_stats(board):
	if board in dict:
		return dict[board]
	board = list(board)
	score = 0.0
	for i in range(1,7):
		board_after_move1 = single_move(board,i)
		for j in range(1,7):
			if i == j:
				board_after_move2 = single_move(board_after_move1,j)
				board_after_move2 = single_move(board_after_move2,j)
				board_after_move2 = single_move(board_after_move2,j)
			else:
				board_after_move2 = single_move(board_after_move1,j)
			score += dict[tuple(board_after_move2)]
	dict[tuple(board)] = 1 + score/36.0

def num_of_checkers(board):
	sum = 0
	for i in board:
		sum += i
	return sum

def single_move(board, move):
	board = list(board)
	if board==[0,0,0,0,0,0]:
		return [0,0,0,0,0,0]
	if board[6-move] > 0:
		board[6-move] -= 1
		return board
	bigger_places = find_bigger_places(board, move)
	if len(bigger_places)>0:
		return move_bigger_places(board,bigger_places,move)
	return remove_smaller_place(board,move)

def find_bigger_places(board, move):
	places_list = []
	for i in range(0,6-move):
		if board[i]>0:
			places_list.append(i)
	return places_list

def remove_smaller_place(board, move):
	for i in range(6-move+1,6):
		if board[i] > 0:
			board[i] -= 1
			return board
	print('remove_smaller_place does not find any')

def move_bigger_places(board,bigger_places,move):
	best_move_key, best_move_score = 0,1000
	for place in bigger_places:
		test_board = list(board)
		test_board[place]-=1
		test_board[place + move] += 1
		tuple_board = tuple(test_board)
		if best_move_score > dict[tuple_board]:
			best_move_key,best_move_score = tuple_board,dict[tuple_board]
	return best_move_key

def create_dict():
	dict[0,0,0,0,0,0] = 0
	for a in tqdm(range(16)):
		for b in range(16):
			for c in range(16):
				for d in range(16):
					for e in range(16):
						for f in range(16):
							board = (a,b,c,d,e,f)
							if num_of_checkers(board) <= 15:
								two_dice_stats(board)
	rotem_helpers.save_obj(dict, 'board_stats.pkl')

if __name__ == '__main__':
    main()