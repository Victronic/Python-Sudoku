__doc__ = "attributes"

from random import *

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (96, 216, 232)
GREEN = (34,139,34)
RED = (254,0,0)
LOCKEDCELLSCOLOUR = (189, 189, 189)
INCORRECTCELLCOLOUR = (194, 120, 120)
TEXTCOLOR = ((96, 216, 232))


# boards
def generateRandomUncompletedBoard():
    possibleNumber = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    board = [[0 for i in range(9)] for j in range(9)]

    line = sample(possibleNumber, len(possibleNumber))
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

    for i in range(30):
        i = randint(0, 8)
        j = randint(0, 8)
        while board[i][j] == 0:
            i = randint(0, 8)
            j = randint(0, 8)
        board[i][j] = 0
    return board


testBoardCompleted1 = [[5, 3, 4, 6, 7, 8, 9, 1, 2],
                      [6, 7, 2, 1, 9, 5, 3, 4, 8],
                      [1, 9, 8, 3, 4, 2, 5, 6, 7],
                      [8, 5, 9, 7, 6, 1, 4, 2, 3],
                      [4, 2, 6, 8, 5, 3, 7, 9, 1],
                      [7, 1, 3, 9, 2, 4, 8, 5, 6],
                      [9, 6, 1, 5, 3, 7, 2, 8, 4],
                      [2, 8, 7, 4, 1, 9, 6, 3, 5],
                      [3, 4, 5, 2, 8, 6, 1, 7, 9]]


testBoardUncompleted1 = [[0, 3, 0, 6, 0, 0, 9, 0, 2],
                         [6, 0, 2, 1, 0, 5, 0, 0, 8],
                         [1, 9, 0, 3, 4, 2, 5, 6, 0],
                         [0, 0, 9, 0, 6, 0, 4, 2, 0],
                         [4, 0, 6, 0, 0, 0, 7, 0, 1],
                         [0, 1, 3, 0, 2, 0, 8, 0, 6],
                         [9, 0, 1, 0, 3, 0, 0, 8, 0],
                         [0, 8, 0, 4, 0, 9, 6, 0, 0],
                         [3, 0, 5, 0, 8, 0, 1, 0, 9]]

# positions
gridPos = (20, 100)

# allSizes

# windowSizes
WIDTH = 1000
HEIGHT = 700

# cellSize
cellSize = 50
gridSize = cellSize * 9
