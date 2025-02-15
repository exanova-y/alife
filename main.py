from boids import Boids

if __name__ == '__main__':
    flock = Boids()
    steps = 100
    for i in range(steps):
        flock.update()
        flock.render()
    