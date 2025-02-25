import numpy as np
import pygame
import random

range_directions = [0, 360]

class Boid:
    def __init__(self, id, width, height): # width, height of matplotlib window
        self.id = id
        self.direction = random.uniform(np.radians(range_directions[0]), np.radians(range_directions[1])) # use the defined range
        self.position = np.array([random.uniform(20, width-20), random.uniform(20, height-20)])
        # Make velocity a 2D vector to match position
        self.velocity = np.array([np.cos(self.direction), np.sin(self.direction)])
        
        self.cumulative_acceleration = np.array([0, 0])
        self.cohere_acceleration = np.array([0, 0])
        self.separate_acceleration = np.array([0, 0])
        self.align_acceleration = np.array([0, 0])

        self.polygon = np.array([(20, 0), (0, 5), (0, -5)])
        self.color = (255, 255, 255) # white, change colours based on time later.
        
        self.width = width
        self.height = height

    def update(self):
        # Update method is now handled by BoidFlock class
        # This is just for individual updates if needed
        
        # Wrap around the edges of the screen
        self.cohere()
        self.separate()
        self.align()
        self.position += self.velocity
        self.position[0] = self.position[0] % self.width
        self.position[1] = self.position[1] % self.height

    # def cohere(self):

    # def separate(self):

    # def align(self):
    

    def render(self, screen):
        # Render the boid as a triangle
        rotation_matrix = np.array([[np.cos(self.direction), -np.sin(self.direction)], [np.sin(self.direction), np.cos(self.direction)]])
        rotated_polygon = np.dot(self.polygon, rotation_matrix.T) + self.position
        pygame.draw.polygon(screen, self.color, rotated_polygon.astype(int), 0)
