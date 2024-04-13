import pygame
from numpy import linalg, cross

from Mangija import Mangija

class Zombie(pygame.sprite.Sprite):
    def __init__(self, x, y, target=(0,0)):
        pygame.sprite.Sprite.__init__(self)
        self.width, self.height = 50, 50
        self.image = pygame.Surface([self.width, self.height])
        self.algvärv = (255, 0,0)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.hp = 30
        self.target = target
        self.kiirus = 2
        self.walking = True
        self.pihtaSaamisRaadius = 30
        

    def getPos(self):
        return (self.x, self.y)
    
    def setTarget(self, target):
        self.target = target
    
    def getPosX(self):
        return self.getPos()[0]
    def getPosY(self):
        return self.getPos()[1]
    
    def setPos(self, givenX, givenY):
        self.x = givenX
        self.y = givenY

    def draw(self, surface):
        surface.blit(self.image, (self.x-self.width/2, self.y-self.height/2))
        pygame.draw.circle(surface, (100,0,0), [self.x, self.y], self.pihtaSaamisRaadius)
    
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
        
        saiPihta = self.KasSaabPihta(mangija.VotaAsuk(), mangija.VotaSuund())
        if saiPihta == True:
            self.image.fill((200, 100, 100))
        else:
            self.image.fill(self.algvärv)
            
        self.draw(surface)

    def KasSaabPihta(self, asuk, suund):
        # Vaja on lisada kontroll, et kas zombi on ikka sirgele lahedal seal suunas, kuhu mangija osutab, mitte tema selja taga.
        
        # Mängija asukohavektor
        P1 = asuk
        # Zombi asukohavektor
        P0 = [self.x, self.y]
        # Mängija suunavektor
        S = suund
        # Mängijast rakendatud zombivektor
        Z=[P0[0]-P1[0], P0[1]-P1[1]]
        # Mängija asukohale rakendatud suunavektori koordinaadid
        P2 = [asuk[0] + suund[0], asuk[1] + suund[1]]
        print(P2)
        

        # Seiab nurga P2 ja Z vahel. Kui see on < 0, siis on mängija seljaga zombi poole.
        koosinus = (S[0]*Z[0]+S[1]*Z[1])/((S[0]**2 + S[1]**2)**0.5 * (Z[0]**2 + Z[1]**2)**0.5)
        #print(koosinus)
        
        try:
            d = abs((P2[0]-P1[0])*(Z[1]-P1[1]) - (Z[0]-P1[0])*(P2[1]-P1[1]))/(((P2[0]-P1[0])**2)+((P2[1]-P1[1])**2))**0.5
        except:
            # Kui toimub nulliga jagamine, ss mdea, mis juhtub, aga igatahes, mängija ei tohiks pihta saada, muidu on exploit.
            d = self.pihtaSaamisRaadius+1
        
        
        if d < self.pihtaSaamisRaadius and koosinus>0:
            return True
        else:
            return False
        

        
    def KasKuulKattub(self, kuul):
        pass
