from cv2 import cv2 as cv
import time

video = cv.VideoCapture(1)
 a = 0
while True:
    a += 1

    check, frame = video.read()

    # print(check)
    # print(frame)

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    cv.imshow("Video", gray)
    # time.sleep(3)

    key = cv.waitKey(1)

    if key == ord('q'):
        break

print(a)
video.release()
cv.destroyAllWindows()
