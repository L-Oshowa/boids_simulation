import world

def det_in(self,in_list,ii) :  #check if in_list is of length 1 or <= ii in the first case, returne 0, in the second, return ii. if ii>len(in_list) return the last element of the liste and print a message
    if ii < len(in_list) :
        return ii
    elif len(in_list) == 1:
        return 0
    else:
        print('not enough argument for the initialisation of the boids')
        return len(in_list)-1

class Simulation :
                  
    def __init__(self, w, b_cond,l_boids,n_binn = [1]):

        if not b_cond == 0:
            print('border condition WIP')

        self.my_world = world.World(w, b_cond)
        
        #--initialisation of the partitionning --#
        self.n_binn = np.array([n_binn[det_in(n_binn, ii)] for ii in range(len(w))])
        self.w_binn = self.my_world.w/self.n_binn
        if len(self.my_world.w)==2 :
            self.binn = [[{b for b in l_boids if all(np.floor(b.pos/self.w_binn) == [x,y]) }for y in range(self.n_binn[1])]for x in range(self.n_binn[0])]
        elif len(self.my_world.w)==3 :
            self.binn = [[[{b for b in l_boids if all(np.floor(b.pos/self.w_binn) == [x,y,z]) }\
                for z in range(self.n_binn[2])]\
                for y in range(self.n_binn[1])]\
                for x in range(self.n_binn[0])]
        else :
            print('dimenstion other then 2 or 3 are not supported (seriously guys ?)')
        #--end of the partitionning--#   
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
      
    def time_step (self,l_boids) : #can bug if only one boids
        pos_temp = []
        v_temp = []
        for looking_boids in l_boids :
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

        for x,y,z in zip(l_boids, pos_temp, v_temp) :
            cond = any(np.floor(x.pos/self.w_binn)!=np.floor(y/self.w_binn))
            if cond :
                self.rmv_binn(x)
            x.update(y,z)
            if cond : 
                self.add_binn(x)  
