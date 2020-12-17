import boids
import numpy as np
'''The World class contain the Boids, the obstacle, the dimention and the rule of the world
!!! in the case of black hole border, the position given to the class need to be shifted to match the real border. check world class to be sure
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
        if not self.b_cond==0 :
            print('border condition WIP')
        if self.b_cond == 2: # if the border_cond is black hole, make an "real windows" with a size = to normal size + twice the biggest boids range.
            self.real_w = w+2*max(l_view_range)
        elif self.b_cond == 1:
            if max(l_view_range) >= min(self.w) :
                print('view range to big for the simulation with b_cond = 1')
        self.l_boids = []
        for ii in range(n_boids):
            self.l_boids.append(boids.Boids(l_pos[self.det_in(l_pos,ii)]+max(l_view_range)*(self.b_cond==2), \
                l_v[self.det_in(l_v,ii)], \
                l_maxv[self.det_in(l_maxv,ii)], \
                l_maxa[self.det_in(l_maxa,ii)], \
                l_view_range[self.det_in(l_view_range,ii)], \
                l_view_angle[self.det_in(l_view_angle,ii)]))
        self.l_obstacle = [] #WIP     
    def position(self,pos,) : #change pos according to border condition NEED ALSO TO CHANGE SPEED
        if self.b_cond == 0 : #hard wall
            for ii in range(len(pos)) :
                if pos[ii] < 0 :
                    pos[ii] = -pos[ii]
                elif pos[ii] > self.w[ii] :
                    pos[ii] = 2*self.w[ii]-pos[ii]
        elif self.b_cond == 1 : # end=start
             for ii in range(len(pos)) :
                if pos[ii] < 0 :
                    pos[ii] = self.w[ii]+pos[ii]
                elif pos[ii] > self.w[ii] :
                    pos[ii] = pos[ii]-self.w[ii]
        return
    def finding_neighbour(self,ii_boids) : #determine the neighbours of the l_boids[ii], depending on his view range and angle and on the border cond. In case of b_cond == 1, also return a list of array for the desired boids position
        # optimisation possibility : slice space in cube or, if avoid the calcule of distance between boids doubled
        l_neighbour = []
        if self.b_cond == 0 : # hard wall case : the line of sight is stoped by the border
            for ii in range(len(self.l_boids)) :
                if ii != ii_boids :
                    vec = self.l_boids[ii].pos-self.l_boids[ii_boids].pos
                    if np.linalg.norm(vec,2) <= self.l_boids[ii_boids].view_range :
                        if np.arccos(np.dot(self.l_boids[ii_boids].v,vec)/np.linalg.norm(self.l_boids[ii_boids].v,2)/np.linalg.norm(vec,2)) <= self.l_boids[ii_boids].view_angle :
                            l_neighbour.append(ii)
            return l_neighbour
        elif self.b_cond == 1 : # end=start case : to have a perfect simu, we should solve the torus geodesic. to complicate -> we deliminate the max view range < min w
            l_calc_pos = []
            for ii in range(len(self.l_boids)) :
                if ii != ii_boids :
                    vec = self.l_boids[ii].pos-self.l_boids[ii_boids].pos
                    calc_pos = 1*(vec > self.w)-1*(vec < -self.w)
                    vec += calc_pos*self.w
                    if np.linalg.norm(vec,2) <= self.l_boids[ii_boids].view_range :
                        if np.arccos(np.dot(self.l_boids[ii_boids].v,vec)/np.linalg.norm(self.l_boids[ii_boids].v,2)/np.linalg.norm(vec,2)) <= self.l_boids[ii_boids].view_angle :
                            l_neighbour.append(ii)
                            l_calc_pos.append(calc_pos)
            return l_neighbour, l_calc_pos

        elif self.b_cond == 2 : # black-hole case : the line of sight is stoped by the real border
            for ii in range(len(self.l_boids)) :
                if ii != ii_boids :
                    vec = self.l_boids[ii].pos-self.l_boids[ii_boids].pos
                    if np.linalg.norm(vec,2) <= self.l_boids[ii_boids].view_range :
                        if np.arccos(np.dot(self.l_boids[ii_boids].v,vec)/np.linalg.norm(self.l_boids[ii_boids].v,2)/np.linalg.norm(vec,2)) <= self.l_boids[ii_boids].view_angle :
                            l_neighbour.append(ii)
            return l_neighbour
                        
