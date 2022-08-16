import cv2
import sys


def rescaleFrame(frame, scale=0.5):
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    dimensions = (width, height)
    return cv2.resize(frame, dimensions, interpolation=cv2.INTER_AREA)


def distance(a, b):
    d = [0,0]
    d[0] = origin[0] - a
    d[1] = origin[1] - b
    print(d)


(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
if __name__ == '__main__':
    tracker_types = ['BOOSTING', 'MIL', 'KCF', 'TLD',
                     'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
    tracker_type = tracker_types[-1]
    if int(minor_ver) < 3:
        tracker = cv2.Tracker_create(tracker_type)
    else:
        if tracker_type == 'BOOSTING':
            tracker = cv2.TrackerBoosting_create()
        if tracker_type == 'MIL':
            tracker = cv2.TrackerMIL_create()
        if tracker_type == 'KCF':
            tracker = cv2.TrackerKCF_create()
        if tracker_type == 'TLD':
            tracker = cv2.TrackerTLD_create()
        if tracker_type == 'MEDIANFLOW':
            tracker = cv2.TrackerMedianFlow_create()
        if tracker_type == 'GOTURN':
            tracker = cv2.TrackerGOTURN_create()
        if tracker_type == 'MOSSE':
            tracker = cv2.TrackerMOSSE_create()
        if tracker_type == "CSRT":
            tracker = cv2.TrackerCSRT_create()
    video = cv2.VideoCapture("footage2.mp4")
    # video = cv2.VideoCapture(0)
    if not video.isOpened():
        print('Could not open video')
        sys.exit()
    ok, frame = video.read()
    if not ok:
        print('Cannot read video file')
        sys.exit()
    origin = [frame.shape[1]//2, frame.shape[0]//2]
    dis = []
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
        if ok:
            x = int(bbox[0])
            y = int(bbox[1])
            p1 = (x, y)
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            distance(x, y)
            cv2.rectangle(frame_resized, p1, p2, (255, 0, 0), 2, 1)
        else:
            cv2.putText(frame_resized, "Tracking failure detected",
                        (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
        cv2.putText(frame_resized, tracker_type + " Tracker",
                    (100, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)
        cv2.putText(frame_resized, "FPS : " + str(int(fps)), (100, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)
        cv2.imshow("ROI selector", frame_resized)
        k = cv2.waitKey(1) & 0xff
        if k == ord('q'):
            break
