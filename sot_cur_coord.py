import cv2
import sys
import math
from mav_override import *
def rescaleFrame(frame, scale=0.5):
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    dimensions = (width, height)
    return cv2.resize(frame, dimensions, interpolation=cv2.INTER_AREA)
def tracking():
    def distance(a, b):
        d = [0, 0]
        d[0] = frame.shape[1]//2 - a
        d[1] = frame.shape[0]//2 - b
        return d
    (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
    if __name__ == '__main__':
        if int(minor_ver) < 3:
            tracker = cv2.Tracker_create('CSRT')
        else:
            tracker = cv2.TrackerCSRT_create()
        #video = cv2.VideoCapture("footage2.mp4")
        video = cv2.VideoCapture(0)
        if not video.isOpened():
            print('Could not open video')
            sys.exit()
        ok, frame = video.read()
        if not ok:
            print('Cannot read video file')
            sys.exit()
        dis = []
        coor = [0,0]
        bbox = (287, 23, 86, 320)
        s_frame = cv2.resize(frame, (int(
            frame.shape[1] * 0.5), int(frame.shape[0] * 0.5)), interpolation=cv2.INTER_AREA)
        bbox = cv2.selectROI(s_frame, False)
        ok = tracker.init(s_frame, bbox)
        while True:
            ret, frame = video.read()
            frame_resized = rescaleFrame(frame)
            if not ret:
                break
            timer = cv2.getTickCount()
            ok, bbox = tracker.update(frame_resized)
            fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
            (h, w) = frame_resized.shape[:2]
            cv2.circle(frame_resized, (w//2, h//2), 5, (0, 255, 0), -1)
            cv2.circle(frame_resized, (960, 0), 5, (0, 255, 0), -1)
            if ok:
                x = int(bbox[0])
                y = int(bbox[1])
                p1 = (x, y)
                p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
                dis = distance(x, y)
                cv2.rectangle(frame_resized, p1, p2, (0, 255, 0), 2, 1)
                cv2.line(frame_resized, (w//2, h//2), (x, y),
                         (255, 255, 255), thickness=3)
                length = int(math.dist((w//2, h//2), (x, y)))
                coor[0] = w//2 - dis[0]
                coor[1] = dis[1] - h//2
                get_cur_coordinates(coor)
                cv2.putText(frame_resized, 'Distance from Centre:' +
                            str(length), (x, y - 7), 0, 0.5, (0, 0, 255), 2)
                set_rc_override(coor)
            else:
                cv2.putText(frame_resized, "Tracking failure detected",
                            (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
            cv2.putText(frame_resized, "CSRT Tracker", (100, 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
            cv2.putText(frame_resized, "FPS : " + str(int(fps)), (100, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
            cv2.imshow("ROI selector", frame_resized)
            k = cv2.waitKey(1) & 0xff
            if k == ord('q'):
                break
def map_range(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min
def get_cur_coordinates(cur_c):
    print(cur_c)

tracking()
