from turtle import right
import cv2 as cv
from cv2 import aruco

marker_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
param_markers = aruco.DetectorParameters_create()

cap = cv.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    grey_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    bbox, ids, r = aruco.detectMarkers(
        grey_frame, marker_dict, parameters=param_markers)
    if bbox:
        for ids_markers, bbox_markers in zip(ids, bbox):
            bbox_markers = bbox_markers.reshape(4,2)
            bbox_markers = bbox_markers.astype(int)
            pos = bbox_markers[0]
            image = cv.putText(frame, f"id: {ids_markers[0]}", pos, cv.FONT_HERSHEY_PLAIN, 1, (250,0,0), 2, cv.LINE_AA)
            aruco.drawDetectedMarkers(frame, bbox)

    cv.imshow("frame", frame)
    key = cv.waitKey(1)
    if key == ord("q"):
        break
cap.release()
cv.destroyAllWindows()
