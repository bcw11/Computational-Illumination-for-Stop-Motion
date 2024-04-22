import sys
import os
import re

def rename_frames(camera_dir):
    print(f"Changing dir to {camera_dir}")
    os.chdir(camera_dir)

    files = [file for file in os.listdir() if file.endswith('.png')]
    files.sort(key=lambda x: int(re.search(r'\d+', x).group()))

    with open("frame_renames.txt", "w") as log:
        light = 0
        frame = 1
        for file in files:
            name = f"frame-{light+1}-{frame:03d}.png"
            os.rename(file, name)
            log.write(f"{file} -> {name}\n")

            # update frame and light
            if light == 2:
                frame += 1
            light = (light + 1) % 3

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 sort_frames.py <path_to_camera_dir>")
        exit(-1)
   
    rename_frames(sys.argv[1])
