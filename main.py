from threading import Thread
from classify_frame import FrameClassifier
from classify_video import VideoClassifier
from video_input import VideoInput
#from mock_classify_frame import MockFrameClassifier
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
    parser.add_argument('--labels-file', default='./labels.txt', type=str)
    args = parser.parse_args()

    with open(args.labels_file, 'r') as lf:
        # todo: possible that only first ??? line needs to be removed
        labels = [line.strip() for line in lf]

    if args.video_file != '':
        input_stream = VideoInput(filename=args.video_file)
    else:
        input_stream = VideoInput()

    interpreter = Interpreter(
            model_path=args.model_file)#,
            #experimental_delegates=[load_delegate('libedgetpu.so.1.0')] # remove the load delegate if coral TPU is not being leveraged
            #)
    interpreter.allocate_tensors()

    print("Allocated tensors")

    #frame_classifier = MockFrameClassifier()
    frame_classifier = FrameClassifier(interpreter, args.thresh, labels)
    video_classifier = VideoClassifier(
            input_stream,
            frame_classifier,
            args.output_dir,
            args.prefix,
            tolerance_secs=args.tolerance
    )
    signal(SIGINT, input_stream.stop_vid)
    reader_thread = Thread(target=input_stream.start)
    
    print('Starting video reader thread')
    reader_thread.start()
    print('Video reader thread started')

    video_classifier.run()
    reader_thread.join()

    print("Done!")

if __name__ == '__main__':
    main()
