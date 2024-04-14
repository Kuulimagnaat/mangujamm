import pygame
from zombie import Zombie
from numpy import linalg, cross
from Mangija import Mangija
import math
import random

pygame.font.init()
font = pygame.font.Font("./assets/demon_panic.otf", 20)

class Angel(pygame.sprite.Sprite):
    def __init__(self, x, y, target):
        self.x = x
        self.y = y
        pygame.sprite.Sprite.__init__(self)
        self.width, self.height = 50, 50
        self.algimage = pygame.image.load(random.choice(["./assets/ingel1.png", "./assets/ingel2.png"]))
        self.image = self.algimage.copy()
        #self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.hp = 30
        self.target = target
        self.kiirus = 4
        self.slow_speed = 2
        self.walking = True
        self.attacking = False

        self.onSurnud = False
        self.Stunned = False

        self.damage = 10
        self.pihtaSaamisRaadius = 50
        self.detection_radius = 250  # Detection radius for the angel
        
        self.last_attack_time = 0
        self.attack_delay = 1000

        self.sword_slash_images = [
            pygame.image.load("./assets/sword_slash_1.png"),
            pygame.image.load("./assets/sword_slash_2.png"),
            pygame.image.load("./assets/sword_slash_3.png"),
            pygame.image.load("./assets/sword_slash_4.png"),
            pygame.image.load("./assets/sword_slash_5.png")
        ]
        self.current_slash_index = 0
        self.frame_delay = 5
        self.slash_duration = 8  # Duration (in frames) for each slash image
        self.slash_timer = 0

        # Dot parameters
        self.dot_radius = 2
        self.dot_color = (0, 255, 0)

        # Health bar parameters
        self.health_bar_length = self.width
        self.health_bar_height = 5
        self.health_bar_color = (0, 255, 0)

    def getPos(self):
        return (self.x, self.y)

    def getPosX(self):
        return self.getPos()[0]

    def getPosY(self):
        return self.getPos()[1]

    def setPos(self, givenX, givenY):
        if self.x > givenX:
            self.image = pygame.transform.flip(self.algimage, flip_x=True, flip_y=False)
            self.image = pygame.transform.scale(self.image, (self.width,self.height))
        else:
            self.image = self.algimage
            self.image = pygame.transform.scale(self.image, (self.width,self.height))
            
        self.x = givenX
        self.y = givenY

    def draw_health_bar(self, surface):
        # Calculate health bar position
        health_bar_x = self.x - self.width / 2
        health_bar_y = self.y - self.height / 2 - 10
        
        # Calculate health bar width based on current health
        health_width = (self.hp / 30) * self.health_bar_length
        
        # Draw health bar background
        pygame.draw.rect(surface, (255, 0, 0), (health_bar_x, health_bar_y, self.health_bar_length, self.health_bar_height))
        # Draw health bar
        pygame.draw.rect(surface, self.health_bar_color, (health_bar_x, health_bar_y, health_width, self.health_bar_height))

    def draw(self, surface):
        if self.attacking:
            color = (255, 0, 0)  # Red when attacking
        elif self.target == None or self.Stunned:
            color = (255, 255, 0)  # Yellow when aimlessly walking
        elif self.target != None:
            color = (255, 255, 255)  # White when following target
        #self.image.fill(color)

        surface.blit(self.image, (self.x - self.width / 2, self.y - self.height / 2))

    def aimless_walking(self, zombieList, mangija):
        # Aimlessly walk around at a slower speed
        if not hasattr(self, "walking_direction"):
            self.walking_direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
            self.remaining_steps = random.randint(30, 60)  # Random steps in one direction

        speedVector = (self.walking_direction[0] * self.slow_speed, self.walking_direction[1] * self.slow_speed)
        new_x = self.x + speedVector[0]
        new_y = self.y + speedVector[1]

        # Check boundaries
        if new_x < 0 or new_x > 1280:
            self.walking_direction = (-self.walking_direction[0], self.walking_direction[1])  # Reverse x direction
        if new_y < 0 or new_y > 720:
            self.walking_direction = (self.walking_direction[0], -self.walking_direction[1])  # Reverse y direction

        self.setPos(max(0, min(new_x, 1280)), max(0, min(new_y, 720)))

        self.remaining_steps -= 1
        if self.remaining_steps <= 0:
            # Choose a new random direction and random number of steps
            self.walking_direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
            self.remaining_steps = random.randint(30, 60)

        # Check for nearby zombies within detection radius
        nearby_entities = [entity for entity in zombieList + [mangija] if self.distance_to_zombie(entity) <= self.detection_radius]
        if nearby_entities:
            # Calculate distances to each entity
            distances = [self.distance_to_zombie(entity) for entity in nearby_entities]
            # Choose the entity with the minimum distance
            min_distance_entity = nearby_entities[distances.index(min(distances))]
            self.target = min_distance_entity


    def update(self, surface, zombieList, mangija=Mangija):
        self.KasSaabPihta(mangija.VotaAsuk(), mangija.VotaSuund())
        if self.Stunned == True and self.hp > 0:
            self.target = None
            self.attacking = False
            self.walking = True
            self.aimless_walking(zombieList, mangija)

            self.draw(surface)
            self.draw_health_bar(surface)
            surface.blit(font.render("STUNNED", False, (255, 255, 255)), (self.x-45, self.y+20))
            self.draw_dot(surface)
            self.draw_detection_radius(surface)  # Draw detection radius  
        elif (not self.Stunned and self.hp > 0):
            if self.walking and self.target != None:
                if self.target.getHP() <= 0 or self.target == None:
                    self.walking = True
                    self.target = None
                    self.aimless_walking(zombieList, mangija)
                else:
                    # Check for nearby zombies within detection radius
                    nearby_entities = [entity for entity in zombieList + [mangija] if self.distance_to_zombie(entity) <= self.detection_radius]
                    if nearby_entities:
                        # Calculate distances to each entity
                        distances = [self.distance_to_zombie(entity) for entity in nearby_entities]
                        # Choose the entity with the minimum distance
                        min_distance_entity = nearby_entities[distances.index(min(distances))]
                        self.target = min_distance_entity
                        
                    targetVector = (self.target.getPosX()-self.x, self.target.getPosY()-self.y)
                    distance = ((targetVector[0])**2+(targetVector[1])**2)**(1/2)
                    if distance <= self.target.pihtaSaamisRaadius:
                        self.walking = False
                        self.attacking = True
                        self.attackMode(zombieList, mangija)
                    else:
                        speedVector = (targetVector[0]/distance*self.kiirus, targetVector[1]/distance*self.kiirus)
                        self.setPos(self.x+speedVector[0], self.y+speedVector[1])

            elif self.attacking:
                if self.target.getHP() <= 0 or self.target == None:  # Check if target is dead or None
                    self.walking = True
                    self.attacking = False
                    self.target = None
                    self.aimless_walking(zombieList, mangija)
                else:
                    if self.slash_timer == 0:
                        self.current_slash_index = random.randint(0, len(self.sword_slash_images) - 1)  # Choose a random slash image
                    self.slash_timer += 1
                    if self.slash_timer >= self.slash_duration:
                        self.slash_timer = 0  # Reset slash timer after finishing the duration
                        self.current_slash_index = None  # Clear current slash index
                    elif self.current_slash_index is not None:
                        if self.slash_timer % self.frame_delay == 0:  # Add a delay between frames
                            self.draw_sword_slashing(surface)  # Draw current slash image
                    self.attackMode(zombieList, mangija)
            else:
                self.aimless_walking(zombieList, mangija)

            self.draw(surface)
            self.draw_health_bar(surface)
            self.draw_dot(surface)
            self.draw_detection_radius(surface)  # Draw detection radius
     
        else:
            self.onSurnud = True

    def draw_sword_slashing(self, surface):
        # Draw current sword slashing image
        surface.blit(self.sword_slash_images[self.current_slash_index], (self.target.getPosX() - self.sword_slash_images[self.current_slash_index].get_width() / 2, self.target.getPosY() - self.sword_slash_images[self.current_slash_index].get_height() / 2))

    def draw_dot(self, surface):
        pygame.draw.circle(surface, self.dot_color, (int(self.x), int(self.y)), self.dot_radius)

    def draw_detection_radius(self, surface):
        pygame.draw.circle(surface, (255, 0, 0), (int(self.x), int(self.y)), self.detection_radius, 1)

    def attackMode(self, zombieList, mangija):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time >= self.attack_delay:
            if self.target.getHP() <= 0:
                self.walking = True
                self.attacking = False
                self.target = None
                
                self.aimless_walking(zombieList, mangija)
            else:
                target_x, target_y = self.target.getPos()
                teleport_distance = 75

                random_angle = random.uniform(0, 2*math.pi)
                teleport_point_x = target_x + teleport_distance * math.cos(random_angle)
                teleport_point_y = target_y + teleport_distance * math.sin(random_angle)

                self.setPos(teleport_point_x, teleport_point_y)
                self.target.SaaViga(self.damage)
                self.last_attack_time = current_time

    def distance_to_zombie(self, zombie):
        zombie_x, zombie_y = zombie.getPos()
        return math.sqrt((self.x - zombie_x)**2 + (self.y - zombie_y)**2)

    def KasSaabPihta(self, asuk, suund):
        # Ingli asukoht
        Z = [self.x, self.y]
        # Mängija asukoht
        P = asuk
        # Mängja suund
        s = suund
        # Suuna punkt
        S = [P[0] + s[0], P[1] + s[1]]
        
        # Küsimus on, kui kaugel on ingli asukoht Z Mängija asukohaga P ja suuna punktiga S määratud sirgest.
        kaugus = abs((S[0]-P[0])*(Z[1]-P[1]) - (S[1]-P[1])*(Z[0]-P[0])) / ((S[0]-P[0])**2 + (S[1]-P[1])**2)**0.5
        

        z = [Z[0] - P[0], Z[1] - P[1]]
        # Küsimus, on kui suur on vektori s ja vektori z vaheline koosinus.
        try:
            koosinus = (s[0]*z[0] + s[1]*z[1]) / ((s[0]**2+s[1]**2)**0.5 * (z[0]**2+z[1]**2)**0.5)
        except:
            koosinus = 0


        if kaugus < self.pihtaSaamisRaadius and koosinus > 0:
            return True
        else:
            return False
        
    def LeiaKaugusMangijast(self, mangija:Mangija):
        P1 = [self.x, self.y]
        P2 = [mangija.asukx, mangija.asuky]
        V = [P2[0]-P1[0], P2[1]-P1[1]]
        l = (V[0]**2 + V[1]**2)**0.5
        return l
        
    def KasKuulKattub(self, kuul):
        pass    
    
    def SaaViga(self, kahju):
        self.hp -= kahju