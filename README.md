# Spec
What we want:
    input: 
        video (live stream or mp4)
        output location for files
    output:
        mp4 files in specified output directory

## Files
- `main.py`: parse args, setup dependencies, call
- `video_file_input.py` - expose video file as input
- `video_stream_input.py` - expose video stream as input
- `classify_video.py` - classification at video level; video output details
- `classify_frame.py` - classification at frame level
