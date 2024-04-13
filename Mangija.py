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

    
    def SaaViga(self, kahju):
        self.elud -= kahju
        

        
            
