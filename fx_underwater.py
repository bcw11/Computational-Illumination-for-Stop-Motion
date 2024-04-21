import cv2 as cv
import numpy as np
import fx_common as fx # shared globals


def fx_underwater():
    """Creates an underwater effect. NOTE: looks more like a night time effect"""

    alpha = 0.33
    for f_idx in range(0, fx.NUM_FRAMES):
        img = cv.addWeighted(fx.FRAMES[1][f_idx], alpha,
                             fx.FRAMES[2][f_idx], alpha, 0)
        img = cv.addWeighted(img, 1, fx.FRAMES[3], alpha, 0)

        img[:, :, 0] = 0
        img[:, :, 1] = img[:, :, 1]/2
        fx.OUT_FRAMES.append(img)

if __name__ == "__main__":
    print("TODO: impl some testing option here. Call editor.py for now.")
    exit()
