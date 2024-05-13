import cv2
import time


def launch():

    cap = cv2.VideoCapture(0) # 0 as argument because 1 causes an error
    cap.set(3,640) #set width
    cap.set(4,480) # set height

    imgBackground = cv2.imread("background.png")
    # imgBackground2 = cv2.imread("background2.jpg")
    #load image
    capturing = True


    while capturing:
        success, img = cap.read()
        # cv2.imshow("WebCam", img)
        imgBackground[162:162+480, 55:55+640] = img
        # imgBackground2[0:480, 0:640] = img
        cv2.imshow("Face Attendance", imgBackground) # display image
        # cv2.imshow("Face Attendance", imgBackground2)
        cv2.waitKey(1)

        # capturing = False


if __name__ == "__main__":
    launch()