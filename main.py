import numpy as np
import asyncio
from Interface_Graphique import run_tk, MainFrame


async def main():

    n_boids = 3
    l_pos = [np.array([110, 120]), np.array([160, 170]), np.array([160, 190])]
    l_v = [np.array([5, 5]), np.array([5, -5]), np.array([5, -5])]
    l_maxv = [40]
    l_maxa = [40]
    l_view_range = [100]
    l_view_angle = [80]
    w = np.array([500, 500])
    b_cond = 0

    simu = MainFrame(n_boids, l_pos, l_v, l_maxv, l_maxa, l_view_range, l_view_angle, w, b_cond)

    await run_tk(simu, 0.01)


if __name__ == "__main__":

    asyncio.get_event_loop().run_until_complete(main())
