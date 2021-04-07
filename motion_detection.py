# import the necessary packages
import cv2
import time
import imutils
import datetime
import argparse
from imutils.video import VideoStream


def checkForArguments(default_min_area=200):
    '''Load the arguments present in the module invoking call'''
    ap = argparse.ArgumentParser()
    ap.add_argument(
        '-v',
        '--video',
        help='Path to the video file'
    )
    ap.add_argument(
        '-a',
        '--min-area',
        type=int,
        default=default_min_area,
        help='Minimum area to be considered a movement'
    )
    arguments = vars(ap.parse_args())

    return arguments


def getVideoCaptureObject(
        arguments=None,
        video_stream_source=0,
        video_stream_fps=30
    ):
    '''Create an object to capture video clip or stream'''
    if arguments.get('video', None) is None:
        video_object = VideoStream(src=video_stream_source).start()
        fps = video_stream_fps
    else:
        video_object = cv2.VideoCapture(arguments['video'])
        fps = video_object.get(5)


def preprocessFrame(frame, width=500, kernel_size=(21, 21)):
    '''Preprocess frame for motion detection'''
    frame = imutils.resize(frame, width=width)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    preprocessed_frame = cv2.GaussianBlur(frame, kernel_size, 0)
    
    return preprocessed_frame


def checkForMotion(video_object=None, arguments=None):
    '''Check for motion in the frames'''
    if video_object is None or arguments is None:
        return -1
    
    frame_count = 0
    frame_of_reference = None

    while(True):
        frame = video_object.read()
        frame_count += 1

        if arguments.get('video', None) is not None:
            frame = frame[1]

        if frame is None:
            break

        preprocessed_frame = preprocessFrame(frame)

        if frame_of_reference is None:
            frame_of_reference = preprocessed_frame
            continue


def main():
    pass


if __name__ == '__main__':
    main()
