# import the necessary packages
import cv2
import time
import imutils
import datetime
import argparse
from imutils.video import VideoStream


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int,
                default=200, help="minimum area size")
args = vars(ap.parse_args())

# if the video argument is None, then we are reading from webcam
if args.get("video", None) is None:
    vs = VideoStream(src=0).start()
    frame = vs.read()
    fps = 30
    size = (frame.shape[1], frame.shape[0])
    # Store video if it is streamed live
    current_date_time = datetime.datetime.now().strftime("%d%m%Y_%I%M%S%p")
    filename = f'recordings/Recording_{current_date_time}.avi'
    recording = cv2.VideoWriter(
        filename, 
        cv2.VideoWriter_fourcc(*'XVID'),
        fps,
        size
    )
    time.sleep(2.0)
# otherwise, we are reading from a video file
else:
    vs = cv2.VideoCapture(args["video"])
    fps = vs.get(5)

    frame = vs.read()
    size = (int(vs.get(4)), int(vs.get(3)))

print('FPS: ', fps)

# initialize the first frame in the video stream
firstFrame = None
frame_count = 0
previous_text = "Unoccupied"

flag_new_entry = 0

refresh_rate = 200


# loop over the frames of the video
while True:
    frame = vs.read()
    frame_count += 1

    if frame_count % 200 == 0:
        firstFrame = None


    if args.get("video", None) is not None:
        frame = frame[1]

    text = "Unoccupied"

    if frame is None:
        break

	# resize the frame, convert it to grayscale, and blur it
    frame = imutils.resize(frame, width=500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
	
    # if the first frame is None, initialize it
    if firstFrame is None:
        firstFrame = gray
        continue

    # compute the absolute difference between the current and first frame
    frameDelta = cv2.absdiff(firstFrame, gray)
    thresh = cv2.threshold(frameDelta, 50, 255, cv2.THRESH_BINARY)[1]
	# dilate the thresholded image to fill in holes, then find contours
	# on thresholded image
    thresh = cv2.dilate(thresh, None, iterations=2)
    cnts = cv2.findContours(
        thresh.copy(),
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )
    cnts = imutils.grab_contours(cnts)
	
    # loop over the contours
    for c in cnts:
		# if the contour is too small, ignore it
        if cv2.contourArea(c) < args["min_area"]:
            continue
		
        # compute the bounding box for the contour, draw it on the frame,
		# and update the text
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        text = "Occupied"
        
    if previous_text == "Unoccupied" and text == 'Occupied':
        print('Frame count: ', frame_count)
        print('Entry time: ', frame_count/fps)
        previous_text = "Occupied"
        flag_new_entry = 1
    elif text == 'Unoccupied':
        previous_text = "Unoccupied"
        flag_new_entry = 0
    elif previous_text == 'Occupied':
        flag_new_entry = 0

    # draw the text and timestamp on the frame
    cv2.putText(
        frame,
        "Frame Status: {}".format(text),
        (10, 20),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (0, 0, 255),
        2
    )
    
    cv2.putText(
        frame,
        datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
        (10, frame.shape[0] - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.35,
        (0, 0, 255),
        1
    )

    if flag_new_entry == 1:
        cv2.imwrite(
            'captured_movements/frame_' + str(frame_count) + '.jpg',
            frame
        )

    if args.get("video", None) is None:
        recording.write(frame)
	
    # show the frame and record if the user presses a key
    cv2.imshow("Security Feed", frame)
    cv2.imshow("Thresh", thresh)
    cv2.imshow("Frame Delta", frameDelta)

    key = cv2.waitKey(1) & 0xFF
	
    # if the `q` key is pressed, break from the lop
    if key == ord("q"):
        break

    # time.sleep(0.03)

# cleanup the camera and close any open windows
vs.stop() if args.get("video", None) is None else vs.release()
if args.get("video", None) is None:
    recording.release()
cv2.destroyAllWindows()
