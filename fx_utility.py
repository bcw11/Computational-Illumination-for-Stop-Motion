import os
import cv2 as cv
from re import findall as re_findall
from datetime import datetime as dt
import fx_common as fx # shared globals

# Effects imports
import fx_cycle
import fx_daycycle
import fx_disco
import fx_lightning
import fx_police_lights
import fx_underwater


def load_frames(src_dir: str, camera: int):
    """Setup shared FRAMES array"""
    fx.FRAMES = {i:[] for i in range(1, fx.NUM_LIGHTS+1)}

    camera_dir = f"{src_dir}/camera{camera}"
    images = [file for file in os.listdir(camera_dir) if file.endswith('.png')]
    images.sort()

    for img in images:
        [light, _] = map(int, re_findall(r'\d+', img))
        # print(f"Reading: camera {camera} light {light} frame {frame}: {img}")
        im = cv.imread(os.path.join(camera_dir, img))
        assert im is not None, f"File couldn't be read at path={os.path.join(camera_dir, img)}"

        fx.FRAMES[light].append(im)
        # fx.FRAMES[light].append(img)

def zoom(wide: bool, camera: int):
    CROP_COORS = {
        True: {
            1: (670, 342),2: (670, 342),3: (500, 342),4: (670, 434),
            5: (670, 434),6: (400, 690),7: (670, 342),8: (750, 690),},
        False: {
            1: (1082, 342),2: (1082, 342),3: (912, 342),4: (1082, 434),
            5: (1082, 434),6: (812, 690),7: (1082, 342),8: (1082, 690),}
    }
    size = (1920, 1013) if wide else (1280, 960)
    crop = (1455, 2760) if wide else (1455, 1940)

    x, y = CROP_COORS[wide][camera]
    for l_idx in range(1, 4):
        for f_idx in range(0, fx.NUM_FRAMES):
            # crop & resize
            img = fx.FRAMES[l_idx][f_idx][y:y+crop[0], x:x+crop[1]]
            fx.FRAMES[l_idx][f_idx] = cv.resize(img, size)

def apply_effect():
    effect = fx.ARGS.effect
    if effect == "cycle":
        fx_cycle.fx_cycle(fx.ARGS.lights, fx.ARGS.t_rate)
    elif effect == "daycycle":
        fx_daycycle.fx_daycycle(2)
    elif effect == "disco":
        fx_disco.fx_disco()
    elif effect == "lightning":
        fx_lightning.fx_lightning()
    elif effect == "police lights":
        fx_police_lights.fx_police_lights(fx.ARGS.lights)
    elif effect == "underwater":
        fx_underwater.fx_underwater()

def render_video(verbose: bool):
    """Render frames out to a mp4 video"""
    assert len(fx.OUT_FRAMES) != 0, f"Nothing to render in fx.OUT_FRAMES"

    d = dt.now()
    filename = f"render_{d.year}-{d.month}-{d.day}-{d.hour}:{d.minute}:{d.second}.mp4"
    size = fx.OUT_FRAMES[0].shape
    size = (size[1], size[0])

    video = cv.VideoWriter(filename, cv.VideoWriter_fourcc(*'mp4v'), fx.FPS, size)
    for idx, frame in enumerate(fx.OUT_FRAMES):
        # video.write(cv.cvtColor(frame, cv.COLOR_RGB2BGR))
        video.write(frame)
        if verbose:
            os.mkdir(f"frames_{filename}")
            cv.imwrite(f"frames_{filename}/frame-{idx+1:03d}.png", frame)
    video.release()

    cv.destroyAllWindows() # NOTE: need?
    print("Video render complete")

if __name__ == "__main__":
    print("TODO: impl some testing option here. Call editor.py for now.")
    exit()
