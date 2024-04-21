import cv2 as cv
import numpy as np
import fx_common as fx # shared globals


def __day_v1(start: int, end: int):
    for f_idx in range(0, end - start):
        alpha = [0.33*(0.4*(np.sin((f_idx/np.pi) + np.pi/2) + 1.5))]

        img = cv.addWeighted(fx.FRAMES[1], alpha, fx.FRAMES[2], alpha, 0)
        fx.OUT_FRAMES.append(cv.addWeighted(img, 1, fx.FRAMES[3], alpha, 0))


def __day_v2(start: int, end: int):
    alpha = 0.33

    for f_idx in range(0, end - start):
        img = cv.addWeighted(fx.FRAMES[1][f_idx], alpha,
                             fx.FRAMES[2][f_idx], alpha, 0)
        img = cv.addWeighted(img, 1, fx.FRAMES[3][f_idx], alpha, 0)

        fx_val = np.sin( (f_idx/np.pi) + np.pi/2 )
        img[:, :, 2] = img[:, :, 2]*( 0.5*(fx_val+1))
        img[:, :, 1] = img[:, :, 1]*(0.25*(fx_val+3))
        img[:, :, 0] = img[:, :, 0](0.1*(fx_val+9))

        fx.OUT_FRAMES.append(img) # NOTE: just leave in bgr

def fx_daycycle(version: int):
    """Creates a day night cycle effect
    version: specify version of the effect to use, 1 or 2
    start: starting frame index, default 0
    end: ending frame index, default fx.NUM_FRAMES
    """
    assert version in [1, 2], "[fx_daycycle] Unknown version"

    if version == 1:
        __day_v1(0, fx.NUM_FRAMES)
    else:
        __day_v2(0, fx.NUM_FRAMES)


if __name__ == "__main__":
    print("TODO: impl some testing option here. Call editor.py for now.")
    exit()
