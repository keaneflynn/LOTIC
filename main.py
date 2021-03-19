from threading import Thread
from classify_frame import FrameClassifier
from classify_video import VideoClassifier
from video_input import VideoInput
from mock_classify_frame import MockFrameClassifier
from signal import signal, SIGINT
from argparse import ArgumentParser
from tflite_runtime.interpreter import Interpreter, load_delegate

def main():
    parser = ArgumentParser()
    parser.add_argument('--video-file', default="", type=str)
    parser.add_argument('--output-dir', default="./out", type=str)
    parser.add_argument('--prefix', default='vid_out', type=str)
    parser.add_argument('--thresh', default=.5, help="confidence threshold (float)", type=float)
    parser.add_argument('--tolerance', default=10, help='Tolerance time (seconds)', type=int)
    parser.add_argument('--model-file', type=str)
    args = parser.parse_args()
    print(args)

    if args.video_file != '':
        input_stream = VideoInput(filename=args.video_file)
    else:
        input_stream = VideoInput()

    interpreter = Interpreter(
            model_path=args.model_file,
            experimental_delegates=[load_delegate('libedgetpu.so.1.0')]
            )

    #frame_classifier = MockFrameClassifier()
    frame_classifier = FrameClassifier(interpreter, thresh)
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
