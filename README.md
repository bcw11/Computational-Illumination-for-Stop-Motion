# Computational-Illumination-for-Stop-Motion

**Main Idea**
Interpolate view and lighting of stop-motion scenes

**Motivation**
Specifically stop-motion because we can capture different lighting and views per frame, not possible in real time capture. Post production fix or stylistic choice for camera angle and lighting

**Final Product**
Application demo of view and lighting interpolation of captured scene with different angles and lighting

## Usage
To apply effects:
```
$ python3.9 main.py --help
usage: Editor.py [-h] --camera-dir CAMERA_DIR --camera {1,2,3,4,5,6,7,8} --effect
                 {cycle,daycycle,disco,lightning,police,underwater} [--lights [LIGHTS ...]] [--t-rate T_RATE]
                 [--zoom {wide,square}] [--verbose]

Applies effects to stop motion frames

optional arguments:
  -h, --help            show this help message and exit
  --camera-dir CAMERA_DIR
                        Path to cameras folder
  --camera {1,2,3,4,5,6,7,8}
                        Number of camera to pull frames from
  --effect {cycle,daycycle,disco,lightning,police,underwater}
                        Name of the effect to apply
  --lights [LIGHTS ...]
                        Light number args for police and cycle effects. Default = [1, 2]. Police: light nums for red
                        and blue (ordered) | Cycle: Order of light nums to transition between
  --t-rate T_RATE       Argument for cycle effect, number of frames to transition between 2 lights. Default 10
  --zoom {wide,square}  Flag to crop & resize frames to FHD. wide=16:9, square=4:3
  --verbose             Output indivitual frames along with video output
```