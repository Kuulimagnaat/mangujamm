import pygame
import numpy

class Mangija:
    def __init__(self, asukx, asuky, kiirus):
        self.suurus = [30,30]
        self.mangijaPilt = pygame.Surface((self.suurus[0], self.suurus[1]))
        self.muzzlefPilt = pygame.image.load("./assets/Muzzle flash.png")
        self.muzzlefRect = self.muzzlefPilt.get_rect()
        
        self.muzzleFlashCounter = 0
        self.asukx = 50
        self.asuky = 50
        self.kiirus = 5
        self.elud = 100
        # Suund olgu alati ühikvektor
        self.suund = [1.0,0.0]
        
    def VotaAsuk(self):
        return self.asukx, self.asuky
    
    def VotaSuund(self):
        return self.suund
    
    def Tulista(self, tegelasteNimek):
        for i in tegelasteNimek:
            i.KasSaabPihta((self.asukx, self.asuky), self.suund)
    
    # Funktsioon arvutab mängijale uue suuna ja liigutab seda
    def Varskenda(self):
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
        print(nurk)
        return nurk-90
        
        
    def TekitaMuzzleFlash(self, mituKaadrit):
        self.muzzleFlashCounter = mituKaadrit
    
            
