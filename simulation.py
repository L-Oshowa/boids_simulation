import world


class Simulation:

    def det_in(self, in_list, ii):  # check if in_list is of length 1 or <= ii in the first case, returne 1, in the second, return ii. if ii>len(in_list) return the last element of the liste and print a message
        if ii < len(in_list):
            return ii
        elif len(in_list) == 1:
            return 0
        else:
            print('not enough argument for the initialisation of the boids')
            return len(in_list)-1

    def __init__(self, w, b_cond):

        if not b_cond == 0:
            print('border condition WIP')

        self.my_world = world.World(w, b_cond)

    def time_step(self, l_boids): #can bug if only one boids
        pos_temp = []
        v_temp = []
        for ix, x in enumerate(l_boids):
            y_temp = []
            for iy, y in enumerate(l_boids):
                if iy != ix and self.my_world.isinrange(x, y):
                    y_temp.append(y)
            temp = x.steering(y_temp)
            temp = self.my_world.position(temp[0], temp[1])
            pos_temp.append(temp[0])
            v_temp.append(temp[1])
        '''
        pos_temp,v_temp = [x.steering(\
                            [y for iy,y in enumerate(self.l_boids) if self.my_world.isinrange(x,y) and iy!=ix]\
                            ) for ix,x in enumerate(self.l_boids)]
        pos_temp,v_temp = [self.my_world.position(x,y) for x,y in zip(pos_temp,v_temp)]
        '''
        for x, y, z in zip(l_boids, pos_temp, v_temp): x.update(y, z)

