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
        self.onSurnud = False
        
        # Dot parameters
        self.dot_radius = 2
        self.dot_color = (0, 255, 0)  # Green color for the dot

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
    
    def draw_dot(self, surface):
        # Draw dot at the zombie's position
        pygame.draw.circle(surface, self.dot_color, (int(self.x), int(self.y)), self.dot_radius)

    # Siia funktiooni on vaja lisada, mis juhtub, kui zombil on elusid vähem kui 0.
    def update(self, surface, mangija=Mangija):
        if (self.hp > 0):
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
        else:
            self.onSurnud = True

    def KasSaabPihta(self, asuk, suund):
        # Zombi asukoht
        Z = [self.x, self.y]
        # Mängija asukoht
        P = asuk
        # Mängja suund
        s = suund
        # Suuna punkt
        S = [P[0] + s[0], P[1] + s[1]]
        
        # Küsimus on, kui kaugel on zombi asukoht Z Mängija asukohaga P ja suuna punktiga S määratud sirgest.
        kaugus = abs((S[0]-P[0])*(Z[1]-P[1]) - (S[1]-P[1])*(Z[0]-P[0])) / ((S[0]-P[0])**2 + (S[1]-P[1])**2)**0.5
        

        z = [Z[0] - P[0], Z[1] - P[1]]
        # Küsimus, on kui suur on vektori s ja vektori z vaheline koosinus.
        koosinus = (s[0]*z[0] + s[1]*z[1]) / ((s[0]**2+s[1]**2)**0.5 * (z[0]**2+z[1]**2)**0.5)


        if kaugus < self.pihtaSaamisRaadius and koosinus > 0:
            return True
        else:
            return False
        
    def LeiaKaugusMangijast(self, mangija:Mangija):
        P1 = [self.x, self.y]
        P2 = [mangija.asukx, mangija.asuky]
        V = [P2[0]-P1[0], P2[1]-P1[1]]
        l = (V[0]**2 + V[1]**2)**0.5
        return l

    def KasKuulKattub(self, kuul):
        pass
    
    def SaaViga(self, kahju):
        self.hp -= kahju
        print("Sain pihta! :(")
