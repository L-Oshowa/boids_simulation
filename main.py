import Interface_Graphique as IG
import tkinter as tk

# Temporary: initialise boids
posX = [110, 200, 400]
posY = [120, 150, 250]
speedX = [10, 10, -20]
speedY = [10, 0, -30]

# Initialise tk window
root = tk.Tk()
root.title("Boids")

# Put the tk window upfront
root.lift()
root.attributes('-topmost', True)
root.after_idle(root.attributes, '-topmost', False)

# Create the window
window = IG.MainFrame(root, posX, posY, speedX, speedY, 500, 500)

# Draw everything and end program
root.mainloop()
