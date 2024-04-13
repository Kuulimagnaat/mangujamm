import pygame
import random
from Mangija import Mangija
from Funktsioonid import *

def clamp(n, min, max): 
    if n < min: 
        return min
    elif n > max: 
        return max
    else: 
        return n

# pygame setup
pygame.init()
pygame.font.init()

my_font = pygame.font.SysFont('Comic Sans MS', 30)

screen = pygame.display.set_mode((1280, 720))


clock = pygame.time.Clock()
mouse = pygame.mouse
running = True

pentaGramPoints = [(635, 100), (350, 300), (950, 300), (492, 620), (800, 620)]

zombies = [spawnZombie(pentaGramPoints)]
angels = []

pentagramImage = pygame.transform.scale_by(pygame.image.load("./assets/pentagram.webp"), 0.5)

summonProgress = 0
summonSpeed = 2
summonReductionSpeed = 1
timePassedFromSummon = 0

zombieSpawnTimer = 5
timePassedFromZombie = 0
maxZombies = 6

angelSpawnTimer = 3
timePassedFromAngel = 0
maxAngels = 10


mangija = Mangija.Mangija(0,0,5)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            print("Tulistati!")
            mangija.TekitaMuzzleFlash(5)
            TegeleTulistamisega(mangija, zombies, angels)
            
    
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

    #Pentagram
    screen.blit(pentagramImage, ((1280-pentagramImage.get_width())/2,(720-pentagramImage.get_height())/2))
    for point in pentaGramPoints:
        pygame.draw.rect(screen, (255, 165, 0), pygame.Rect((point[0]-50, point[1]-50), (100,100)))

    if len(zombies)<=maxZombies:
        if timePassedFromZombie == 0:
            timePassedFromZombie = pygame.time.get_ticks()
        elif pygame.time.get_ticks() >= timePassedFromZombie + zombieSpawnTimer*1000:
            zombies.append(spawnZombie(pentaGramPoints))
            timePassedFromZombie=0

    if len(angels)<=maxAngels:
        if timePassedFromAngel == 0:
            timePassedFromAngel = pygame.time.get_ticks()
        elif pygame.time.get_ticks() >= timePassedFromAngel + angelSpawnTimer*1000:
            angels.append(spawnAngel(zombies))
            timePassedFromAngel=0


    mangija.Varskenda()
    mangija.Joonista(screen)

    zombiesArrived=0
    for zombie in zombies:
        if zombie.onSurnud:
            zombies.remove(zombie)
            continue
        newZombiesList = zombies.copy()
        newZombiesList.remove(zombie)
        for zombie2 in newZombiesList:
            if not zombie2.walking and zombie2.target == zombie.target and ((zombie.getPosX()-zombie2.getPosX())**2+(zombie.getPosY()-zombie2.getPosY())**2)**(1/2)<=100:
                newTargets = pentaGramPoints.copy()
                newTargets.remove(zombie2.target)
                zombie.setTarget(random.choice(newTargets))
        zombie.update(screen, mangija)
        if not zombie.walking:
            zombiesArrived+=1
    if zombiesArrived==len(pentaGramPoints):
        if timePassedFromSummon==0:
            timePassedFromSummon=pygame.time.get_ticks()
        elif pygame.time.get_ticks()>=timePassedFromSummon+1.5*1000:
            summonProgress=clamp(summonProgress+summonSpeed, 0, 100)
            timePassedFromSummon=0
    else:
        if timePassedFromSummon==0:
            timePassedFromSummon=pygame.time.get_ticks()
        elif pygame.time.get_ticks()>=timePassedFromSummon+1.5*1000:
            summonProgress=clamp(summonProgress-summonReductionSpeed, 0, 100)
            timePassedFromSummon=0
    
    for angel in angels:
        angel.update(screen, zombies, mangija)
        if angel.onSurnud:
            angels.remove(angel)

    # Progress bar
    if summonProgress>=0:
        progressBarPos = (1050,30)
        progressBarWidth, progressBarHeight = 200, 80
        progressBarBackground = pygame.Rect(progressBarPos, (progressBarWidth, progressBarHeight))
        progressBarBackgroundColor = (100,100,100)
        progressBarProgress = pygame.Rect(progressBarPos, (progressBarWidth*summonProgress/100, progressBarHeight))
        progressBarProgressColor = (200,200,200)
        pygame.draw.rect(screen, progressBarBackgroundColor, progressBarBackground)
        pygame.draw.rect(screen, progressBarProgressColor, progressBarProgress)
        text_surface = my_font.render(f'{summonProgress}%', False, (255, 0, 0))
        screen.blit(text_surface, (progressBarPos[0]+(progressBarWidth-text_surface.get_width())/2, progressBarPos[1]+(progressBarHeight)/4))

    

    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()