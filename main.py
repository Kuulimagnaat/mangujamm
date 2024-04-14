import pygame
import random
from Mangija import Mangija
from Funktsioonid import *
from button import *
import Tekst

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

my_font = pygame.font.Font("./assets/demon_panic.otf", 30)

screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("DemonSUMMON")

clock = pygame.time.Clock()
mouse = pygame.mouse
mixer = pygame.mixer_music
running = True
game_over = False
game_won = False

pentaGramPoints = [(650, 150), (350, 300), (950, 300), (492, 620), (800, 620)]

zombies = [spawnZombie(pentaGramPoints)]
angels = []
mixer.load("./assets/loadAndChamber.mp3")

#pentagramImage = pygame.transform.scale_by(pygame.image.load("./assets/pentagram.webp"), 0.5)
backgroundImage = pygame.image.load("./assets/background.png").convert()
candleImage = pygame.image.load("./assets/candle.png").convert_alpha()
forestImage = pygame.image.load("./assets/puud.png").convert_alpha()
angelImage = pygame.transform.scale_by(pygame.image.load("./assets/ingel2.png").convert_alpha(), 7)
tegelaseImage = pygame.transform.scale_by(pygame.image.load("./assets/peategelane.png").convert_alpha(), 7)
zombiImage = pygame.transform.scale_by(pygame.image.load("./assets/zombie1.png").convert_alpha(), 7)
textboxImage = pygame.transform.scale_by(pygame.image.load("./assets/textbox.png").convert_alpha(), 2.5)

vignette_alpha = 0
vignette_speed = 2
vignette_color = (0, 0, 0)

# Load the vignette image
vignette_image = pygame.image.load("./assets/vignette.jpg")
vignette_image = pygame.transform.scale(vignette_image, (1280, 720))
vignette_image.set_alpha(vignette_alpha)  # Set initial alpha value

game_over_font = pygame.font.Font("./assets/demon_panic.otf", 36)
stats_font = pygame.font.Font("./assets/demon_panic.otf", 24)

game_over_quotes = [
    "In the end, darkness consumes all.",
    "Lost in the shadows, a forgotten soul.",
    "The abyss beckons, claiming another.",
    "Whispers of despair echo in the void.",
    "Beyond the veil lies only oblivion.",
    "Fate's cruel embrace, eternal and cold.",
    "Gone, but not forgotten. Remembered in darkness.",
    "Silent screams in the night, fading into nothingness.",
    "Embrace the darkness, for it is your companion.",
    "In the depths of despair, find solace in the void."
]

backToMainMenuButton = Button((1280-300)/2, 400, 300, 100, "Back to Main Menu", bgcolor=(15,15,15), textcolor=(255,255,255))

# Function to draw Game Over text on the screen
def draw_game_over_text(screen, chosen_quote, mangija, currentZomb):
    game_over_text = game_over_font.render(chosen_quote, True, (255, 0, 0))
    shadow_text = game_over_font.render(chosen_quote, True, (0,0,0))
    text_rect = game_over_text.get_rect(center=(640, 360))  # Center the text on the screen
    shadow_offset = (5, 5)
    shadow_rect = shadow_text.get_rect(center=(640 + shadow_offset[0], 360 + shadow_offset[1]))
    screen.blit(shadow_text, shadow_rect)
    screen.blit(game_over_text, text_rect)

    stats_text = f"Friends Killed: {currentZomb} | Angels Killed: {mangija.angelKills} | Damage Done: {mangija.damageDone}"
    shadow_text = stats_font.render(stats_text, True, (0,0,0))
    stats_rendered = stats_font.render(stats_text, True, (255, 0, 0))

    shadow_offset = (5, 5)
    shadow_rect = shadow_text.get_rect(center=(640 + shadow_offset[0], 200 + shadow_offset[1]))
    stats_rect = stats_rendered.get_rect(center=(640, 200))
    
    screen.blit(shadow_text, shadow_rect)
    screen.blit(stats_rendered, stats_rect)




pygame.font.init()
pygfont = pygame.font.Font("HANDMEDS.TTF", 40)
    
tekst1 = "Tumedad rituaalid on ainus asi, mille nimel ma veel elan."
t1 = Tekst.MitmeReaTekst(screen, tekst1, pygfont)
t1.MääraAsukoht((130,600))
t1.MääraLaius(700)

tekst2 = "Aga ka need muutuvad üksluiseks."
t2 = Tekst.MitmeReaTekst(screen, tekst2, pygfont)
t2.MääraAsukoht((130,600))
t2.MääraLaius(700)
    
tekst3 = "Ma olen valmis ülimaks riituseks, mille lõpuks kohtun vanakuradi endaga."
t3 = Tekst.MitmeReaTekst(screen, tekst3, pygfont)
t3.MääraAsukoht((130,600))
t3.MääraLaius(700)

tekst4 = "Pimeduse elukad on minu sõbrad."
t4 = Tekst.MitmeReaTekst(screen, tekst4, pygfont)
t4.MääraAsukoht((130,600))
t4.MääraLaius(700)

tekst5 = "Jumala teenrid üritavad mind takistada. Mu püstol aitab nendega tegeleda.\nF-nupp, mu kaitseloits, ajab nad segadusse."
t5 = Tekst.MitmeReaTekst(screen, tekst5, pygfont)
t5.MääraAsukoht((130,600))
t5.MääraLaius(675)

tekst6 = "Rituaali töötamiseks peavad poolsurnud pentagrammi otstes elus püsima."
t6 = Tekst.MitmeReaTekst(screen, tekst6, pygfont)
t6.MääraAsukoht((130,600))
t6.MääraLaius(590)

tekst7 = "Ma liigun WASD-nuppudega ja tulistan\nhiireklõpsuga."
t7 = Tekst.MitmeReaTekst(screen, tekst7, pygfont)
t7.MääraAsukoht((130,600))
t7.MääraLaius(700)

def dialogScene(scene, n):
    if n == 1:
        screen.blit(tegelaseImage, (85, 320))
        screen.blit(textboxImage, (55,500))
        t1.Joonista()
    if n == 2:
        screen.blit(tegelaseImage, (75, 320))
        screen.blit(textboxImage, (55,500))
        t2.Joonista()
    if n == 3:
        a = pygame.transform.flip(tegelaseImage, True, False)
        screen.blit(a, (65, 320))
        screen.blit(textboxImage, (55,500))
        t3.Joonista()
    if n == 4:
        a = pygame.transform.flip(tegelaseImage, True, False)
        screen.blit(a, (85, 320))
        screen.blit(zombiImage, (600, 320))
        screen.blit(textboxImage, (55,500))
        t4.Joonista()
    if n == 5:
        a = pygame.transform.flip(tegelaseImage, True, False)
        screen.blit(a, (95, 320))
        screen.blit(angelImage, (600, 320))
        screen.blit(textboxImage, (55,500))
        t5.Joonista()
    if n == 6:
        screen.blit(tegelaseImage, (105, 320))
        screen.blit(textboxImage, (55,500))
        t6.Joonista()
    if n == 7:
        screen.blit(tegelaseImage, (85, 320))
        screen.blit(textboxImage, (55,500))
        t7.Joonista()


summonProgress = 0
summonSpeed = 5
summonReductionSpeed = 1
timePassedFromSummon = 0

zombieSpawnTimer = 5
timePassedFromZombie = 0
maxZombies = 7

angelSpawnTimer = 3
timePassedFromAngel = 0
maxAngels = 10

waveCooldown = 16
timePassedFromWave = 0

waves = [2]

mangija = Mangija.Mangija(100,100,5)

paused = False
mainMenu = True

dialogActivated = False
dialogCounter = 1

menuWidth, menuHeight = 400, 350

# Pause menu
continueButton = Button((1280-menuWidth)/2+100, (720-menuHeight)/2+50, 200, 100, "Continue")
exitButton = Button((1280-menuWidth)/2+100, (720-menuHeight)/2+50+150, 200, 100, "Exit")

#Main menu
startButton = Button((1280-menuWidth)/2+100, (720-menuHeight)/2+50, 200, 100, "Start")

#Dialog scene button
nextButton = Button(1280-250, 720-150, 200, 100, "Next")

# Add these variables to your code
blood_pool_radius = 0
blood_pool_max_radius = 60
blood_pool_color = (255, 0, 0, 100)  # Semi-transparent red color for blood pool

vignette_alpha = 0  # Initial alpha value for vignette
vignette_speed = 2  # Speed at which the vignette appears
vignette_color = (0, 0, 0)  # Black color for vignette

stun_cooldown_timer = 0
stun_cooldown_duration = 10

f_ability_box_pos = (50, 50)  # Position of the cooldown box
f_ability_box_size = (200, 30)  # Size of the cooldown box
f_ability_ready_color = (255, 0, 0)  # Color when ability is ready
f_ability_cooldown_color = (0, 255, 0)  # Color when ability is on cooldown

# Function to draw the cooldown bar with the indicator decreasing from right to left
def draw_cooldown_bar(screen, current_cooldown, max_cooldown):
    cooldown_progress = max(0, min(1, current_cooldown / max_cooldown))  # Calculate cooldown progress (between 0 and 1)
    bar_width = int(cooldown_progress * f_ability_box_size[0])  # Calculate width of the filled portion of the bar
    filled_width = f_ability_box_size[0] - bar_width  # Calculate the width of the filled portion
    bar_rect = pygame.Rect((f_ability_box_pos[0] + filled_width, f_ability_box_pos[1]), (bar_width, f_ability_box_size[1]))  # Create rectangle for the filled portion
    remaining_rect = pygame.Rect(f_ability_box_pos, (filled_width, f_ability_box_size[1]))  # Create rectangle for the remaining portion
    pygame.draw.rect(screen, f_ability_ready_color, bar_rect)  # Draw the filled portion
    pygame.draw.rect(screen, f_ability_cooldown_color, remaining_rect)  # Draw the remaining portion
    
    # Draw text above the cooldown bar
    text_surface = stats_font.render("Stun (F)", True, (0, 0, 0))  # Create text surface
    text_rect = text_surface.get_rect(midtop=(f_ability_box_pos[0] + f_ability_box_size[0] // 2, f_ability_box_pos[1]))  # Position the text
    screen.blit(text_surface, text_rect)  # Blit the text onto the screen

def draw_ingame_stats(screen, x, y):
    pygame.draw.rect(screen, ((125,125,125)), pygame.rect.Rect((x,y), (400, 100)))
    angelsKilledText = stats_font.render(f"Angels killed: {mangija.angelKills}", False, (255, 255, 255))
    murderedFriends = stats_font.render(f"Friends murdered: {mangija.zombieKills}", False, (255, 255, 255))
    screen.blit(angelsKilledText, (x+25, y+25))
    screen.blit(murderedFriends, (x+25, y+55))


    

def init():
    global zombies, angels, mangija, timePassedFromAngel, timePassedFromSummon, timePassedFromZombie, mixer, game_over, vignette_alpha
    zombies = [spawnZombie(pentaGramPoints)]
    angels = []
    mangija = Mangija.Mangija(1280/2,720/2,5)
    timePassedFromZombie, timePassedFromAngel, timePassedFromSummon = 0, 0, 0
    game_over=False
    game_won = False
    vignette_alpha





while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
    
    screen.blit(backgroundImage, (0,0))

    if mainMenu or paused:
        screen.blit(forestImage, (0,0))
        pygame.draw.rect(screen, (125,125,125), pygame.Rect(((1280-menuWidth)/2, (720-menuHeight)/2), (menuWidth, menuHeight)))
        exitButton.draw(screen)

    if mainMenu:
        startButton.draw(screen)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if startButton.isOver(mouse.get_pos()):
                        mixer.play()
                        mainMenu = False
                        init()
                        dialogActivated = True
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
                        mixer.load("./assets/loadAndChamber.mp3")
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                paused=False
        pygame.display.flip()
        clock.tick(60)
        continue

    if dialogActivated:
        screen.blit(forestImage, (0,0))
        dialogScene(screen, dialogCounter)
        nextButton.draw(screen)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if nextButton.isOver(mouse.get_pos()):
                        if dialogCounter >= 7:
                            dialogActivated = False
                            dialogCounter = 1
                        else:
                            dialogCounter += 1
        pygame.display.flip()
        clock.tick(60)
        continue


    for event in events:
        if not game_over and not game_won:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mixer.load("./assets/pistolShot.mp3")
                    mangija.TekitaMuzzleFlash(5)
                    mixer.play()
                    TegeleTulistamisega(mangija, zombies, angels)
                    mangija.SaaTagasilööki(5,1)
                elif event.button == 2:
                    print("angels on screen: ", len(angels))
                    print("angels killed: ", mangija.angelKills)
                    print("zombies on screen: ", len(zombies))
                    print("zombies killed: ", mangija.zombieKills)
                    print("Damage done to angels: ", mangija.damageDone)
                    print(dialogCounter)
                #print("Tulistati!")
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                paused=True
        # Check if the timer event is triggered
        if event.type == pygame.USEREVENT + 3:
            for angel in angels:
                angel.Stunned = False
    
    keys = pygame.key.get_pressed()
    if not game_over and not game_won:
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            mangija.asukx=clamp(mangija.asukx-mangija.kiirus, 0, 1280)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            mangija.asukx=clamp(mangija.asukx+mangija.kiirus, 0, 1280)
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            mangija.asuky=clamp(mangija.asuky-mangija.kiirus, 0, 720)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            mangija.asuky=clamp(mangija.asuky+mangija.kiirus, 0, 720)
        if keys[pygame.K_f] and stun_cooldown_timer <= 0:
            # Iterate over angels and stun those targeting the player
            for angel in angels:
                if angel.target == mangija:
                    angel.Stunned = True
                    pygame.time.set_timer(pygame.USEREVENT + 3, 3000)

            stun_cooldown_timer = stun_cooldown_duration

    if stun_cooldown_timer > 0:
        stun_cooldown_timer -= clock.get_time() / 1000  # Decrease cooldown timer
        if stun_cooldown_timer <= 0:
            stun_cooldown_timer = 0  # Ensure timer doesn't go below 0

    # fill the screen with a color to wipe away anything from last frame

    #Pentagram
    #screen.blit(pentagramImage, ((1280-pentagramImage.get_width())/2,(720-pentagramImage.get_height())/2))
    for point in pentaGramPoints:
        #pygame.draw.rect(screen, (255, 165, 0), pygame.Rect((point[0]-50, point[1]-50), (100,100)))
        screen.blit(candleImage, (point[0]-50, point[1]-50))

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
        
        if timePassedFromWave == 0:
            timePassedFromWave = pygame.time.get_ticks()
        elif pygame.time.get_ticks() >= timePassedFromWave + waveCooldown*1000:
            wave = random.choice(waves)
            if len(angels)+wave>maxAngels:
                angels.extend(spawnAngel(zombies, maxAngels-len(angels)))
            else:
                angels.extend(spawnAngel(zombies, wave))
            timePassedFromWave = 0

    #Game over blood display
    if game_over:
        # Animate blood pool
        if blood_pool_radius < blood_pool_max_radius:
            blood_pool_radius += 5  # Increase blood pool radius gradually
        pygame.draw.circle(screen, blood_pool_color, (mangija.asukx, mangija.asuky), blood_pool_radius)

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

    # Forest cover
    screen.blit(forestImage, (0,0))

    #Draws the stun cooldown bar
    draw_cooldown_bar(screen, stun_cooldown_timer, stun_cooldown_duration)

    #On screen stats
    draw_ingame_stats(screen, 0, 620)

    # Progress bar
    if summonProgress>=0 and not game_won:
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


    # Update vignette alpha if game is over
    if game_over and vignette_alpha < 200:
        vignette_alpha = min(200, vignette_alpha + vignette_speed)

    # Handle events outside the event loop
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Check if left mouse button is clicked
                if backToMainMenuButton.isOver(event.pos) and (game_won or game_over):
                    mainMenu = True
                    game_over = False
                    game_won = False
                    summonProgress=0
                    init()

    # Draw vignette image if game is over
    if game_over:
        # Set the alpha value for the image
        vignette_image.set_alpha(vignette_alpha)
        
        # Blit the vignette image onto the screen
        screen.blit(vignette_image, (0, 0))  # Adjust position if neededs
        draw_game_over_text(screen, chosen_quote, mangija, currentFriendKills)

        backToMainMenuButton.draw(screen)
    
    #Game end logic
    if mangija.elud <= 0 and not game_over and not game_won:
        game_over = True
        currentFriendKills = mangija.zombieKills
        chosen_quote = random.choice(game_over_quotes)
        
        # Disable player controls
        keys = pygame.key.get_pressed()  # Clear the key state

    #Game victory
    # Check if victory condition is met
    if summonProgress >= 100 or game_won:
        game_won = True
        mangija.elud = 0 #to avoid attacks
        # Display victory screen
        screen.fill((0, 0, 0))  # Fill the screen with black
        victory_text = game_over_font.render("Saatan on saabunud", True, (255, 255, 255))  # Render victory text
        text_rect = victory_text.get_rect(center=(640, 360))  # Center the text on the screen
        screen.blit(victory_text, text_rect)  # Blit the victory text onto the screen

        # Draw a button to return to the main menu
        backToMainMenuButton.draw(screen)
        
    #a.Joonista()

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()