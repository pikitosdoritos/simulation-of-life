import pygame
import random
import time
import math

WIDTH = 800
HEIGHT = 600

class Entity:
    def __init__(self):
        self.x = random.randint(50, WIDTH - 50)
        self.y = random.randint(50, HEIGHT - 50)
        self.speed = random.randint(1, 5)
        self.direction = random.random() * (2 * math.pi)
        self.color = (0, 255, 0)
        self.radius = 10

    def move(self):
        self.x += self.speed * math.cos(self.direction)
        self.y += self.speed * math.sin(self.direction)
        self.direction += random.uniform(-0.1, 0.1)
        self.speed += random.uniform(-0.1, 0.1)
        
        self.normalize() 

    def normalize(self):
        if self.x + self.radius > WIDTH:
            self.x = WIDTH - self.radius
            self.direction = math.pi - self.direction
        
        elif self.x - self.radius < 0:
            self.x = self.radius
            self.direction = math.pi - self.direction
            
        if self.y + self.radius > HEIGHT:
            self.y = HEIGHT - self.radius
            self.direction = 2 * math.pi - self.direction
            
        elif self.y - self.radius < 0:
            self.y = self.radius 
            self.direction = 2 * math.pi - self.direction  
            
    def bounce(self, other):
        collision_angle = math.atan2(other.y - self.y, other.x - self.x)

        self.direction = 2 * collision_angle - self.direction + math.pi
        other.direction = 2 * collision_angle - other.direction + math.pi
            
    def does_overlap(self, other):
        hypot = math.hypot(self.x - other.x, self.y - other.y)
        return hypot < self.radius + other.radius       
    
    def find_closest(self, entities):
        closest = None
        min_dist = math.inf
        
        for entity in entities:
            hypot = math.hypot(self.x - entity.x, self.y - entity.y)
            
            if hypot < min_dist:
                min_dist = hypot
                closest = entity
                
        return closest
            
    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        
class Food(Entity):
    def __init__(self):
        super().__init__()
        self.color = (0, 255, 0)
        self.radius = 3
        self.speed = 0.5
        
class Predator(Entity):
    def __init__(self):
        super().__init__()
        self.color = (255, 0, 0)
        self.radius = 10
        
    def hunt(self):
        target = self.find_closest(food_list)
        
        if target is None:
            return
        
        self.direction = math.atan2(target.y - self.y, target.x - self.x)
        self.move()
        
        if self.does_overlap(target):
            food_list.remove(target)   

pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill((0, 0, 0))

i = 0

predators = [Predator() for _ in range(3)]

food_list = [Food() for _ in range(10)]

def fix_overlaping(entities):
    pairs = []
    j = 0
    
    while j < len(entities) - 1:
        k = j + 1
        ent1 = entities[j]
        
        while k < len(entities):
            ent2 = entities[k]
        
            if ent1.does_overlap(ent2):
                pairs.append((ent1, ent2))
                
            k += 1

        j += 1
        
    for pair in pairs:
        pair[0].bounce(pair[1])
        
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
            
    screen.fill((0, 0, 0))
    
    for predator in predators:
        predator.draw()
        predator.hunt()
        
    for food in food_list:
        food.draw()
        food.move()
        
    fix_overlaping(predators)
    
    i += 1
     
    clock.tick(60)
    
    pygame.display.flip()