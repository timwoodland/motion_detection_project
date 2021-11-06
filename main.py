import time
import pandas
from cv2 import cv2 as cv
from datetime import datetime
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.plotting import figure
from bokeh.io import output_file, show


def motion_detection():
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
        gray = cv.GaussianBlur(gray, (21, 21), 0)

        if first_frame is None:
            first_frame = gray
            continue

        delta_frame = cv.absdiff(first_frame, gray)

        thresh_frame = cv.threshold(delta_frame, 30, 255, cv.THRESH_BINARY)[1]
        thresh_frame = cv.dilate(thresh_frame, None, iterations=2)

        (cnts, _) = cv.findContours(thresh_frame.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        for contour in cnts:
            if cv.contourArea(contour) < 10000:
                continue
            status = 1
            (x, y, w, h) = cv.boundingRect(contour)
            cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

        # append the status to the list and then trim the list to only the last two items as that is all that we need
        status_list.append(status)
        status_list = status_list[-2:]

        if status_list[-1] == 1 and status_list[-2] == 0:
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
        df = df.append({"Start": times[i], "End": times[i + 1]}, ignore_index=True)

    df.to_csv("times.csv")

    video.release()
    cv.destroyAllWindows()
    return df


def plotting(df):
    df["Start_String"] = df["Start"].dt.strftime("%Y-%m-%d %H:%M:%S")
    df["End_String"] = df["End"].dt.strftime("%Y-%m-%d %H:%M:%S")

    cds = ColumnDataSource(df)

    p = figure(x_axis_type='datetime', height=100, width=500, sizing_mode='scale_width', title="Motion Graph")
    p.yaxis.minor_tick_line_color = None
    p.yaxis.ticker.desired_num_ticks = 1

    hover = HoverTool(tooltips=[("Start", "@Start_String"), ("End", "@End_String")])
    p.add_tools(hover)

    p.quad(left="Start", right="End", bottom=0, top=1, color="Green", source=cds)

    output_file("motion_graph.html")
    show(p)


def main():
    df = motion_detection()
    plotting(df)


if __name__ == '__main__':
    main()
