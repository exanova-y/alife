import numpy as np
import pygame
import random

range_directions = [0, 360]

class Boid:
    def __init__(self, id, width, height, max_speed=2.0): # width, height of matplotlib window
        self.id = id
        self.direction = random.uniform(np.radians(range_directions[0]), np.radians(range_directions[1])) # use the defined range
        self.position = np.array([random.uniform(20, width-20), random.uniform(20, height-20)])
        self.velocity = np.array([np.cos(self.direction), np.sin(self.direction), random.uniform(-1, 1)])
        self.max_speed = max_speed
        
        self.cumulative_acceleration = np.array([0, 0])
        self.cohere_acceleration = np.array([0, 0])
        self.separate_acceleration = np.array([0, 0])
        self.align_acceleration = np.array([0, 0])

        self.polygon = np.array([(20, 0), (0, 5), (0, -5)])
        self.color = (255, 255, 255) # white, change colours based on time later.
        
        self.width = width
        self.height = height

    def separate(self, boids, separation_radius=25, separation_strength=0.05):
        """
        Apply separation rule - avoid crowding neighbors
        """
        separation_force = np.zeros(2)
        too_close_count = 0
        
        for other_boid in boids:
            if self.id != other_boid.id:
                # Calculate distance between this boid and other boid
                distance = np.linalg.norm(self.position - other_boid.position)
                
                if distance < separation_radius:
                    # Calculate direction away from neighbor
                    diff = self.position - other_boid.position
                    # Normalize and weight by distance (closer boids have stronger effect)
                    if distance > 0:  # Avoid division by zero
                        diff = diff / distance
                    separation_force += diff
                    too_close_count += 1
        
        # Apply separation force if there are neighbors too close
        if too_close_count > 0:
            separation_force = separation_force / too_close_count
            # Scale to desired magnitude
            if np.linalg.norm(separation_force) > 0:
                separation_force = separation_force / np.linalg.norm(separation_force)
            separation_force *= separation_strength
            
            # Store separation acceleration for reference
            self.separate_acceleration = separation_force
            
            # Apply separation force to velocity (only to x and y components)
            self.velocity[0] += separation_force[0]
            self.velocity[1] += separation_force[1]
    
    
    def cohere(self, boid_list, distance_l, power, radius):
        # Extract nearby flock
        near_boid_ids = [
            d[1] for d in distance_l[self.id] 
            if 0 < d[0] < radius and boid_list[d[1]].color == self.color]
        if len(near_boid_ids) > 0:
            near_boid = [boid_list[boid_id] for boid_id in near_boid_ids]
            # Center of gravity vector of nearby flock
            center_of_near = np.mean(np.array([boid.position for boid in near_boid]))
            # Difference between self and center of gravity vector of the flock
            vector = np.subtract(center_of_near, self.position)
            # Calculate acceleration towards the center of gravity vector of the flock
            if np.linalg.norm(vector) > 0:  # Avoid division by zero
                self.cohere_acceleration = power * (vector/np.linalg.norm(vector))
                # Apply cohesion force to velocity (only to x and y components)
                self.velocity[0] += self.cohere_acceleration[0]
                self.velocity[1] += self.cohere_acceleration[1]
            else:
                self.cohere_acceleration = np.array([0, 0])
        else:
            self.cohere_acceleration = np.array([0, 0])

    def align(self, boid_list, distance_l, power, radius):
        # Extract nearby flock
        near_boid_ids = [
            d[1] for d in distance_l[self.id] 
            if 0 < d[0] < radius and boid_list[d[1]].color == self.color]
        if len(near_boid_ids) > 0:
            near_boid = [boid_list[boid_id] for boid_id in near_boid_ids]
            # Determine the direction of the flock
            vector = np.sum([boid.velocity[:2] for boid in near_boid], axis=0)  # Only use x,y components
            # Calculate acceleration to align with the flock's direction
            if np.linalg.norm(vector) > 0:  # Avoid division by zero
                self.align_acceleration = power * (vector/np.linalg.norm(vector))
                # Apply alignment force to velocity (only to x and y components)
                self.velocity[0] += self.align_acceleration[0]
                self.velocity[1] += self.align_acceleration[1]
            else:
                self.align_acceleration = np.array([0, 0])
        else:
            self.align_acceleration = np.array([0, 0])


    def limit_speed(self):
        """
        Limit the speed of the boid to max_speed
        """
        speed = np.linalg.norm(self.velocity[:5])
        if speed > self.max_speed:
            # Scale velocity to max_speed
            self.velocity[0] = (self.velocity[0] / speed) * self.max_speed
            self.velocity[1] = (self.velocity[1] / speed) * self.max_speed
    
    def update(self, distance_list, power_of_cohere, radius_of_cohere, power_of_align, radius_of_align, boids=None):
        """
        Update boid position and orientation
        If boids list is provided, apply separation rule
        """
        # Apply separation rule if boids list is provided
        if boids is not None:
            self.separate(boids)
            self.cohere(boids, distance_list, power_of_cohere, radius_of_cohere)
            self.align(boids, distance_list, power_of_align, radius_of_align)
        
        # Limit speed before updating position
        self.limit_speed()
        
        # Update position using only the x and y components of velocity
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]
        
        # Wrap around the edges of the screen
        self.position[0] = self.position[0] % self.width
        self.position[1] = self.position[1] % self.height
        
        # Update direction based on velocity
        if np.linalg.norm(self.velocity[:2]) > 0:
            self.direction = np.arctan2(self.velocity[1], self.velocity[0])


    def render(self, screen):
        # Render the boid as a triangle
        rotation_matrix = np.array([[np.cos(self.direction), -np.sin(self.direction)], [np.sin(self.direction), np.cos(self.direction)]])
        rotated_polygon = np.dot(self.polygon, rotation_matrix.T) + self.position
        pygame.draw.polygon(screen, self.color, rotated_polygon.astype(int), 0)
