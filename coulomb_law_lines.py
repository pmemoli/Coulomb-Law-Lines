import pygame
import random
import numpy as np
import math
from pygame.locals import *

flags = DOUBLEBUF

# Attributes
max_flow_lifespan = 50
max_length = 70
chage_magnitude = 1
flow_lines = 200
flux_compensation = 8  # Rate at which lines disapear when approaching negative charges

class FlowLine(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Line attributes
        self.lifespan = random.randrange(max_flow_lifespan)
        self.length = random.randrange(max_length)
        self.lifetime = 0

        # Sprite attributes
        self.pos = (random.randrange(screen_width), random.randrange(screen_height))
        self.generation = 1

        self.image = pygame.Surface([screen_width, screen_height], pygame.SRCALPHA, 32).convert_alpha()

        self.points = [self.pos, self.pos]

        pygame.draw.lines(self.image, white, False, self.points, 2)

        self.rect = self.image.get_rect()

        self.flux_compensation = False


    def update(self, charges):
        # Drawing
        self.image.fill((0, 0, 0, 0))

        if self.lifespan < self.lifetime:  # Paso su esperanza de vida
            if len(self.points) > 2:
                if self.flux_compensation and len(self.points) > flux_compensation + 2:
                    for i in range(flux_compensation):
                        self.points.pop(0)
                  
                else: 
                    self.points.pop(0)

            else:
                self.lifetime = 0
                self.flux_compensation = False
                pos = (random.randrange(screen_width), random.randrange(screen_height))
                self.points = [pos, pos]

        else:  # Mientras esta viva
            self.lifetime += 1
            asymptote = False

            new_point = np.asarray(self.points[-1])
            for charge in charges:
                if charge.electric_field(self.points[-1])[0] == 0 and charge.electric_field(self.points[-1])[1] == 0:
                    if charge.charge < 0:
                        asymptote = True
                        self.flux_compensation = True

                    else:
                        asymptote = True                        

                else:
                    new_point = new_point + charge.electric_field(self.points[-1]) / fps  # Euler's method

            if asymptote:
                self.lifetime = self.lifespan + 1

            else:
                self.points.append(new_point)

                if len(self.points) > self.length:
                    self.points.pop(0)

        pygame.draw.lines(self.image, white, False, self.points, 1)

        self.rect = self.image.get_rect()


class Charge(pygame.sprite.Sprite):
    def __init__(self, charge, position):
        super().__init__()

        self.charge = charge
        self.position = position

        radius = 5
        self.image = pygame.Surface([radius * 2, radius * 2], pygame.SRCALPHA, 32).convert_alpha()

        if charge >= 0:
            color = white
        else: 
            color = gray

        pygame.draw.circle(self.image, color, (radius, radius), radius)

        self.rect = self.image.get_rect()
        self.rect.center = position

    def electric_field(self, location):  # Returns the electric field the charge itself produces
        center_prop = (self.position[0] - screen_width / 2, -self.position[1] + screen_height / 2)
        x_prop = location[0] - screen_width / 2
        y_prop = - location[1] + screen_height / 2

        constant = 20000  # Arbitrary constant to make the lines more visible
        distance = np.linalg.norm(np.asarray(self.position) - np.asarray(location))
        direction = np.asarray(center_prop) - np.asarray([x_prop, y_prop])
        if distance < 50 and self.charge < 0:
            coulomb_speed = 0
            direction = np.asarray([0, 0])
        elif distance < 8:
            coulomb_speed = 0
            direction = np.asarray([0, 0])
        else:
            coulomb_speed = - constant * self.charge / (distance)
            direction /= distance

        return coulomb_speed * np.asarray([direction[0], -direction[1]])


class Simulation:
    def __init__(self):
        for i in range(flow_lines):
            flow_group.add(FlowLine())

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.MOUSEBUTTONDOWN:  # To set charges
                    if event.button == 1: # Sets positive charge
                        charge_group.add(Charge(chage_magnitude, pygame.mouse.get_pos()))

                    elif event.button == 3: # Sets negative charge
                        charge_group.add(Charge(-chage_magnitude, pygame.mouse.get_pos()))

                elif event.type == pygame.KEYDOWN:  # To adjust parameters
                    if event.key == pygame.K_BACKSPACE:  # Deletes charge
                        if len(charge_group) > 0:
                            charge_group.remove(charge_group.sprites()[-1])

            # Draws elements
            screen.fill(black)
            flow_group.draw(screen)
            flow_group.update(charge_group)
            charge_group.draw(screen)
            charge_group.update()

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
charge_group = pygame.sprite.Group()
flow_group = pygame.sprite.Group()

simulation = Simulation()

simulation.run()
