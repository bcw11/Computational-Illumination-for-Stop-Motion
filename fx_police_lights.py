import cv2 as cv
import numpy as np
import fx_common as fx # shared globals


def fx_police_lights(l_red, l_blue):
    """Creates effect of police lights flashing
    - l_red: light num to use for red flashes
    - l_blue: light num to use for blue flashes
    """

    alpha = 0.33
    for f_idx in range(0, fx.NUM_FRAMES):

        # red light
        if f_idx > 2:
            fx_val = np.ceil(93*(np.sin((4*f_idx/np.pi) + np.pi/2))+93)
            lim = 255 - fx_val
            gray = cv.cvtColor(fx.FRAMES[l_red][f_idx], cv.COLOR_RGB2GRAY)
            fx.FRAMES[l_red][f_idx][gray > lim, 0] = 255

        # blue light
        fx_val = np.ceil(93*(np.sin((4*f_idx/np.pi) - np.pi/2))+93)
        lim = 255 - fx_val
        gray = cv.cvtColor(fx.FRAMES[l_blue][f_idx], cv.COLOR_RGB2GRAY)
        fx.FRAMES[l_blue][f_idx][gray > lim, 2] = 255

        img = cv.addWeighted(fx.FRAMES[1][f_idx], alpha,
                             fx.FRAMES[2][f_idx], alpha, 0)
        img = cv.addWeighted(img, 1, fx.FRAMES[3][f_idx], alpha, 0)
        fx.OUT_FRAMES.append(img)

if __name__ == "__main__":
    print("TODO: impl some testing option here. Call editor.py for now.")
    exit()
