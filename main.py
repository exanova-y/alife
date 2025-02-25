import pygame
import random
import numpy as np

from .clip import CLIP
from .Boid import Boid

p_of_cohere = 0.1
r_of_cohere = 150
p_of_align = 0.1
r_of_align = 50

def create_fm(fm_name):
    if fm_name == "clip":
        fm = CLIP()
    return fm

def distance_between_vectors(vectors):
    '''calculate pairwise distance between vectors, returns
    a 2d list'''
    vector_num = len(vectors)
    distance_list = [[0] * vector_num for _ in range(vector_num)]
    for i in range(vector_num):
        distance_list[i][i] = (0, i)
        for j in range(vector_num):
            if i < j:
                # Calculate the distance between two vectors.
                distance = np.linalg.norm(np.subtract(vectors[i], vectors[j]))
                # Store the calculated distance at index i,j.
                distance_list[i][j] = (distance, j)
                distance_list[j][i] = (distance, i)
    return distance_list

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


    sample_prompts = ["a flock of boids", "boids circling"]
    prompt = sample_prompts[1]
    fm = create_fm("clip")
    z_txt = fm.embed_txt(sample_prompts)
    # to be continued
    # 1. Embeds each text prompt
    # 2. Runs the simulation and captures images at multiple time steps
    # 3. Compares each image embedding to the corresponding text embedding
    # 4. Optimizes the boid parameters to make the simulation evolve through states that match each prompt in sequence

    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # Calculate distances between all boids
        dlist = distance_between_vectors([boid.position for boid in boid_list])
        # Update each boid, passing the full boid list for separation calculations
        for boid in boid_list:
            boid.update(dlist, p_of_cohere, r_of_cohere, p_of_align, r_of_align, boid_list)

        screen.fill((0, 0, 0))  # Black background
        for boid in boid_list:
            boid.render(screen)

        pygame.display.flip()
        clock.tick(fps)




if __name__ == "__main__":
    main()
