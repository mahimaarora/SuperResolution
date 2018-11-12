'''
Using OpenCV takes a mp4 video and produces a number of images.
Requirements
----
You require OpenCV 3.2 to be installed.
Run
----
'''

import cv2
import numpy as np
import sys
# sys.path.insert( 0, 'D:\Super-Resolution-master\SR_Project\Application')
from .cnn import *

# from . import cnn

import moviepy.editor as mp
import subprocess
from os.path import isfile, join
import os, shutil
import subprocess

from .cnn_image import process as p_
# from . import cnn_imag

def handle_uploaded_file(testfile):

    # if the file is a video
    # file_path = type(testfile)
    if testfile.endswith('.mp4'):

        # print(testfile)
        #extracting audio from the file
        command = "ffmpeg -i " + testfile + " -ab 160k -ac 2 -ar 44100 -vn media/audio.mp3"

        subprocess.call(command, shell=True)

    # Playing video from file:
        cap = cv2.VideoCapture(testfile)
        # print(type(testfile))
        try:
            if os.path.exists('media/output.mp4'):
                os.remove('media/output.mp4')
        except OSError:
            print('Output buffer already full with video/output.mp4')
        try:
            if os.path.exists('media/video.mp4'):
                os.remove('media/video.mp4')
        except OSError:
            print('Output buffer already full with video/output.mp4')

        try:
            if not os.path.exists('data'):
                os.makedirs('data')
            elif os.path.exists('data'):
                shutil.rmtree('data')
                os.makedirs('data')
        except OSError:
            print('data nahi ban rha')

        currentFrame = 0
        while(True):

            # Capture frame-by-frame
            ret, frame = cap.read()
            if not ret: break
            # Saves image of the current frame in jpg file
            name = './data/frame' + str(currentFrame) + '.png'
            print('Creating...' + name)
            cv2.imwrite(name, frame)

            # To stop duplicate images
            currentFrame += 1


        # When everything done, release the capture

        cap.release()
        cv2.destroyAllWindows()


        process()
        write_video()

        clear_command = 'find . -name "data/*.png" -type f -delete'
        subprocess.call(clear_command, shell=True)

    elif testfile.endswith('jpeg') or testfile.endswith('jpg') or testfile.endswith('png'):
        p_(testfile)

        pass
    else:
        print('Error!!')


def convert_frames_to_video(pathIn,pathOut,fps):
    frame_array = []
    files = [f for f in os.listdir(pathIn) if isfile(join(pathIn, f))]

    #for sorting the file names properly
    files.sort(key = lambda x: int(x[5:-4]))

    for i in range(len(files)):
        filename=pathIn + files[i]
        #reading each files
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width,height)
        print(filename)
        #inserting the frames into an image array
        frame_array.append(img)

    out = cv2.VideoWriter(pathOut, cv2.VideoWriter_fourcc(*'DIVX'), fps, size)

    for i in range(len(frame_array)):
        # writing to a image array
        out.write(frame_array[i])
    out.release()




def write_video():
    pathIn= 'data/'
    pathOut = 'media/video.mp4'
    fps = 25
    convert_frames_to_video(pathIn,pathOut,fps)
    video = mp.VideoFileClip("media/video.mp4")
    video.write_videofile("media/output.mp4", audio="media/audio.mp3")




# def delete_data():
#     if os.path.exists("./data"):
#         os.rmdir("./data")
#     else:
#         print("The file does not exist")
#

def clear_media():
    folder = 'media'
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            #elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)
