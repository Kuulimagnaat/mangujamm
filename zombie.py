import pygame

class Zombie(pygame.sprite.Sprite):
    def __init__(self, x, y, target=(0,0)):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.hp = 30
        self.target = target
        self.kiirus = 10
        self.walking = True


    def getPos(self):
        return (self.x, self.y)
    
    def setPos(self, givenX, givenY):
        self.x = givenX
        self.y = givenY
    
    def update(self):
        if self.walking:
            targetVector = (self.x-self.target[0], self.y-self.target[1])
            distance = ((targetVector[0])**2+(targetVector[1])**2)**(1/2)
            if distance <= 0.01:
                self.setPos(self.target[0], self.target[1])
            else:
                speedVector = (targetVector[0]/distance*self.kiirus, targetVector[1]/distance*self.kiirus)
                self.setPos(self.x+speedVector[0], self.y+speedVector[1])