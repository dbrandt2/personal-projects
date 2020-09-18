import pprint

#solver
def solve(board):
	"""
	Solves a sudoku board using backtracking
	:param board: 2D list of ints
	:return: solution - list of ints with no 0 elements
	"""
	find = findEmpty(board)
	if (find):
		row, col = find
	else:
		return True; #return True equals no empty boxes found, puzzle is solved

	for i in range(1, 10):
		if isValid(board, (row, col), i):
			board[row][col] = i

			if solve(board):
				return True

			board[row][col] = 0

	return False

def isValid(board, position, num):
	"""
	Returns- if the attempt move is valid
	:param-board: 2D list of ints
	:param-position: (row, col) on board
	:param-num:-bool
	"""

	#check row
	for i in range(0, len(board)):
		if board[position[0]][i] == num and position[1] != i:
			return False

	#check col
	for i in range(0, len(board)):
		if board[i][position[1]] == num and position[0] != i:
			return False

	#Check box
	box_x = position[1] // 3
	box_y = position[0] // 3

	for i in range(box_y * 3, box_y * 3 + 3):
		for j in range(box_x * 3, box_x * 3 + 3):
			if board[i][j] == num and (i, j) != position:
				return False

	return True

def findEmpty(board):
	"""
	finds and empty space in the board
	:param-board: partially complete board
	:return: (int, int) row, col
	"""

	for i in range(len(board)):
		for j in range(len(board[0])):
			if board[i][j] == 0:
				return (i, j) #return row and col of empty position
	return None #no empty boxes found

def printBoard(board):
	"""
	prints the board 
	:param board: 2D list of ints
	:return: None
	"""

	for i in range(len(board)):
		if i % 3 == 0 and i != 0:
			print("- - - - - - - - - - - - -")
		for j in range(len(board[0])):
			if j % 3 == 0 and j != 0:
				print(" | ", end="")
				
			if j == 8:
				print(board[i][j], end="\n")
			else:
				print(str(board[i][j]) + " ", end="")
				

