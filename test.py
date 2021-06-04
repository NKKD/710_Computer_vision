import cv2
import numpy as np
import matplotlib.pyplot as plt
import math
import socket
import requests

host = "http://192.168.12.20/api/v2.0.0/"
# Headers:

headers = {"Content-Type": "application/json",
           "Authorization": "Basic RGlzdHJpYnV0b3I6NjJmMmYwZjFlZmYxMGQzMTUyYzk1ZjZmMDU5NjU3NmU0ODJiYjhlNDQ4MDY0MzNmNGNmOTI5NzkyODM0YjAxNA==",
           "Host" : "192.168.12.20",
           "Accept-Language" : "en_US"
            }

# initialize camera streaming
cam = 0
cap = cv2.VideoCapture(cam)
ret, frame = cap.read()
#
# # define the socket IP address and port number
# Tcp_IP = '192.168.12.253'
# Tcp_Port = 5050

# for localhost testing purpose
Tcp_IP = '127.0.0.1'
Tcp_Port = 8888

def surf(img):
    print('surf starting')

    i = 0

    while i < 5:

        MIN_MATCH_COUNT = 10

        ret, frame = cap.read()

        cap.set(3, 3840)  # Width
        cap.set(4, 2160)  # Height

        img2 = frame  # Scene Image

        # Initiate Surf detector
        s = cv2.xfeatures2d.SURF_create()
        # find key points and descriptors with SURF
        kp1, des1 = s.detectAndCompute(img, None)
        kp2, des2 = s.detectAndCompute(img2, None)
        FLANN_INDEX_KDTREE = 1
        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        search_params = dict(checks=50)
        flann = cv2.FlannBasedMatcher(index_params, search_params)
        matches = flann.knnMatch(des1, des2, k=2)
        # store all the good matches as per Lowe's ratio test.
        good = []
        for m, n in matches:
            if m.distance < 0.7 * n.distance:
                good.append(m)

        if len(good) > MIN_MATCH_COUNT:
            src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
            dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

            M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

            matchesMask = mask.ravel().tolist()
            h, w = img.shape
            pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
            dst = cv2.perspectiveTransform(pts, M)
            img2 = cv2.polylines(img2, [np.int32(dst)], True, 255, 3, cv2.LINE_AA)

            draw_params = dict(matchColor=(0, 255, 0),  # draw matches in green color
                               singlePointColor=None,
                               matchesMask=matchesMask,  # draw only inliers
                               flags=2)
            img3 = cv2.drawMatches(img, kp1, img2, kp2, good, None, **draw_params)

            i = i + 1

            plt.imshow(img3), plt.show()

            return M, dst

            break

        else:
            print("Not enough matches are found - {}/{}".format(len(good), MIN_MATCH_COUNT))
            # matchesMask = None
            i = i + 1

    M = []
    dst = []

    return M, dst


def sendcoordinate(R, dst):
    print('Transformation matrix M is:', '\n', R, '\n')
    print('Bounding box corners coordinates dst: ', '\n', dst, '\n')

    # calculate all the needed values
    tx, ty, ex, ey, ez = calculate(R, dst)

    print("returned values are", tx, ty, ex, ey, ez)

    print("object detection program finished")

    z = 0.4
    a = 2.252
    b = -2.191
    c = 0

    coordinate = tx / 1000, ty / 1000, z, a, b, c

    # Send data
    message1 = bytes(str(coordinate), 'ascii')
    print('sending X coordinate "%s"' % message1)
    conn.send(message1)

    conn.close()
    cap.release()
    # cv2.destroyAllWindows()


def calculate(R, dst):
    sy = math.sqrt(R[0, 0] * R[0, 0] + R[1, 0] * R[1, 0])

    singular = sy < 1e-6

    if not singular:
        ex = math.atan2(R[2, 1], R[2, 2])
        ey = math.atan2(-R[2, 0], sy)
        ez = math.atan2(R[1, 0], R[0, 0])
    else:
        ex = math.atan2(-R[1, 2], R[1, 1])
        ey = math.atan2(-R[2, 0], sy)
        ez = 0

    print("The euler angle is ", ex, ey, ez, '\n')

    x0 = dst[0][0][0]
    y0 = dst[0][0][1]

    x1 = dst[1][0][0]
    y1 = dst[1][0][1]

    x2 = dst[2][0][0]
    y2 = dst[2][0][1]

    x3 = dst[3][0][0]
    y3 = dst[3][0][1]

    x = [x1, x2, x3, x0]
    y = [y0, y1, y2, y3]

    print("Max value of all x: ", max(x))
    print("Max value of all y: ", max(y))
    print("Min value of all x: ", min(x))
    print("Min value of all y: ", min(y))

    x_center = 0.5 * (max(x) - min(x)) + min(x)
    y_center = 0.5 * (max(y) - min(y)) + min(y)

    print("the center of the object is x y: ", x_center, y_center)

    tx = (-(y_center - (2160 / 2))) * (400 / 2160) + (785)  # mm
    ty = (-(x_center - (3840 / 2))) * (700.6 / 3840) + (109)

    return tx, ty, ex, ey, ez


if __name__ == '__main__':

    # define socket category and socket type in our case using TCP/IP
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # open the socket and listen
    s.bind((Tcp_IP, Tcp_Port))
    s.listen(1)

    # accept any incoming connection
    conn, addr = s.accept()
    print('Connection address:', addr)

    while True:

        # read the received data buffer size 1024
        data = conn.recv(1024)

        # show the received data
        print("received data: ", data)

        if data != b'1\r\n':
            print("Communication lost")
            break

        else:
            print("Tcp/ip communication established")

            # Target Object
            img = cv2.imread('coke.jpg', 0)

            R1, dst1 = surf(img)

            if R1 and dst1 != 0:

                print(R1, dst1,"coke")

                sendcoordinate(R1, dst1)

                # run coke

                data = "{\"mission_id\" : \"79579d2e-c52c-11eb-be53-0001299df20a\" }"

                send_mission = requests.post(host + "mission_queue", headers = headers, data = data)

                print(send_mission)

                break
            else:
                img = cv2.imread('lp.jpg', 0)
                R2, dst2 = surf(img)

                if R2.size and dst2.size is not None:

                    print (R2,dst2)
                    sendcoordinate(R2, dst2)

                    # run lp

                    data = "{\"mission_id\" : \"954fc36a-c52c-11eb-be53-0001299df20a\" }"

                    send_mission = requests.post(host + "mission_queue", headers = headers, data = data)

                    print(send_mission)

                    break

                else:
                    print("both not enough matches")
                    conn.close()
                    cap.release()
                    # cv2.destroyAllWindows()
                    break

