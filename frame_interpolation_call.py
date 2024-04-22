import replicate
from dotenv import load_dotenv
import time

load_dotenv()

start = time.time()

path = 'D:\Downloads\\Raw Camera Pan.mp4'

input = {
    "mp4": open(path, 'rb'),
    "num_interpolation_steps": 1,
    "playback_frames_per_second": 30
}

output = replicate.run(
    "zsxkib/film-frame-interpolation-for-large-motion:222d67420da179935a68afff47093bab48705fe9e09c3c79268c1eb2ee7c5e91",
    input=input
)

end = time.time()

print(output, f'time took: {end-start}')