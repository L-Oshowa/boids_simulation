import boids.py 
'''The World class contain the Boids, the obstacle, the dimention and the rule of the world
arument :
    l_boids : an array of Boids
    l_obstacle : an array of obstacle (WIP)
    w : [wx,wy]
    real_w : [rwx,rwy] for the black_hole border cond
    b_cond : border condition (0-hard wall, 1-end=start, 2-black hole border)
function : 
    __init__ : init the world and all the Boids and obstacle in it
