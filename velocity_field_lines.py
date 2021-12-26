import pygame
import random
import numpy as np
import math
from pygame.locals import *

flags = DOUBLEBUF

def vector_field(x, y):  # Velocity field goes here
    # Takes pygame coordinates to the cartesian plane
    x_prop = x - screen_width / 2
    y_prop = - y + screen_height / 2

    return np.asarray([x_prop, y_prop])


class FlowLine(pygame.sprite.Sprite):
    def __init__(self, x_pos=-1, y_pos=-1):
        super().__init__()

        # Line attributes
        self.lifespan = random.randrange(40)
        self.length = random.randrange(30)
        self.lifetime = 0

        # Sprite attributes
        if x_pos == -1 and y_pos == -1:
            self.pos = (random.randrange(screen_width), random.randrange(screen_height))
            self.generation = 1
        else:
            self.pos = (x_pos, y_pos)
            self.generation = 0

        self.image = pygame.Surface([screen_width, screen_height], pygame.SRCALPHA, 32).convert_alpha()

        self.points = [self.pos, self.pos]

        pygame.draw.lines(self.image, white, False, self.points, 2)

        self.rect = self.image.get_rect()


    def update(self):
        # Drawing
        self.image.fill((0, 0, 0, 0))

        if self.lifespan < self.lifetime:  # Paso su esperanza de vida
            
            if self.generation == 0:
                if len(self.points) > 2:
                    self.points.pop(0)

                else:
                    self.lifetime = 0
                    self.points = [self.pos, self.pos]

            elif self.generation == 1:
                if len(self.points) > 2:
                    self.points.pop(0)

                else:
                    self.lifetime = 0
                    pos = (random.randrange(screen_width), random.randrange(screen_height))
                    self.points = [pos, pos]

        else: 
            self.lifetime += 1

            new_point = tuple(np.asarray(self.points[-1]) + vector_field(self.points[-1][0], self.points[-1][1]) / fps)
            self.points.append(new_point)

            if len(self.points) > self.length:
                self.points.pop(0)

        pygame.draw.lines(self.image, white, False, self.points, 1)

        self.rect = self.image.get_rect()


class Simulation:
    def __init__(self, generation):
        # Crea size^2 puntos equiespaciados sobre la pantalla
        if generation == 0:
            size = 10
            for i in range(size + 1):
                for j in range(size + 1):
                    flow_group.add(FlowLine(i * screen_width / size, j * screen_height / size))

        elif generation == 1:
            for i in range(100):
                flow_group.add(FlowLine())

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                        
            # Draws elements
            screen.fill(black)
            flow_group.draw(screen)
            flow_group.update()

            pygame.display.update()
            clock.tick(60)            


# General Setup
pygame.init()
pygame.font.init()
clock = pygame.time.Clock()

# Game screen
screen_width = 500
screen_height = 500
screen = pygame.display.set_mode((screen_width, screen_height), flags)
screen.set_alpha(None)

# Images and variables
black = (0, 0, 0)
white = (255, 255, 255)
gray = (93, 93, 93)

fps = 60

# Objects
particle_group = pygame.sprite.Group()
flow_group = pygame.sprite.Group()

simulation = Simulation(1)

simulation.run()
