import cv2


while True:

    cam = 0
    cap = cv2.VideoCapture(cam)
    ret, frame = cap.read()

    cv2.imshow("xxx",frame)




