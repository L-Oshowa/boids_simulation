import tkinter as tk
import math
import asyncio
import simulation
import boids


async def start_simulation(button, simu, l_boids, frame):
    try:
        while button['text'] == 'Stop':
            simu.time_step(l_boids)
            frame.update([x.pos[0] for x in l_boids], [x.pos[1] for x in l_boids],
                                       [x.v[0] for x in l_boids],
                                       [x.v[1] for x in l_boids])  # graphic update
            await asyncio.sleep(0.1)
    finally:
        pass


async def run_tk(window, interval=0.05):
    '''
    Run a tkinter app in an asyncio event loop.
    '''
    try:
        while True:
            window.root.update()
            await asyncio.sleep(interval)

    except tk.TclError as e:
        if "application has been destroyed" not in e.args[0]:
            raise


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

    def __init__(self, n_boids, l_pos, l_v, l_maxv, l_maxa, l_view_range, l_view_angle, w, b_cond):

        self.l_boids = [boids.Boids(l_pos[self.det_in(l_pos, ii)],
                                    l_v[self.det_in(l_v, ii)],
                                    l_maxv[self.det_in(l_maxv, ii)],
                                    l_maxa[self.det_in(l_maxa, ii)],
                                    l_view_range[self.det_in(l_view_range, ii)],
                                    l_view_angle[self.det_in(l_view_angle, ii)]) for ii in range(n_boids)]

        self.root = tk.Tk()
        self.root.title("Boids")
        self.root.lift()
        self.root.attributes('-topmost', True)
        self.root.after_idle(self.root.attributes, '-topmost', False)

        self.boid_window = BoidFrame(self.root, self.l_boids, w[0], w[1])

        self.button_canvas = tk.Canvas(self.root, width=w[0], height=20, highlightthickness=0)
        self.button_canvas.pack()

        self.b_start = tk.Button(self.button_canvas, text='Start', command=self.start_button)
        self.b_start.pack()

        self.root.update()

        self.f = 0

        self.simu = simulation.Simulation(w, b_cond)

    def start_button(self):
        if self.b_start['text'] == 'Start':
            self.b_start['text'] = 'Stop'
            self.f = asyncio.ensure_future(start_simulation(self.b_start, self.simu, self.l_boids, self.boid_window))
            return self.f
        else:
            self.b_start['text'] = 'Start'
            self.f.cancel()


    def det_in(self, in_list, ii):  #check if in_list is of length 1 or <= ii in the first case, returne 1, in the second, return ii. if ii>len(in_list) return the last element of the liste and print a message
        if ii < len(in_list):
            return ii
        elif len(in_list) == 1:
            return 0
        else :
            print('not enough argument for the initialisation of the boids')
            return len(in_list)-1
