import pygame

class Button:
    def __init__(self,x,y,width,height, text=None, colou = (73,73,73),highlightedColour=(189,189,189),function = None,parameters=None):
        self.image = pygame.Surface((width,height))
        self.pos = (x,y)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos
        self.text = text
        self.colour = colou
        self.highlightedColour = highlightedColour
        self.function = function
        self.parameters = parameters
        self.highlighted = False

    def update(self,mouse):
        if self.rect.collidepoint(mouse):
            self.highlighted = True
        else:
            self.highlighted = False

    def draw(self,window):
        # self.image.fill(self.highlightedColour if self.highlighted else self.colour)
        if self.highlighted:
            self.image.fill(self.highlightedColour)
        else:
            self.image.fill(self.colour)
        window.blit(self.image,self.pos)