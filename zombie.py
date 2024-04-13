import pygame
from numpy import linalg, cross

class Zombie(pygame.sprite.Sprite):
    def __init__(self, x, y, target=(0,0)):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([100, 100])
        self.image.fill((255,255,255))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.hp = 30
        self.target = target
        self.kiirus = 10
        self.walking = True
        self.pihtaSaamisRaadius = 50
        


    def getPos(self):
        return (self.x, self.y)
    
    def setPos(self, givenX, givenY):
        self.x = givenX
        self.y = givenY

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))
    
    def update(self, surface):
        if self.walking:
            targetVector = (self.target[0]-self.x, self.target[1]-self.y)
            distance = ((targetVector[0])**2+(targetVector[1])**2)**(1/2)
            if distance <= self.kiirus:
                self.setPos(self.target[0], self.target[1])
                self.walking = False
            else:
                speedVector = (targetVector[0]/distance*self.kiirus, targetVector[1]/distance*self.kiirus)
                self.setPos(self.x+speedVector[0], self.y+speedVector[1])
        self.draw(surface)
                

    def KasSaabPihta(self, asuk, suund):
        # Vaja on lisada kontroll, et kas zombi on ikka sirgele lahedal seal suunas, kuju mangija osutab, mitte tema selja taga.
        vahevek = [self.x - asuk[0], self.y - asuk[1]]
        sihivek = suund
        vekkorr = cross(vahevek, sihivek)
        vekkorrp = linalg.norm(vekkorr, ord = 2)
        sihivekp = linalg.norm(sihivek, ord = 2)
        vastus = vekkorrp / sihivekp
        if vastus < self.pihtaSaamisRaadius:
            return True
        else:
            return False
        

        
    def KasKuulKattub(self, kuul):
        pass
