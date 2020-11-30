import tkinter as tk
import math


class BoidFrame:  # Create a window for the boids and update their position. ATTENTION: Take only lists !!!
    def __init__(self, master, x_position, y_position, x_speed, y_speed, width, height):

        # Create variables used for drawing
        self.nbr_object = len(x_position)
        self.drawing = []

        # Create and draw the canvas
        self.canvas = tk.Canvas(master, width=width, height=height)
        self.canvas.pack()

        # Draw the boids and store them in self.drawing
        for x in range(self.nbr_object):
            draw = self.canvas.create_polygon(self.points_polygon(x_position[x], y_position[x], x_speed[x], y_speed[x]))
            self.drawing.append(draw)

    def points_polygon(self, x, y, sx, sy):  # Create the shape of the boids

        # Three parameters which define the shape of the boids
        l1 = 7  # Distance between the position and the tip of the boid
        l2 = 7  # Distance between the position and the back of the boid
        l3 = 4  # Half the length of the back of the boid

        # The norm of the speed
        norm = math.sqrt(sx**2 + sy**2)

        # Store the points in the format (x1, y1, x2, y2, x3, y3, ...)
        points = []

        #points.append(x)
        #points.append(y)

        points.append(x+(sy*l3-sx*l2)/norm)
        points.append(y-(sx*l3+sy*l2)/norm)

        points.append(x+(sx*l1)/norm)
        points.append(y+(sy*l1)/norm)

        points.append(x-(sy*l3+sx*l2)/norm)
        points.append(y+(sx*l3-sy*l2)/norm)

        return points

    def update(self, x_position, y_position, x_speed, y_speed):  # Update the position of the boids
        for x in range(self.nbr_object):
            self.canvas.coords(self.drawing[x], self.points_polygon(x_position[x], y_position[x], x_speed[x], y_speed[x]))


class MainFrame:  # The big frame containing the boids frame and some buttons, used to run the simulation

    def __init__(self, master, x_position, y_position, x_speed, y_speed, width, height):

        # Recover information for all the function of the object
        self.posX = x_position
        self.posY = y_position
        self.speedX = x_speed
        self.speedY = y_speed
        self.master = master

        # Variables used for running the simulation
        self.simulation_on = 0
        self.timer = 50
        self.step = 0

        # Create the window for the boids
        self.boid_window = BoidFrame(master, x_position, y_position, x_speed, y_speed, width, height)

        # The canvas for the button
        self.button_canvas = tk.Canvas(master, width=width, height=20, highlightthickness=0)
        self.button_canvas.pack()

        # Add a button to start the simulation
        self.b_start = tk.Button(self.button_canvas, text='Start', command=self.start)  # on click call start()
        self.b_start.pack()

    def start(self):  # Stop the simulation if on and launch the simulation if not
        if self.simulation_on:
            self.b_start['text'] = 'start'  # Change the name of the button
            self.simulation_on = False

        else:
            self.simulation_on = True
            self.b_start['text'] = 'stop'  # Change the name of the button
            self.running_simulation()  # Launch the simulation function

    def running_simulation(self):  # Recurring function which should do something if simulation is on

        if self.simulation_on:

            # Temporary: to evolve the boids
            self.step += 1
            pos1 = []
            pos2 = []
            s1 = []
            s2 = []
            for x in range(len(self.posX)):
                pos1.append(self.posX[x] + self.step * self.speedX[x])
                pos2.append(self.posY[x] + self.step * self.speedY[x])
                s1.append(self.speedX[x])
                s2.append(self.speedY[x])

            self.boid_window.update(pos1, pos2, s1, s2)  # Update the position of the boids
            self.master.after(self.timer, self.running_simulation)  # Wait x ms than call the self.running_game function
