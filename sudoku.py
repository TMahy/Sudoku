
"""
Suduko Solver - Text Based
Given a solvable sudoku board, find a solution to the board.
Using the backtracking algorithm
"""
from random import randint, shuffle
from copy import deepcopy

def solveBoard(board):
    """
    Solves a given Sudoku board
    Param: 2d list of integers. (9x9 Board)
    1.Finds next empty cell
    2.Checks if value is valid
    3.Checks if board is solved
    4.Backtrack if no possible valid input
    """
    position = find_empty(board)
    if position:
        row, col = position
    else:
        print_board(board) 
        return True

    for value in range(1,10):
        if valid(board, row, col, value):
            board[row][col] = value
            if solveBoard(board):
                return True
            board[row][col] = 0
    return False

def fillBoard(board):
    """
    Fills an empty Sudoku board
    Param: 2d list of integers. (9x9 Board)
    1.Finds next empty cell
    2.Checks if value is valid in the empty position 
    (Randomised Value so board is generated differently each time)
    3.Checks if board is solved
    4.Backtrack if no possible valid input
    """
    position = find_empty(board)
    if position:
        row, col = position
    else:
        return True
    numberList = [1,2,3,4,5,6,7,8,9]
    shuffle(numberList)
    for value in numberList:
        if valid(board, row, col, value):
            board[row][col] = value
            if fillBoard(board):
                return True
            board[row][col] = 0
    return False

def gen_board():
    """
    Generates A Solvable Sudoku Puzzle
    param: None
    1. Starting with an empty board
    2. Fill a board completely
    3. Remove values one by one, checking that a solution still exists
    4. Until 55 numbers have been removed from the board
    or 
       3 attempts at removing a value fails. ie the board is unsovable.
    5. Return the solvable sudoku puzzle board
    """
    board = [  
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0]
            ]
    #Generate fully solved grid
    fillBoard(board)
    #Start removing numbers one by one 
    attempts = 3
    removed = 0
    while attempts>0 and removed <= 55:
        #Select a random cell that is not empty
        row = randint(0,8)
        col = randint(0,8)
        while board[row][col]== 0:
            row = randint(0,8)
            col = randint(0,8)
        backup = board[row][col]
        board[row][col] = 0
        #Takes a copy of the board with the removed element
        copyBoard = deepcopy(board)
        #Check if the board is still solvable, if not replace the value.
        if not solveBoard(copyBoard):
            board[row][col] = backup
            attempts -= 1
        removed +=1
    return board

def valid(board, row, col, value):
    """
    Returns if value is valid in the board
    param: board: 2d list of integers
    param: row, col: int
    param: value: int
    return: bool
    """
    #Check Row
    for i in range(0, len(board)):
        if board[row][i] == value and col != i:
            return False
    #Check Col
    for i in range(0, len(board)):
        if board[i][col] == value and col != i:
            return False
    #Check Square
    sq_x = (col//3)*3
    sq_y = (row//3)*3

    for i in range(sq_y, sq_y+3):
        for j in range(sq_x, sq_x+3):
            if board[i][j] == value and (i, j) != (row, col):
                return False
    return True

def find_empty(board):
    """
    finds the next empty space in the board
    param: board: 2d list of ints
    return: (int,int) row and column
    """
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0: 
                return (i,j)
    return None


def print_board(board):
    """
    prints the board
    param board: 2d list of ints
    """
    print("")
    for i in range(len(board)):
        if i%3==0 and i != 0:
            print(" --------------------------")
        for j in range(len(board[0])):
            if j%3==0:
                print(" | ", end="")
            if j == 8:
                print(str(board[i][j])+"|", end="\n")
            else:
                print(str(board[i][j])+" ", end="")
    print("")

board = [
        [3,0,6,5,0,8,4,0,0],
        [5,2,0,0,0,0,0,0,0],
        [0,8,7,0,0,0,0,3,1],
        [0,0,3,0,1,0,0,8,0],
        [9,0,0,8,6,3,0,0,5],
        [0,5,0,0,9,0,6,0,0],
        [1,3,0,0,0,0,2,5,0],
        [0,0,0,0,0,0,0,7,4],
        [0,0,5,2,0,6,3,0,0]
        ]

print_board(board)
print(solveBoard(board))