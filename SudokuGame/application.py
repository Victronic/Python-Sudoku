import pygame, sys
from attributes import *
from button import *

class App:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        self.running = True
        self.grid = testBoard1
        self.selectedCell = None
        self.mousePosition = None
        self.state = "playing"
        self.playButtons = []
        self.menuButtons = []
        self.endButtons = []
        self.loadButtons()

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

    def play_update(self):
        self.mousePosition = pygame.mouse.get_pos()
        for button in self.playButtons:
            button.update(self.mousePosition)

    def play_draw(self):
        self.window.fill(WHITE)

        for button in self.playButtons:
            button.draw(self.window)

        if self.selectedCell:
            self.drawSelected(self.window, self.selectedCell)
        self.drawGrid(self.window)
        pygame.display.update()

    # Helpers

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
