import time
import cv2
import sys
import logging


class VideoGenerator(object):

    def generate(self, frames, video_filename=None):
        '''
        Generates a avi file from a list of frames.
        
        video_output will be set to 'video.avi' if not specified.
        '''
        if video_filename is None:
            video_filename = 'video.avi'
        height, width = frames[0].shape[0:2]
        video_writer = cv2.VideoWriter(video_filename,
                                       cv2.cv.CV_FOURCC('M', 'J', 'P', 'G'),
                                       25,
                                       (width, height))
        tic = time.clock()
        for frame in frames:
           video_writer.write(frame)
        del video_writer
        toc = time.clock()
        duration = toc - tic
        num_frames = len(frames)
        print 'A video was generated from ' + str(num_frames) + ' frames in ' + \
              str(duration) + ' seconds.'
        print 'The average processing time was ' + str(duration / num_frames) + \
              ' seconds per frame.'

if __name__ == "__main__":
    import frames_annotating_functions as fa

    # TODO: Ordering the videos ...
    
    logging.basicConfig(level=logging.DEBUG);
    if len(sys.argv) < 3:
        logging.error('Not Enough Argument!')
        logging.info('Usage:\n\t python video_generator.py /path/to/frames/ /path/to/prediction_file')
	exit(1)
    # annotated_frames = fa.annotated_frames_from_folder('/mnt/neocortex/scratch/yejiayu/data/manikin_07/', 'combine_regr_07_thresholded.txt')
    logging.info('Target Frames:' + sys.argv[1])
    annotated_frames = fa.annotated_frames_from_folder(sys.argv[1], sys.argv[2])
    if len(sys.argv) == 4:
        VideoGenerator().generate(annotated_frames, sys.argv[3])
    else:
        VideoGenerator().generate(annotated_frames)
