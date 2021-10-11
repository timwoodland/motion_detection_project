import time
import pandas
from cv2 import cv2 as cv
from datetime import datetime

first_frame = None

video = cv.VideoCapture(1)
video.read()
time.sleep(2.0)

status_list = [None, None]
times = []
df = pandas.DataFrame(columns=["Start", "End"])

while True:
    check, frame = video.read()

    status = 0

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    gray = cv.GaussianBlur(gray, (21,21), 0)

    if first_frame is None:
        first_frame = gray
        continue

    delta_frame = cv.absdiff(first_frame, gray)

    thresh_frame = cv.threshold(delta_frame, 30, 255, cv.THRESH_BINARY)[1]
    thresh_frame = cv.dilate(thresh_frame, None, iterations=2)

    (cnts,_) = cv.findContours(thresh_frame.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    for contour in cnts:
        if cv.contourArea(contour) < 10000:
            continue
        status = 1
        (x, y, w, h) = cv.boundingRect(contour)
        cv.rectangle(frame, (x,y), (x+w,y+h), (0,255,0),3)

    status_list.append(status)
    if status_list[-1] == 1 and status_list[-2] ==0:
        times.append(datetime.now())
    if status_list[-1] == 0 and status_list[-2] == 1:
        times.append(datetime.now())

    cv.imshow("Gray Frame", gray)
    cv.imshow("Delta Frame", delta_frame)
    cv.imshow("Threshold Frame", thresh_frame)
    cv.imshow("Colour Frame", frame)

    key = cv.waitKey(1)

    if key == ord('q'):
        if status == 1:
            times.append(datetime.now())
        break
print(times)

for i in range(0, len(times), 2):
    df = df.append({"Start":times[i], "End":times[i+1]}, ignore_index=True)

df.to_csv("times.csv")

video.release()
cv.destroyAllWindows()
