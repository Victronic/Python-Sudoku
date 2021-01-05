import pygame
import sys
import time
from attributes import *


class App:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("SUDOKU")
        self.running = True
        self.grid = generateRandomUncompletedBoard()
        self.selectedCell = None
        self.mousePosition = None
        self.state = "playing"
        self.cellChanged = False
        self.endGame = False
        self.lockedCells = []
        self.font = pygame.font.SysFont("arial", cellSize // 2)
        self.start = 0
        self.load()
        self.playTime = 0
        self.timeOut = False

    def run(self):
        self.start = time.time()
        while self.running:
            self.playTime = round(time.time() - self.start)
            if self.state == "playing":
                self.play_events()
                self.play_update()
                self.play_draw()
        pygame.quit()
        sys.exit()

    # PLAYING GAME STATE #
    # 1.Events
    def play_events(self):
        """
        Handles the events of the game
        """
        for event in pygame.event.get():

            # Quit button
            if event.type == pygame.QUIT:
                self.running = False

            # Mouse Click
            if event.type == pygame.MOUSEBUTTONDOWN:
                selected = self.mouseOnGrid()
                if not selected or selected in self.lockedCells:
                    self.selectedCell = None
                else:
                    self.selectedCell = selected

            # Key press
            if event.type == pygame.KEYDOWN:
                if self.selectedCell is not None and self.selectedCell not in self.lockedCells and not self.endGame and not self.timeOut:
                    if self.isInt(event.unicode):
                        self.grid[self.selectedCell[0]][self.selectedCell[1]] = int(event.unicode)
                        self.cellChanged = True

            # Reset game
            if self.endGame or self.timeOut:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.resetGame()

    # 2.Update
    def play_update(self):
        """
        Handles the updates of the game state
        """
        self.mousePosition = pygame.mouse.get_pos()

        if self.cellChanged:
            if self.allCellsAreCompleted():
                if self.allConditionsAreTrue():
                    self.endGame = True

        if self.playTime > 1800:
            self.timeOut = True

    # 3.Draw
    def play_draw(self):
        """
        Handles the draws of the games components
        """
        self.window.fill(WHITE)

        if self.selectedCell:
            self.drawSelected(self.window, self.selectedCell)

        self.colourLockedCells(self.window, self.lockedCells)

        self.instructions()
        self.timer()

        self.drawNumbers(self.window)
        self.drawGrid(self.window)

        pygame.display.update()

        self.cellChanged = False

    # BOARD FUNCTIONS

    def allCellsAreCompleted(self):
        """
        :return: boolean (depending on the state of the completed cells)
        """
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0:
                    return False
        return True

    def allConditionsAreTrue(self):
        """
        :return: boolean (depending on the completed puzzle)
        """
        if not self.checkRowsCondition():
            return False
        if not self.checkColumnsCondition():
            return False
        if not self.checkLittleSquares():
            return False
        return True

    def checkRowsCondition(self):
        """
        :return: boolean (depending on the correctness of the rows)
        """
        for row in range(9):
            d = []
            for col in range(9):
                val = self.grid[row][col]
                if val in d:
                    return False
                d.append(val)
        return True

    def checkColumnsCondition(self):
        """
        :return: boolean (depending on the correctness of the columns)
        """
        for col in range(9):
            d = []
            for row in range(9):
                val = self.grid[row][col]
                if val in d:
                    return False
                d.append(val)
        return True

    def checkLittleSquares(self):
        """
        :return: boolean (depending on the correctness of the small squares)
        """
        for i in range(3):
            for j in range(3):
                d = []
                for ii in range(3):
                    for jj in range(3):
                        row = (3 * i) + ii
                        col = (3 * j) + jj
                        val = self.grid[row][col]
                        if val in d:
                            return False
                        d.append(val)
        return True

    # HELPERS

    def resetGame(self):
        """
        Resets the variables of the game so a new one is created
        """
        self.endGame = False
        self.grid = generateRandomUncompletedBoard()
        self.lockedCells = []
        self.load()
        self.start = time.time()
        self.timeOut = False
        self.playTime = 0

    def instructions(self):
        """
        calls the function to write on the window
        """
        self.textToWindow(self.window, "Complete the sudoku grid before the", [700, 10], BLACK)
        self.textToWindow(self.window, "timer reaches 0 ", [700, 35], BLACK)
        self.textToWindow(self.window, "Instructions:", [700, 100], BLACK)
        self.textToWindow(self.window, "1. the grey cells are locked", [700, 150], LOCKEDCELLSCOLOUR)
        self.textToWindow(self.window, "you can not change them", [700, 175], LOCKEDCELLSCOLOUR)
        self.textToWindow(self.window, "2. click on a not locked cell", [700, 220], BLUE)
        self.textToWindow(self.window, "to select it", [700, 245], BLUE)
        self.textToWindow(self.window, "3. type in a number while a cell is selected", [700, 290], BLUE)
        self.textToWindow(self.window, "to input a number in it", [700, 315], BLUE)
        self.textToWindow(self.window, "4.you can delete a number from", [700, 360], BLACK)
        self.textToWindow(self.window, " a not locked cell by pressing 0", [700, 385], BLACK)
        self.textToWindow(self.window, "5.If you won the game", [700, 430], GREEN)
        self.textToWindow(self.window, "or the time runs out,", [700, 455], RED)
        self.textToWindow(self.window, "you can press 'r' to start a new game ", [700, 480], BLACK)
        self.textToWindow(self.window, "6. Once the game is over you can't", [700, 525], BLACK)
        self.textToWindow(self.window, "interact with the board anymore", [700, 550], BLACK)

    def timer(self):
        """
        Calls the function to write the timer or the state of the game on the window
        """
        if not self.endGame and not self.timeOut:
            self.textToWindow(self.window,
                              "time: " + str(29 - self.playTime // 60) + ":" + str(60 - (self.playTime % 60) - 1),
                              [50, 600], BLACK)
        elif self.timeOut and not self.endGame:
            self.textToWindow(self.window, "Time out", [200, 600], RED)
        else:
            self.textToWindow(self.window, "Congratulations you won the game", [200, 600], GREEN)

    def colourLockedCells(self, window, locked):
        """
        :param window: the window where the modifications are made
        :param locked: the list of position where the change is made
        Colours the list of numbers that are already in the puzzle
        """
        for cell in locked:
            pygame.draw.rect(window, LOCKEDCELLSCOLOUR,
                             (cell[1] * cellSize + gridPos[0], cell[0] * cellSize + gridPos[1], cellSize, cellSize))

    def drawNumbers(self, window):
        """
        :param window: the window where the modifications are made
        Draws the numbers of the puzzle
        """
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] != 0:
                    pos = [(j * cellSize) + gridPos[0], (i * cellSize) + gridPos[1]]
                    self.textToWindow(window, str(self.grid[i][j]), pos, BLACK)

    def textToWindow(self, window, text, pos, color):
        """
        :param window: the window where the modifications are made
        :param text: the text given
        :param pos: the position to be draw
        :param color: the color to be used
        Writes text on the window
        """

        font = self.font.render(text, False, color)
        font_width = font.get_width()
        font_height = font.get_height()
        pos[0] += (cellSize - font_width) // 2
        pos[1] += (cellSize - font_height) // 2
        window.blit(font, pos)

    def drawSelected(self, window, pos):
        """
        :param window: the window where the modifications are made
        :param pos: the position to be draw
        Draws a square at the selected square to highlight it
        """
        pygame.draw.rect(window, BLUE,
                         ((pos[1] * cellSize) + gridPos[0], (pos[0] * cellSize) + gridPos[1], cellSize, cellSize))

    def drawGrid(self, window):
        """
        :param window: the window where the modifications are made
        Draws the sudoku grid
        """
        for x in range(10):
            if x % 3 != 0:
                pygame.draw.line(window, BLACK, (gridPos[0] + (x * cellSize), gridPos[1]),
                                 (gridPos[0] + (x * cellSize), gridPos[1] + 450))
                pygame.draw.line(window, BLACK, (gridPos[0], gridPos[1] + (x * cellSize)),
                                 (gridPos[0] + 450, gridPos[1] + (x * cellSize)))
            else:
                pygame.draw.line(window, BLACK, (gridPos[0] + (x * cellSize), gridPos[1]),
                                 (gridPos[0] + (x * cellSize), gridPos[1] + 450), 3)
                pygame.draw.line(window, BLACK, (gridPos[0], gridPos[1] + (x * cellSize)),
                                 (gridPos[0] + 450, gridPos[1] + (x * cellSize)), 3)

    def mouseOnGrid(self):
        """
        :return: the position in matrix indices where the mouse left button was pressed (if on the puzzle)
        """
        if self.mousePosition[0] < gridPos[0] or self.mousePosition[1] < gridPos[1]:
            return False
        if self.mousePosition[0] > gridPos[0] + gridSize or self.mousePosition[1] > gridPos[1] + gridSize:
            return False
        return [(self.mousePosition[1] - gridPos[1]) // cellSize, (self.mousePosition[0] - gridPos[0]) // cellSize]

    def load(self):
        """
        Creates locked cells list
        :return:
        """
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] != 0:
                    self.lockedCells.append([i, j])

    def isInt(self, string):
        """
        :param string: key the user has pressed
        :return: True if a number, False if not
        """
        try:
            int(string)
            return True
        except:
            return False
