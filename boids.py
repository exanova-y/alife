import numpy as np

class Boids:
    def __init__(self, num_boids=128, width=500, height=500): # width, height of matplotlib window
        self.num_boids = num_boids
        self.width = width
        self.height = height
        self.positions = np.random.rand(num_boids, 2) * np.array([width, height]) # create a matrix of num_boids by 2 between 0 and 1, scales it to the width and height
        self.velocities = np.random.rand(num_boids, 2) * 2 - 1 # matrix of num_boids by 2 (to get 0, 2) minus 1 to get (-1, 1)

    def update(self):
        # Simple flocking rules: cohesion, alignment, and separation
        cohesion_strength = 0.01
        alignment_strength = 0.05
        separation_strength = 0.1

        # Cohesion: Move towards the center of mass
        center_of_mass = np.mean(self.positions, axis=0)
        cohesion = (center_of_mass - self.positions) * cohesion_strength

        # Alignment: Align with the average velocity of neighbors
        average_velocity = np.mean(self.velocities, axis=0)
        alignment = (average_velocity - self.velocities) * alignment_strength

        # Separation: Avoid crowding neighbors
        separation = np.zeros_like(self.positions) #[x, y]
        for i in range(self.num_boids): # for each other boid, calculate distance
            distances = np.linalg.norm(self.positions[i] - self.positions, axis=1)
            too_close = distances < 25 # assigns boolean array length num_boids.
            too_close[i] = False  # ignore itself in the array.
            if np.any(too_close): # if itself is too close to any other boid, then we update 'separation force' by reverse distance
                separation[i] = -np.mean(self.positions[too_close] - self.positions[i], axis=0) * separation_strength

        # velocity updates by three factors: cohesion, alignment, and separation
        self.velocities += cohesion + alignment + separation
        self.positions += self.velocities

        # Wrap around the edges of the screen
        self.positions %= np.array([self.width, self.height])

    def render(self):
        # Render the boids as points on a 2D plane
        import matplotlib.pyplot as plt
        plt.scatter(self.positions[:, 0], self.positions[:, 1], s=10)
        plt.xlim(0, self.width)
        plt.ylim(0, self.height)
        plt.show()
        # replace with manim code later.