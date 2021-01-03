import pygame, sys, time
from attributes import *
from button import *


class App:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("SUDOKU")
        self.running = True
        self.grid = testBoardUncompleted
        self.completedGrid = testBoardCompleted
        self.selectedCell = None
        self.mousePosition = None
        self.state = "playing"
        self.finished = False
        self.cellChanged = False
        self.playButtons = []
        self.menuButtons = []
        self.endButtons = []
        self.lockedCells = []
        self.incorrectCells = []
        self.font = pygame.font.SysFont("arial", cellSize // 2)
        self.load()
        self.playTime = 0

    def run(self):
        start = time.time()
        while self.running and self.playTime<1800:
            self.playTime = round(time.time() - start)
            print(self.playTime)
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
                if self.selectedCell != None and self.selectedCell not in self.lockedCells:
                    if self.isInt(event.unicode):
                        self.grid[self.selectedCell[0]][self.selectedCell[1]] = int(event.unicode)
                        # self.cellChanged = True



    # 2.Update
    def play_update(self):
        self.mousePosition = pygame.mouse.get_pos()
        for button in self.playButtons:
            button.update(self.mousePosition)

        if self.grid == self.completedGrid:
            print("Congratulations")

        # if self.cellChanged:
        #     self.incorrectCells = []
        #     if self.allCellsAreDone():
        #         # check if board is correct
        #         self.checkAllCells()
        #         if len(self.incorrectCells) == 0:
        #             print("Congratulation!")

    # 3.Draw
    def play_draw(self):
        self.window.fill(WHITE)  # fill with white

        for button in self.playButtons:
            button.draw(self.window)

        if self.selectedCell:
            self.drawSelected(self.window, self.selectedCell)

        self.colourLockedCells(self.window, self.lockedCells)
        self.colourIncorrectCells(self.window, self.incorrectCells)

        self.textToWindow(self.window,"time: " + str(29-self.playTime//60) + ":" + str(60-(self.playTime%60)-1),[50,600])

        self.drawNumbers(self.window)

        self.drawGrid(self.window)


        pygame.display.update()

        self.cellChanged = False

    # Time
    def format_time(secs):
        sec = secs % 60
        minute = secs // 60
        hour = minute // 60

        mat = " " + str(minute) + ":" + str(sec)
        return mat
    # Board functions

    # def allCellsAreDone(self):
    #     for row in self.grid:
    #         for number in row:
    #             if number == 0:
    #                 return False
    #     return True
    #
    # def checkAllCells(self):
    #     self.checkRows()
    #     self.checkColls()
    #     self.checkSmallGrid()
    #
    # def checkRows(self):
    #     for yindx, row in enumerate(self.grid):
    #         possible = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    #         for xindx in range(9):
    #             if self.grid[yindx][xindx] in possible:
    #                 possible.remove(self.grid[yindx][xindx])
    #             else:
    #                 if [xindx, yindx] not in self.lockedCells and [xindx][yindx] not in self.incorrectCells:
    #                     self.incorrectCells.append([xindx, yindx])
    #                 if [xindx, yindx] in self.lockedCells:
    #                     for k in range(9):
    #                         if self.grid[yindx][k] == self.grid[yindx][xindx] and [k, yindx] not in self.lockedCells:
    #                             self.incorrectCells.append([k, yindx])
    #
    # def checkColls(self):
    #     for xindx in range(9):
    #         possible = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    #         for yindx, row in enumerate(self.grid):
    #             if self.grid[yindx][xindx] in possible:
    #                 possible.remove(self.grid[yindx][xindx])
    #             else:
    #                 if [xindx, yindx] not in self.lockedCells and [xindx][yindx] not in self.incorrectCells:
    #                     self.incorrectCells.append([xindx, yindx])
    #                 if [xindx, yindx] in self.lockedCells:
    #                     for k, row in enumerate(self.grid):
    #                         if self.grid[k][xindx] == self.grid[yindx][xindx] and [xindx, k] not in self.lockedCells:
    #                             self.incorrectCells.append([xindx, k])
    #
    # def checkSmallGrid(self):
    #     for x in range(3):
    #         for y in range(3):
    #             possibles = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    #             for i in range(3):
    #                 for j in range(3):
    #                     xindx = x * 3 + i
    #                     yindx = y * 3 + j
    #                     if self.grid[yindx][xindx] in possibles:
    #                         possibles.remove(self.grid[yindx][xindx])
    #                     else:
    #                         if [xindx, yindx] not in self.lockedCells and [xindx, yindx] not in self.incorrectCells:
    #                             self.incorrectCells.append([xindx, yindx])
    #                         if [xindx, yindx] in self.lockedCells:
    #                             for k in range(3):
    #                                 for l in range(3):
    #                                     xindx2 = x * 3 + k
    #                                     yindx2 = y * 3 + l
    #                                     if self.grid[yindx2][xindx2] == self.grid[yindx][xindx] and [xindx2,
    #                                                                                                  yindx2] not in self.lockedCells:
    #                                         self.incorrectCells.append([xindx2, yindx2])

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
                    self.textToWindow(window, str(self.grid[i][j]), pos)
        # for yindx, row in enumerate(self.grid):
        #     for xindx, number in enumerate(row):
        #         if number != 0:
        #             pos = [(xindx * cellSize) + gridPos[0], (yindx * cellSize) + gridPos[1]]
        #             self.textToWindow(window, str(number), pos)

    #
    def textToWindow(self, window, text, pos):
        font = self.font.render(text, False, BLACK)
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
