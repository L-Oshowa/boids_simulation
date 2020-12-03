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
    def __init__(self,x,y,vx,vy,maxv,maxa,view_range,view_angle) :
        self.name='mon nom est boids !'
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.maxv = x
        self.maxa = x
        self.view_range = view_range
        self.view_angle = view_angle
boids = Boids(0,0,1,1,)
print(boids.vy)
print(boids.name)