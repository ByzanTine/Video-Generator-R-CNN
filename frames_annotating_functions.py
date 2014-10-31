import os
import copy
import time
import sys
import logging
import numpy as np
import shutil
import cv2


def class2color(class_id):
    if class_id is 1:
        return (0, 0, 255) # Red
    if class_id is 2:
        return (0, 255, 0) # Green
    if class_id is 3:
        return (255, 0, 0) # Blue
    if class_id is 4:
        return (0, 255, 255) # Yellow
    
    # TODO: Does not really work. Always outputs a blackish color for small class IDs.
    '''
    # simple alogrithm for color mapping
    red = class_label % 4
    grn = (class_label / 4) % 4 
    blu = (class_label / 16) % 4
    return (red, grn, blu)
    '''

def class2label(class_id):
    return('epiglottis', 'vocalcord', 'trachea', 'carina')[class_id - 1]
    
def annotated_frame(frame, xmin, ymin, xmax, ymax, color=(0, 0, 255), label=None):
    new_frame = copy.copy(frame)
    # draw = ImageDraw.Draw(new_frame)
    # draw.rectangle(((xmin, ymin), (xmax, ymax)), outline='red')
    cv2.rectangle(new_frame, (xmin, ymin), (xmax, ymax), color)
    if label is not None:
        cv2.putText(new_frame, label, (xmin + 3, ymax - 3), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color)
    return new_frame

def annotated_frames_from_folder(folder, label_file, output_folder=None):
    '''
    TODO: Get rid of output_folder ...

    The label_file is expected to have the following structure:
        frame_name (less the extension, which is expected to be jpg), xmin, ymin, xmax, ymax

    Each frame should be located in the folder.
    
    Annotated frames will be saved in output_folder if it is specified.

    Returns a list of cv2 images.
    '''
    if output_folder is not None:
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        elif os.listdir(output_folder) != []:
            print 'output_folder \'' + output_folder + '\' is not empty. ' + \
                  'The frames in the (input) folder \'' + folder + '\' will not be annotated.'
            sys.exit(0)
    annotated_frames = []
    tic = time.clock()
    with open(label_file) as file:
        lines = file.readlines()
        num_frames = len(lines)
        print 'About to annotate ' + str(num_frames) + ' frames'
        print
        for line in lines:
            line_elements = line.split()
            
            '''
            TODO: Handle the fact that some label file contain filenames with
            extension and some contain filenames without extension.
            '''
            # frame_filename = line_elements[0]
            frame_filename = line_elements[0] + '.jpg'
            
            frame_path = os.path.join(folder, frame_filename)
            print 'Annotating frame ' + frame_filename + ' ...'
            # frame = Image.open(frame_path)
            frame = cv2.imread(frame_path)
            if frame is None:
                logging.error('Frame not Exist')
                exit(1)
            if output_folder is not None:
                output_path = os.path.join(output_folder, frame_filename)
            xmin = float(line_elements[1])
            ymin = float(line_elements[2])
            xmax = float(line_elements[3])
            ymax = float(line_elements[4])
            # class_color = (255, 0, 0) # (0, 0, 255)
            if len(line_elements) > 5 and int(line_elements[5]) > 0:
                class_id = int(line_elements[5])
                class_color = class2color(class_id)
                class_label = class2label(class_id)
            box = np.asarray((xmin, ymin, xmax, ymax))
            if np.any(box != 0):
                new_frame = annotated_frame(frame,
                                            int(xmin), int(ymin), int(xmax), int(ymax),
                                            class_color, 
                                            class_label)
                annotated_frames.append(new_frame)
                if output_folder is not None:
                    # new_frame.save(output_path)
                    cv2.imwrite(output_path, new_frame)
            else:
                annotated_frames.append(frame)
                if output_folder is not None:
                    shutil.copy(frame_path, output_path)
    toc = time.clock()
    duration = toc - tic
    print
    print str(num_frames) + ' frames were annotated in ' + str(duration) + ' seconds.'
    print 'The average processing time was ' + str(duration / num_frames) + ' seconds per frame.'
    return annotated_frames


if __name__ == '__main__':
    # annotated_frame('VID009_1_3179.jpg', 50, 50, 100, 100)
    annotated_frames = annotated_frames_from_folder('/mnt/neocortex/scratch/hkuhn/Intubation/datasets/VID009_data_set_01/vocalcord/JPEGImages',
                                                    'carina_det.txt') # ,
                                                    # 'labeled_frames')
