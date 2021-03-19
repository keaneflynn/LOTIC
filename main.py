from threading import Thread
from classify_frame import FrameClassifier
from classify_video import VideoClassifier
from video_input import VideoInput
from mock_classify_frame import MockFrameClassifier
from signal import signal, SIGINT
from argparse import ArgumentParser

def main():
    parser = ArgumentParser()
    parser.add_argument('--video-file', default="", type=str)
    parser.add_argument('--output-dir', default="./out", type=str)
    parser.add_argument('--prefix', default='vid_out', type=str)
    parser.add_argument('--thresh', default=.5, help="confidence threshold (float)", type=float)
    parser.add_argument('--tolerance', default=10, help='Tolerance time (seconds)', type=int)
    args = parser.parse_args()
    print(args)

    if args.video_file != '':
        input_stream = VideoInput(filename=args.video_file)
    else:
        input_stream = VideoInput()

    frame_classifier = MockFrameClassifier()
    # frame_classifier = todo
    video_classifier = VideoClassifier(
            input_stream,
            frame_classifier,
            args.output_dir,
            args.prefix,
            tolerance_secs=args.tolerance
    )
    signal(SIGINT, input_stream.stop_vid)
    reader_thread = Thread(target=input_stream.start)
    reader_thread.start()
    video_classifier.run()

if __name__ == '__main__':
    main()
