# TODO: Maybe we should threshold before we combine?

# Top Level Interface


# Place to store frames
frame_place=$1
# Place to store detections 
# Make sure there are only class corresponding detection files
# For our case: it's epiglottis_det.txt vocalcord_det.txt trachea_det.txt carina_det.txt

detection_place=$2

# Argument checking 
if [ "$detection_place" == "" ];then
	echo 'DEBUG:INFO: Not Enough Argument!'
	echo 'Usage: '
	echo -e '\t sh pipe.sh /path/to/frame /path/to/detection/'
	exit
fi

# Optional Video name
video_name=$3
if [ "$video_name" == "" ];then
	video_name='video.avi'
fi

# Number of classes will be accumulated with the files
number_classes=0

# Name of the combined list file
combined_list='combined_list'

# Cache Dir
# cache_dir='cache/'$(date +%Y-%m-%d-%T)
# another choice
cache_dir=$detection_place

# Create a tmp folder
mkdir $cache_dir



# Find the files in the detection folder
for file in $(ls $detection_place)
do
	class_file_array[$number_classes]=$file
        # TODO if file is directory, jump for error
	number_lines[$number_classes]=$(cat $detection_place$file | wc -l)
	number_classes=$((number_classes+1))
done

#Consistency Check
for i in $(seq 0 $((number_classes-1)))
do
	echo ${number_lines[i]}
	if [ ${number_lines[i]} -ne ${number_lines[0]} ];then
		echo 'DEBUG:ERROR the file lines doesnot match'
		echo -e '\t' ${class_file_array[i]} ${number_lines[i]}
		echo -e '\t' ${class_file_array[0]} ${number_lines[0]}
		exit
	fi
done


echo 'DEBUG:INFO: Number of Class' $number_classes

# Run the maxjoin and store in cache_dir
python maxjoin.py $detection_place $cache_dir'/'$combined_list
# Run the thresholding and store in cache_dir

python threshold_images.py $cache_dir$combined_list

# Name for the final prediction file

predictio_nclass=$cache_dir'/'$combined_list'_thresholded'

# video generator 
# args: frames directory, combined list, video name(optional)
# python video_generator.py ../../datasets/intubation_rcnn/VOCdevkit/intubation/JPEGImages/ ./sample/combined_bb_07_thresholded.txt 07_bb.avi
python video_generator.py $frame_place $predictio_nclass $cache_dir'/'$video_name

