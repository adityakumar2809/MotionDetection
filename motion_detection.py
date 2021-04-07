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


def main():
    pass


if __name__ == '__main__':
    main()
