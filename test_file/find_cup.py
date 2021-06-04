import cv2
import numpy as np
import matplotlib.pyplot as plt
import math
import socket


def surf():
    print('surf starting')

    while True:

        MIN_MATCH_COUNT = 20

        ret, frame = cap.read()

        cap.set(3, 1920)  # Width
        cap.set(4, 1080)  # Height

        img2 = frame  # Scene Image

        # Initiate Surf detector
        s = cv2.xfeatures2d.SURF_create()
        # find key points and descriptors with SURF
        kp1, des1 = s.detectAndCompute(img1, None)
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
            h, w = img1.shape
            pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
            dst = cv2.perspectiveTransform(pts, M)
            img2 = cv2.polylines(img2, [np.int32(dst)], True, 255, 3, cv2.LINE_AA)

            draw_params = dict(matchColor=(0, 255, 0),  # draw matches in green color
                               singlePointColor=None,
                               matchesMask=matchesMask,  # draw only inliers
                               flags=2)
            img3 = cv2.drawMatches(img1, kp1, img2, kp2, good, None, **draw_params)

            plt.imshow(img3), plt.show()

            break

        else:
            # matchesMask = None
            print("Not enough matches are found - {}/{}".format(len(good), MIN_MATCH_COUNT))

    return M, dst


def calculate(R, dst):

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

    # change the numbers accordingly

    tx = (-(y_center - 540)) * (280 / 1080) + 447  # mm
    ty = (-(x_center - 960)) * (500 / 1920) - 392

    return tx, ty, ex, ey, ez


if __name__ == '__main__':

    # # define the socket IP address and port number
    # Tcp_IP = '192.168.x.x'
    # Tcp_Port = 5050
    #
    # # define socket category and socket type in our case using TCP/IP
    # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #
    # # open the socket and listen
    # s.bind((Tcp_IP, Tcp_Port))
    # s.listen(1)
    #
    # # accept any incoming connection
    # conn, addr = s.accept()
    # print('Connection address:', addr)

    # initialize camera streaming
    cam = 0
    cap = cv2.VideoCapture(cam)
    ret, frame = cap.read()

    # Target object
    # can add a if loop to retrieve different target image
    # img2 = cv2.imread('coke.jpg',0)

    img1 = cv2.imread('../coke.jpg', 0)

    R, dst = surf()

    tx, ty, ex, ey, ez = calculate(R, dst)

    print("returned values are", tx, ty, ex, ey, ez)

    cap.release()
    cv2.destroyAllWindows()

    # while True:
    #
    #     # the robot needs to send a binary 1 to activate the computer vision program
    #
    #     # read the received data buffer size 1024
    #     data = conn.recv(1024)
    #
    #     # show the received data
    #     print("received data: ", data)
    #
    #     if data == b'1':
    #
    #         R, dst = surf()
    #
    #         print('Bounding box corners coordinates dst: ', '\n', dst, '\n')
    #
    #         # calculate all the needed values
    #         tx, ty, ex, ey, ez = calculate(R, dst)
    #
    #         print("returned values are", tx, ty, ex, ey, ez)
    #
    #         print("object detection program finished")
    #
    #         coordinate = tx / 1000, ty / 1000
    #
    #         # Send data using tcp/ip
    #
    #         message1 = bytes(str(coordinate), 'ascii')
    #         print('sending X coordinate "%s"' % message1)
    #         conn.send(message1)
    #
    #         cap.release()
    #         cv2.destroyAllWindows()
    #
    #         conn.close()
    #         cap.release()
    #         cv2.destroyAllWindows()
    #
    #         break
    #
    #     else:
    #
    #         print("Communication lost")
    #         conn.close()
    #         cap.release()
    #         cv2.destroyAllWindows()
    #
    #     break



