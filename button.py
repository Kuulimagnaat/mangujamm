import pygame

class Button():
    def __init__(self, x, y, width, height, text, bgcolor=(176, 156, 113), textcolor=(0,0,0)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.bgcolor = bgcolor
        self.textcolor = textcolor

    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False

    def draw(self, win, outline=None):
        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x-2, self.y-2, self.width+4, self.height+4), 0)
            
        pygame.draw.rect(win, self.bgcolor, (self.x, self.y, self.width, self.height), 0)
        
        if self.text != '':
            font = pygame.font.Font("./assets/demon_panic.otf", 32)
            text = font.render(self.text, 1, self.textcolor)
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))