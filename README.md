# **LOTIC**
Open source code developed by Keane Flynn, Ryan Flynn, and Gabriel Rossi (2021) for fisheries research on the north coast of California

## **Introduction**
Welcome to LOTIC (Lightweight Object Tracking Image Capturer)! This program has been designed for underwater use with a Tensorflow Lite object detection model to record out migrating juvenile salmonids, however with slight tweaks it can be reconfigured for any object detection project. The use of the following files and scripts will result in a Raspberry Pi computer that, on startup, will perform live object detection at over 20fps. The output from this object detection model is a video record with a bounding box around your object of interest with a timestamp as well as an additional  file containing time of first observation, species ID, duration in frame, and count of total observations. For ease of back-end data configuration, this file is output in .json format. 


## **Example Output**
![LOTIC performing salmonid identification on a tributary of the South Fork Eel River](https://github.com/keaneflynn/LOTIC/blob/main/media/fish.gif)

*LOTIC performing salmonid identification on a tributary of the South Fork Eel River*

![LOTIC performing adult salmonid identification on the mainstem Russian River](https://github.com/keaneflynn/LOTIC/blob/main/media/mirabelSample.GIF)

*LOTIC performing adult salmonid identification on the mainstem Russian River (video courtesy of Sonoma Water)*


## **Necessary Hardware**
This currently makes use of the following hardware (however we intend to update it with whatever more efficient hardware becomes available):
* Raspberry Pi 4 B
  * Raspbian OS
* Raspberry Pi Camera Unit (although it should work with any auxiliary camera input (untested) )
* Google Coral TPU
* Some additional storage unit (although a large capacity SD card in the RasPi should suffice)
* Some sort of active cooling for CPU (imperative if raspi is overclocked)
* Blue Robotics 4" tube (aluminum tube helps with cooling while submerged), clear face plate, potted back plate, and necessary sealing gaskets
* Plenty of marine grade plywood to craft weir and flume to your specifications
* Two waterproof cat 6 cables to run from battery storage box to submersed computer unit (used for powering and data transfer)
* Buck Converter 24 volt to 5 volt 3 amp to power RasPi (wired in tube) from car batteries wired in series
* Two 12 volt car batteries connected to charge controller and solar panels for remote powering
* Miscelaneous wiring equipment

![Configuration diagram for installation in creek](https://github.com/keaneflynn/LOTIC/blob/main/media/LOTIC-InStream.png)

*Configuration diagram for installation in creek*

![Video weir installed in Willow Creek](https://github.com/keaneflynn/LOTIC/blob/main/media/InstalledVideoWeir.jpg)

*Video weir installed in Willow Creek*

![Video weir submersible tube placement](https://github.com/keaneflynn/LOTIC/blob/main/media/VideoWeir.jpeg)

*Video weir submersible tube placement*

![LOTIC submersible tube component containing computer and camera](https://github.com/keaneflynn/LOTIC/blob/main/media/LOTICtube.png)

*LOTIC submersible tube component containing computer and camera*

![Lock box containing car batteries, excess wiring, and charge controller from solar panel](https://github.com/keaneflynn/LOTIC/blob/main/media/LockBox.jpg)

*Lock box containing car batteries, excess wiring, and charge controller from solar panel*

![Solar panels placed 20 meters from lock box for better, direct sunlight](https://github.com/keaneflynn/LOTIC/blob/main/media/SolarPower.jpeg)

*Solar panels placed 20 meters from lock box for better, direct sunlight*


## **Inference Specifications**
This program takes in a .tflite file (converted into an edgetpu compatible .tflite file) and a video file or video stream. It reads the video's frames
and, upon identifying an object based on the tflite file, starts writing the output
to a new video and json file. Once the object has left the frame for a configurable amount of time,
it closes that file. When it sees an object again, the process repeats.

## **Run It**

Run the following to show a help message detailing inputs accepted by the program:

```shell
$ python main.py -h
```

## **Relevant Files**
- `main.py`: parse args, setup dependencies, run video reader thread, run inference (blocking)
- `video_input.py`: contains class that reads frames from video and writes to queue (in own thread)
  - also has method for reading from queue to be used by main thread
- `classify_video.py`: classification at video level; video output details
- `classify_frame.py`: classification at frame level; used by `classify_video.py`
- `classification.py`: classification for .json file output; used by `classify_frame.py` and `classify_video.py`
- `models`: directory containing .tflite files (useful for testing)
- `lotic.service`: a service file to be placed in systemd of the RasPi to allow the program to run on boot or reboot on failure

## **Known Issue**
Due to (perhaps) a race condition in the tflite interpreter destructor code, the program
occasionally prints `Segmentation fault` at the end of running. As long as you see this
after "Done" is printed, rest assured that the program completed normally.

Machine learning models will be updated as regularly as I can to improve object detection results from more species with more accuracy, these models are still being beta tested and have some issues. With more images these will hopefully be updated in the near future.
