# Spec
This program takes in a .tflite file and a video file. It reads the video's frames
and, upon identifying an object based on the tflite file, starts writing the output
to a new video file. Once the object has left the frame (for a (configurable) while),
it closes that file. When it sees an object again, the process repeats.

## Run It

Run the following to show a help message detailing inputs accepted by the program:

```shell
$ python main.py -h
```

## Files
- `main.py`: parse args, setup dependencies, run video reader thread, run inference (blocking)
- `video_input.py`: contains class that reads frames from video and writes to queue (in own thread)
  - also has method for reading from queue to be used by main thread
- `classify_video.py`: classification at video level; video output details
- `classify_frame.py`: classification at frame level; used by `classify_video.py`
- `models`: directory containing .tflite files (useful for testing)

## Known Issue

Due to (perhaps) a race condition in the tflite interpreter destructor code, the program
occasionally prints `Segmentation fault` at the end of running. As long as you see this
after "Done" is printed, rest assured that the program completed normally.
