import simulation
import numpy as np
import time

n_boids = 3
l_pos = [np.array([110,120]),np.array([160,170]),np.array([160,190])]
l_v = [np.array([5,5]),np.array([5,-5]),np.array([5,-5])]
l_maxv = [40]
l_maxa = [40]
l_view_range = [100]
l_view_angle = [80]
w = np.array([500,500])
b_cond = 0

n = 300

simu = simulation.Simulation(n_boids,l_pos,l_v,l_maxv,l_maxa,l_view_range,l_view_angle,w,b_cond)

for ii in range(n) :
    time.sleep(0.05)
    simu.time_step()
