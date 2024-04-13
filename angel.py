import pygame
from zombie import Zombie
from numpy import linalg, cross
from Mangija import Mangija

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
            target_x, target_y = self.target.getPos()
            zombie_width, zombie_height = 50, 50
            center_distance_x = (target_x + zombie_width / 2) - self.x
            center_distance_y = (target_y + zombie_height / 2) - self.y
            distance = linalg.norm([center_distance_x, center_distance_y])

            if distance <= self.kiirus:
                angle = pygame.math.Vector2(center_distance_x, center_distance_y).angle_to((1, 0))
                adjusted_distance = max(distance - self.kiirus, 0)
                target_x_adjusted = target_x + zombie_width / 2 + (adjusted_distance + self.width) * math.cos(math.radians(angle))
                target_y_adjusted = target_y + zombie_height / 2 + (adjusted_distance + self.height) * math.sin(math.radians(angle))
                self.setPos(target_x_adjusted, target_y_adjusted)

                if pygame.time.get_ticks() - self.last_attack_time >= self.attack_delay:
                    self.attackMode()
                    self.last_attack_time = pygame.time.get_ticks()
                self.walking = False
            else:
                speedVector = (center_distance_x / distance * self.kiirus, center_distance_y / distance * self.kiirus)
                self.setPos(self.x + speedVector[0], self.y + speedVector[1])

        else:
            self.attackMode()
        self.draw(surface)


    def attackMode(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time >= self.attack_delay:
            target_x, target_y = self.target.getPos()
            zombie_width, zombie_height = 50, 50
            teleport_distance = 50

            angel_to_zombie_vector = pygame.math.Vector2(target_x - self.x, target_y - self.y)
            
            perpendicular_vector = angel_to_zombie_vector.rotate(45)
            perpendicular_vector.scale_to_length(teleport_distance)

            teleport_point = (target_x + zombie_width / 2 + perpendicular_vector.x,
                            target_y + zombie_height / 2 + perpendicular_vector.y)

            self.setPos(*teleport_point)

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
        
        
