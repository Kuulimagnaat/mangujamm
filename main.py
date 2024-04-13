import pygame
import random
from Mangija import Mangija
from Funktsioonid import *
from button import *

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
pygame.display.set_caption("DemonSUMMON")

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


mangija = Mangija.Mangija(100,100,5)

paused = False
mainMenu = True

menuWidth, menuHeight = 400, 350

# Pause menu
continueButton = Button((1280-menuWidth)/2+100, (720-menuHeight)/2+50, 200, 100, "Continue")
exitButton = Button((1280-menuWidth)/2+100, (720-menuHeight)/2+50+150, 200, 100, "Exit")

#Main menu
startButton = Button((1280-menuWidth)/2+100, (720-menuHeight)/2+50, 200, 100, "Start")

def init():
    global zombies, angels, mangija, timePassedFromAngel, timePassedFromSummon, timePassedFromZombie
    zombies = [spawnZombie(pentaGramPoints)]
    angels = []
    mangija = Mangija.Mangija(0,0,5)
    timePassedFromZombie, timePassedFromAngel, timePassedFromSummon = 0, 0, 0

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill("purple")

    if mainMenu or paused:
        pygame.draw.rect(screen, (125,125,125), pygame.Rect(((1280-menuWidth)/2, (720-menuHeight)/2), (menuWidth, menuHeight)))
        exitButton.draw(screen)

    if mainMenu:
        startButton.draw(screen)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if startButton.isOver(mouse.get_pos()):
                        mainMenu = False
                        init()
                    elif exitButton.isOver(mouse.get_pos()):
                        running= False
        pygame.display.flip()
        clock.tick(60)
        continue
    
    if paused:
        continueButton.draw(screen)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if continueButton.isOver(mouse.get_pos()):
                        paused = False
                    elif exitButton.isOver(mouse.get_pos()):
                        paused = False
                        mainMenu = True

        pygame.display.flip()
        clock.tick(60)
        continue

    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mangija.TekitaMuzzleFlash(5)
                TegeleTulistamisega(mangija, zombies, angels)
            elif event.button == 3:
                paused = True
            elif event.button == 2:
                print("angels on screen: ", len(angels))
                print("angels killed: ", mangija.angelKills)
                print("zombies on screen: ", len(zombies))
                print("zombies killed: ", mangija.zombieKills)
                print("Damage done to angels: ", mangija.damageDone)
            print("Tulistati!")
            mangija.TekitaMuzzleFlash(5)
            TegeleTulistamisega(mangija, zombies, angels)
            mangija.SaaTagasilööki(30,2.5)
            
        if event.type == pygame.USEREVENT + 3:
            for angel in angels:
                angel.Stunned = False
    
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        mangija.asukx-= mangija.kiirus
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        mangija.asukx+=mangija.kiirus
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        mangija.asuky-=mangija.kiirus
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        mangija.asuky+=mangija.kiirus
    if keys[pygame.K_f]:
        # Iterate over angels and stun those targeting the player
        for angel in angels:
            if angel.target == mangija:
                angel.Stunned = True
                pygame.time.set_timer(pygame.USEREVENT + 3, 3000)

    # fill the screen with a color to wipe away anything from last frame

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