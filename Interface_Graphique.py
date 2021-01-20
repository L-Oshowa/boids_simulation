import tkinter as tk
import math
import asyncio
import simulation
import boids


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
            simu.time_step(l_boids)
            frame.update([x.pos[0] for x in l_boids], [x.pos[1] for x in l_boids],
                         [x.v[0] for x in l_boids],
                         [x.v[1] for x in l_boids])
            await asyncio.sleep(frame_rate)
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

        l1 = 7  # Distance between the position and the tip of the boid
        l2 = 7  # Distance between the position and the back of the boid
        l3 = 4  # Half the length of the back of the boid

        s = math.sqrt(sx**2 + sy**2)

        return [x+(sy*l3-sx*l2)/s, y-(sx*l3+sy*l2)/s, x+(sx*l1)/s, y+(sy*l1)/s, x-(sy*l3+sx*l2)/s, y+(sx*l3-sy*l2)/s]

    def update(self, x_position, y_position, x_speed, y_speed):

        for x in range(self.nbr_boids):
            self.canvas.coords(self.drawing[x], self.polygon(x_position[x], y_position[x], x_speed[x], y_speed[x]))
        self.master.update()


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

        self.l_boids = [boids.Boids(l_pos[self.simu.det_in(l_pos, ii)],
                                    l_v[self.simu.det_in(l_v, ii)],
                                    l_maxv[self.simu.det_in(l_maxv, ii)],
                                    l_maxa[self.simu.det_in(l_maxa, ii)],
                                    l_view_range[self.simu.det_in(l_view_range, ii)],
                                    l_view_angle[self.simu.det_in(l_view_angle, ii)]) for ii in range(n_boids)]

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

        self.f = asyncio.ensure_future(start_simulation(self.simu, self.l_boids, self.boid_window))
        self.f.cancel()

    def start_button(self):
        if self.b_start['text'] == 'Start':
            self.b_start['text'] = 'Stop'
            self.f = asyncio.ensure_future(start_simulation(self.simu, self.l_boids, self.boid_window))
            return self.f
        else:
            self.b_start['text'] = 'Start'
            self.f.cancel()
