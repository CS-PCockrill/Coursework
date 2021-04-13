#-------------------------------------------------------------------------------
# Name: Patrick Cockrill
# Project 4
# Due Date: Monday, April 1, 2019
#-------------------------------------------------------------------------------
# Honor Code Statement: I received no assistance on this assignment that
# violates the ethical guidelines set forth by professor and class syllabus.
#-------------------------------------------------------------------------------
# References: (list resources used - remember, projects are individual effort!)
#-------------------------------------------------------------------------------
# Comments and assumptions: A note to the grader as to any problems or
# uncompleted aspects of the assignment, as well as any assumptions about the
# meaning of the specification.
#-------------------------------------------------------------------------------
# NOTE: width of source code should be <=80 characters to be readable on-screen.
#2345678901234567890123456789012345678901234567890123456789012345678901234567890 # 10 20 30 40 50 60 70 80
#-------------------------------------------------------------------------------
def init_empty_cells(width, height):
	rows = []
	if width > 0 and height > 0:
		# The width or height parameters cannot equal 0 or be negative
		for i in range(int(height)):
			# Outer loop of the amount of rows
			columns = []
			for j in range(int(width)):
				# Creating the nested columns inside the list of rows
				cell = [0]
				columns += cell
			rows += [columns]
	else:
		return []
	return rows

def copy(cells):
	# Init a new empty list to create a deep copy
	deepCopy = []
	for i in range(len(cells)):
		nestList = []
		# Init an inner list that fills each row every loop
		for j in range(len(cells[i])):
			nestList.append(cells[i][j])
		deepCopy.append(nestList)
	return deepCopy

def is_valid(cells, row, col):
	# Declaring variables that get length of rows and columns
	height = len(cells)
	width = len(cells[0])

	# Conditional statements to check if rows and columns are in bounds
	if row < 0 or row >= height:
		return False
	elif col < 0 or col >= width:
		return False
	else:
		return True

def toggle_cell(row, column, cells):
	#cells = copy(cells)
	# if is_valid(row,column,cells):
	if is_valid(cells,row,column):
		if cells[row][column] == 0:
			cells[row][column] = 1
			return True
		if cells[row][column] == 1:
			cells[row][column] = 0
			return True
	else:
		return False

def set_pattern(shape,row,column,cells): #Half the tests have passed. Create the torus
	shape = str(shape)
	width = len(cells[0])
	height = len(cells)
	# if (row+1 % height) >= 1 or (column+1 % width) >= 1:
	# 	print('Index out of range')

	# It takes you back up to the top, if youre at row 29 col 0 and i put a block there

	if is_valid(cells,row,column) == True:
		# Use toggle cell to toggle each cell respective to the input
		# Block creates a 2 x 2 Square
		if shape == 'block':
			cell = toggle_cell(row,column,cells)
			cell += toggle_cell(row,(column+1 % width),cells)
			cell += toggle_cell((row+1 % height),(column+1 % width),cells)
			cell += toggle_cell((row+1 % height),column,cells)
			return cell

		# This is 3 blocks high and is a line
		if shape == 'blinker':
			cell = toggle_cell(row,(column+1 % width),cells)
			cell += toggle_cell((row+1 % height),(column+1 % width),cells)
			cell += toggle_cell((row+2 % height),(column+1 % width),cells)
			return cell

		# A weird looking pixel glider
		if shape == 'glider':
			cell = toggle_cell(row,(column+1 % width),cells)
			cell += toggle_cell((row+1 % height),(column+2 % width),cells)
			cell += toggle_cell((row+2 % height),column,cells)
			cell += toggle_cell((row+2 % height),(column+1 % width),cells)
			cell += toggle_cell((row+2 % height),(column+2 % width),cells)
			return cell

		# A bigger block with the same concept as 'block'
		if shape == 'bigblock':
			cell = toggle_cell(row,column,cells)
			cell += toggle_cell(row,column+1,cells)
			cell += toggle_cell(row,column+2,cells)
			cell += toggle_cell((row+1 % height),column,cells)
			cell += toggle_cell((row+1 % height),(column+1 % width),cells)
			cell += toggle_cell((row+1 % height),(column+2 % width),cells)
			cell += toggle_cell((row+2 % height),column,cells)
			cell += toggle_cell((row+2 % height),(column+1 % width),cells)
			cell += toggle_cell((row+2 % height),(column+2 % width),cells)
			return cell

		# the letter R i guess?
		if shape == 'R':
			cell = toggle_cell(row,(column+1 % width),cells)
			cell += toggle_cell(row,(column+2 % width),cells)
			cell += toggle_cell((row+1 % height),column,cells)
			cell += toggle_cell((row+1 % height),(column+1 % width),cells)
			cell += toggle_cell((row+2 % height),(column+1 % width),cells)
			return cell
	else:
		return False

def count_neighbors(cells,row,col):
	# Init count
	count = 0
	height = len(cells)
	width = len(cells[0])
	# If the initial row,col is valid move forward
	if is_valid(cells,row,col):
		for i in range(row-1,row+2):
			# Declaring the range in which neighbors are
			for j in range(col-1,col+2):
				if is_valid(cells,i,j) and cells[i][j] == True:
					count += 1

				# If the row is on the bottom edge then look at the top row
# ======Comment this boundary, and the update will run but its buggy======================
				elif row == (len(cells)-1):
					if i+1 == len(cells):
						first = cells[0]
						if first[j] == 1:
							count += 1
				# If the row is on the top edge then look at the bottom row
				elif row == 0:
					if i-1 == 0:
						last = cells[-1]
						if last[j] == 1:
							count += 1
				# If the call is on the last element of the inner list
				# we need to look at the elements at the front of the lists
		if col == (len(cells[0])-1):
			# Define variables for the neighbor locations on columns elements
			# if the column is hanging on the rightside edge
			centerRight = cells[row][0]
			upRight = cells[row-1][0]
			downRight = cells[row+1][0]
			# These are 1 up, 1 down, and center elements
			if centerRight == 1:
				count += 1
			if upRight == 1:
				count += 1
			if downRight == 1:
				count += 1

		if col == 0:
			# Define variables for the neighbor locations on columns elements
			# if the column is hanging on the lefthand side
			centerLeft = cells[row][-1]
			upLeft = cells[row-1][-1]
			downLeft = cells[row+1][-1]
			# These variables are the 1 up, 1 down, and the center
			if centerLeft == 1:
				count += 1
			if upLeft == 1:
				count += 1
			if downLeft == 1:
				count += 1
# =========Comment this boundary and the program will run, however update is buggy=======================

	# If the index is at the original point subtract it if it was True/1
	if cells[row][col] == 1:
		count -= 1

	if is_valid(cells,row,col) != True:
		return -1
	return count

def reflect(cells, axis):
	reflection = []
	# Init new list for the reflection
	if axis == 'x':
		# X axis reflection
		for i in range(len(cells)-1,-1,-1):
			reflection.append(cells[i])
	if axis == 'y':
		# Y axis reflection
		for i in range(len(cells)):
			# a new nested list to create
			# new instances of every 2d List in order to append later
			nested = []
			# Reverses each value inside cells[i] using Range
			for j in range(len(cells[i])-1,-1,-1):
				nested.append(cells[i][j])
			reflection.append(nested)
	return reflection

def invert(cells):
	# Invert just turns the cells that are value 0 to 1 and vise versa
	for i in range(len(cells)):
		nested = cells[i]
		for j in range(len(nested)):
			if nested[j] == 1:
				nested[j] = 0
			else:
				nested[j] = 1
	return cells

def translate(cells, direction):
	deep = copy(cells)
	shift = 1
	# Changes the location 1 by one every time arrow keys are touched
	if direction == 'left':
		newList = []
		for i in range(len(deep)):
			# Slicing the list of a deep copy and setting cells to it
			newList.append(deep[i][shift:] + deep[i][:shift])
		cells = newList
		return cells

	if direction == 'right':
		newList = []
		for i in range(len(deep)):
			# Slicing the list of a deep copy and setting cells to it
			newList.append(deep[i][-shift:] + deep[i][:-shift])
		cells = newList
		return cells

	if direction == 'up':
		newList = []
		for i in range(len(deep)):
			# Slicing the list of a deep copy and returning it
			return deep[shift:] + deep[:shift]

	if direction == 'down':
		newList = []
		for i in range(len(deep)):
			# Slicing the list of a deep copy and returning it
			return deep[-shift:] + deep[:-shift]

def update(cells):
	height = len(cells)

	nextGen = copy(cells)
	for i in range(height):
		totalCols = len(nextGen[i])
		for j in range(totalCols):
			neighbors = count_neighbors(cells,i,j)
			# if the value at cells[i][j] is 1 and fulfills the cases then
			# set a deep copy of the lists item to either 0 or 1 based on
			# The rules to the Conway's game of life....
			if cells[i][j] == 1:
				if neighbors < 2:
					nextGen[i][j] = 0
					# del cells[i][j]
				elif neighbors > 3:
					nextGen[i][i] = 0
					# del cells[i][j]
			else:
				if neighbors == 3:
					nextGen[i][j] = 1
					# del cells[i][j]
				elif neighbors == 2 or neighbors == 3:
					nextGen[i][j] = 0

	return nextGen

# If it has a remainder that is 1 or higher, wrap it to the first element
