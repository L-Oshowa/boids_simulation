import numpy as np
import boids
import world
import Interface_Graphique

class simulation :
    def det_in(self,in_list,ii) :  #check if in_list is of length 1 or <= ii in the first case, returne 1, in the second, return ii. if ii>len(in_list) return the last element of the liste and print a message
        if ii <= len(in_list) :
            return ii
        elif len(in_list)==1:
            return 1
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
    def time_step (self) :
        pos_temp,v_temp = [x.steering(\
                            [y for y in self.l_boids[0:ix]+self.l_boids[ix+1:] if self.my_world.isinrange(x,y)]\
                            ) for ix,x in enumerate(self.l_boids)]
        pos_temp,v_temp = [self.my_world.position(x,y) for x,y in zip(pos_temp,v_temp)]
        [x.update(y,z) for x,y,z in zip(self.l_boids, pos_temp, v_temp)]
