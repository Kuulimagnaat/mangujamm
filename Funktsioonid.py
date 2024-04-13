import Mangija, zombie, angel, random
from typing import List

def TegeleTulistamisega(mangija:Mangija.Mangija, zombinimek:List[zombie.Zombie], inglinimek:List[angel.Angel]):

    bulletDamage = mangija.damage

    # Zombide tabamine
    zpihtasaajad:List[zombie.Zombie] = []
    for z in zombinimek:
        if z.KasSaabPihta(mangija.VotaAsuk(), mangija.VotaSuund()) == True:
            zpihtasaajad.append(z)
            
    def sortija(z:zombie.Zombie):
        return z.LeiaKaugusMangijast(mangija)
    
    zpihtasaajad.sort(key=sortija)
    

    # Inglite tabamine
    ipihtasaajad:List[angel.Angel] = []
    for z in inglinimek:
        if z.KasSaabPihta(mangija.VotaAsuk(), mangija.VotaSuund()) == True:
            ipihtasaajad.append(z)
            
    def sortija(z:angel.Angel):
        return z.LeiaKaugusMangijast(mangija)
    
    ipihtasaajad.sort(key=sortija)

    if (len(ipihtasaajad) != 0 and len(zpihtasaajad) != 0):
        if (ipihtasaajad[0].LeiaKaugusMangijast(mangija) <= zpihtasaajad[0].LeiaKaugusMangijast(mangija)):
            ipihtasaajad[0].SaaViga(bulletDamage)
        else:
            zpihtasaajad[0].SaaViga(bulletDamage)
    
    elif (len(ipihtasaajad) != 0 and len(zpihtasaajad) == 0):
        ipihtasaajad[0].SaaViga(bulletDamage)
        
    elif (len(ipihtasaajad) == 0 and len(zpihtasaajad) != 0):
        zpihtasaajad[0].SaaViga(bulletDamage)
        
    else:
        pass

def spawnZombie(points):
    return zombie.Zombie(random.randrange(-10, 0) if random.random() < 0.5 else random.randrange(1280, 1280+10),
                              random.randrange(-10, 0) if random.random() < 0.5 else random.randrange(720, 720+10),
                              random.choice(points))

def spawnAngel(zombies):
    return angel.Angel(random.randrange(-10, 0) if random.random() < 0.5 else random.randrange(1280, 1280+10),
                             random.randrange(-10, 0) if random.random() < 0.5 else random.randrange(720, 720+10),
                             random.choice(zombies) if len(zombies)!= 0 else None)