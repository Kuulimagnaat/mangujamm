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
mouse = pygame.mouse
running = True

zombies = []

summonProgress = 0
summonSpeed = 2
timePassedFromSummon = 0

pentaGramPoints = [(100, 100), (500,500), (300, 150), (400, 400), (621,199)]

mangija = Mangija(0,0,5)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            zombies.remove(random.choice(zombies))
    
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        mangija.asukx-= mangija.kiirus
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        mangija.asukx+=mangija.kiirus
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        mangija.asuky-=mangija.kiirus
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        mangija.asuky+=mangija.kiirus

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    if len(zombies) != 5:
        zombies.append(Zombie(random.randrange(0, 1280), random.randrange(0,720), random.choice(pentaGramPoints)))
        

    mangija.Varskenda()
    mangija.Joonista(screen)

    for point in pentaGramPoints:
        pygame.draw.rect(screen, (255, 165, 0), pygame.Rect((point[0]-50, point[1]-50), (100,100)))

    allZombiesArrived = True
    for zombie in zombies:
        newZombiesList = zombies.copy()
        newZombiesList.remove(zombie)
        for zombie2 in newZombiesList:
            if not zombie2.walking and zombie2.target == zombie.target and ((zombie.getPosX()-zombie2.getPosX())**2+(zombie.getPosY()-zombie2.getPosY())**2)**(1/2)<=100:
                newTargets = pentaGramPoints.copy()
                newTargets.remove(zombie2.target)
                zombie.setTarget(random.choice(newTargets))
        zombie.update(screen, mangija)
        if zombie.walking:
            allZombiesArrived=False
    if allZombiesArrived and len(zombies)==5:
        if timePassedFromSummon==0:
            timePassedFromSummon=pygame.time.get_ticks()
        elif pygame.time.get_ticks()>=timePassedFromSummon+1.5*1000:
            summonProgress=clamp(summonProgress+summonSpeed, 0, 100)
            print(summonProgress)
            timePassedFromSummon=0
    else:
        if timePassedFromSummon==0:
            timePassedFromSummon=pygame.time.get_ticks()
        elif pygame.time.get_ticks()>=timePassedFromSummon+0.5*1000:
            summonProgress=clamp(summonProgress-summonSpeed, 0, 100)
            print(summonProgress)
            timePassedFromSummon=0


    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()