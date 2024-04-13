import pygame
import random
from Mangija import Mangija
from zombie import *

def clamp(n, min, max): 
    if n < min: 
        return min
    elif n > max: 
        return max
    else: 
        return n 

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

zombies = []

summonProgress = 0
summonSpeed = 2
timePassedFromSummon = 0

pentaGramPoints = [(100, 100), (500,500), (300, 150)]

mangija = Mangija(0,0,5)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    if len(zombies) == 0:
        zombies.append(Zombie(random.randrange(0, 1280), random.randrange(0,720), random.choice(pentaGramPoints)))
        zombies.append(Zombie(random.randrange(0, 1280), random.randrange(0,720), zombies[0].target))   

    mangija.Varskenda()
    mangija.Joonista(screen)

    for point in pentaGramPoints:
        pygame.draw.rect(screen, (255, 165, 0), pygame.Rect((point[0]-50, point[1]-50), (100,100)))

    allZombiesArrived = True
    for zombie in zombies:
        newZombiesList = zombies.copy()
        newZombiesList.remove(zombie)
        for zombie2 in newZombiesList:
            if not zombie2.walking and ((zombie.getPosX()-zombie2.getPosX())**2+(zombie.getPosY()-zombie2.getPosY())**2)**(1/2)<=200:
                newTargets = pentaGramPoints.copy()
                newTargets.remove(zombie2.target)
                zombies[zombies.index(zombie2)].target = random.choice(newTargets)
                print("test")
        zombie.update(screen)
        if zombie.walking:
            allZombiesArrived=False
    if allZombiesArrived:
        if timePassedFromSummon==0:
            timePassedFromSummon=pygame.time.get_ticks()
        elif pygame.time.get_ticks()>=timePassedFromSummon+1.5*1000:
            summonProgress=clamp(summonProgress+summonSpeed, 0, 100)
            print(summonProgress)
            timePassedFromSummon=0



    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()