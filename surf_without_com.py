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

    tx = (-(y_center - 540)) * (400 / 1080) + 650  # mm
    ty = (-(x_center - 960)) * (700.6 / 1920) - 127

    return tx, ty, ex, ey, ez


if __name__ == '__main__':

    # initialize camera streaming
    cam = 0
    cap = cv2.VideoCapture(cam)
    ret, frame = cap.read()

    # Target object
    # can add a if loop to retrieve different target image
    # img2 = cv2.imread('coke.jpg',0)

    img1 = cv2.imread('fanta.jpg', 0)


    while True:

        R, dst = surf()

        print('Bounding box corners coordinates dst: ', '\n', dst, '\n')

        # calculate all the needed values
        tx, ty, ex, ey, ez = calculate(R, dst)

        print("returned values are", tx, ty, ex, ey, ez)

        print("object detection program finished")

        coordinate = tx / 1000, ty / 1000

        cap.release()
        cv2.destroyAllWindows()

        break



