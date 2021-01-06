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

class Boids :
    def __init__(self,pos,v,maxv,maxa,view_range,view_angle) :
        self.pos = pos
        self.v = v
        self.maxv = maxv
        self.maxa = maxa
        self.view_range = view_range
        self.view_angle = view_angle