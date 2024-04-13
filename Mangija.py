import pygame
import numpy

def clamp(n, min, max): 
    if n < min: 
        return min
    elif n > max: 
        return max
    else: 
        return n

class Mangija:
    def __init__(self, asukx, asuky, kiirus):
        self.suurus = [30,30]
        self.mangijaPilt = pygame.Surface((self.suurus[0], self.suurus[1]))
        self.muzzlefPilt = pygame.image.load("./assets/Muzzle flash.png")
        self.muzzlefRect = self.muzzlefPilt.get_rect()
        self.tagasilöögiKiirus = [0,0]
        self.tagasilöögiVähenemiseKiirendus = 3
        
        self.muzzleFlashCounter = 0
        self.asukx = asukx
        self.asuky = asuky
        self.kiirus = 5
        self.elud = 100
        self.suurus = [30,30]
        # Suund olgu alati �hikvektor
        self.suund = [1.0,0.0]
        self.damage = 10
        self.angelKills = 0
        self.zombieKills = 0
        self.damageDone = 0

        self.pihtaSaamisRaadius = 75

        # Health bar parameters
        self.health_bar_length = self.suurus[0]
        self.health_bar_height = 5
        self.health_bar_color = (0, 255, 0)

    def getPos(self):
        return self.asukx, self.asuky
    
    def getPosX(self):
        return self.getPos()[0]
    def getPosY(self):
        return self.getPos()[1]
    
    def getHP(self):
        return self.elud
        
    def VotaAsuk(self):
        return self.asukx, self.asuky
    
    def VotaSuund(self):
        return self.suund
    
    def draw_health_bar(self, surface):
        # Calculate health bar position
        health_bar_x = self.asukx - self.suurus[0] / 2
        health_bar_y = self.asuky - self.suurus[1] / 2 - 10
        
        # Calculate health bar width based on current health
        health_width = (self.elud / 100) * self.health_bar_length
        
        # Draw health bar background
        pygame.draw.rect(surface, (255, 0, 0), (health_bar_x, health_bar_y, self.health_bar_length, self.health_bar_height))
        # Draw health bar
        pygame.draw.rect(surface, self.health_bar_color, (health_bar_x, health_bar_y, health_width, self.health_bar_height))
    
    def Tulista(self, tegelasteNimek):
        for i in tegelasteNimek:
            i.KasSaabPihta((self.asukx, self.asuky), self.suund)
    
    # Funktsioon arvutab m�ngijale uue suuna ja liigutab seda
    def Varskenda(self):
        v1 = self.tagasilöögiKiirus[0]
        v2 = self.tagasilöögiKiirus[1]
        k = self.tagasilöögiVähenemiseKiirendus

        self.asukx = clamp(self.asukx+v1, 0, 1280)
        self.asuky = clamp(self.asuky+v2, 0, 720)
        
        if self.tagasilöögiKiirus != [0,0]:
            # Vähendatud tagasilöögikiiruse leidmine:
            # Tagasilöögikiiruse vektori pikkus V
            V = (v1**2 + v2**2)**0.5
            tegur = (V-k)/V
            # uus tagaslöögikiirus:
            u1 = v1*tegur
            u2 = v2 * tegur
            # Kui uus kiirus osutub suuremaks, kui vana, ss lõpeta.
            U = (u1**2 + u2**2)**0.5
            if V < U:
                self.tagasilöögiKiirus = [0,0]
            else:
                self.tagasilöögiKiirus = [u1, u2]
            
            

        P = [self.asukx, self.asuky]
        H = pygame.mouse.get_pos()
        s = [H[0]-P[0], H[1]-P[1]]
        # Suunavektori pikkus
        p = (s[0]**2 + s[1]**2)**0.5
        self.suund = [s[0]/p, s[1]/p]
         
        
    def Joonista(self, pind):
        pygame.draw.rect(pind, (30,30,30), [self.asukx-self.suurus[0]/2, self.asuky-self.suurus[1]/2, self.suurus[0],self.suurus[1]])
        P = [self.asukx, self.asuky]
        s = self.suund
        suunaOts = [P[0] + s[0]*50, P[1] + s[1]*50]
        pygame.draw.line(pind, (255,255,255), P, suunaOts)

        self.draw_health_bar(pind)    
        if self.muzzleFlashCounter > 0:
            #self.muzzlefRect.
            rot_image = pygame.transform.scale(self.muzzlefPilt, (350,700))
            rot_image = pygame.transform.rotate(rot_image, self.VotaSihinurk())
            
            rot_rect = rot_image.get_rect(center = (self.asukx, self.asuky))
            pind.blit(rot_image, [rot_rect[0]+200*self.suund[0], rot_rect[1]+200*self.suund[1], rot_rect[2], rot_rect[3]]) 
            
            self.muzzleFlashCounter -= 1
    

    def VotaSihinurk(self):
        x1 = self.suund[0]
        y1 = self.suund[1]
        x2 = 1
        y2 = 0
        dot = x1*x2 + y1*y2      # dot product
        det = x1*y2 - y1*x2      # determinant
        angle = numpy.arctan2(det, dot)
        nurk = numpy.rad2deg(angle)
        return nurk-90
        
        
    def TekitaMuzzleFlash(self, mituKaadrit):
        self.muzzleFlashCounter = mituKaadrit
    
    def SaaViga(self, kahju):
        self.elud -= kahju
        
    def SaaTagasilööki(self, kiirus, kiirendus):
        self.tagasilöögiVähenemiseKiirendus = kiirendus
        self.tagasilöögiKiirus = [-kiirus*self.suund[0],-kiirus*self.suund[1]]
            
