import numpy
import os
import sys

index_score = []
content = []
filenames = []
# Find the files in the specified folder
# TODO: I don't think we can guarantee the order of os.listdir().
#       I'll sort the list for now and assume that the filenames are specified
#       accordingly (to match the expected order, for the labels for instance).
#       Needs to be rethink.
list = os.listdir(sys.argv[1])
list.sort()
for filename in list:
    print filename
    # Join the path with pwd
    filename=os.path.realpath(sys.argv[1]+filename)
    filenames.append(filename)
    # Extract the score info
    index_score.append(numpy.loadtxt(filename,usecols={1}))
    # Extract the whole info
    content.append(numpy.loadtxt(filename,usecols=range(1,6)))
# e = numpy.loadtxt('epiglottis_det_regr.txt',usecols={1})
# v = numpy.loadtxt('vocalcord_det_regr.txt',usecols={1})
# t = numpy.loadtxt('trachea_det_regr.txt',usecols={1})
# c = numpy.loadtxt('carina_det_regr.txt',usecols={1})

combine = numpy.column_stack(index_score)
arg = numpy.argmax(combine, axis=1)
# content.append(numpy.loadtxt('epiglottis_det_regr.txt',usecols=range(1,6)))
# content.append(numpy.loadtxt('vocalcord_det_regr.txt',usecols=range(1,6)))
# content.append(numpy.loadtxt('trachea_det_regr.txt',usecols=range(1,6)))
# content.append(numpy.loadtxt('carina_det_regr.txt',usecols=range(1,6)))
# Get the index string for final writting
index = numpy.loadtxt(filenames[0],usecols={0},dtype='string')

fid = open(sys.argv[2],'w')
for i in range(0,len(arg)):
    cur_cell = content[arg[i]][i]
   
    cur_class = arg[i] + 1

    fid.write(str(index[i]) +' '+str(cur_cell[0])+' ' + str(int(cur_cell[1]))+ ' '+ str(int(cur_cell[2]))+ ' ' + str(int(cur_cell[3])) + ' '+ str(int(cur_cell[4])) + ' ' + str(cur_class)+'\n')
fid.close()
