import pygame
import time
from random import randint, shuffle
from copy import deepcopy
pygame.init()

def solveBoard(board):
    """
    Solves a given Sudoku board
    Param: 2d list of integers. (9x9 Board)
    1.Finds next empty cell
    2.Checks if value is valid in the empty position
    3.Checks if board is solved
    4.Backtrack if no possible valid input
    """
    position = find_empty(board)
    if position:
        row, col = position
    else:
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

class Board:
    """
    Defines the board object
    params: rows: int, cols: int, width: int, height: int, screen: pygame window
    """
    board = gen_board()
    
    def __init__(self, rows, cols, width, height, screen):
        #Number of rows in the board: 9
        self.rows = rows
        #Number of cols in the board: 9 
        self.cols = cols
        #Boxes is a 2D array of box objects (9 x 9) 
        self.boxes = [[Box(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        #Width of the board on the screen
        self.width = width
        #Height of the board on the screen 
        self.height = height
        #Model stores the values of each box in the board
        self.model = None
        self.update_model()
        #Screen is the pygame window
        self.screen = screen 

    def update_model(self):
        """
        Updates the model to the new values stored in the boxes on the board
        """
        self.model = [[self.boxes[i][j].value for j in range(self.cols)] for i in range(self.rows)]
    
    def draw(self):
        """
        Draws the enitre sudoku board to the screen
        1. 1st the grid lines
        2. Draws the boxes
        """
        #Draw board
        gap = self.width / 9
        for i in range(self.rows+1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else: 
                thick = 1
            #Outer lines thicker. inner lines thinner.
            pygame.draw.line(self.screen, (0,0,0), (0, i*gap), (self.width, i*gap), thick)
            pygame.draw.line(self.screen, (0,0,0), (i*gap, 0), (i*gap, self.height), thick)
        #Draw boxes
        for i in range(self.rows):
            for j in range(self.cols):
                self.boxes[i][j].draw(self.screen)

    def solve_gui(self):
        """
        Solves the board.
        Colouring solved cells red, and checked but unsolved cells red.
        """
        self.update_model()
        find = find_empty(self.model)
        if not find:
            return True
        else:
            row, col = find
        for value in range(1,10):
            if valid(self.model, row, col, value):
                self.model[row][col] = value
                self.boxes[row][col].set(value)
                self.boxes[row][col].draw_change(self.screen, True)
                self.update_model()
                pygame.display.update()
                pygame.time.delay(10)
                if self.solve_gui():
                    return True
                self.model[row][col] = 0
                self.boxes[row][col].set(0)
                self.boxes[row][col].draw_change(self.screen, False)
                self.update_model()
                pygame.display.update()
                pygame.time.delay(10)
        return False

class Box:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width, height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col 
        self.width = width 
        self.height = height

    def draw(self, screen):
        fnt = pygame.font.SysFont("comicsans", 40)

        gap = self.width / 9
        x = self.col * gap 
        y = self.row * gap

        if not (self.value == 0):
            text = fnt.render(str(self.value), 1, (0,0,0))
            screen.blit(text, (x+(gap / 2 - text.get_width() / 2), y+(gap / 2 - text.get_height() / 2)))

    def draw_change(self, screen, g=True):
        fnt = pygame.font.SysFont("comicsans", 40)
        
        gap = self.width / 9 
        x = self.col * gap 
        y = self.row * gap

        pygame.draw.rect(screen, (255,255,255), (x, y, gap, gap), 0)

        text = fnt.render(str(self.value), 1, (0,0,0))
        screen.blit(text, (x+(gap / 2 - text.get_width() / 2), y+(gap / 2 - text.get_height() / 2)))
        if g:
            pygame.draw.rect(screen, (0,255,0), (x,y,gap,gap), 3)
        else:
            pygame.draw.rect(screen, (255,0,0), (x,y,gap,gap), 3)

    def set(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val

def draw_screen(screen, board, time):
    #Colour screen white
    screen.fill((255,255,255))
    #Draw Timer
    font = pygame.font.SysFont("comicsans", 40)
    text = font.render("Time to Solve: " + str(time/1000), True, pygame.Color("black"))
    screen.blit(text, (20, 560))
    #Draw Board
    board.draw()

def main():
    screen = pygame.display.set_mode((540,600))
    pygame.display.set_caption('Sudoku - press spacebar to solve.')
    board = Board(9,9, 540,540, screen)

    clock = pygame.time.Clock()
    passed_time = 0
    timer_started = False
    key = None
    done = False

    #Event loop
    while not done: 
        for event in pygame.event.get():
            #Exit on close window
            if event.type == pygame.QUIT:
                done = True
            #Keydown events
            if event.type == pygame.KEYDOWN:
                #Solve the board on spacebar press
                if event.key == pygame.K_SPACE:
                    timer_started = not timer_started
                    if timer_started:
                        #Starts a timer to see how long it takes to solve the board
                        start_time = pygame.time.get_ticks()
                    #Solve the board
                    board.solve_gui()
        #Stops the timer after .solve_gui() completes 
        if timer_started:
            passed_time = pygame.time.get_ticks()-start_time
            timer_started = not timer_started
        draw_screen(screen, board, passed_time)
        pygame.display.update()
        clock.tick(30)  

main()
                