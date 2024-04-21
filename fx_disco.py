import cv2 as cv
import numpy as np
import fx_common as fx # shared globals


def fx_disco():
    """Created an effect of disco lights"""

    alpha = 0.33
    for f_idx in range(0, fx.NUM_FRAMES):
        img = cv.addWeighted(fx.FRAMES[1][f_idx], alpha,
                             fx.FRAMES[2][f_idx], alpha, 0)
        img = cv.addWeighted(img, 1, fx.FRAMES[3][f_idx], alpha, 0)

        fx_val = f_idx % 12
        if fx_val in [0, 1]:
            img[:,:, 0] = 0.3*img[:,:, 0]
            img[:,:, 1] = 0.3*img[:,:, 1]
        elif fx_val in [2, 3]:
            img[:,:, 2] = 0.3*img[:,:, 2]
        elif fx_val in [4, 5]:
            img[:,:, 0] = 0.3*img[:,:, 0]
        elif fx_val in [6, 7]:
            img[:,:, 1] = 0.3*img[:,:, 1]
        elif fx_val in [8, 9]:
            img[:,:, 0] = 0.3*img[:,:, 0]
            img[:,:, 1] = 0.3*img[:,:, 1]
        elif fx_val in [10, 11]:
            img[:,:, 0] = 0.3*img[:,:, 0]
            img[:,:, 2] = 0.3*img[:,:, 2]

        fx.OUT_FRAMES.append(img)

if __name__ == "__main__":
    print("TODO: impl some testing option here. Call editor.py for now.")
    exit()
