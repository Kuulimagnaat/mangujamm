import pygame
from zombie import Zombie
from numpy import linalg, cross
from Mangija import Mangija
import math
import random

class Angel(pygame.sprite.Sprite):
    def __init__(self, x, y, target=Zombie):
        pygame.sprite.Sprite.__init__(self)
        self.width, self.height = 50, 50
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.hp = 100
        self.target = target
        self.kiirus = 4
        self.walking = True
        self.pihtaSaamisRaadius = 50

        
        self.last_attack_time = 0
        self.attack_delay = 1000

        # Dot parameters
        self.dot_radius = 2
        self.dot_color = (0, 255, 0)  # Green color for the dot

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
        surface.blit(self.image, (self.x - self.width / 2, self.y - self.height / 2))

    def update(self, surface):
        if self.walking:
            targetVector = (self.target.getPosX()-self.x, self.target.getPosY()-self.y)
            distance = ((targetVector[0])**2+(targetVector[1])**2)**(1/2)
            if distance <= self.kiirus:
                self.setPos(self.target.getPosX() + 10, self.target.getPosY() + 10)
                self.walking = False

            else:
                speedVector = (targetVector[0]/distance*self.kiirus, targetVector[1]/distance*self.kiirus)
                self.setPos(self.x+speedVector[0], self.y+speedVector[1])

        else:
            self.attackMode()
        self.draw(surface)
        self.draw_dot(surface)

    def draw_dot(self, surface):
        pygame.draw.circle(surface, self.dot_color, (int(self.x), int(self.y)), self.dot_radius)

    def attackMode(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time >= self.attack_delay:
            target_x, target_y = self.target.getPos()
            teleport_distance = 75

            random_angle = random.uniform(0, 2*math.pi)
            teleport_point_x = target_x + teleport_distance * math.cos(random_angle)
            teleport_point_y = target_y + teleport_distance * math.sin(random_angle)


            self.setPos(teleport_point_x, teleport_point_y)

            self.last_attack_time = current_time


    def KasSaabPihta(self, asuk, suund):
        # Ingli asukoht
        Z = [self.x, self.y]
        # Mängija asukoht
        P = asuk
        # Mängja suund
        s = suund
        # Suuna punkt
        S = [P[0] + s[0], P[1] + s[1]]
        
        # Küsimus on, kui kaugel on ingli asukoht Z Mängija asukohaga P ja suuna punktiga S määratud sirgest.
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
        
        
