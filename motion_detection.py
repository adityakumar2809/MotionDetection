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


def main():
    pass


if __name__ == '__main__':
    main()
