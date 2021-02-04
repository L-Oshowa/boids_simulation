import tkinter as tk
import math
import asyncio
import simulation
import boids
import random
import numpy as np
import time


async def start_simulation(simu, l_boids, frame, frame_rate=1/20):
    """
    Launch the simulation which is done in two steps:
        1) Numerically: with time_step() from simu
        2) Graphically: with update() from frame

    Parameters:
        simu: object containing all the numerical aspects of the simulation
        l_boids: List of the boids
        frame: Frame that display the simulation
        frame_rate: Waiting time between two time steps
    """
    try:
        while True:
            t0 = time.perf_counter()
            simu.time_step(l_boids)
            frame.update([x.pos[0] for x in l_boids], [x.pos[1] for x in l_boids],
                         [x.v[0] for x in l_boids],
                         [x.v[1] for x in l_boids])
            t1 = time.perf_counter() - t0
            if t1 < frame_rate:
                await asyncio.sleep(frame_rate-t1)
    finally:
        pass


async def run_tk(window, refresh_time=0.05):
    """
    Create an infinite loop that will update the tk_window and acknowledge changes e.g. button pressed
    The loop end when an error is raised . If the error comes from the known cause, don't raise it

    Parameters:
            window: Entire tk_window that will be display on screen
            refresh_time: Time it takes for the windows to update and acknowledge changes
    """
    try:
        while True:
            window.root.update()
            await asyncio.sleep(refresh_time)

    except tk.TclError as e:
        if "application has been destroyed" not in e.args[0]:
            raise
    finally:
        window.f.cancel()


class BoidFrame:
    '''
    The BoidFrame class creates a canvas containing all the drawing of boids
    The input are a list of boids, tk and the dimensions of the window

    Initialisation Parameters:
        master: tk environment
        boids: list of the boids
        width: width of the boid window
        height: height of the boid window

    Fct:
        __init__:   create the canvas and draw the original position of the boids
        polygon:    create a polygon with the shape of the boids
        update:     graphical update of the position of the boids

    Variables:

        drawing:    list of the boids polygons
        canvas:     canvas on which the boids are drawn

        l1, l2, l3: variable used to create the shape of the boids
        s: norm of the speed
    '''

    def __init__(self, master, canvas, l_boids):

        nbr_boids = len(l_boids)
        self.master = master
        self.canvas = canvas

        self.drawing = [self.canvas.create_polygon(
                                self.polygon(l_boids[x].pos[0], l_boids[x].pos[1], l_boids[x].v[0], l_boids[x].v[1])
                        ) for x in range(nbr_boids)]

    @staticmethod
    def polygon(x, y, sx, sy):

        l1 = 7  # Distance between the position and the tip of the boid
        l2 = 7  # Distance between the position and the back of the boid
        l3 = 4  # Half the length of the back of the boid

        s = math.sqrt(sx**2 + sy**2)

        return [x+(sy*l3-sx*l2)/s, y-(sx*l3+sy*l2)/s, x+(sx*l1)/s, y+(sy*l1)/s, x-(sy*l3+sx*l2)/s, y+(sx*l3-sy*l2)/s]

    def update(self, x_position, y_position, x_speed, y_speed):
        n_draw_boids = len(x_position)
        n_boids = len(self.drawing)
        if n_draw_boids <= n_boids:
            for x in range(n_boids):
                if x <= n_draw_boids:
                    self.canvas.coords(self.drawing[x], self.polygon(x_position[x], y_position[x], x_speed[x], y_speed[x]))
                else:
                    self.drawing.pop(x)
        else:
            for x in range(n_draw_boids):
                if x <= n_boids:
                    self.canvas.coords(self.drawing[x], self.polygon(x_position[x], y_position[x], x_speed[x], y_speed[x]))
                else:
                    self.add_draw_boid([x_position[x], y_position[x]], [x_speed[x], y_speed[x]])

        self.master.update()

    def add_draw_boid(self, pos, v):
        self.drawing.append(self.canvas.create_polygon(self.polygon(pos[0], pos[1], v[0], v[1])))


class MainFrame:
    """
        The MainFrame class creates a window containing multiples canvas including boids, button, etc.
        The input are a list of boids and the dimensions of the window

        Initialisation Parameters:
            n_boids: the number of boids
            l_pos: list of the position of each boids
            l_v: list of the speed of each boids
            l_maxv: list of the maximum speed of each boids
            l_maxa: list of the maximum acceleration of each boids
            l_view_range: list of the view range of each boids
            l_view_angle: list of the view angle of each boids
            w: width and height of the window
            b_cond: boundary condition

        Fct:
            __init__:   create the window and the different canvas
            start_button: when the star-button is pressed, change its name and launch/stop the simulation

        Variables:
            root:           contain the TK
            boid_window:    the canvas containing the boids (a BoidFrame object)
            button_canvas:  the canvas containing the buttons
            b_start:        the start button which launch the simulation
            f:              task to run in asyncio the simulation
    """

    def __init__(self, n_boids, l_pos, l_v, l_maxv, l_maxa, l_view_range, l_view_angle, w, b_cond):

        self.simu = simulation.Simulation(w, b_cond)
        self.n_boids = n_boids
        self.w = w

        self.l_boids = [boids.Boids(l_pos[self.simu.det_in(l_pos, ii)],
                                    l_v[self.simu.det_in(l_v, ii)],
                                    l_maxv[self.simu.det_in(l_maxv, ii)],
                                    l_maxa[self.simu.det_in(l_maxa, ii)],
                                    l_view_range[self.simu.det_in(l_view_range, ii)],
                                    l_view_angle[self.simu.det_in(l_view_angle, ii)]) for ii in range(self.n_boids)]

        self.root = tk.Tk()
        self.root.title("Boids")
        self.root.lift()
        self.root.attributes('-topmost', True)
        self.root.after_idle(self.root.attributes, '-topmost', False)

        self.boid_canvas = tk.Canvas(self.root, width=w[0], height=w[1])
        self.boid_canvas.grid(row=0, column=0, columnspan=5)

        self.boid_window = BoidFrame(self.root, self.boid_canvas, self.l_boids)

        self.b_start = tk.Button(self.root, text='Start', command=self.start_button)
        self.b_start.grid(row=1, column=2)

        self.slider_separation = tk.Scale(self.root, from_=0, to=200, resolution=10, orient='horizontal', state='active')
        self.slider_separation.set(100)
        self.slider_separation.grid(row=2, column=0)

        self.slider_cohesion = tk.Scale(self.root, from_=0, to=200, resolution=10, orient='horizontal', state='active')
        self.slider_cohesion.set(100)
        self.slider_cohesion.grid(row=2, column=2)

        self.slider_alignment = tk.Scale(self.root, from_=0, to=200, resolution=10, orient='horizontal', state='active')
        self.slider_alignment.set(100)
        self.slider_alignment.grid(row=2, column=4)

        self.b_add = tk.Button(self.root, text='Add', command=self.add_boids)
        self.b_add.grid(row=3, column=1)

        self.b_remove = tk.Button(self.root, text='Remove', command=self.remove_boids)
        self.b_remove.grid(row=3, column=3)

        self.root.update()

        self.f = asyncio.ensure_future(start_simulation(self.simu, self.l_boids, self.boid_window))
        self.f.cancel()

    def start_button(self):
        if self.b_start['text'] == 'Start':
            self.n_boids = len(self.l_boids)
            self.b_start['text'] = 'Stop'
            self.f = asyncio.ensure_future(start_simulation(self.simu, self.l_boids, self.boid_window))
            self.slider_separation.configure(state='disabled')
            self.slider_cohesion.configure(state='disabled')
            self.slider_alignment.configure(state='disabled')
            self.b_add.configure(state='disabled')
            self.b_remove.configure(state='disabled')

            percent = [self.slider_separation.get()/100, self.slider_cohesion.get()/100, self.slider_alignment.get()/100]

            for i in range(self.n_boids):
                self.l_boids[i].percent_coeff = percent

        else:
            self.b_start['text'] = 'Start'
            self.f.cancel()
            self.slider_separation.configure(state='active')
            self.slider_cohesion.configure(state='active')
            self.slider_alignment.configure(state='active')
            self.b_add.configure(state='active')
            self.b_remove.configure(state='active')

    def add_boids(self):
        margin = 12
        pos = np.array([random.randint(margin, self.w[0]-margin), random.randint(margin, self.w[1]-margin)])
        maxv = 10
        v = np.array([random.uniform(-maxv, maxv), random.uniform(-maxv, maxv)])
        if v[0] == 0 and v[1] == 0:
            v = [0.01, 0.01]
        maxa = 1
        view_range = 100
        view_angle = 80
        self.l_boids.append(boids.Boids(pos, v, maxv, maxa, view_range, view_angle))
        self.boid_window.add_draw_boid(pos, v)

    def remove_boids(self):
        self.l_boids.pop()
        l = len(self.boid_window.drawing)
        self.boid_window.canvas.delete(self.boid_window.drawing[l-1])
        self.boid_window.drawing.pop()
