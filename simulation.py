import numpy as np
import boids
import world
import Interface_Graphique as ui

class Simulation :
    def det_in(self,in_list,ii) :  #check if in_list is of length 1 or <= ii in the first case, returne 0, in the second, return ii. if ii>len(in_list) return the last element of the liste and print a message
        if ii < len(in_list) :
            return ii
        elif len(in_list)==1:
            return 0
        else :
            print('not enough argument for the initialisation of the boids')
            return len(in_list)-1 
    def __init__(self,n_boids,l_pos,l_v,l_maxv,l_maxa,l_view_range,l_view_angle,w,b_cond,n_binn=[1]):
        
        if b_cond == 1:
            if max(l_view_range) >= min(w) :
                print('view range to big for the simulation with b_cond = 1')
            
            
        #------------------------------------#
        elif b_cond == 2: # if the border_cond is black hole, make an "real windows" with a size = to normal size + twice the biggest boids range.
            self.real_w = w+2*max(l_view_range)
        #------------------------------------#
        self.my_world = world.World(w,b_cond)
        self.l_boids = [boids.Boids(l_pos[self.det_in(l_pos,ii)]+max(l_view_range)*(b_cond==2), \
                l_v[self.det_in(l_v,ii)], \
                l_maxv[self.det_in(l_maxv,ii)], \
                l_maxa[self.det_in(l_maxa,ii)], \
                l_view_range[self.det_in(l_view_range,ii)], \
                l_view_angle[self.det_in(l_view_angle,ii)]) for ii in range(n_boids)]
        
        #--initialisation of the partitionning --#
        self.n_binn = np.array([n_binn[self.det_in(n_binn, ii)] for ii in range(len(w))])
        self.w_binn = self.my_world.w/self.n_binn
        if len(self.my_world.w)==2 :
            self.binn = [[{b for b in self.l_boids if all(np.floor(b.pos/self.w_binn) == [x,y]) }for y in range(self.n_binn[1])]for x in range(self.n_binn[0])]
        elif len(self.my_world.w)==3 :
            self.binn = [[[{b for b in self.l_boids if all(np.floor(b.pos/self.w_binn) == [x,y,z]) }\
                for z in range(self.n_binn[2])]\
                for y in range(self.n_binn[1])]\
                for x in range(self.n_binn[0])]
        else :
            print('dimenstion other then 2 or 3 are not supported (seriously guys ?)')
        #--end of the partitionning--#   

        self.window = ui.MainFrame(self.l_boids, self.my_world.w[0], self.my_world.w[1])  #creation of the UI
    def rmv_binn(self,boids) :
        p = ((boids.pos)/self.w_binn).astype(int)
        if len(self.my_world.w)==2 :
            self.binn[p[0]][p[1]].remove(boids)
        elif len(self.my_world.w)==3 :
            self.binn[p[0]][p[1]][p[2]].remove(boids)
        return
    def add_binn(self,boids) :
        p = np.floor((boids.pos)/self.w_binn).astype(int)
        if len(self.my_world.w)==2 :
            self.binn[p[0]][p[1]].add(boids)
        elif len(self.my_world.w)==3 :
            self.binn[p[0]][p[1]][p[2]].add(boids)
        return
    def time_step (self) : #can bug if only one boids
        pos_temp = []
        v_temp = []
        for looking_boids in self.l_boids :
            in_range_boids = []
            #no need to floor since we use int() later on
            pmin = np.maximum((looking_boids.pos-looking_boids.view_range)/self.w_binn,0).astype(int)
            pmax = np.minimum((looking_boids.pos+looking_boids.view_range)/self.w_binn,self.n_binn-1).astype(int)
            if len(self.my_world.w)==2 :
                for ls_boids in self.binn[pmin[0]:pmax[0]+1] :
                    for s_boids in ls_boids[pmin[1]:pmax[1]+1] :
                        for looked_boids in s_boids :
                            if looking_boids!=looked_boids and self.my_world.isinrange(looking_boids,looked_boids) :
                                in_range_boids.append(looked_boids)
            elif len(self.my_world.w)==3 :
                for lls_boids in self.binn[pmin[0]:pmax[0]] :
                    for ls_boids in lls_boids[pmin[1]:pmax[1]] :
                        for s_boids in ls_boids[pmin[2]:pmax[2]] :
                            for looked_boids in s_boids :
                                if looking_boids!=looked_boids and self.my_world.isinrange(looking_boids,looked_boids) :
                                    in_range_boids.append(looked_boids)
            temp = looking_boids.steering(in_range_boids)
            temp = self.my_world.position(temp[0],temp[1])
            pos_temp.append(temp[0])
            v_temp.append(temp[1])
        for x,y,z in zip(self.l_boids, pos_temp, v_temp) :
            cond = any(np.floor(x.pos/self.w_binn)!=np.floor(y/self.w_binn))
            if cond :
                self.rmv_binn(x)
            x.update(y,z)
            if cond : 
                self.add_binn(x)        
        self.window.boid_window.update([x.pos[0] for x in self.l_boids], [x.pos[1] for x in self.l_boids], [x.v[0] for x in self.l_boids], [x.v[1] for x in self.l_boids]) #graphic update
