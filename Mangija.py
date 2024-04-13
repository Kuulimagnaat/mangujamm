import pygame

class Mangija:
    def __init__(self, asukx, asuky, kiirus):
        self.asukx = 50
        self.asuky = 50
        self.kiirus = 5
        self.elud = 100
        self.suurus = [30,30]
        # Suund olgu alati �hikvektor
        self.suund = [1.0,0.0]
        self.damage = 10
        self.angelKills = 0
        self.zombieKills = 0
        self.damageDone = 0
        
    def VotaAsuk(self):
        return self.asukx, self.asuky
    
    def VotaSuund(self):
        return self.suund
    
    def Tulista(self, tegelasteNimek):
        for i in tegelasteNimek:
            i.KasSaabPihta((self.asukx, self.asuky), self.suund)
    
    # Funktsioon arvutab m�ngijale uue suuna ja liigutab seda
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
        

        
            
