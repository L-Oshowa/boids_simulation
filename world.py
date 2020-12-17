import boids
import numpy as np
'''The World class contain the Boids, the obstacle, the dimention and the rule of the world
!!! in the case of black hole border, the position given to the class need to be shifted to match the real border. check world class to be sure
arument :
    l_obstacle : an array of obstacle (WIP)
    w : [wx,wy]
    real_w : [rwx,rwy] for the black_hole border cond
    b_cond : border condition (0-hard wall, 1-end=start, 2-black hole border)
function : 
    __init__ : init the world and all the Boids and obstacle in it
'''
class World:
    
    def __init__(self,w,b_cond):
        self.w = w
        self.b_cond = b_cond
        self.l_obstacle = [] #WIP
    def position(self,pos,speed) : #change pos and speed according to border condition
        if self.b_cond == 0 : #hard wall
            return [[-x,-v] if x<0 else [2*y-x,-v] if x>y else [x,v] for x,y,v in zip(pos,self.w,speed)]
        elif self.b_cond == 1 : # end=start
            return [[x+y,v] if x<0 else [x-y,v] if y>y else [x,y] for x,y,v in zip(pos,self.w,speed)]
        else :
            return [pos,speed]
    def isinrange(self,boids1,boids2) : #determine if boids1 see boids2 according to the world
        if self.b_cond == 0 : # hard wall case : the line of sight is stoped by the border
            vec = boids2.pos-boids1.pos
            if np.linalg.norm(vec,2) <= boids1.view_range :
                if np.arccos(np.dot(boids1.v,vec)/np.linalg.norm(boids1.v,2)/np.linalg.norm(vec,2)) <= boids1.view_angle :
                    return 1
            return 0
        else :
            print('WIP')
            return 0
    '''  
    def finding_neighbour(self,ii_boids,l_boids) : #determine the neighbours of the l_boids[ii], depending on his view range and angle and on the border cond. In case of b_cond == 1, also return a list of array for the desired boids position
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
    '''            
