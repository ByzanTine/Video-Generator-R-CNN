import sys
import os
import numpy as np

#Specify the threshold the score you want to use
thresholds = [-1, -1, -1, -1]

# detection_file = 'combine_regr_11'
detection_file = sys.argv[1]
# frame_id, score, x_min, y_min, x_max, y_max, label

output_file = os.path.splitext(detection_file)[0] # We get rid of the extension.
output_file = open(output_file + '_thresholded', 'w')

with open(detection_file) as input_file:
    for line in input_file:
        line_elements = line.split()
        score = float(line_elements[1])
        label = int(line_elements[6])
        frame_id = str(line_elements[0])
        if score >= thresholds[label - 1]:
            bounding_box = " ".join(line_elements[2:6])
            new_line = " ".join([frame_id, bounding_box, str(label), '\n'])
        else:
            new_line = frame_id + ' 0 0 0 0 0 \n'
        output_file.write(new_line)

output_file.close()
