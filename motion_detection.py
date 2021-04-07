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

    return video_object, fps


def preprocessFrame(frame, width=500, kernel_size=(21, 21)):
    '''Preprocess frame for motion detection'''
    resized_frame = imutils.resize(frame, width=width)
    preprocessed_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)
    preprocessed_frame = cv2.GaussianBlur(preprocessed_frame, kernel_size, 0)
    
    return resized_frame, preprocessed_frame


def getFrameDifferenceContours(
        frame,
        frame_of_reference,
        thresh_value=50,
        thresh_max_val=255,
        dilation_kernel=None,
        dilation_iter=2
    ):
    '''Calculate the difference between current and reference frame'''
    frame_delta = cv2.absdiff(frame_of_reference, frame)
    
    thresh_object = cv2.threshold(
        src=frame_delta,
        thresh=thresh_value,
        maxval=thresh_max_val,
        type=cv2.THRESH_BINARY
    )
    thresh_frame = thresh_object[1]

    dilated_frame = cv2.dilate(
        thresh_frame,
        kernel=dilation_kernel,
        iterations=dilation_iter
    )

    contours = cv2.findContours(
        dilated_frame.copy(),
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    contours = imutils.grab_contours(contours)

    return contours


def markObjectBoundary(frame, contour):
    '''Mark the object being detected in the frame'''
    (x, y, w, h) = cv2.boundingRect(contour)
    frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    return frame


def saveCapturedMovement(
        frame,
        frame_count,
        fps,
        arguments,
        directory_name='captured_movements'
    ):
    '''Save the frames with detected motion'''
    directory_name = 'captured_movements'
    
    if arguments['video'] is not None:
        sub_path_name = arguments['video'].split('/')[-1]
        ext_index = sub_path_name.rindex('.')
        sub_path_name = sub_path_name[:ext_index]
    else:
        sub_path_name = (
            'stream_' + datetime.datetime.now().strftime("%d%m%Y")
        )

    time_of_appearance = round(frame_count/fps)
    frame_name = f'frame_{frame_count}_{time_of_appearance}'


    cv2.imwrite(
        f'{directory_name}/{sub_path_name}_{frame_name}.jpg',
        frame
    )

    return


def checkForMotion(video_object=None, arguments=None, fps=30):
    '''Check for motion in the frames'''
    if video_object is None or arguments is None:
        return -1
    
    frame_count = 0
    frame_of_reference = None
    motion_detected = False
    continuous_motion_detected = False

    while(True):
        frame = video_object.read()
        frame_count += 1

        if arguments.get('video', None) is not None:
            frame = frame[1]

        if frame is None:
            break

        resized_frame, processed_frame = preprocessFrame(frame)

        if frame_of_reference is None:
            frame_of_reference = processed_frame
            continue

        contours = getFrameDifferenceContours(
            processed_frame,
            frame_of_reference
        )

        for contour in contours:
            if cv2.contourArea(contour) > arguments['min_area']:
                resized_frame = markObjectBoundary(resized_frame, contour)
                motion_detected = True

        if motion_detected and not continuous_motion_detected:
            continuous_motion_detected = True
            saveCapturedMovement(resized_frame, frame_count, fps, arguments)
        elif not motion_detected:
            continuous_motion_detected = False

        cv2.imshow('Security Feed', resized_frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break


def killWindowsAndObjects(video_object, arguments):
    '''Kill all dangling windows and objects'''
    if arguments.get('video', None) is None:
        video_object.stop()
    else:
        video_object.release()
    
    cv2.destroyAllWindows()


def main():
    '''Driver Function'''
    arguments = checkForArguments(default_min_area=200)
    video_object, fps = getVideoCaptureObject(arguments=arguments)
    checkForMotion(video_object, arguments, fps)
    killWindowsAndObjects(video_object, arguments)


if __name__ == '__main__':
    main()
