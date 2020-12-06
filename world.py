import boids.py 
import numpy as np
'''The World class contain the Boids, the obstacle, the dimention and the rule of the world
/!\ in the case of black hole border, the position given to the class need to be shifted to match the real border. check world class to be sure
arument :
    l_boids : an array of Boids
    l_obstacle : an array of obstacle (WIP)
    w : [wx,wy]
    real_w : [rwx,rwy] for the black_hole border cond
    b_cond : border condition (0-hard wall, 1-end=start, 2-black hole border)
function : 
    __init__ : init the world and all the Boids and obstacle in it
'''
class world:
    def det_in(self,in_list,ii) :  #check if in_list is of length 1 or <= ii in the first case, returne 1, in the second, return ii. if ii>len(in_list) return the last element of the liste and print a message
        if ii <= len(in_list) :
            return ii
        elif len(in_list)==1:
            return 1
        else :
            print('not enough argument for the initialisation of the boids')
            return len(in_list)-1 
    def __init__(self,n_boids,l_pos,l_v,l_maxv,l_maxa,l_view_range,l_view_angle,w,b_cond):
        self.w = w
        self.b_cond = b_cond
        if self.b_cond == 2: # if the border_cond is black hole, make an "real windows" with a size = to normal size + twice the biggest boids range.
            self.real_w = w+2*max(l_view_range)
        self.l_boids = []
        for ii in range(n_boids):
            self.l_boids.append(Boids(l_pos[det_in(l_pos,ii)]+max(l_view_range)*(self.b_cond==2), \
                l_v[det_in(l_v,ii)], \
                l_maxv[det_in(l_maxv,ii)], \
                l_maxa[det_in(l_maxa,ii)], \
                l_view_range[det_in(l_view_range,ii)], \
                l_view_angle[det_in(l_view_angle,ii)]))
        self.l_obstacle = [] #WIP     
    def position(self,pos) : #change pos according to border condition
        if self.b_cond == 0 : #hard wall
            for ii in range(len(pos)) :
                if pos[ii] < 0
                    pos[ii] = -pos[ii]
                elif pos[ii] > self.w[ii] :
                    pos[ii] = 2*self.w[ii]-pos[ii]
        elif self.b_cond == 1 : # end=start
             for ii in range(len(pos)) :
                if pos[ii] < 0
                    pos[ii] = self.w[ii]+pos[ii]
                elif pos[ii] > self.w[ii] :
                    pos[ii] = pos[ii]-self.w[ii]
        return
    def finding_neighbour(self,boids) : #determine the neighbour of a given boids, depending his view range and angle and on the border cond. 
        # optimisation possibility : slice space in cube or, if avoid the calcule of distance between boids doubled
        l_neighbour = []
        if b_cond == 0 : # hard wall case : the line of sight is stoped by the border
            for ii in range(len(self.l_boids)) :
                vec = sel-l_boids[ii].pos-boids.pos
                if np.linalg.norm(vec,2) <= boids.view_range :
                    if np.arccos(np.dot(boids.v,vec)/np.linalg.norm(boids.v,2)/np.linalg.norm(vec,2)) <= boids.view_angle :
                        l_neighbour.append(ii)
        elif b_cond == 1 : # end=start case : to have a perfect simu, we should solve the torus geodesic. to complicate -> 