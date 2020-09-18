#GUI for the sudoku game
import pygame as py
from SudokuSolver import solve, isValid
import time
import random
py.font.init()

#Grid class holds the board
class Grid:
	"""
	board = [
	[0, 6, 2, 0, 3, 0, 4, 0, 7],
	[3, 0, 5, 0, 0, 0, 0, 0, 9],
	[1, 7, 0, 8, 0, 5, 0, 2, 3],
	[0, 5, 0, 9, 0, 0, 0, 3, 0],
	[2, 3, 0, 7, 5, 4, 9, 8, 0],
	[0, 0, 0, 2, 6, 3, 7, 4, 5],
	[0, 0, 0, 0, 1, 0, 5, 0, 2],
	[5, 2, 3, 0, 9, 0, 1, 7, 0],
	[0, 1, 0, 0, 2, 8, 3, 0, 4]
]
	"""

	#constructor for the grid class
	def __init__(self, rows, cols, width, height, board):
		self.board = board
		self.rows = rows
		self.cols = cols
		self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
		self.width = width
		self.height = height
		self.model = None
		self.selected = None
		

	#update the grid 
	def updateModel(self):
		self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

	#place a value into the grid space 
	def place(self, value):
		row, col = self.selected
		if self.cubes[row][col].value == 0: #if the space is empty then fill with the value
			self.cubes[row][col].setValue(value)
			self.updateModel()

			#check to see if the placement is a valid placement
			#then check to see if the puzzle can be solved with that placement to determine if this is a correct placement and not just a valid one
			if isValid(self.model, (row, col), value) and solve(self.model):
				return True
			else: #undo the placement
				self.cubes[row][col].setValue(0)
				self.cubes[row][col].setTemp(0)
				self.updateModel()
				return False

	#temp placement (value the player thinks might go in this position with out actually attempting to place the value here)
	def tempPlacement(self, value):
		row, col = self.selected
		self.cubes[row][col].setTemp(value)

	#draw the grid
	def drawGrid(self, window):
		#draw the grid lines (size of grid / number of elements in a row or col of grid)
		spacer = self.width / 9
		for i in range(self.rows + 1):
			if i % 3 == 0 and i != 0:
				thickness = 4
			else: 
				thickness = 1
			py.draw.line(window, (0, 0, 0), (0, i * spacer), (self.width, i * spacer), thickness) #draw row lines
			py.draw.line(window, (0, 0, 0), (i * spacer, 0), (i * spacer, self.height), thickness) #draw col lines
			

		#draw the cubes in the grid
		for i in range(self.rows):
			for j in range(self.cols):
				self.cubes[i][j].drawValue(window)

	#select the cube the player clicks on (unselect all other cubes)
	def select(self, mouseRow, mouseCol):
		for i in range(self.rows):
			for j in range(self.cols):
				self.cubes[i][j].isSelected = False

		self.cubes[mouseRow][mouseCol].isSelected = True
		self.selected = (mouseRow, mouseCol)

	#clear a temp value for the space
	def clear(self):
		row, col = self.selected
		if self.cubes[row][col].value == 0:
			self.cubes[row][col].setTemp(0)

	#trigger a click return row and col of click
	def click(self, position):
		if position[0] < self.width and position[1] < self.height: #we are in the board 
			spacer = self.width / 9
			x = position[0] // spacer
			y = position[1] // spacer
			return (int(y), int(x)) #make sure we are returning int values not floats
		else:
			return None #we are not in the board

	#the board is full (no more 0's for values)
	def isFinished(self):
		for i in range(self.rows):
			for j in range(self.cols):
				if self.cubes[i][j].value == 0:
					return False
				
		return True

class Cube:
	rows = 9
	cols = 9

	#constructer for the Cube class
	def __init__(self, value, row, col, width, height):
		self.value = value
		self.temp = 0
		self.row = row
		self.col = col
		self.width = width
		self.height = height
		self.isSelected = False

	def drawValue(self, window):
		font = py.font.SysFont("Times new Roman", 30)

		spacer = self.width / 9
		x = self.col * spacer
		y = self.row * spacer

		#draw the value or the temp value in the space
		if self.temp != 0 and self.value == 0:
			text = font.render(str(self.temp), 1, (255, 0, 0))
			window.blit(text, (x + 5, y + 5))
		elif not(self.value == 0):
			text = font.render(str(self.value), 1, (0, 0, 0))
			window.blit(text, (x + (spacer / 2 - text.get_width() / 2), y + (spacer / 2 - text.get_height() / 2)))

		#draw a blue rectangle around the selected space
		if self.isSelected:
			py.draw.rect(window, (0, 0 , 255), (x, y, spacer, spacer), 3)

	#set value
	def setValue(self, value):
		self.value = value


	#def set temp 
	def setTemp(self, temp):
		self.temp = temp

#draw updated window
def redrawWindow(window, board, time, faults):
	window.fill((255, 255, 255))
	font = py.font.SysFont("Times new Roman", 40)
	text = font.render("Time: " + formatTime(time), 1, (0, 0, 0))
	window.blit(text, (20, 560))
	board.drawGrid(window)

#create a format to display the time
def formatTime(secs):
	sec = secs % 60
	minute = secs // 60
	hour = minute // 60

	format = " " + str(minute) + " : " + str(sec)
	return format

#print the instructions for  the game in the console window
def printInstructions():
	print("Welcome to my Sudoku game!\n")
	print("Select a space with the mouse (highlighted blue means it is the selected space)")
	print("Use the numbers or keypad to enter the number")
	print("Press space to confirm placement")
	print("Press delete or backspace to remove a place holder number")
	print("Press the g key to generate a new random board")
	print("Press the s key to auto solve the current puzzle")
	print("If you make three incorrect moves the game ends\n")

#create a list of 9 numbers this will be the first line of a randomly generated puzzle
def createListOfNine():
	baseList = [1, 2, 3, 4, 5, 6, 7, 8, 9]
	tempList = []

	for i in range(9):
		num = baseList.pop(random.randint(0, (9 - (i + 1))))
		tempList.append(num)
	return tempList

#shift the given list by one element and return list
def shiftByOne(baseList):
	tempList = [0, 0, 0, 0, 0, 0, 0, 0, 0]

	for i in range(len(baseList) - 1):
		if (i + 1) < len(baseList):
			tempList[i + 1] = baseList[i]
	tempList[0] = baseList[8]
	return tempList

#generate a random grid and return a grid object
def generateRandomGrid():
	board = []
	
	#create the first set of three rows
	board.append(createListOfNine())
	board.append(shiftByThree(board[0]))
	board.append(shiftByThree(board[1]))

	#create the second set of three rows
	board.append(shiftByOne(board[2]))
	board.append(shiftByThree(board[3]))
	board.append(shiftByThree(board[4]))

	#create the third set of three rows
	board.append(shiftByOne(board[5]))
	board.append(shiftByThree(board[6]))
	board.append(shiftByThree(board[7]))

	return board


#shift the given list by three elements and return
def shiftByThree(baselist):
	tempList = shiftByOne(baselist)
	tempList = shiftByOne(tempList)
	tempList = shiftByOne(tempList)
	return tempList

#this will reorder the entire group of rows
def reorderRowGroups(board):
	#board[0, 1, 2] [3, 4, 5] [6, 7, 8]
	#given 3 groups of row we can get 6 combinations (123)(132)(231)(213)(312)(321)

	#this will randomly determine if we are going to swap groups of rows or not
	whatSwap = random.randint(0, 5)

	if whatSwap == 5: #(132)
		temp1 = board[3]
		temp2 = board[4]
		temp3 = board[5]
		board[3] = board[6]
		board[4] = board[7]
		board[5] = board[8]
		board[6] = temp1
		board[7] = temp2
		board[8] = temp3

	elif whatSwap == 4: #(231)
		temp1 = board[0]
		temp2 = board[1]
		temp3 = board[2]

		board[0] = board[3]
		board[1] = board[4]
		board[2] = board[5]
		board[3] = board[6]
		board[4] = board[7]
		board[5] = board[8]

		board[6] = temp1
		board[7] = temp2
		board[8] = temp3

	elif whatSwap == 3: #(213)
		temp1 = board[0]
		temp2 = board[1]
		temp3 = board[2]

		board[0] = board[3]
		board[1] = board[4]
		board[2] = board[5]
		board[3] = temp1
		board[4] = temp2
		board[5] = temp3

	elif whatSwap == 2: #(312)
		temp1 = board[0]
		temp2 = board[1]
		temp3 = board[2]

		board[0] = board[6]
		board[1] = board[7]
		board[2] = board[8]
		board[6] = board[3]
		board[7] = board[4]
		board[8] = board[5]
		board[3] = temp1
		board[4] = temp2
		board[5] = temp3

	elif whatSwap == 1: #(321)
		temp1 = board[0]
		temp2 = board[1]
		temp3 = board[2]

		board[0] = board[6]
		board[1] = board[7]
		board[2] = board[8]

		board[6] = temp1
		board[7] = temp2
		board[8] = temp3
		#else whatSwap = 0 no change
	return board

def reorderIndividualRows(board):

	#27 is a random max number (9 lines and 3 groups so... 3 * 9)
	numOfSwaps = random.randint(4, 27)

	for i in range(numOfSwaps):
		whatGroup = random.randint(0, 2)
		if whatGroup == 0: #(0, 1, 2)
			randRow1 = random.randint(0, 2)
			randRow2 = random.randint(0, 2)

			#make sure we are using the same row
			while randRow1 == randRow2:
				randRow2 = random.randint(0, 2)

			#swap rows
			tempRow = board[randRow1]
			board[randRow1] = board[randRow2]
			board[randRow2] = tempRow

		elif whatGroup == 1: #(0, 1, 2)
			randRow1 = random.randint(3, 5)
			randRow2 = random.randint(3, 5)

			#make sure we are using the same row
			while randRow1 == randRow2:
				randRow2 = random.randint(3, 5)

			#swap rows
			tempRow = board[randRow1]
			board[randRow1] = board[randRow2]
			board[randRow2] = tempRow

		elif whatGroup == 2: #(0, 1, 2)
			randRow1 = random.randint(6, 8)
			randRow2 = random.randint(6, 8)

			#make sure we are using the same row
			while randRow1 == randRow2:
				randRow2 = random.randint(6, 8)

			#swap rows
			tempRow = board[randRow1]
			board[randRow1] = board[randRow2]
			board[randRow2] = tempRow

	return board

#this will reorder the entire group of rows
def reorderColGroups(board):
	#board[0, 1, 2] [3, 4, 5] [6, 7, 8]
	#given 3 groups of row we can get 6 combinations (123)(132)(231)(213)(312)(321)

	#this will randomly determine if we are going to swap groups of rows or not
	whatSwap = random.randint(0, 5)
	for i in range(len(board)):
		if whatSwap == 5: #(132)
			temp1 = board[i][3]
			temp2 = board[i][4]
			temp3 = board[i][5]
			board[i][3] = board[i][6]
			board[i][4] = board[i][7]
			board[i][5] = board[i][8]
			board[i][6] = temp1
			board[i][7] = temp2
			board[i][8] = temp3

		elif whatSwap == 4: #(231)
			temp1 = board[i][0]
			temp2 = board[i][1]
			temp3 = board[i][2]

			board[i][0] = board[i][3]
			board[i][1] = board[i][4]
			board[i][2] = board[i][5]
			board[i][3] = board[i][6]
			board[i][4] = board[i][7]
			board[i][5] = board[i][8]

			board[i][6] = temp1
			board[i][7] = temp2
			board[i][8] = temp3

		elif whatSwap == 3: #(213)
			temp1 = board[i][0]
			temp2 = board[i][1]
			temp3 = board[i][2]

			board[i][0] = board[i][3]
			board[i][1] = board[i][4]
			board[i][2] = board[i][5]
			board[i][3] = temp1
			board[i][4] = temp2
			board[i][5] = temp3

		elif whatSwap == 2: #(312)
			temp1 = board[i][0]
			temp2 = board[i][1]
			temp3 = board[i][2]
	
			board[i][0] = board[i][6]
			board[i][1] = board[i][7]
			board[i][2] = board[i][8]
			board[i][6] = board[i][3]
			board[i][7] = board[i][4]
			board[i][8] = board[i][5]
			board[i][3] = temp1
			board[i][4] = temp2
			board[i][5] = temp3

		elif whatSwap == 1: #(321)
			temp1 = board[i][0]
			temp2 = board[i][1]
			temp3 = board[i][2]

			board[i][0] = board[i][6]
			board[i][1] = board[i][7] 
			board[i][2] = board[i][8]

			board[i][6] = temp1
			board[i][7] = temp2
			board[i][8] = temp3
		#else whatSwap = 0 no change
	return board

def reorderIndividualCols(board):

	#27 is a random max number (9 lines and 3 groups so... 3 * 9)
	numOfSwaps = random.randint(4, 27)

	for i in range(numOfSwaps):
		whatGroup = random.randint(0, 2)
		if whatGroup == 0: #(0, 1, 2)

			randCol1 = random.randint(0, 2)
			randCol2 = random.randint(0, 2)

			#make sure we are using the same row
			while randCol1 == randCol2:
				randCol2 = random.randint(0, 2)

			#swap cols
			for i in range(len(board)):
				tempCol = board[i][randCol1]
				board[i][randCol1] = board[i][randCol2]
				board[i][randCol2] = tempCol

		elif whatGroup == 1: #(0, 1, 2)

			randCol1 = random.randint(3, 5)
			randCol2 = random.randint(3, 5)

			#make sure we are using the same row
			while randCol1 == randCol2:
				randCol2 = random.randint(3, 5)

			#swap cols
			for i in range(len(board)):
				tempCol = board[i][randCol1]
				board[i][randCol1] = board[i][randCol2]
				board[i][randCol2] = tempCol

		elif whatGroup == 2: #(0, 1, 2)

			randCol1 = random.randint(6, 8)
			randCol2 = random.randint(6, 8)

			#make sure we are using the same row
			while randCol1 == randCol2:
				randCol2 = random.randint(6, 8)

			#swap cols
			for i in range(len(board)):
				tempCol = board[i][randCol1]
				board[i][randCol1] = board[i][randCol2]
				board[i][randCol2] = tempCol

	return board


#accepts a board object and returns a grid (turns 2d array in to a puzzle)
#this will remove elements from the board and insert blanks (0) into those spaces
def createPuzzleFromBoard(board):
	#17 is the minimum number of givens for a valid sudoku puzzle
	#this generator will provide more given numbers to create easier puzzles
	#this can be modified later to add a difficulty rating for generated puzzles based on user preference
	#81 - 17 = 64 remove at most 64 elements for a valid puzzle
	
	numEleRem = random.randint(18, 49)

	for i in range(numEleRem):
		remRow = random.randint(0, 8)
		remCol = random.randint(0, 8)

		if board[remRow][remCol] != 0:
			board[remRow][remCol] = 0

	return Grid(9, 9, 540, 540, board)

#main function
def main():
	printInstructions()

	#here we can ask the user how difficult they want the puzzle and then generate the board based on the input
	#pass the input into createPuzzleFromBoard() 

	#randomly generate the first board
	board = generateRandomGrid()
	board = reorderRowGroups(board)
	board = reorderIndividualRows(board)
	board = reorderColGroups(board)
	board = reorderIndividualCols(board)
	completeBoard = Grid(9, 9, 540, 540, board)
	
	board = createPuzzleFromBoard(board)

	window = py.display.set_mode((540, 600))
	key = None
	run = True
	start = time.time()
	faults = 0
	maxFaults = 3

	#game loop
	while run:
		playTime = round(time.time() - start)
				
		for e in py.event.get():
			if e.type == py.QUIT:
				run = False
			if e.type == py.KEYDOWN:
				if e.key == py.K_1 or e.key == py.K_KP1:
					key = 1
				if e.key == py.K_2 or e.key == py.K_KP2:
					key = 2
				if e.key == py.K_3 or e.key == py.K_KP3:
					key = 3
				if e.key == py.K_4 or e.key == py.K_KP4:
					key = 4
				if e.key == py.K_5 or e.key == py.K_KP5:
					key = 5
				if e.key == py.K_6 or e.key == py.K_KP6:
					key = 6
				if e.key == py.K_7 or e.key == py.K_KP7:
					key = 7
				if e.key == py.K_8 or e.key == py.K_KP8:
					key = 8
				if e.key == py.K_9 or e.key == py.K_KP9:
					key = 9

				if e.key == py.K_DELETE or e.key == py.K_BACKSPACE:
					board.clear()
					key = None

				if e.key == py.K_RETURN:
					i, j = board.selected
					if board.cubes[i][j].temp != 0:
						if board.place(board.cubes[i][j].temp):
							print("Correct")
						else:
							print("Incorrect")
							faults += 1
							if faults >= maxFaults:
								print("Game Over!!!!")
								run = False
						key = None

						#board is full
						if board.isFinished():
							print("Congradulations!!!!!")
							board = generateRandomGrid()
							board = reorderRowGroups(board)
							board = reorderIndividualRows(board)
							board = reorderColGroups(board)
							board = reorderIndividualCols(board)
							completeBoard = Grid(9, 9, 540, 540, board)
							board = createPuzzleFromBoard(board)
							start = time.time()
							#run = False

				#auto solve the board when S key is clicked
				if e.key == py.K_s:
					board = completeBoard

				#generate a new board
				if e.key == py.K_g:
					board = generateRandomGrid()
					board = reorderRowGroups(board)
					board = reorderIndividualRows(board)
					board = reorderColGroups(board)
					board = reorderIndividualCols(board)
					completeBoard = Grid(9, 9, 540, 540, board)
					board = createPuzzleFromBoard(board)
					start = time.time()

			if e.type == py.MOUSEBUTTONDOWN:
				position = py.mouse.get_pos()
				clicked = board.click(position)	
				if clicked:
					board.select(clicked[0], clicked[1])
					key = None

		if board.selected and key != None:
			board.tempPlacement(key)


		redrawWindow(window, board, playTime, faults)
		py.display.update()

main()
py.quit()
