import os
import cv2 as cv
import fx_common as fx
import argparse

# FX imports
import fx_utility as fx_util
"""Effects:
    - cycle
    - daycycle
    - disco
    - lightning
    - police lights
    - underwater
"""

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='Editor.py',
        description='Applies effects to stop motion frames'
    )

    parser.add_argument('--camera-dir', dest='camera_dir', required=True,
                        help="Path to cameras folder")

    parser.add_argument('--camera', type=int, choices=range(1, 9), required=True,
                        help="Number of camera to pull frames from")

    parser.add_argument('--effect', required=True,
                        choices=['cycle', 'daycycle', 'disco', 'lightning', 'police', 'underwater'],
                        help="Name of the effect to apply")
    # parser.add_argument('--args', nargs='*', default = [],
    #                     help='Effect specific arguments, defaults used if not provided. List args space separated')

    parser.add_argument('--lights', nargs='*', default = [1, 2], required=False,
                        help=('Light number args for police and cycle effects. Default = [1, 2]. '
                              'Police: light nums for red and blue (ordered) | Cycle: Order of light nums to transition between'))

    parser.add_argument('--t-rate', dest='t_rate', default=10, required=False,
                        help='Argument for cycle effect, number of frames to transition between 2 lights. Default 10')

    parser.add_argument('--zoom', choices=['wide', 'square'], required=False,
                        help="Flag to crop & resize frames to FHD. wide=16:9, square=4:3")

    parser.add_argument('--verbose', action='store_true', default=False,
                        help="Output indivitual frames along with video output")
    fx.ARGS = parser.parse_args()
    print(fx.ARGS)
    # exit()
    print("Beginning....")
    cv.setUseOptimized(True)

    # if len(sys.argv) != 8: # camera_path camera_num effect
    #     print("Usage: python3 editor.py <path_to_cameras> <camera_num> <effect_name> ")
    #     exit(-1)

    # # TODO: add start end assertions here
    # _, src_dir, camera = sys.argv
    # assert os.path.exists(src_dir), f"Invalid path: {src_dir}"

    camera_dir = fx.ARGS.camera_dir
    camera = fx.ARGS.camera
    assert os.path.exists(camera_dir), f"[Editor] Invalid camera dir {camera_dir}"

    fx_util.load_frames(camera_dir, camera)
    if fx.ARGS.zoom:
        fx_util.zoom(fx.ARGS.zoom == 'wide', camera)

    # TODO: call effects applier function
    fx_util.apply_effect()
    fx_util.render_video(fx.ARGS.verbose)
    # print(f"Camera {camera} w/ {len(fx.FRAMES.keys())} lights & frames {len(fx.FRAMES[2])} per light")
    # print(fx.FRAMES[1][0].shape[:2])