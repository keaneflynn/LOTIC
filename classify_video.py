import os
import cv2
from time import time
from classification import Stats

class VideoClassifier:
    def __init__(
            self,
            input_stream,
            frame_classifier,
            output_dir,
            fname_prefix,
            tolerance_secs=10,
            ):
        self.input_stream = input_stream
        self.frame_classifier = frame_classifier
        self.output_dir = output_dir
        self.fname_prefix = fname_prefix
        self.tolerance_secs = tolerance_secs
        self.frame_rate = int(self.input_stream.get_frame_rate())
        self.last_found_time = 0
        self.num_read = 0

    def time_since_last_found(self):
        if self.input_stream.is_live:
            return time() - self.last_found_time
        return (self.num_read / self.frame_rate) - self.last_found_time

    def update_time_offset(self):
        if self.input_stream.is_live:
            self.last_found_time = time()
        else:
            self.last_found_time = self.num_read / self.frame_rate

    def run(self):
        outfile_idx = 0
        dims = self.input_stream.get_dims()
        self.num_read = 1
        frame = self.input_stream.read()
        self.last_found_time = time() if self.input_stream.is_live else 0
        while frame is not None:
            outfile_idx += 1
            outfile = os.path.join(self.output_dir, f'{self.fname_prefix}_{outfile_idx}.mp4')
            json_outfile = os.path.join(self.output_dir, f'{self.fname_prefix}_{outfile_idx}.json')
            started = False
            while frame is not None:
                self.num_read += 1
                cfc = self.frame_classifier.classify(frame)
                found = len(cfc.items) > 0
                frame = self.input_stream.read()
                if started:
                    vid_out.write(cfc.frame)
                    stats.observe(cfc)
                    if found:
                        self.update_time_offset()
                    else:
                        if self.time_since_last_found() > self.tolerance_secs:
                            vid_out.release()
                            stats.finish()
                            json_stats = stats.to_json()
                            with open(json_outfile, 'w') as json_fout:
                                json_fout.write(json_stats)
                            break
                else:
                    if found:
                        vid_out = cv2.VideoWriter(outfile, fourcc=cv2.VideoWriter_fourcc(*'mp4v'), fps=int(self.frame_rate), frameSize=dims)
                        stats = Stats(outfile)
                        started = True
                        self.update_time_offset()
                        vid_out.write(cfc.frame)
                        stats.observe(cfc) 
                    else:
                        pass
