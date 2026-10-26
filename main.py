import pygame
from time import sleep
from enum import Enum
import random
from pygame.sprite import Sprite, Group
import math


# Initialization & Settings
pygame.init()

WIDTH = 1200
HEIGHT = 1000
PARTICES_NUMBER = 100
background_colour = (0,0,0)
fps = 60

# Setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Partical Life')

screen.fill(background_colour)
pygame.display.flip()
clock = pygame.time.Clock()


attraction_matrix = [[0.2, 0.05, -0.1], 
                    [-0.05, 0.2, 0.03], 
                    [0.05, -0.03, 0.2]]

class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

# Points
class Particle():
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.verbose_x = 0.0
        self.verbose_y = 0.0
        self.color = random.choice(list(Color))
        self.radius = 10


    def update(self):
        if self.x <=0 + self.radius or self.x >= WIDTH - self.radius:
            self.verbose_x = self.verbose_x * -1
        if self.y <=0 + self.radius or self.y >= HEIGHT - self.radius:
            self.verbose_y = self.verbose_y * -1
        self.x += self.verbose_x
        self.y += self.verbose_y


    def attraction_math(self, other, force):
        dx = other.x - self.x
        dy = other.y - self.y

        distance = math.sqrt(dx**2 + dy**2)

        if distance == 0 or distance > 150:
            return

        force = force
        self.verbose_x += (dx / distance) * force
        self.verbose_y += (dy / distance) * force

        speed = math.sqrt(self.verbose_x**2 + self.verbose_y**2)
        max_speed = 10

        if speed > max_speed:
            self.verbose_x = (self.verbose_x / speed) * max_speed
            self.verbose_y = (self.verbose_y / speed) * max_speed


        
    def draw(self,screen):
        match self.color:
            case Color.RED:
                color = (255,0,0)
            case Color.GREEN:
                color = (0,255,0)
            case Color.BLUE:
                color = (0,0,255)
            case _:
                raise ValueError("Wrong color")
                                                
        pygame.draw.circle(screen,color,(self.x,self.y), self.radius)

 

particles = [Particle() for _ in range(PARTICES_NUMBER)]


def count_distance(a,b):
        distance = math.sqrt(pow(a.x - b.x,2) + pow(a.y-b.y,2))
        if distance < 20:
            print("KOLIZCJA")
        return distance



# Main
def main():
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        for particle in particles:
            particle.update()

        for i in range (len(particles)):
            for j in range(i+1,len(particles)):
                a = particles[i]
                b = particles[j]
                ix_a = a.color.value
                ix_b = b.color.value
                a.attraction_math(b,attraction_matrix[ix_a-1][ix_b-1])
                b.attraction_math(a,attraction_matrix[ix_b-1][ix_a-1])
                
                    
        
        screen.fill(background_colour)

        for particle in particles:
            particle.draw(screen)
        
        pygame.display.flip()
        clock.tick(fps)




main()