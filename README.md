# LOTIC Introduction
Welcome to LOTIC (Lightweight Object Tracking Image Capturer)! This program has been designed for underwater use with a Tensorflow Lite object detection model to record out migrating juvenile salmonids, however with slight tweaks it can be reconfigured for any object detection project. The use of the following files and scripts will result in a Raspberry Pi computer that, on startup, will perform live object detection at over 20fps. The output from this object detection model is a video record with a bounding box around your object of interest with a timestamp as well as an additional  file containing time of first observation, species ID, duration in frame, and count of total observations. For ease of back-end data configuration, this file is output in .json format. 

## Necessary Hardware
This currently makes use of the following hardware (however we intend to update it with whatever more efficient hardware becomes available):
* Raspberry Pi 4 B
  * Raspbian OS
* Raspberry Pi Camera Unit (although it should work with any camera input (untested) )
* Google Coral TPU
* Some sort of active cooling for CPU (imperative if raspi is overclocked)


## Spec
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
