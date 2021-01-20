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

    n_boids = 3
    l_pos = [np.array([110, 120]), np.array([160, 170]), np.array([160, 190])]
    l_v = [np.array([5, 5]), np.array([5, -5]), np.array([5, -5])]
    l_maxv = [40]
    l_maxa = [40]
    l_view_range = [100]
    l_view_angle = [80]
    w = np.array([500, 500])
    b_cond = 0

    tk_window = MainFrame(n_boids, l_pos, l_v, l_maxv, l_maxa, l_view_range, l_view_angle, w, b_cond)

    asyncio.get_event_loop().run_until_complete(await_inf_loop(tk_window))
