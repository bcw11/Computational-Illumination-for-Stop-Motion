import cv2 as cv
import numpy as np
import fx_common as fx # shared globals


def fx_lightning():
    """Creates effect of lightning striking"""

    # random choice of lighting frames
    l_idx = np.random.randint(0, fx.NUM_FRAMES, fx.NUM_FRAMES//17+1)

    alpha = [0.33, 0.33, 0.33]

    for f_idx in range(0, fx.NUM_FRAMES):
        if f_idx in l_idx:
            alpha[np.random.randint(0, 2)] = np.random.uniform(1.5, 2.25)

        img = cv.addWeighted(fx.FRAMES[1], alpha[0],
                             fx.FRAMES[2], alpha[1], 0)
        img = cv.addWeighted(img, 1, fx.FRAMES[3], alpha[2], 0)
        fx.OUT_FRAMES.append(img)

if __name__ == "__main__":
    print("TODO: impl some testing option here. Call editor.py for now.")
    exit()
