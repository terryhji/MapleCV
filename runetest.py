import cv2
import numpy as np
from matplotlib import pyplot as plt
import time
from math import sqrt

def nothing(x):
    pass

def capture():

    cv2.namedWindow('Trackbars', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Trackbars', 600, 350)  
    cv2.createTrackbar('tlow', 'Trackbars', 0, 1000, nothing) 
    cv2.createTrackbar('tupp', 'Trackbars', 0, 1000, nothing) 
    cv2.createTrackbar("L - H", "Trackbars", 0, 179, nothing)
    cv2.createTrackbar("L - S", "Trackbars", 0, 255, nothing)
    cv2.createTrackbar("L - V", "Trackbars", 0, 255, nothing)
    cv2.createTrackbar("U - H", "Trackbars", 179, 179, nothing)
    cv2.createTrackbar("U - S", "Trackbars", 255, 255, nothing)
    cv2.createTrackbar("U - V", "Trackbars", 255, 255, nothing)
    cv2.createTrackbar("test", "Trackbars", 10000, 50000, nothing)

    while True:

        tl = cv2.getTrackbarPos('tlow', 'Trackbars')
        tup = cv2.getTrackbarPos('tupp', 'Trackbars')
        l_h = cv2.getTrackbarPos("L - H", "Trackbars")
        l_s = cv2.getTrackbarPos("L - S", "Trackbars")
        l_v = cv2.getTrackbarPos("L - V", "Trackbars")
        u_h = cv2.getTrackbarPos("U - H", "Trackbars")
        u_s = cv2.getTrackbarPos("U - S", "Trackbars")
        u_v = cv2.getTrackbarPos("U - V", "Trackbars")
        test = cv2.getTrackbarPos("test", "Trackbars")

        img = cv2.imread('rune3.png')

        image = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2HSV)

        l_h = 95
        l_s = 0
        l_v = 0
        u_h = 130
        u_s = 255
        u_v = 220
        # tl = 900
        # tup = 450

        # l_h = 75
        # l_s = 0
        # l_v = 0
        # u_h = 179
        # u_s = 255
        # u_v = 200
        # tl = 900
        # tup = 200

        lower_range = np.array([l_h, l_s, l_v])
        upper_range = np.array([u_h, u_s, u_v])
        mask = cv2.inRange(image, lower_range, upper_range)

        blur = cv2.GaussianBlur(mask,(5,5),0)

        edge = cv2.Canny(blur, tl, tup)
    
        contours, _ = cv2.findContours(edge, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
        filtered_contours = []
        for i in contours:
            if 25000 <= cv2.contourArea(i) <= 30000:
                filtered_contours.append(i)

        cv2.drawContours(image, filtered_contours, -1, (0, 255, 0), 4)

        leftVert = 999999
        leftLoc = []
        botHeight = 0
        topHeight = 999999
        rightHorz = 0

        for i in filtered_contours:
            for x in i:
                if x[0][0] < leftVert:
                    leftVert = x[0][0]
                    leftLoc = x[0]
                if x[0][0] > rightHorz:
                    rightHorz = x[0][0]
                if x[0][1] > botHeight:
                    botHeight = x[0][1]
                if x[0][1] < topHeight:
                    topHeight = x[0][1]

        cv2.circle(image, (leftLoc[0], int(leftLoc[1] - (topHeight - botHeight)/2)), 5, (0, 255, 255), 1)
        cv2.circle(image, (rightHorz, int(leftLoc[1] - (topHeight - botHeight)/2)), 5, (0, 255, 255), 1)
        cv2.circle(image, (leftLoc[0], topHeight), 5, (0, 0, 255), 1)
        cv2.circle(image, (rightHorz, topHeight), 5, (0, 0, 255), 1)
        cv2.rectangle(image, (leftLoc[0], int(leftLoc[1] - (topHeight - botHeight)/2)), (rightHorz, topHeight), (0, 0, 255), 3)

        cropped = image[topHeight:botHeight, leftLoc[0]:rightHorz]

        mask1 = cv2.inRange(cropped, lower_range, upper_range)

        blur1 = cv2.GaussianBlur(mask1,(5,5),0)

        edge1 = cv2.Canny(blur1, tl, tup)
    
        contours, _ = cv2.findContours(edge1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
        arrow1 = []
        arrow2 = []
        arrow3 = []
        arrow4 = []

        for i in contours:
            for x in i:
                if x[0][0] <= 125:
                    if 300 <= cv2.contourArea(i) <= 700:
                        arrow1.append(i)
                if 125 < x[0][0] <= 200:
                    if 300 <= cv2.contourArea(i) <= 700:
                        arrow2.append(i)
                if 200 <= x[0][0] <= 275:
                    if 300 <= cv2.contourArea(i) <= 700:
                        arrow3.append(i)
                if 275 <= x[0][0]:
                    if 300 <= cv2.contourArea(i) <= 700:
                        arrow4.append(i)
        # print(arrow1)
        i = arrow1[0]
        arclength_filter = 0.03 * cv2.arcLength(i, True)
        polygons = cv2.approxPolyDP(i, arclength_filter, True)

        print(polygons.max())

        # for i in polygons:
        #     arrDir = ""
        #     prevVal = i[0][0]
        #     largestLine = 0
        #     secondLL = 0
        #     # print(prevVal)
        #     for v in i:
        #         currentVal = [v[0][0], v[0][1]]
        #         line = sqrt((prevVal[0] - currentVal[0]) ** 2 + (prevVal[1] - currentVal[1]) ** 2)
        #         if line > largestLine:
        #             largestLine = line
        #         if line > secondLL and line != largestLine:
        #             secondLL = line
                
        #         prevVal = currentVal
        #         # print(line)
        #     print(largestLine)
        #     print(secondLL)

        black = np.zeros((botHeight - topHeight, rightHorz - leftLoc[0]), dtype = np.uint8)

        cv2.drawContours(black, polygons, -1, (255, 255, 255), 2)

        # print(polygons)
                
        # cv2.namedWindow('gaming', cv2.WINDOW_NORMAL)
        # cv2.resizeWindow('gaming', 1406, 472)  
        # cv2.namedWindow('gaming2', cv2.WINDOW_NORMAL)
        # cv2.resizeWindow('gaming2', 1406, 472)   

        # cv2.namedWindow('gaming4', cv2.WINDOW_NORMAL)
        # cv2.resizeWindow('gaming4', 1406, 472)  

        cv2.imshow('gaming', np.array(black))
        cv2.imshow('gaming2', np.array(edge1))

        cv2.imshow('gaming4', np.array(mask1))

        if (cv2.waitKey(1) & 0xFF) == ord('q'):
            cv2.destroyAllWindows()
            break

capture()