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
PARTICES_NUMBER = 50
RANGE = 300
RADIUS = 30
background_colour = (0,0,0)
fps = 60
font = pygame.font.SysFont("Arial", 40)

# Setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Partical Life')

screen.fill(background_colour)
pygame.display.flip()
clock = pygame.time.Clock()

MATRIX_ROW = 3
MATRIX_COL = 3


attraction_matrix = [[0.5, 0.5, 0.5], 
                    [0.5, 0.5, 0.5], 
                    [0.5, 0.5, 0.5]]

# attraction_matrix = [[0.2, 0.05, -0.1], 
#                     [-0.05, 0.2, 0.03], 
#                     [0.1, -0.03, 0.2]]

class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

STATE_MENU = "menu"
STATE_GAME = "game"


# Points
class Particle():
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.verbose_x = 0.0
        self.verbose_y = 0.0
        self.color = random.choice(list(Color))
        self.radius = RADIUS


    def update(self):
        if self.x <= self.radius:
            self.x = self.radius
            self.verbose_x = abs(self.verbose_x)

        elif self.x >= WIDTH - self.radius:
            self.x = WIDTH - self.radius
            self.verbose_x = -abs(self.verbose_x)

        if self.y <= self.radius:
            self.y = self.radius
            self.verbose_y = abs(self.verbose_y)

        elif self.y >= HEIGHT - self.radius:
            self.y = HEIGHT - self.radius
            self.verbose_y = -abs(self.verbose_y)

        self.x += self.verbose_x
        self.y += self.verbose_y


    def attraction_math(self, other, force):
        dx = other.x - self.x
        dy = other.y - self.y

        distance = math.sqrt(dx**2 + dy**2)

        if distance == 0 or distance > RANGE:
            return

        force = force
        self.verbose_x += (dx / distance) * force
        self.verbose_y += (dy / distance) * force

        speed = math.sqrt(self.verbose_x**2 + self.verbose_y**2)
        max_speed = 10

        if speed > max_speed:
            self.verbose_x = (self.verbose_x / speed) * max_speed
            self.verbose_y = (self.verbose_y / speed) * max_speed

    def resolve_overlap(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        distance = math.sqrt(dx**2 + dy**2)

        if distance == 0 :
            return

        if distance < self.radius + other.radius:
            overlap = self.radius + other.radius - distance
            nx = dx/distance
            ny = dy/distance
            self.x -= nx * (overlap / 2)
            self.y -= ny * (overlap / 2)
            other.x += nx * (overlap / 2)
            other.y += ny * (overlap / 2)



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

# TO DO:
# detect colision
# rozdzielci nachodzace na sibie kulki - przesuniecie ich o d sibie wzdluz lni laczecej srodki
# zmiana preskosci
def reset_simulation():
    global particles
    particles = [Particle() for _ in range(PARTICES_NUMBER)]

def randomize_matrix():
    global attraction_matrix
    for i in range(MATRIX_ROW):
        for j in range(MATRIX_COL):
            attraction_matrix[i][j] = random.randint(-100,100)/ 100


def draw_text(text, font, color, surface, x, y):
    """Draw text in center """
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)

# Main
def main():
    current_state = STATE_GAME
    running = True

    while running:
        screen.fill(background_colour)
        if current_state == STATE_GAME:

            # Menu section
            play_button = pygame.Rect(
                WIDTH * 0.95 - 150, 0.05 * HEIGHT, 200, 50
            )
            pygame.draw.rect(screen, (255,255,255), play_button)
            draw_text(
                "PAUSE", font, (0,0,0), screen, play_button.centerx, play_button.centery
            ) 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = event.pos
                        if play_button.collidepoint(mouse_pos):
                            current_state = STATE_MENU
                

                
                
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
                    a.resolve_overlap(b)

                        
                            
                
            

            for particle in particles:
                particle.draw(screen)
        elif current_state == STATE_MENU:
            # Menu section
            play_button = pygame.Rect(
                WIDTH * 0.95 - 150, 0.05 * HEIGHT, 200, 50
            )
            reset_button = pygame.Rect(
                WIDTH * 0.95 - 150, 0.05 * HEIGHT + 100, 200, 50
            )
            randomize_matrix_button = pygame.Rect(
                WIDTH * 0.95 - 250, 0.05 * HEIGHT + 200, 300, 50
            )
            pygame.draw.rect(screen, (255,255,255), play_button)
            pygame.draw.rect(screen, (255,255,255), reset_button)
            pygame.draw.rect(screen, (255,255,255), randomize_matrix_button)
            draw_text(
                "PLAY", font, (0,0,0), screen, play_button.centerx, play_button.centery
            )
            draw_text(
                "RESET", font, (0,0,0), screen, reset_button.centerx, reset_button.centery
            )
            draw_text(
                "ROLL THE DICE", font, (0,0,0), screen, randomize_matrix_button.centerx, randomize_matrix_button.centery
            )

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = event.pos
                        if play_button.collidepoint(mouse_pos):
                            current_state = STATE_GAME
                        if reset_button.collidepoint(mouse_pos):
                            reset_simulation()
                            print("RESET GAME")
                            current_state = STATE_GAME

                        if randomize_matrix_button.collidepoint(mouse_pos):
                            randomize_matrix()
                            reset_simulation()
                            print("NEW MATRIX:", attraction_matrix)
                            current_state = STATE_GAME

        pygame.display.flip()
        clock.tick(fps)




main()