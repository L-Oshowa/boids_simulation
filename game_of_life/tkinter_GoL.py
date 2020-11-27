from tkinter import *
import numpy


class GridApp:

    def __init__(self, master, nx, ny):  # Initialize a grid and the Tk Frame on which it is rendered.

        """Set variables"""
        # Number of cells in each dimension.
        self.nx = nx
        self.ny = ny

        # Some dimensions for the canvas.
        self.grid_canvas_width, self.grid_canvas_height = 800, 800
        self.canvas_button_height = 50
        self.canvas_button_width = self.grid_canvas_width

        # Management of the blank spaces
        self.space_between_cells = 0
        self.n_space_x = self.nx + 1
        self.n_space_y = self.ny + 1
        self.offset_x = 3
        self.offset_y = 3

        # Set the width of the cells (square cells => width=height)
        self.cell_width = self.cell_size()

        # Set the grid in a matrix
        self.matrix_grid = numpy.zeros(shape=(self.nx, self.ny))

        # Game On or Off
        self.game_on = False

        # Timer
        self.timer = 100

        """Set all the canvas"""
        # The main frame onto which we draw all the elements.
        self.frame = Frame(master)
        self.frame.pack()

        # The canvas for the button and input
        self.button_canvas = Canvas(master, width=self.canvas_button_width, height=self.canvas_button_height,
                                    highlightthickness=0)
        self.button_canvas.pack()

        # The canvas onto which the grid is drawn.
        self.grid_canvas = Canvas(master, width=self.grid_canvas_width, height=self.grid_canvas_height)
        self.grid_canvas.pack()

        """Set all the widgets"""
        # Add a button to make a new grid
        self.b_new = Button(self.button_canvas, text='new', command=lambda: restart(self.rows.get(), self.column.get()))
        self.b_new.grid(column=0, row=0, columnspan=4)

        # Text and entry for the number of rows
        txt_rows = Label(self.button_canvas, text="Nbr of rows: ")
        txt_rows.grid(column=0, row=1)
        self.rows = Entry(self.button_canvas, width=10)
        self.rows.insert(END, nx)
        self.rows.grid(column=1, row=1)

        # Text and entry for the number of columns
        txt_column = Label(self.button_canvas, text=" Nbr of columns: ")
        txt_column.grid(column=2, row=1)
        self.column = Entry(self.button_canvas, width=10)
        self.column.insert(END, ny)
        self.column.grid(column=3, row=1)

        # Add a button to start the game
        self.b_start = Button(self.button_canvas, text='Start', command=self.start_game)
        self.b_start.grid(column=0, row=2, columnspan=4)

        # Add the cell rectangles to the grid canvas.
        self.cells = []
        for iy in range(ny):
            for ix in range(nx):
                x = self.space_between_cells * (ix + 1) + ix * self.cell_width + self.offset_x
                y = self.space_between_cells * (iy + 1) + iy * self.cell_width + self.offset_y
                rect = self.grid_canvas.create_rectangle(y, x, y+self.cell_width, x+self.cell_width, fill='white')
                self.cells.append(rect)

        def click_on_grid(event):  # Function called when someone clicks on the grid canvas.
            y, x = event.x-self.offset_x, event.y-self.offset_y
            # Did the user click a cell in the grid?
            # Indexes into the grid of cells (including padding)
            ix = int(x // (self.cell_width + self.space_between_cells))
            iy = int(y // (self.cell_width + self.space_between_cells))
            xc = x - ix * (self.cell_width + self.space_between_cells) - self.space_between_cells
            yc = y - iy * (self.cell_width + self.space_between_cells) - self.space_between_cells
            if ix < self.nx and iy < self.ny and 0 < xc < self.cell_width and 0 < yc < self.cell_width:
                i = iy * self.nx + ix
                color = self.grid_canvas.itemcget(self.cells[i], 'fill')  # get the color of the rectangle
                if color == 'black':
                    color = 'white'
                    self.matrix_grid[ix, iy] = 0
                else:
                    color = 'black'
                    self.matrix_grid[ix, iy] = 1

                self.grid_canvas.itemconfig(self.cells[i], fill=color)

        # Bind the click_on_grid function to the left mouse button
        # press event on the grid canvas.
        self.grid_canvas.bind('<ButtonPress-1>', click_on_grid)

    # --------------------------- end __init__() -----------------------------------------------------------------------

    def cell_size(self):  # compute the size of the cells in order to fit in the canvas
        default_cell_width = 54
        modify = 'z'

        default_canvas_height = self.nx * default_cell_width + self.n_space_x * self.space_between_cells \
                                + 2 * self.offset_x
        default_canvas_width = self.ny * default_cell_width + self.n_space_y * self.space_between_cells \
                               + 2 * self.offset_y

        if default_canvas_height > self.grid_canvas_height:
            if default_canvas_height > self.grid_canvas_height:
                if default_canvas_height-self.grid_canvas_height > default_canvas_width-self.grid_canvas_width:
                    modify = 'x'
                else:
                    modify = 'y'
            else:
                modify = 'x'
        else:
            if default_canvas_width > self.grid_canvas_width:
                modify = 'y'

        if modify == 'x':
            width = (self.grid_canvas_height - 2 * self.offset_x - self.n_space_x * self.space_between_cells) / self.nx
        elif modify == 'y':
            width = (self.grid_canvas_width - 2 * self.offset_y - self.n_space_y * self.space_between_cells) / self.ny
        else:
            width = default_cell_width

        return width
    # --------------------------- end cell_size() ----------------------------------------------------------------------

    def obliterate(self):  # destroy the frame, the buttons and the grid
        self.frame.destroy()
        self.button_canvas.destroy()
        self.grid_canvas.destroy()

    # --------------------------- end obliterate() ---------------------------------------------------------------------

    def redraw(self, matrix):
        for iy in range(self.ny):
            for ix in range(self.nx):
                i = iy * self.nx + ix
                if matrix[ix, iy] == 0:
                    color = 'white'
                else:
                    color = 'black'
                self.grid_canvas.itemconfig(self.cells[i], fill=color)
        self.matrix_grid = matrix

    def start_game(self):

        if self.game_on:
            self.b_start['text'] = 'start'
            self.game_on = False

        else:
            self.game_on = True
            self.b_start['text'] = 'stop'
            self.running_game()

    def running_game(self):

        if self.game_on:
            evolve(self.matrix_grid, self.nx, self.ny)
            root.after(self.timer, self.running_game)


# ----------------------------------------------------------------------------------------------------------------------
# --------------------------- end Class GridApp() ----------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

def restart(nx, ny):  # restart the frame with nx rows and ny columns
    global big_frame
    x = verify_nbr(nx)
    y = verify_nbr(ny)
    if x == -1:
        messagebox.showerror('Error', 'Error in the rows entry')
    elif y == -1:
        messagebox.showerror('Error', 'Error in the columns entry')

    else:
        big_frame.obliterate()
        big_frame = GridApp(root, x, y)


# --------------------------- end restart() ----------------------------------------------------------------------------

def verify_nbr(nbr):  # verify if the numbers in the rows/columns entry are integers > 0 if not return -1
    try:
        user_input = int(nbr)
    except ValueError:
        return -1
    else:
        if user_input <= 0:
            return -1
        else:
            return user_input


# --------------------------- end verify_nbr() -------------------------------------------------------------------------

def living_neighbour(matrix, center):

    return matrix.sum()-center


# --------------------------- end living_neighbour() -------------------------------------------------------------------

def parameters(number, dim):
    param1 = 1
    param2 = 2
    if number == 0:
        param1 = 0
    elif number == dim-1:
        param2 = 1

    return [param1, param2]


# --------------------------- end parameters() -------------------------------------------------------------------------

def evolve(matrix, nx, ny):
    evolved_matrix = numpy.zeros(shape=(nx, ny))
    for x in range(nx):
        for y in range(ny):
            param_row = parameters(x, nx)
            param_column = parameters(y, ny)
            M = matrix[x - param_row[0]:x + param_row[1], y - param_column[0]:y + param_column[1]]
            neighbour = living_neighbour(M, matrix[x, y])
            if matrix[x, y] == 0 and neighbour == 3:
                evolved_matrix[x, y] = 1

            elif matrix[x, y] == 1 and (neighbour == 2 or neighbour == 3):
                evolved_matrix[x, y] = 1

            else:
                evolved_matrix[x, y] = 0

    big_frame.redraw(evolved_matrix)


# ----------------------------------------------------------------------------------------------------------------------
# ------------------------------- beginning main() ---------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
root = Tk()
big_frame = GridApp(root, 20, 20)
root.title("Game of Life")
root.lift()
root.attributes('-topmost', True)
root.after_idle(root.attributes, '-topmost', False)
root.mainloop()
