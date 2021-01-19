import simulation
import numpy as np
import asyncio
from tkinter import TclError as tcl


async def start_simulation(button):
    try:
        while button['text'] == 'Stop':
            print('0')
            await asyncio.sleep(0.05)
    except:
        pass


async def run_tk(simu, interval=0.05):
    '''
    Run a tkinter app in an asyncio event loop.
    '''
    try:
        while True:
            simu.window.root.update()
            await asyncio.sleep(interval)

    except tcl as e:
        if "application has been destroyed" not in e.args[0]:
            raise

async def main():
    n_boids = 3
    l_pos = [np.array([110,120]),np.array([160,170]),np.array([160,190])]
    l_v = [np.array([5,5]),np.array([5,-5]),np.array([5,-5])]
    l_maxv = [40]
    l_maxa = [40]
    l_view_range = [100]
    l_view_angle = [80]
    w = np.array([500,500])
    b_cond = 0

    n = 300
    global simul
    simul = simulation.Simulation(n_boids,l_pos,l_v,l_maxv,l_maxa,l_view_range,l_view_angle,w,b_cond)

    await run_tk(simul, 0.01)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
