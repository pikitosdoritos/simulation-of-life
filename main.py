import pygame
import random
import time
import math

WIDTH = 800
HEIGHT = 600

game_over = False

class Entity:
    def __init__(self, x=None, y=None, speed=None, direction=None, color=None, radius=None):
        self.x = x if x is not None else random.randint(50, WIDTH - 50)
        self.y = y if y is not None else random.randint(50, HEIGHT - 50)
        self.speed = speed if speed is not None else random.randint(1, 5)
        self.direction = direction if direction is not None else random.random() * (2 * math.pi)
        self.color = color if color is not None else (0, 255, 0)
        self.radius = radius if radius is not None else 10

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
        
class Prey(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.color = kwargs.get("color", (0, 255, 0))
        self.radius = kwargs.get("radius", 3)
        self.speed = kwargs.get("speed", 0.5)
        
    def reproduce(self):
        return Prey(x=self.x, y=self.y, speed=self.speed, direction=self.direction, color=self.color, radius=self.radius)
    
class Predator(Entity):
    def __init__(self, **kwargs):
        super().__init__()
        self.color = kwargs.get("color", (255, 0, 0))
        self.radius = kwargs.get("radius", 10)
        
    def hunt(self):
        target = self.find_closest(food_list)
        
        if target is None:
            return
        
        self.direction = math.atan2(target.y - self.y, target.x - self.x)
        self.move()
        
        if self.does_overlap(target):
            food_list.remove(target)
            self.radius += 0.5
            self.speed += 0.01   

pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.Font("fonts/Audiowide-Regular.ttf", 48)
but_font = pygame.font.Font("fonts/Audiowide-Regular.ttf", 28)

screen.fill((0, 0, 0))

predators = [Predator() for _ in range(3)]

reproduce_coef = 18 

food_list = [Prey() for _ in range(10)]

def draw_game_over():
    text = font.render("GAME OVER", True, (255, 0, 0))
    button_text = but_font.render("RESTART", True, (0, 0, 0))

    text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2 - 80))
    
    button_rect = pygame.Rect(0, 0, 220, 60)
    button_rect.center = (WIDTH//2, HEIGHT//2 + 40)

    # hover эффект
    mouse_pos = pygame.mouse.get_pos()
    if button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, (200, 200, 200), button_rect)
    else:
        pygame.draw.rect(screen, (150, 150, 150), button_rect)

    pygame.draw.rect(screen, (255, 255, 255), button_rect, 2)

    text_button_rect = button_text.get_rect(center=button_rect.center)

    screen.blit(text, text_rect)
    screen.blit(button_text, text_button_rect)

    return button_rect

def restart():
    global predators, food_list, game_over
    
    predators = [Predator() for _ in range(3)]
    food_list = [Prey() for _ in range(10)] 
    game_over = False


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
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_over:
                if restart_button.collidepoint(event.pos):
                    restart()
    screen.fill((0, 0, 0))
    
    if not game_over:
        for predator in predators:
            predator.draw()
            predator.hunt()
            
        for food in food_list:
            food.draw()
            food.move()
            
            if not random.randint(0, len(food_list) * reproduce_coef):
                food_list.append(food.reproduce())

        fix_overlaping(predators)
        
        if len(food_list) == 0:
            game_over = True
            
    else:
        restart_button = draw_game_over()
        
    pygame.display.flip()
    clock.tick(60)