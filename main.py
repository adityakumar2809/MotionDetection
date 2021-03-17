import cv2

cap = cv2.VideoCapture('data/sample.mp4')

fps = int(cap.get(5)) # argument 5 means to get the fps of the video

ret, frame = cap.read()
height, width, _ = frame.shape

reduced_video = cv2.VideoWriter(
    filename='reduced_video.avi',
    fourcc=cv2.VideoWriter_fourcc(*'DIVX'),
    fps=fps,
    frameSize=(width, height)
)

i = 0
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == False:
        break

    reduced_video.write(frame)
    i += 1

cap.release()
reduced_video.release()
cv2.destroyAllWindows()