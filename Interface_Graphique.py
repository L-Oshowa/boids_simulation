import tkinter as tk
import math


class BoidFrame:
    '''
    The BoidFrame class creates a canvas containing all the drawing of boids
    The input are a list of boids, tk and the dimensions of the window

    Fct:
        __init__:   create the canvas and draw the original position of the boids
        polygon:    create a polygon with the shape of the boids
        update:     update the position of the boids

    Variables:

        master:     contain the TK
        drawing:    list of boids
        canvas:     canvas on which the boids are drawn

        l1, l2, l3: variable used to create the shape of the boids
    '''

    def __init__(self, master, boids, width, height):

        self.nbr_boids = len(boids)
        self.master = master

        self.canvas = tk.Canvas(self.master, width=width, height=height)
        self.canvas.pack()

        self.drawing = [self.canvas.create_polygon(
                                self.polygon(boids[x].pos[0], boids[x].pos[1], boids[x].v[0], boids[x].v[1])
                        ) for x in range(self.nbr_boids)]

    @staticmethod
    def polygon(x, y, sx, sy):

        # Three parameters which define the shape of the boids
        l1 = 7  # Distance between the position and the tip of the boid
        l2 = 7  # Distance between the position and the back of the boid
        l3 = 4  # Half the length of the back of the boid

        s = math.sqrt(sx**2 + sy**2)  # norm of the speed

        return [x+(sy*l3-sx*l2)/s, y-(sx*l3+sy*l2)/s, x+(sx*l1)/s, y+(sy*l1)/s, x-(sy*l3+sx*l2)/s, y+(sx*l3-sy*l2)/s]

    def update(self, x_position, y_position, x_speed, y_speed):

        for x in range(self.nbr_boids):
            self.canvas.coords(self.drawing[x], self.polygon(x_position[x], y_position[x], x_speed[x], y_speed[x]))
        self.master.update()


class MainFrame:
    '''
        The MainFrame class creates a window containing multiples canvas including boids, button, etc.
        The input are a list of boids and the dimensions of the window

        Fct:
            __init__:   create the window and the different canvas

        Variables:
            root:           contain the TK
            boid_window:    the canvas containing the boids (a BoidFrame object)
            button_canvas:  the canvas containing the buttons
            b_start:        the start button

        '''

    def __init__(self, list_boids, width, height):

        self.root = tk.Tk()
        self.root.title("Boids")
        self.root.lift()
        self.root.attributes('-topmost', True)
        self.root.after_idle(self.root.attributes, '-topmost', False)

        self.boid_window = BoidFrame(self.root, list_boids, width, height)

        self.button_canvas = tk.Canvas(self.root, width=width, height=20, highlightthickness=0)
        self.button_canvas.pack()

        self.b_start = tk.Button(self.button_canvas, text='Start')  # !!! Currently without function !!!
        self.b_start.pack()

        self.root.update()
