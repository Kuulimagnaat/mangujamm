import pygame
import random
from zombie import *

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

zombies = []

pentaGramPoints = [(100, 100), (500,500)]

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    if len(zombies) == 0:
        x=random.randrange(0, 1280)
        y=random.randrange(0,720)
        zombie = Zombie(x, y, pentaGramPoints[0])
        print(zombie.x, zombie.y)
        for point in pentaGramPoints:
            if ((point[0]-x)**2+(point[1]-y)**2) < (zombie.target[0]-x)**2+(zombie.target[1]-y)**2:
                zombie.target=point
        zombies.append(zombie)

    for zombie in zombies:
        zombie.update(screen)

    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()