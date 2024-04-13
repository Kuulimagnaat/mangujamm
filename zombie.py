import pygame
from numpy import linalg, cross

from Mangija import Mangija

class Zombie(pygame.sprite.Sprite):
    def __init__(self, x, y, target=(0,0)):
        pygame.sprite.Sprite.__init__(self)
        self.width, self.height = 50, 50
        self.image = pygame.Surface([self.width, self.height])
        self.algVärv = (255, 0,0)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.hp = 30
        self.target = target
        self.kiirus = 2
        self.walking = True
        self.pihtaSaamisRaadius = 50
        


    def getPos(self):
        return (self.x, self.y)
    
    def getPosX(self):
        return self.getPos()[0]
    def getPosY(self):
        return self.getPos()[1]
    
    def setPos(self, givenX, givenY):
        self.x = givenX
        self.y = givenY

    def draw(self, surface):
        surface.blit(self.image, (self.x-self.width/2, self.y-self.height/2))
    
    def update(self, surface, mangija=Mangija):
        if self.walking:
            targetVector = (self.target[0]-self.x, self.target[1]-self.y)
            distance = ((targetVector[0])**2+(targetVector[1])**2)**(1/2)
            if distance <= self.kiirus:
                self.setPos(self.target[0], self.target[1])
                self.walking = False
            else:
                speedVector = (targetVector[0]/distance*self.kiirus, targetVector[1]/distance*self.kiirus)
                self.setPos(self.x+speedVector[0], self.y+speedVector[1])
        
        saiPihta = self.KasSaabPihta(mangija.VotaAsuk, mangija.VotaSuund)
        if saiPihta == True:
            self.image.fill((200, 100, 100))
        else:
            self.image.fill(self.algvärv)
            
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
