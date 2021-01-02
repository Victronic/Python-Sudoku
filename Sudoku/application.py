import pygame, sys
from attributes import *
from button import *

class App:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        self.running = True
        self.grid = testBoard2
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
        self.font = pygame.font.SysFont("arial",cellSize//2)
        self.load()

    def run(self):
        while self.running:
            if self.state == "playing":
                self.play_events()
                self.play_update()
                self.play_draw()
        pygame.quit()
        sys.exit()

    # Play

    def play_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                selectedCell = self.mouseOnGrid()
                if selectedCell:
                    self.selectedCell = selectedCell
                else:
                    print("not on Board")
                    self.selectedCell = None
            #user types a key
            if event.type == pygame.KEYDOWN:
                if self.selectedCell != None and self.selectedCell not in self.lockedCells:
                    if self.isInt(event.unicode):
                        self.grid[self.selectedCell[1]][self.selectedCell[0]] = int(event.unicode)
                        self.cellChanged = True

    def play_update(self):
        self.mousePosition = pygame.mouse.get_pos()
        for button in self.playButtons:
            button.update(self.mousePosition)

        if self.cellChanged:
            self.incorrectCells = []
            if self.allCellsAreDone():
                #check if board is correct
                self.checkAllCells()
                if len(self.incorrectCells) == 0:
                    print("Congratulation!")

    def play_draw(self):
        self.window.fill(WHITE)

        for button in self.playButtons:
            button.draw(self.window)

        if self.selectedCell:
            self.drawSelected(self.window, self.selectedCell)

        self.colourLockedCells(self.window,self.lockedCells)
        self.colourIncorrectCells(self.window,self.incorrectCells)

        self.drawNumbers(self.window)

        self.drawGrid(self.window)
        pygame.display.update()
        self.cellChanged = False

    #Board functions

    def allCellsAreDone(self):
        for row in self.grid:
            for number in row:
                if number == 0:
                    return False
        return True

    def checkAllCells(self):
        self.checkRows()
        self.checkColls()
        self.checkSmallGrid()

    def checkRows(self):
        for yindx, row in enumerate(self.grid):
            possible = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            for xindx in range(9):
                if self.grid[yindx][xindx] in possible:
                    possible.remove(self.grid[yindx][xindx])
                else:
                    if [xindx, yindx] not in self.lockedCells and [xindx][yindx] not in self.incorrectCells:
                        self.incorrectCells.append([xindx,yindx])
                    if [xindx, yindx] in self.lockedCells:
                        for k in range(9):
                            if self.grid[yindx][k] == self.grid[yindx][xindx] and [k,yindx] not in self.lockedCells:
                                self.incorrectCells.append([k,yindx])

    def checkColls(self):
        for xindx in range(9):
            possible = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            for yindx, row in enumerate(self.grid):
                if self.grid[yindx][xindx] in possible:
                    possible.remove(self.grid[yindx][xindx])
                else:
                    if [xindx, yindx] not in self.lockedCells and [xindx][yindx] not in self.incorrectCells:
                        self.incorrectCells.append([xindx,yindx])
                    if [xindx,yindx] in self.lockedCells:
                        for k,row in enumerate(self.grid):
                            if self.grid[k][xindx] == self.grid[yindx][xindx] and [xindx,k] not in self.lockedCells:
                                self.incorrectCells.append([xindx,k])

    def checkSmallGrid(self):
        for x in range(3):
            for y in range(3):
                possibles = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                for i in range(3):
                    for j in range(3):
                        xindx = x*3+i
                        yindx = y*3+j
                        if self.grid[yindx][xindx] in possibles:
                            possibles.remove(self.grid[yindx][xindx])
                        else:
                            if [xindx,yindx] not in self.lockedCells and [xindx,yindx] not in self.incorrectCells:
                                self.incorrectCells.append([xindx,yindx])
                            if [xindx, yindx] in self.lockedCells:
                                for k in range(3):
                                    for l in range(3):
                                        xindx2 = x*3+k
                                        yindx2 = y*3+l
                                        if self.grid[yindx2][xindx2] == self.grid[yindx][xindx] and [xindx2,yindx2] not in self.lockedCells:
                                            self.incorrectCells.append([xindx2,yindx2])




    # Helpers

    def colourLockedCells(self,window,locked):
        for cell in locked:
            pygame.draw.rect(window,LOCKEDCELLSCOLOUR,(cell[0]*cellSize+gridPos[0],cell[1]*cellSize+gridPos[1],cellSize,cellSize))

    def colourIncorrectCells(self,window,incorrect):
        for cell in incorrect:
            pygame.draw.rect(window,INCORRECTCELLCOLOUR,(cell[0]*cellSize+gridPos[0],cell[1]*cellSize+gridPos[1],cellSize,cellSize))


    def drawNumbers(self,window):
        for yindx,row in enumerate(self.grid):
            for xindx, number in enumerate(row):
                if number !=0:
                    pos = [(xindx*cellSize)+gridPos[0],(yindx*cellSize)+gridPos[1]]
                    self.textToWindow(window,str(number),pos)

    def drawSelected(self, window, pos):
        pygame.draw.rect(window, BLUE,
                         ((pos[0] * cellSize) + gridPos[0], (pos[1] * cellSize) + gridPos[1], cellSize, cellSize))

    def drawGrid(self, window):
        pygame.draw.rect(window, BLACK, (gridPos[0], gridPos[1], WIDTH - 150, HEIGHT - 150), 3)
        for x in range(9):
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
        if self.mousePosition[0] < gridPos[0] or self.mousePosition[1] < gridPos[1]:
            return False
        if self.mousePosition[0] > gridPos[0] + gridSize or self.mousePosition[1] > gridPos[1] + gridSize:
            return False
        return (self.mousePosition[0] - gridPos[0]) // cellSize, (self.mousePosition[1] - gridPos[1]) // cellSize

    def loadButtons(self):
        self.playButtons.append(Button(20,40,100,40))

    def textToWindow(self, window, text, pos):
        font = self.font.render(text,False,BLACK)
        fontWidth = font.get_width()
        fontHeight = font.get_height()
        pos[0] += (cellSize-fontWidth)//2
        pos[1] += (cellSize-fontHeight)//2
        window.blit(font, pos)

    def load(self):
        self.loadButtons()
        for yindx, row in enumerate(self.grid):
            for xindx, number in enumerate(row):
                if number !=0:
                    self.lockedCells.append([xindx,yindx])

    def isInt(self,string):
        try:
            int(string)
            return True
        except:
            return False
