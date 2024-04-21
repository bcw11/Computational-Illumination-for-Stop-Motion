# Shared globals across modules
FRAMES = {} # dict { key=light_num : value=[ordered list of cv::Mat images] }
OUT_FRAMES = []
FPS = 10
NUM_CAMS = 8
NUM_LIGHTS = 3
NUM_FRAMES = 59
ARGS = None
# Shared utility functions
import cv2 as cv

def show(title, img):
    """Utility func to show images at 720, so window fits screen"""
    cv.imshow(title, cv.resize(img, (1280, 720)))
    cv.waitKey(0)
    cv.destroyAllWindows()
