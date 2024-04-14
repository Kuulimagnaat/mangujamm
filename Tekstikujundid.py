import pygame
from Klassid.Kujundid import Ristkülik
from Klassid.Tekst import MitmeReaTekst, Tekst
from Klassid.Sündmus import Sündmus
from math import floor
from typing import List
from Programmiolek import ProgrammiOlek
from Klassid.Kuupäev import Kuupäev
from Klassid.Päev import Päev
from Funktsioonid.SündNimekFunktsioonid import *
from Funktsioonid.UtilityFunktsioonid import *
from Klassid.Nupp import NupuAlus

# SündmuseRida
# Vastutab loetelutäpi ja sündmuse nimest koosneva rea joonistamise eest päevaruudu sees. Kui päevaruudus on mitu sündmust, ss neid ridu on vastavalt nii mitu. Iga sündmuse jaoks 1.
class SündmuseRida:
    # Oke, mu jaoks on see süntaks uus, aga pmst see on ainus viis pythonis märkida, et sisestatud parameeter peab olema mingi kindla klassi esindaja ja kui pole, ss ei tohiks joosta. Süntaks järgmine: parameeter: "klassiNimi". Klassinimi justkui oleks tekst, aga tegelt pole.
    def __init__(self, olek:"ProgrammiOlek", pind, sündmus: "Sündmus"):
        self.olek = olek
        self.sündmus = sündmus
        self.pind = pind
        self.asukoht = (0,0)
        self.laius = 100
        self.värv = olek.ruuduTekstiVärv
        pealkTekst = self.sündmus.VõtaNimi()
        pealkFont = self.olek.sündmuseReaKirjaFont
        self.tekst = MitmeReaTekst(self.olek, self.pind, pealkTekst, pealkFont)

    def Joonista(self):
        värv = self.värv

        # Täpp
        täpiAsukx, asuky = self.asukoht[0], self.asukoht[1]
        raadius = self.olek.sündmuseReaTäpiRaadius
        pygame.draw.circle(self.pind, värv, (täpiAsukx, asuky), raadius)
        
        # Pealkiri
        täpivahe = self.olek.sündmuseReaTäpiVahe
        pealkAsukx = täpiAsukx + täpivahe
        pealkRuum = self.laius - täpivahe
        

        # See, kui mitu rida võib sündmuserida olla.
        ridu = self.olek.sündmuseReaRidu
        reavahe = self.olek.sündmuseReaReavahe
        
        
        self.tekst.MääraLaius(pealkRuum)
        self.tekst.MääraAsukoht((pealkAsukx, self.asukoht[1]))
        self.tekst.MääraReavahe(reavahe)
        self.tekst.MääraRidadeArv(ridu)
        self.tekst.Joonista()    
 


    def MääraLaius(self, laius):
        self.laius = laius

    def MääraAsukoht(self, asukoht):
        self.asukoht = asukoht

    def KuiPaljuRuumiOnVaja(self):
        
        täpivahe = self.olek.sündmuseReaTäpiVahe
        pealkRuum = self.laius - täpivahe

        # See, kui mitu rida võib sündmuserida olla.
        ridu = self.olek.sündmuseReaRidu
        reavahe = self.olek.sündmuseReaReavahe
        
        self.tekst.MääraLaius(pealkRuum)
        self.tekst.MääraReavahe(reavahe)
        self.tekst.MääraRidadeArv(ridu)
        
        tulemus = self.tekst.KuiPaljuRuumiOnVaja()
        return tulemus
        
        


# PäevaPealkiri
class PäevaPealkiri:
    def __init__(self, olek:"ProgrammiOlek", pind, kuupäev:"Kuupäev"):
        self.kpFont = olek.päevaruuduPealkKpPygFont
        self.aFont = olek.päevaruuduPealkAastaPygFont
        self.kuupäev = kuupäev
        self.asukoht = (0,0)
        self.pind = pind
        self.värv = olek.ruuduTekstiVärv
        self.päevaAastaVahe = olek.päevaruuduPealkPäevaAastaVahe

    def MääraAsukoht(self, x, y):
        self.asukoht = (x,y)

    def Joonista(self):
        pk = self.kuupäev.VõtaPäevKuuTekstina()
        a = self.kuupäev.VõtaAastaTekstina()

        päevKuuTekst = Tekst(self.pind, pk, self.kpFont, self.värv)
        päevKuuTekst.MääraAsukoht(self.asukoht)
        päevKuuTekst.Joonista()
        
        aAsuk = (self.asukoht[0] + self.kpFont.size(pk)[0] + 10, self.asukoht[1])
        aastaTekst = Tekst(self.pind, a, self.aFont, self.värv)
        aastaTekst.MääraAsukoht(aAsuk)
        aastaTekst.Joonista()

    def VõtaLaius(self):
        pk = self.kuupäev.VõtaPäevKuuTekstina()
        a = self.kuupäev.VõtaAastaTekstina()

        laius = self.kpFont.size(pk)[0] + self.päevaAastaVahe + self.aFont.size(a)[0]
        return laius




# PäevaRuut
class PäevaRuut:
    def __init__(self, olek:"ProgrammiOlek", pind, päev:"Päev"):
        self.kuupäev = päev.kuupäev
        self.suurus = (10,10)
        self.asuk = (10,10)
        self.pealkiri = PäevaPealkiri(olek, pind, self.kuupäev)
        self.olek = olek

        self.värv = olek.päevaruuduVärv
    
        self.taust = Ristkülik(pind)
        self.pind = pind
        self.sündmused = päev.sündmusteNimekiri
        
        def päevaRuuduDetailsemVaade():
            # Debuginfo
            if self.olek.SündmuseLisamine == True:
                if self.olek.tegevuseNäitamine == True: print("Täpsemat vaadet ei avata, sest käsil on sündmuse lisamine.")
                return
            if self.olek.tegevuseNäitamine is True:
                print("Täpsema vaate päev: None -> Päev")
                
            # Funktsiooni sisu
            päev = Päev(self.kuupäev, self.sündmused)
            
            if self.olek.TäpsemaVaatePäev is None:
                self.olek.TäpsemaVaatePäev = päev
            #elif self.olek.TäpsemaVaatePäev is not None and võrdleObjektiParameetreid(päev, self.olek.TäpsemaVaatePäev):
                #self.olek.TäpsemaVaatePäev = None
            else:
                self.olek.TäpsemaVaatePäev = päev

            self.olek.eelminePäevaObjekt = None
            
        prio = self.olek.nuppudePrioriteedid["päevaruut"]
        self.nupp = NupuAlus(olek, prio, päevaRuuduDetailsemVaade)
        
    def MääraAsukoht(self, x, y):
        self.asuk = (x,y)
        self.nupp.MääraAsukoht((x,y))

    def MääraSuurus(self, x, y):
        if x != None: 
            self.suurus = (x, self.suurus[1])
            self.nupp.MääraSuurus((x, self.suurus[1]))
        if y != None: 
            self.suurus = (self.suurus[0], y)
            self.nupp.MääraSuurus((self.suurus[0], y))


    # Seda on vaja kutsuda peale seda, kui on määratud ruudu laius. Seda meetodit kasutab päevaruudustik, et saada teada, kui kõrgeks on mõistlik teha üks päevaruutude rida. Päevaruudustik uurib selle funktsiooni abil, mis on ruumivajaduse seis sama rea teistel ruutudel ja selle järgi valib mingi kõrguse, mis keskmiselt sobiks kõigile rea ruutudele ja mille see siis tegelikult annab igale ruudule joonistamiseks. On crazy, kui see lõpuks töötab kah.
    # Meetod uurib välja, kui kõrge oleks ruut antud laiuse korral. Kõrgus oleneb peamiselt sellest kui mitu sündmuserida on ja kui palju kordi need sündmuseread peavad enda joonistamisel uuele reale minema. Aga sellele liituvad veel kuupäeva ja teksti vahe, ruudu alumise ja ülemise osa kaugused ülemisest tekstist, alumisest tekstist, ridade vahede suurused ja mõni muu kaugus veel.
    def KuiPaljuRuumiOnVaja(self):
        ülevalt = self.olek.päevaruuduPealkKaugusÜlaservast
        ridaKuupäevast = self.olek.sündmuseReadKuupäevast
        sündmuseRidadeRead = 0
        
        täpivahe = self.olek.sündmuseReaTäpiVahe
        for i in self.sündmused:
            uusRida = SündmuseRida(self.olek, self.pind, i)
            laius = self.suurus[0] - täpivahe
            uusRida.MääraLaius(laius)
            sündmuseRidadeRead += uusRida.KuiPaljuRuumiOnVaja()
        
        ridadeVahe = (max(0, len(self.sündmused)-1)) * self.olek.sündmuseRidadeVahe
        alt = ülevalt        

        return ülevalt + ridaKuupäevast + sündmuseRidadeRead + ridadeVahe + alt


    def Joonista(self):
        self.nupp.TegeleNupuga()
        olek = self.nupp.VõtaOlek() 
        
        # Värvi valimine vastavalt sellele, mis nupp ütleb, et peaks olema
        origVärv = self.olek.päevaruuduVärv        
        if olek == 0:
            self.värv = origVärv
        elif olek == 1:
            self.värv = MuudaHeledust(30, origVärv)
        elif olek == 2:
            self.värv = MuudaHeledust(-50, origVärv)
        
        # Päevaruudu taust
        print(self.asuk)
        self.taust.MääraAsukoht(self.asuk)
        self.taust.MääraSuurus(self.suurus)
        self.taust.MääraVärv(self.värv)
        self.taust.Joonista()

        # Kuupäev ja aasta
        pealkAsukx = self.asuk[0] + self.olek.päevaruuduPealkKaugusVasakult
        pealkAsuky = self.asuk[1] + self.olek.päevaruuduPealkKaugusÜlaservast
        self.pealkiri.MääraAsukoht(pealkAsukx, pealkAsuky)
        self.pealkiri.Joonista()

        # Päevaruudu sündmused
        kuupäevast = self.olek.sündmuseReadKuupäevast
        asuky = pealkAsuky + kuupäevast
        täpivahe = self.olek.sündmuseReaTäpiVahe
        for i in self.sündmused:
            asukoht = (self.asuk[0] + täpivahe, asuky)
            uusRida = SündmuseRida(self.olek, self.pind, i)
            uusRida.MääraAsukoht((self.asuk[0] + täpivahe, asuky))
            laius = self.suurus[0] - täpivahe
            uusRida.MääraLaius(laius)
            
            vajaminevRuum = uusRida.KuiPaljuRuumiOnVaja()
            allesjäänudRuum = self.asuk[1] + self.suurus[1] - asukoht[1]
            
            if allesjäänudRuum >= vajaminevRuum+3:
                uusRida.Joonista()

            
            
            vahe = self.olek.sündmuseRidadeVahe
            asuky = asuky + uusRida.KuiPaljuRuumiOnVaja() + vahe
    
    def VaataSündmusedÜle(self):
        sündmused = VõtaKindlalKuupäeval(self.olek.sündmusteNimekiri, self.kuupäev)
        self.sündmused = sündmused



class FakePäevaRuut:
    def __init__(self, olek:ProgrammiOlek, pind):
        self.olek = olek
        self.pind = pind
        self.suurus = (200,200)
        self.asukoht = (0,0)
        
        # Taust
        self.taust = Ristkülik(pind)
        värv = olek.päevaruuduVärv
        self.taust.MääraVärv(värv)
        
        # Nupp
        """
        def f1():
            print("Avati blurrblurr aken.")
        prio = olek.nuppudePrioriteedid["päevaruut"]
        self.nupp = NupuAlus(olek, prio)"""
        
        
    def Joonista(self):
        #self.nupp.TegeleNupuga()
        
        self.taust.MääraSuurus(self.suurus)
        self.taust.MääraAsukoht(self.asukoht)
        self.taust.Joonista()
        #self.nupp.Joonista(self.pind)
        
    def MääraAsukoht(self, asukoht):
        self.asukoht = asukoht
        #self.nupp.MääraAsukoht(asukoht)
        
        
    def MääraSuurus(self, suurus):
        self.suurus = suurus   
        #self.nupp.MääraSuurus(suurus)




class PäevaRuudustik:
    def __init__(self, olek:ProgrammiOlek, pind):
        self.olek = olek
        self.pind = pind
        self.laius = 400
        self.asukoht = (0,0)
        self.päevaRuudud: List[PäevaRuut] = []
        päevad = VõtaKõikAlgusPäevad(olek.sündmusteNimekiri)
        for i in päevad:
            #print(olek.päevaruuduVärv)
            uusRuut = PäevaRuut(olek, pind, i)
            self.päevaRuudud.append(uusRuut)
    
    def VõtaRuudustikuKuupäevad(self):
        kuupäevad = []
        for i in self.päevaRuudud:
            kuup = i.kuupäev
            if kuup not in kuupäevad:
                kuupäevad.append(kuup)
        return kuupäevad
    
    def MääraLaius(self, laius):
        self.laius = laius

    def MääraAsukoht(self, asukoht):
        self.asukoht = asukoht

    def VärskendaRuute(self):
        for i in self.päevaRuudud:
            i.VaataSündmusedÜle()
            
        for i in self.päevaRuudud:
            if len(i.sündmused) == 0:
                try:
                    self.olek.aktiivsedNupud.remove(i.nupp)
                except:
                    pass
                self.päevaRuudud.remove(i)
                break
            
        
        ruutudeKuupäevad = [i.kuupäev for i in self.päevaRuudud]
        sündmusteKuupäevad = [i.kuupäev for i in VõtaKõikAlgusPäevad(self.olek.sündmusteNimekiri)]
        for i in sündmusteKuupäevad:
            if KasKuupäevNimekirjas(ruutudeKuupäevad, i) == False:
                kp = i
                sündmused = VõtaKindlalKuupäeval(self.olek.sündmusteNimekiri, kp)
                päev = Päev(kp,sündmused)
                uusRuut = PäevaRuut(self.olek, self.pind,päev)
                print("Tajus, et on uut ruutu vaja")
                self.päevaRuudud.append(uusRuut)            
    


    def VõtaSuurus(self):
        # Tausta kõrgus leitakse selle põhjal mitu rida ruute tuleb ja see arvutatakse hiljem.
        taustaAsukx = self.asukoht[0]
        taustaAsuky = self.asukoht[1]
        taustaLaius = self.laius

        # Mitu ruutu mahub ühte ritta.
        äärevahe = self.olek.päevaruutudeTaustaJaRuutudeVahe
        ruuduvahe = self.olek.päevaruutudeVahe
        minLaius = self.olek.päevaruuduMinLaius
        # Leiab, mitu ruutu mahub ühte ritta. Põhineb sellel, et vaatab kui palju ruutudevahe suurusid saab vahemikku panna nii, et ülejäänud vahemikku ühe võrra suurema kogusega jagades ei annaks tulemust alla min laiuse.
        mituReas = 0
        mituVahet = 0
        ruum = taustaLaius-2*äärevahe
        while True:
            if (ruum - mituVahet * ruuduvahe) / (mituVahet+1) < minLaius:
                mituReas = mituVahet
                break
            else:
                mituVahet += 1
        
        # Võib olla olukord, kus aken läheb nii kitsaks, et isegi, kui reas on ainult 1 ruut, on sellel ikkagi nii vähe ruumi, et reas peaks olema null ruutu. See kood parandab olukorra ja lic lepib sellega, et ruudu laius on väiksem, kui minlaius.
        if mituReas == 0: mituReas = 1
        
        # Arvutab, kui palju ruumi jääb vahede kõrvalt ruutudele. Mis peab ühe reasoleva ruudu laius olema. 
        vahesidKokku = 2*äärevahe + (mituReas-1)*ruuduvahe
        ruudulaius = (taustaLaius - vahesidKokku)/mituReas

        # RUUTUDE PAIGUTAMINE ALGAB:

        ridadeArv = 0
        vasakServ = taustaAsukx
        ülemServ = taustaAsuky

        # KÕigile ruutudele määratakse ühtne laius.
        for i in self.päevaRuudud:
            i.MääraSuurus(ruudulaius, None)

        ridadeKõrgused = []
        reaKõrgus = 0
        counter = 0
        for i in self.päevaRuudud:
            
            # Kui ollakse paigutamisega rea alguses, käiakse läbi sellele reale tulevad ruudud ja küsitakse kui palju neil ruumi oleks vaja.
            antavRuum = 0
            if counter % (mituReas) == 0:
                ruumivajadused = []
                for j in self.päevaRuudud[counter:counter+mituReas]:
                    ruumivajadused.append(j.KuiPaljuRuumiOnVaja())
                    
                #Antavaks ruumiks määratakse vajaduste keskmine, aga vb tulevikus võib mingi intelligentsema otsustaja teha
                antavRuum = sum(ruumivajadused)/len(ruumivajadused)
                reaKõrgus = antavRuum
                ridadeKõrgused.append(reaKõrgus)
            
            
                
            mitmesTulp = counter % mituReas
            mitmesRida = floor(counter/mituReas)
            # Kui kõik ruudud on läbi käidud, ss on ridadeArv võrdne sellega, kui palju ridasid on ruudustikus. Seda väärtust kasutab taust, et oma kõrgus leida.
            ridadeArv = mitmesRida


            asukx = vasakServ + äärevahe + mitmesTulp*(ruudulaius + ruuduvahe)
            asuky = ülemServ + äärevahe + sum(ridadeKõrgused[:-1]) + max(len(ridadeKõrgused)-1, 0) * ruuduvahe

            i.MääraAsukoht(asukx, asuky)
            i.MääraSuurus(ruudulaius, reaKõrgus)
            counter += 1
        
        taustaKõrgus = 2*äärevahe + sum(ridadeKõrgused)+ (ridadeArv)*ruuduvahe

        return (taustaLaius, taustaKõrgus)




    def Joonista(self):
        # Tausta kõrgus leitakse selle põhjal mitu rida ruute tuleb ja see arvutatakse hiljem.
        taustaAsukx = self.asukoht[0]
        taustaAsuky = self.asukoht[1]
        taustaLaius = self.laius

        # Mitu ruutu mahub ühte ritta.
        äärevahe = self.olek.päevaruutudeTaustaJaRuutudeVahe
        ruuduvahe = self.olek.päevaruutudeVahe
        minLaius = self.olek.päevaruuduMinLaius
        # Leiab, mitu ruutu mahub ühte ritta. Põhineb sellel, et vaatab kui palju ruutudevahe suurusid saab vahemikku panna nii, et ülejäänud vahemikku ühe võrra suurema kogusega jagades ei annaks tulemust alla min laiuse.
        mituReas = 0
        mituVahet = 0
        ruum = taustaLaius-2*äärevahe
        while True:
            if (ruum - mituVahet * ruuduvahe) / (mituVahet+1) < minLaius:
                mituReas = mituVahet
                break
            else:
                mituVahet += 1
        
        # Võib olla olukord, kus aken läheb nii kitsaks, et isegi, kui reas on ainult 1 ruut, on sellel ikkagi nii vähe ruumi, et reas peaks olema null ruutu. See kood parandab olukorra ja lic lepib sellega, et ruudu laius on väiksem, kui minlaius.
        if mituReas == 0: mituReas = 1
        
        # Arvutab, kui palju ruumi jääb vahede kõrvalt ruutudele. Mis peab ühe reasoleva ruudu laius olema. 
        vahesidKokku = 2*äärevahe + (mituReas-1)*ruuduvahe
        ruudulaius = (taustaLaius - vahesidKokku)/mituReas

        # RUUTUDE PAIGUTAMINE ALGAB:

        ridadeArv = 0
        vasakServ = taustaAsukx
        ülemServ = taustaAsuky

        # KÕigile ruutudele määratakse ühtne laius.
        for i in self.päevaRuudud:
            i.MääraSuurus(ruudulaius, None)

        fakeRuudud = []
        ridadeKõrgused = []
        reaKõrgus = 0
        counter = 0
        for i in self.päevaRuudud:
            
            # Kui ollakse paigutamisega rea alguses, käiakse läbi sellele reale tulevad ruudud ja küsitakse kui palju neil ruumi oleks vaja.
            antavRuum = 0
            if counter % (mituReas) == 0:
                ruumivajadused = []
                for j in self.päevaRuudud[counter:counter+mituReas]:
                    ruumivajadused.append(j.KuiPaljuRuumiOnVaja())
                    
                #Antavaks ruumiks määratakse vajaduste keskmine, aga vb tulevikus võib mingi intelligentsema otsustaja teha
                antavRuum = sum(ruumivajadused)/len(ruumivajadused)
                reaKõrgus = antavRuum
                ridadeKõrgused.append(reaKõrgus)
            
            
                
            mitmesTulp = counter % mituReas
            mitmesRida = floor(counter/mituReas)
            # Kui kõik ruudud on läbi käidud, ss on ridadeArv võrdne sellega, kui palju ridasid on ruudustikus. Seda väärtust kasutab taust, et oma kõrgus leida.
            ridadeArv = mitmesRida


            asukx = vasakServ + äärevahe + mitmesTulp*(ruudulaius + ruuduvahe)
            asuky = ülemServ + äärevahe + sum(ridadeKõrgused[:-1]) + max(len(ridadeKõrgused)-1, 0) * ruuduvahe

            i.MääraAsukoht(asukx, asuky)
            i.MääraSuurus(ruudulaius, reaKõrgus)
            counter += 1
        
        taustaKõrgus = 2*äärevahe + sum(ridadeKõrgused)+ (ridadeArv)*ruuduvahe

        fakeRuuteVaja = (ridadeArv+1) * mituReas - len(self.päevaRuudud)
        fakeRuudud = []
        for i in range(fakeRuuteVaja):
            a = FakePäevaRuut(self.olek, self.pind)
            asukx = asukx + ruudulaius + ruuduvahe

            a.MääraAsukoht((asukx, asuky))
            a.MääraSuurus((ruudulaius, reaKõrgus))
            fakeRuudud.append(a)
        #print(len(fakeRuudud))

        # PAIGUTAMINE LÕPPES



        # ALGAB JOONISTAMINE

        # Taust
        taustaVärv = self.olek.päevaruutudeTaustaVärv
        nurgaRaadius = self.olek.päevaruutudeTaustaNurgaÜmardus
        pygame.draw.rect(self.pind, taustaVärv, (taustaAsukx, taustaAsuky, taustaLaius, taustaKõrgus), border_radius=nurgaRaadius)

        # Ruudud
        for i in self.päevaRuudud:
            i.Joonista()

        for i in fakeRuudud:
            i.Joonista()
            

            


  