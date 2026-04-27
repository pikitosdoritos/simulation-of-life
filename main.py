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
        
        if self.x + self.radius > WIDTH:
            self.x = WIDTH - self.radius
        
        elif self.x - self.radius < 0:
            self.x = self.radius
            
        if self.y + self.radius > HEIGHT:
            self.y = HEIGHT - self.radius
            
        elif self.y - self.radius < 0:
            self.y = self.radius        

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)


pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill((0, 0, 0))

i = 0

entities = [Entity() for _ in range(10)]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
            
    screen.fill((0, 0, 0))
    
    for entity in entities:
        entity.draw()
        entity.move()
    
    i += 1
     
    clock.tick(60)
    
    pygame.display.flip()   
    
    time.sleep(0.25)
        