import numpy as np
import asyncio
from Interface_Graphique import run_tk, MainFrame



async def await_inf_loop(window):
    """
    Tell __main__ to wait for the tk loop to finish.
    The infinite loop will end when an error occurs => the window is closed.

    Parameters:
        window: Entire tk_window that will be display on screen

    Variables:
        refresh_time: Time it takes for the windows to update and acknowledge changes.
    """

    refresh_time = 0.01
    await run_tk(window, refresh_time)


if __name__ == "__main__":
    rng = np.random.default_rng()
    
    n_boids = 3
    w = np.array([500, 500])
    l_pos = [rng.random(2)*w for ii in range(n_boids)]
    l_v = [(rng.random(2)-0.5)*3 for ii in range(n_boids)]
    l_maxv = [10]
    l_maxa = [1]
    l_view_range = [60]
    l_view_angle = [120]
    b_cond = 0
    l_n_binn = [n_binn]

    tk_window = MainFrame(n_boids, l_pos, l_v, l_maxv, l_maxa, l_view_range, l_view_angle, w, b_cond,l_n_binn)

    asyncio.get_event_loop().run_until_complete(await_inf_loop(tk_window))