import numpy as np
import boids
import world
import Interface_Graphique as ui

class Simulation :
    def det_in(self,in_list,ii) :  #check if in_list is of length 1 or <= ii in the first case, returne 1, in the second, return ii. if ii>len(in_list) return the last element of the liste and print a message
        if ii < len(in_list) :
            return ii
        elif len(in_list)==1:
            return 0
        else :
            print('not enough argument for the initialisation of the boids')
            return len(in_list)-1 
    def __init__(self,n_boids,l_pos,l_v,l_maxv,l_maxa,l_view_range,l_view_angle,w,b_cond):

        if not b_cond==0 :
            print('border condition WIP')

        #------------------------------------#
        if b_cond == 2: # if the border_cond is black hole, make an "real windows" with a size = to normal size + twice the biggest boids range.
            self.real_w = w+2*max(l_view_range)
        elif b_cond == 1:
            if max(l_view_range) >= min(w) :
                print('view range to big for the simulation with b_cond = 1')
        #------------------------------------#

        self.my_world = world.World(w,b_cond)
        self.l_boids = [boids.Boids(l_pos[self.det_in(l_pos,ii)]+max(l_view_range)*(b_cond==2), \
                l_v[self.det_in(l_v,ii)], \
                l_maxv[self.det_in(l_maxv,ii)], \
                l_maxa[self.det_in(l_maxa,ii)], \
                l_view_range[self.det_in(l_view_range,ii)], \
                l_view_angle[self.det_in(l_view_angle,ii)]) for ii in range(n_boids)]   
        self.window = ui.MainFrame([x.pos[0] for x in self.l_boids], [x.pos[1] for x in self.l_boids], \
             [x.v[0] for x in self.l_boids], [x.v[1] for x in self.l_boids], self.my_world.w[0], self.my_world.w[1])  #creation of the UI          
    def time_step (self) : #can bug is only one boids
        pos_temp = []
        v_temp = []
        for ix,x in enumerate(self.l_boids) :
            y_temp = []
            for iy,y in enumerate(self.l_boids) :
                if iy!=ix and self.my_world.isinrange(x,y) :
                    y_temp.append(y)
            temp = x.steering(y)
            temp = self.my_world.position(temp[0],temp[1])
            pos_temp.append(temp[0])
            v_temp.append(temp[1])
        '''
        pos_temp,v_temp = [x.steering(\
                            [y for iy,y in enumerate(self.l_boids) if self.my_world.isinrange(x,y) and iy!=ix]\
                            ) for ix,x in enumerate(self.l_boids)]
        pos_temp,v_temp = [self.my_world.position(x,y) for x,y in zip(pos_temp,v_temp)]
        '''
        for x,y,z in zip(self.l_boids, pos_temp, v_temp) : x.update(y,z)
        self.window.boid_window.update([x.pos[0] for x in self.l_boids], [x.pos[1] for x in self.l_boids], [x.v[0] for x in self.l_boids], [x.v[1] for x in self.l_boids]) #graphic update
