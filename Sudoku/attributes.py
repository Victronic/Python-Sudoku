__doc__ = "The file where I store the constants and generate the puzzle"

from random import *

# Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (96, 216, 232)
GREEN = (34, 139, 34)
RED = (254, 0, 0)
LOCKEDCELLSCOLOUR = (189, 189, 189)


# Board


def generateRandomUncompletedBoard():
    """
    :return: a random sudoku puzzle
    """
    possible_number = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    board = [[0 for i in range(9)] for j in range(9)]
    line = sample(possible_number, len(possible_number))
    board[0] = line
    line = line[3:] + line[:3]
    board[1] = line
    line = line[3:] + line[:3]
    board[2] = line
    line = line[1:] + line[:1]
    board[3] = line
    line = line[3:] + line[:3]
    board[4] = line
    line = line[3:] + line[:3]
    board[5] = line
    line = line[1:] + line[:1]
    board[6] = line
    line = line[3:] + line[:3]
    board[7] = line
    line = line[3:] + line[:3]
    board[8] = line

    for i in range(50):
        i = randint(0, 8)
        j = randint(0, 8)
        while board[i][j] == 0:
            i = randint(0, 8)
            j = randint(0, 8)
        board[i][j] = 0
    return board


# positions

gridPos = (20, 100)

# windowSizes
WIDTH = 1000
HEIGHT = 700

# cellSize
cellSize = 50
gridSize = cellSize * 9
