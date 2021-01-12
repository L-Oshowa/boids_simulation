import Interface_Graphique as UI
import time
import boids
import numpy as np

# Temporary: initialise boids
posX = [110, 200, 400]
posY = [120, 150, 250]
speedX = [10, 10, -20]
speedY = [10, 0, -30]

b1 = boids.Boids(np.array([110, 120]), np.array([10, 10]), 0, 0, 0, 0)
b2 = boids.Boids(np.array([200, 150]), np.array([10, 0]), 0, 0, 0, 0)
b3 = boids.Boids(np.array([400, 250]), np.array([-30, -20]), 0, 0, 0, 0)

list_boids = [b1, b2, b3]

# Create the window
window = UI.MainFrame(list_boids, 500, 500)


for y in range(20):
    time.sleep(0.1)
    # Temporary: to evolve the boids
    pos1 = []
    pos2 = []
    s1 = []
    s2 = []
    for x in range(len(posX)):
        pos1.append(posX[x] + (y+1) * speedX[x])
        pos2.append(posY[x] + (y+1) * speedY[x])
        s1.append(speedX[x])
        s2.append(speedY[x])

    window.boid_window.update(pos1, pos2, s1, s2)  # Update the position of the boids

b1.steering([b2, b3])
