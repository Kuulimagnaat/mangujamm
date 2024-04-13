class Mangija:
    def __init__(self, asukx, asuky, kiirus):
        self.asukx = 0
        self.asuky = 0
        self.kiirus = 5
        self.elud = 100
        self.suund = [100,0]
        
    def VaataAsuk(self):
        return self.asukx, self.asuky
    
    def Tulista(self, tegelasteNimek):
        for i in tegelasteNimek:
            i.KasSaabPihta((self.asukx, self.asuky), self.suund)
            
