import pygame, sys, time
from attributes import *
from button import *


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
        self.finished = False
        self.cellChanged = False
        self.endGame = False
        self.playButtons = []
        self.menuButtons = []
        self.endButtons = []
        self.lockedCells = []
        self.incorrectCells = []
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

    # Playing Game State
    # 1.Events
    def play_events(self):
        for event in pygame.event.get():
            # Quit button
            if event.type == pygame.QUIT:
                self.running = False

            # Mouse Click
            if event.type == pygame.MOUSEBUTTONDOWN:
                selected = self.mouseOnGrid()
                if not selected:
                    print("not on Board")
                    self.selectedCell = None
                elif selected in self.lockedCells:
                    print("You can not select locked cells")
                    self.selectedCell = None
                else:
                    self.selectedCell = selected
                    print(selected)


            # Key press
            if event.type == pygame.KEYDOWN:
                if self.selectedCell != None and self.selectedCell not in self.lockedCells and not self.endGame and not self.timeOut:
                    if self.isInt(event.unicode):
                        self.grid[self.selectedCell[0]][self.selectedCell[1]] = int(event.unicode)
                        self.cellChanged = True

            if self.endGame or self.timeOut:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        print("reset")
                        self.endGame = False
                        self.grid = generateRandomUncompletedBoard()
                        self.lockedCells = []
                        self.load()
                        self.start = time.time()
                        self.timeOut = False
                        self.playTime = 0
                        print(self.timeOut)
                        self.play_events()
                        self.play_update()
                        self.play_draw()



    # 2.Update
    def play_update(self):
        self.mousePosition = pygame.mouse.get_pos()
        for button in self.playButtons:
            button.update(self.mousePosition)

        if self.cellChanged:
            if self.allCellsAreCompleted():
                if self.checkAllConditionsAreTrue():
                    self.endGame = True

        if self.playTime>1800:
            self.timeOut = True



    # 3.Draw
    def play_draw(self):
        self.window.fill(WHITE)  # fill with white

        for button in self.playButtons:
            button.draw(self.window)

        if self.selectedCell:
            self.drawSelected(self.window, self.selectedCell)

        self.colourLockedCells(self.window, self.lockedCells)
        self.colourIncorrectCells(self.window, self.incorrectCells)

        self.textToWindow(self.window, "Complete the sudoku grid before the", [700, 10],BLACK)
        self.textToWindow(self.window, "timer reaches 0 ", [700, 35],BLACK)
        self.textToWindow(self.window, "Instructions:", [600, 100],BLACK)
        self.textToWindow(self.window, "1. the grey cells are locked", [700, 150],LOCKEDCELLSCOLOUR)
        self.textToWindow(self.window, "you can not change them", [700, 175],LOCKEDCELLSCOLOUR)
        self.textToWindow(self.window, "2. click on a not locked cell", [700, 220],BLUE)
        self.textToWindow(self.window, "to select it", [700, 245],BLUE)
        self.textToWindow(self.window, "3. type in a number while a cell is selected", [700, 290],BLUE)
        self.textToWindow(self.window, "to input a number in it",[700, 315],BLUE)
        self.textToWindow(self.window, "4.you can delete a number from", [700, 360],BLACK)
        self.textToWindow(self.window, " a not locked cell by pressing 0", [700, 385],BLACK)
        self.textToWindow(self.window, "5.If you won the game", [700, 430], GREEN)
        self.textToWindow(self.window, "or the time runs out,", [700, 455], RED)
        self.textToWindow(self.window, "you can press 'r' to start a new game ", [700, 480], BLACK)

        if not self.endGame and not self.timeOut:
            self.textToWindow(self.window,"time: " + str(29-self.playTime//60) + ":" + str(60-(self.playTime%60)-1),[50,600],BLACK)
        elif self.timeOut and not self.endGame:
            self.textToWindow(self.window, "Time out", [200, 600], RED)
        else:
            self.textToWindow(self.window, "Congratulations you won the game", [200, 600], GREEN)

        self.drawNumbers(self.window)

        self.drawGrid(self.window)


        pygame.display.update()

        self.cellChanged = False

    # Board functions

    def allCellsAreCompleted(self):
        print("am ajuns aici")
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0:
                    return False
        return True

    def checkAllConditionsAreTrue(self):
        if not self.checkRowsCondition():
            print("falserows")
            return False
        if not self.checkColumnsCondition():
            print("falseCol")
            return False
        if not self.checkLittleSquares():
            print("falseSquare")
            return False
        return True

    def checkRowsCondition(self):
        for row in range(9):
            d = []
            for col in range(9):
                val = self.grid[row][col]
                if val in d:
                    return False
                d.append(val)
        return True

    def checkColumnsCondition(self):
        for col in range(9):
            d = []
            for row in range(9):
                val = self.grid[row][col]
                if val in d:
                    return False
                d.append(val)
        return True

    def checkLittleSquares(self):
        for i in range(3):
            for j in range(3):
                d=[]
                for ii in range(3):
                    for jj in range(3):
                        row = (3*i) + ii
                        col = (3*j) + jj
                        val = self.grid[row][col]
                        if val in d:
                            return False
                        d.append(val)
        return True
    # Helpers

    # Colors the locked cells correctly
    def colourLockedCells(self, window, locked):
        for cell in locked:
            pygame.draw.rect(window, LOCKEDCELLSCOLOUR,
                             (cell[1] * cellSize + gridPos[0], cell[0] * cellSize + gridPos[1], cellSize, cellSize))

    def colourIncorrectCells(self, window, incorrect):
        for cell in incorrect:
            pygame.draw.rect(window, INCORRECTCELLCOLOUR,
                             (cell[1] * cellSize + gridPos[0], cell[0] * cellSize + gridPos[1], cellSize, cellSize))

    # The initial numbers are drawn correctly
    def drawNumbers(self, window):
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] != 0:
                    pos = [(j * cellSize) + gridPos[0], (i * cellSize) + gridPos[1]]
                    self.textToWindow(window, str(self.grid[i][j]), pos,BLACK)
        # for yindx, row in enumerate(self.grid):
        #     for xindx, number in enumerate(row):
        #         if number != 0:
        #             pos = [(xindx * cellSize) + gridPos[0], (yindx * cellSize) + gridPos[1]]
        #             self.textToWindow(window, str(number), pos)

    #
    def textToWindow(self, window, text, pos,color):
        font = self.font.render(text, False, color)
        fontWidth = font.get_width()
        fontHeight = font.get_height()
        pos[0] += (cellSize - fontWidth) // 2
        pos[1] += (cellSize - fontHeight) // 2
        window.blit(font, pos)

    # Draw the selected cell correctly
    def drawSelected(self, window, pos):
        pygame.draw.rect(window, BLUE,
                         ((pos[1] * cellSize) + gridPos[0], (pos[0] * cellSize) + gridPos[1], cellSize, cellSize))

    # Grid draw correctly
    def drawGrid(self, window):
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

    # Mouse position on grid correctly taken
    def mouseOnGrid(self):
        # mouse on the board=> return the matrix indices, else return false
        if self.mousePosition[0] < gridPos[0] or self.mousePosition[1] < gridPos[1]:
            return False
        if self.mousePosition[0] > gridPos[0] + gridSize or self.mousePosition[1] > gridPos[1] + gridSize:
            return False
        return [(self.mousePosition[1] - gridPos[1]) // cellSize, (self.mousePosition[0] - gridPos[0]) // cellSize]

    # Load buttons to window correctly
    def loadButtons(self):
        self.playButtons.append(Button(20, 40, 100, 40))

    # Load the buttons and make the locked cells list
    def load(self):
        self.loadButtons()
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] != 0:
                    self.lockedCells.append([i,j])
        # for yindx, row in enumerate(self.grid):
        #     for xindx, number in enumerate(row):
        #         if number != 0:
        #             self.lockedCells.append([xindx, yindx])

    def isInt(self, string):
        try:
            int(string)
            return True
        except:
            return False
