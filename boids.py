import numpy as np

class Boids :
    '''The Boids class has for purpose to embody the boids with the argument and fonction linked to it
    argument :
        x : x position of the boids
        y : y position of the boids
        vx : x speed of the boids (position/cicle)
        vy : y speed of the boids (position/cicle)
        maxv : max speed
        maxa : max acceleration
        view_range : range in which the boids take the other boids in account
        view_angle : angle of view in which the boids take the other boids in account (determined from the speed direction, on the both side)
    function :
        __init__ : init function
        '''

    def __init__(self,pos,v,maxv,maxa,view_range,view_angle) :
        self.pos = pos
        self.v = v
        self.mass = 1
        self.attraction = 1
        self.maxv = maxv
        self.maxa = maxa
        self.view_range = view_range
        self.view_angle = view_angle
        self.steering_coeff = [1, 1, 1]

    def steering(self, list_neighbour):
        nbr_neighbour = len(list_neighbour)
        force_separation = np.array([0, 0])
        center_gravity = np.array([0, 0])
        alignment = np.array([0, 0])
        total_attraction = 0

        for i in range(nbr_neighbour):

            # separation computation
            separation = list_neighbour[i].pos - self.pos
            force_separation = force_separation -separation / np.square(np.linalg.norm(separation))

            # cohesion computation
            neighbour_attraction = list_neighbour[i].attraction
            total_attraction += neighbour_attraction
            center_gravity += list_neighbour[i].pos * neighbour_attraction

            # alignment computation
            alignment = alignment + list_neighbour[i].v/nbr_neighbour

        center_gravity = center_gravity / total_attraction
        alignment -= self.v

        force = self.steering_coeff[0] * force_separation\
              + self.steering_coeff[1] * (center_gravity-self.pos)\
              + self.steering_coeff[2] * alignment

        acceleration = force / self.mass
        new_v = acceleration + self.v
        new_pos = self.pos + self.v
        return new_pos, new_v
    def update(self,npos,nv) :
        self.pos = npos
        self.v = nv
