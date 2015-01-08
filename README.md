# N-Class Prediction Combine and Video Generation
For the usage of RCNN Prediction Combined

## USAGE

	sh pipe.sh /path/to/frames /path/to/detection video_name

## INPUT 

R-CNN prediction file (intermediate result)
See Samples if you are not clear ./sample/vocalcord_det.txt

	Content: index 	 score     xmin ymin xmax ymax
		 	 07_0123 -1.062129 45   97   68   118
Also for video generation, you need corresponding frames
## OUTPUT

The Video, the ap_result(for better threshold bounding)
The default value of the score filtering will be -1 for all class

## PIPELINE

N-Class files(.txt) -> maxjoin.py -> single prediction file(.txt)
single prediction file -> threshold_image.py -> filtered_pred file(.txt)
Frames and filtered file -> video_generator.py -> video

## GENERAL NOTICE

Video_generator will find the corresponding images by the reference in prediction list. So as long as the prediciton list is consistent and image exist, then it will work.



