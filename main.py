import simulation
import numpy as np
import time
import matplotlib.pyplot as plt
rng = np.random.default_rng()

l = range(2,123,40) #number of boids
L = range(1,12,1) # number of binn
dt = [[0.0 for i in l] for j in L]
dataname = 'output.txt'
f = open(dataname,'w')
f.write('n_boids n_binn dt[s] \n')
f.close()
for ll,n_binn in enumerate(L) :
    for ii,n_boids in enumerate(l) :
        w = np.array([500,500])
        b_cond = 0
        l_pos = [rng.random(2)*w for ii in range(n_boids)]
        l_v = [(rng.random(2)-0.5)*3 for ii in range(n_boids)]
        l_maxv = [10]
        l_maxa = [1]
        l_view_range = [60]
        l_view_angle = [120]
        l_n_binn = [n_binn]
        n = 100

        simu = simulation.Simulation(n_boids,l_pos,l_v,l_maxv,l_maxa,l_view_range,l_view_angle,w,b_cond,l_n_binn)

        for jj in range(n) :
            ts = 0.05
            start = time.time()
            simu.time_step()
            end = time.time()
            dt[ll][ii] = (end-start+jj*dt[ll][ii])/(jj+1)
            #time.sleep(max(0,ts+start-end))
        simu.window.root.destroy()
        
        print('n_boids :'+str(ii+1)+'/'+str(len(l))+'\nn_binn :'+str(ll+1)+'/'+str(len(L))+'\ndt :'+str(dt[ll][ii]))
        f = open(dataname,'a')
        f.write(str(n_boids)+' '+str(n_binn)+' '+str(dt[ll][ii])+'\n')
        f.close()

for ll,n_binn in enumerate(L) :
    plt.plot(list(l),dt[ll],'-x',label = 'n_binn='+str(n_binn))
plt.xlabel('nbr boids')
plt.ylabel('t_moyen sur 100 pas [s]')
plt.legend()
plt.grid()
plt.show()

'''
n_boids = 2
w = np.array([500,500])
b_cond = 0
l_pos = [np.array([100,100]),np.array([100,150])]
l_v = [np.array([1,0]),np.array([0,1])]
l_maxv = [1]
l_maxa = [0.1]
l_view_range = [100]
l_view_angle = [120]
n_binn = [100]
n = 100

simu = simulation.Simulation(n_boids,l_pos,l_v,l_maxv,l_maxa,l_view_range,l_view_angle,w,b_cond,n_binn)

for jj in range(n) :
    ts = 0.02
    start = time.time()
    simu.time_step()
    end = time.time()
    time.sleep(max(0,ts+start-end))
 '''