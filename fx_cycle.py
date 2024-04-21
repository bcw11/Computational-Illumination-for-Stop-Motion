import cv2 as cv
import numpy as np
import fx_common as fx # shared globals
from itertools import cycle


def fx_cycle(lights: list, t_rate: int):
    """Cycles between different lights
    - lights: list of light num's indicating lights to cycle through in the given order
    - t_rate: number of frames it takes to transition between two lights, default=5"""
    assert len(lights) > 0 and len(lights) <= fx.NUM_LIGHTS, f"[fx_cycle] Invalid lights_order={lights}"
    assert t_rate > 0 and t_rate < fx.FPS, f"[fx_cycle] Invalid t_rate={t_rate}"

    light = cycle(lights)
    l1 = next(light)
    l2 = next(light)
    W = cycle(np.linspace(1, 0, t_rate))
    for f_idx in range(0, fx.NUM_FRAMES):
        alpha = next(W)
        img = cv.addWeighted(fx.FRAMES[l1][f_idx], alpha,
                             fx.FRAMES[l2][f_idx], (1-alpha), 0)
        fx.OUT_FRAMES.append(img)

        # update lights
        if alpha == 0:
            l1 = next(light) if l2 == lights[-1] else l2
            l2 = next(light)

            # if l2 == lights[-1]: # NOTE: should prevent weird back and forth, maybe test w/o this
            #     l1 = next(light)
            #     l2 = next(light)
            # else:
            #     l1 = l2
            #     l2 = next(light)



if __name__ == "__main__":
    print("TODO: impl some testing option here. Call editor.py for now.")
    exit()
