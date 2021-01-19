import simulation
import numpy as np
import time
import matplotlib.pyplot as plt
rng = np.random.default_rng()

l = range(2,100,10)
dt = [0.0]*len(l)
for ii,n_boids in enumerate(l) :
    w = np.array([500,500])
    b_cond = 0
    l_pos = [rng.random(2)*w for ii in range(n_boids)]
    l_v = [rng.random(2)*3 for ii in range(n_boids)]
    l_maxv = [10]
    l_maxa = [1]
    l_view_range = [100]
    l_view_angle = [80]

    n = 100

    simu = simulation.Simulation(n_boids,l_pos,l_v,l_maxv,l_maxa,l_view_range,l_view_angle,w,b_cond)

    for jj in range(n) :
        ts = 0.05
        #time.sleep(ts)
        start = time.time()
        simu.time_step()
        end = time.time()
        dt[ii] = (end-start+ii*dt[ii])/(ii+1)
plt.plot(list(l),dt,'-x')
plt.xlabel('nbr boids')
plt.ylabel('t_moyen sur 100 pas [s]')
plt.grid()
plt.show()