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
'''
pos_temp = []
v_temp = []
for ix,x in enumerate(simu.l_boids) :
    y_temp = []
    for iy,y in enumerate(simu.l_boids) :
        if iy!=ix and simu.my_world.isinrange(x,y) :
            y_temp.append(y)
    temp = x.steering(y)
    temp = simu.my_world.position(temp[0],temp[1])
    pos_temp.append(temp[0])
    v_temp.append(temp[1])
for x,y,z in zip(simu.l_boids, pos_temp, v_temp) : x.update(y,z)
input('please press a key')
simu.window.boid_window.update([x.pos[0] for x in simu.l_boids], [x.pos[1] for x in simu.l_boids], [x.v[0] for x in simu.l_boids], [x.v[1] for x in simu.l_boids]) #graphic update
input('please press a key')
'''
