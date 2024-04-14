import pygame

from ObjektiAlus import ObjektiAlus


# Funktsioon võtab sisse teksti, pikkuse pikslites ja pygame fonti objekti.
# Funktsioon tagastab esialgse teksti kahe tekstilise tuplena, millest esimene osa on nii pikk, et mahuks täpselt antud pikkusesse ja teine osa on kõik ülejäänud tekst.

# Kui antud laius on väiksem, kui üksik täht, ss ei crashi, vaid ikkagi tagastab teksti üksikute tähtede listina, kuigi mõni neist ei pruugi mahtuda antud laiusesse. Ei garanteeri õiget käitumist. lic lükkab crashimise edasi. 
def EraldaSobivaPikkusegaTekst(algtekst, sobivPikkus, fontObject:pygame.font.Font):
    kasvatatav = ""
    for i in algtekst:
        if i == "\n":
            esiPool = kasvatatav
            tagaPool = algtekst[len(esiPool)+1:]
            return [esiPool, tagaPool]
        kasvatatav += i
        
        laius = fontObject.size(kasvatatav)[0]
        if laius > sobivPikkus:
            esiPool = kasvatatav[:-1]
            tagaPool = algtekst[len(kasvatatav)-1:]
            if esiPool == "":
                esiPool = kasvatatav
                tagaPool = algtekst[len(kasvatatav):]
            
            return [esiPool, tagaPool]
    return [kasvatatav,""]


def TekstRidadeks(tekst, pygFont, laius):
    read = []
    paar = EraldaSobivaPikkusegaTekst(tekst, laius, pygFont)
    read.append(paar[0])
    while paar[1] != "":
        paar = EraldaSobivaPikkusegaTekst(paar[1], laius, pygFont)
        if "\n" in paar[0]:
            uueReaIndeks = paar[0].index("\n")
            paar[1] = paar[0][uueReaIndeks+1:]+paar[1]
            paar[0] = paar[0][:uueReaIndeks]
        read.append(paar[0])
    return read
        
        
def MituRidaOnVaja(tekst, font, laius):
    kogus = len(TekstRidadeks(tekst, font, laius))
    return kogus



class Tekst(ObjektiAlus):

    def __init__(self, pind, tekst, pygFont:"pygame.font.Font", värv=(255,0,0)):
        super().__init__()
        self.pygFont = pygFont
        self.pind = pind
        self.tekst = tekst
        self.värv = värv
    
    
    def Joonista(self):
        suurtäheKõrgus = self.pygFont.get_ascent()
        
        # Oke, see on scuffed ja töötab kindlalt ainult selle fondiga. 0.22 on silma järgi valitud, aga see arv aitab teha nii, et tekst joonistuks valitud kohta täpselt nii, et väiketähe kõrguse keskkoht oleks soovitud kõrgusel. Keskkoht selle pärast, et ss on bullet pointe lihtsam joondada. Seda peaks vist täiendama, kui on vaja kirjutada mitmerealine tekst. Scuffed on veel see, et height on fontide terminoloogias väiketähe kõrgus, aga siin imo on vahemik nt j tähe langusest l tähe tõusuni, seega u 2x väiketähe kõrgus.
        poolVäiketäheKõrgus = self.pygFont.get_height()*0.22
        tekstiAsuk = (self.asukoht[0], self.asukoht[1]-suurtäheKõrgus + poolVäiketäheKõrgus)
        img = self.pygFont.render(self.tekst, True, self.värv)
        self.pind.blit(img, tekstiAsuk)


    def MääraTekst(self, tekst):
        self.tekst = tekst
        
    # Annab teksti laiuse
    def VõtaSuurus(self):
        self.suurus = (self.pygFont.size(self.tekst)[0], 0)
        return self.suurus



class MitmeReaTekst:
    def __init__(self, pind, tekst, pygfont:pygame.font.Font):
        self.debugnumber = 0        

        self.pind = pind
        self.laius = 100
        self.asukoht = (0,0)
        self.font = pygfont
        self.värv = (10,10,10,255)
        self.reavahe = 30
        self.tekst = tekst
        self.keskeleJoondus = False
        self.kasArvestadaLaiust = True
        self.read = []

        # Ridade arv vastab sellele, kui mitu rida joonistatakse. Väärtus 0 tähendab, et joonistatakse nii palju ridu kui kulub kogu teksti joonistamiseks.
        self.ridadeArv = 3

    def MääraRidadeArv(self, ridu):
        self.ridadeArv = ridu

    def MääraLaius(self, laius):
        self.laius = laius
    
    def MääraAsukoht(self, asukoht):
        self.asukoht = asukoht

    def MääraVärv(self, värv):
        self.värv = värv

    def MääraReavahe(self, reavahe):
        self.reavahe = reavahe
        
    def MääraKeskeleJoondus(self, väärtus:bool):
        self.keskeleJoondus = väärtus
        
    # See funktsioon võtab sisse nimekirja stringidest, millest igaüks tuleb joonistada omale reale. Ühtlasi see funktsioon lülitab välja laiuse kontrolli ja ridade piirarvu
    def MääraRead(self, read):
        self.read = read
        self.kasArvestadaLaiust = False
        self.ridadeArv = len(read)

    # Erinevalt peaaegu kõigi teiste objektide Joonista funktsioonidest see siin returnib midagi. See  viimase rekstirea asukoha. Kasutades seda infot saavad muud asjad väljaspreturnibool objekti end paigutada.
    def Joonista(self):
        # Määrab read, mida joonistada:
        if self.read != []:
            read = self.read
        elif self.ridadeArv == 0:
            read = TekstRidadeks(self.tekst, self.font, self.laius)
        elif self.ridadeArv > 0:
            read = TekstRidadeks(self.tekst, self.font, self.laius)[0:self.ridadeArv]
        

        
        if self.keskeleJoondus == True:
            counter = 0
            for i in read:
                tekst = Tekst(self.pind, i, self.font, self.värv)
                laius = tekst.VõtaSuurus()[0]
                asukx = self.asukoht[0] - laius/2
                asuky = self.asukoht[1] + counter * self.reavahe
                tekst.MääraAsukoht((asukx, asuky))
                counter += 1
                tekst.Joonista()
        else:
            counter = 0
            for i in read:
                tekst = Tekst(self.pind, i, self.font, self.värv)
                asukx = self.asukoht[0]
                asuky = self.asukoht[1] + counter * self.reavahe
                tekst.MääraAsukoht((asukx, asuky))
                counter += 1
                tekst.Joonista()
                
    # Funktsioon annab selle, kui palju võtab tekst ruumi laiupidi. Saadav väärtus on kindlasti väiksem, kui määratud laius, sest sellest ei tohi tekst üle minna. Tagastab selle, kui palju tegelikult laiust läheb. Võrdub kõige pikema rea laiusega.
    def VõtaLaius(self):
        if self.read != []:
            read = self.read
        elif self.ridadeArv == 0:
            read = TekstRidadeks(self.tekst, self.font, self.laius)
        elif self.ridadeArv > 0:
            read = TekstRidadeks(self.tekst, self.font, self.laius)[0:self.ridadeArv]

        maxLaius = 0
        for i in read:
            tekst = Tekst(self.pind, i, self.font, self.värv)
            laius = tekst.VõtaLaius()
            if laius > maxLaius:
                maxLaius = laius
        return maxLaius


    def KuiPaljuRuumiOnVaja(self):
        
        ridu = 0
        if self.read != []:
            ridu = len(self.read)
        else:
            ridu = len(TekstRidadeks(self.tekst, self.font, self.laius))
            
        vajadus = min((ridu-1) * self.reavahe, (self.ridadeArv-1)*self.reavahe)
        return vajadus
        

    def MääraTekst(self, tekst):
        self.tekst = tekst