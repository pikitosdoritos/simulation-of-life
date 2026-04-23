import pygame
import random
import time

WIDTH = 800
HEIGHT = 600

class Entity:
    def __init__(self):
        self.x = random.randint(50, WIDTH - 50)
        self.y = random.randint(50, HEIGHT - 50)
        self.color = (0, 255, 0)
        self.radius = 10

    def move(self):
        if self.x + self.radius < WIDTH or self.y + self.radius < HEIGHT:
            self.x += random.randint(-2, 2)
            self.y += random.randint(-2, 2)
        else:
            self.x

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
    
    # time.sleep(0.25)
        