import pygame
import random
import numpy as np
from Boid import Boid

def main():
    pygame.init()
    # Set up the display
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Boids flocking")

    # Create the boid flock
    num_boids = 50
    boid_list = []
    for i in range(num_boids):
        b = Boid(i, width, height)
        boid_list.append(b)

    clock = pygame.time.Clock()
    fps = 60
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        for boid in boid_list:
            boid.update()

        screen.fill((0, 0, 0))  # Black background
        for boid in boid_list:
            boid.render(screen)
            
        pygame.display.flip()
        clock.tick(fps)


if __name__ == "__main__":
    main()
                
    