import cv2
import numpy as np
from matplotlib import pyplot as plt
import dxcam
import time
import math
from keyevent import PressKey, ReleaseKey, HoldKey, CheckKey

def capture(center, trainPath, path, track, startBot):
    camera = dxcam.create(output_idx = 0, output_color = "BGRA")
    player_img = cv2.imread('player.png', cv2.IMREAD_UNCHANGED)

    camera.start(target_fps = 60, region=(0, 35, 250, 225))

    cv2.namedWindow('record', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('record', 300, 100)  
    cv2.createTrackbar('set path', 'record', 0, 1, nothing)
    cv2.createTrackbar('start', 'record', 0, 1, nothing) 
    # cv2.createTrackbar('topbound', 'record', 1, 100, nothing) 
    # cv2.createTrackbar('lefthorz', 'record', 1, 100, nothing) 
    # cv2.createTrackbar('righthorz', 'record', 1, 100, nothing) 


    while True:
        image = camera.get_latest_frame()
        info = np.iinfo(image.dtype)
        image = image.astype(np.float64) / info.max 
        image = 255 * image 
        image = image.astype(np.uint8)

        result = cv2.matchTemplate(image, player_img, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        print(image)

        w = player_img.shape[1]

        center[0] = max_loc[0] + int(w/2)
        center[1] = max_loc[1] + int(w/2)

        cv2.circle(image, center, int(w/2), (0, 0, 255), 1)
        cv2.circle(image, center, 27, (0, 0, 255), 1)
        cv2.circle(image, center, 1, (25,25,112), 1)

        coords = center[:]
        t1 = cv2.getTrackbarPos('set path', 'record')
        t2 = cv2.getTrackbarPos('start', 'record')
        stretchX = cv2.getTrackbarPos('hstretch', 'record') / 10
        stretchY = cv2.getTrackbarPos('vstretch', 'record') / 10

        if t1 == 0:
            prevButton = 0
            
        if t1 == 1:
            track.append(1)
            track.pop(0)
            if prevButton == 0:
                trainPath.append(coords)
                prevButton = 1

        if t2 == 0:
            startBot.append(0)
            startBot.pop(0)

        if t2 == 1:
            startBot.append(1)
            startBot.pop(0)

        if track[0] == 1:
            path = []
            shortestPath(trainPath, path, track)
        
        for previous, current in zip(path, path[1:]):
            if path[0] != None:
                cv2.line(image, previous, current, (255,105,180), 1)
            cv2.circle(image, current, 3, (0,255,0), 1)
            cv2.circle(image, current, 10, (245,255,250), 1)

        cv2.namedWindow('gaming', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('gaming', 500, 370)     

        # cv2.resize(image, ((image[1] * stretchX), (image[2] * stretchY)))

        cv2.imshow('gaming', np.array(image))

        # print(image)

        if (cv2.waitKey(1) & 0xFF) == ord('q'):
            cv2.destroyAllWindows()
            break

def movement(center, trainPath, path, track, startBot):
    while True:
        if track[0] == 1:
            path = []
            shortestPath(trainPath, path, track)
            # time.sleep(1)
        if startBot[0] == 1 and CheckKey('shift') != 0:
            for currentPath in path:
                # print(currentPath[0])
                moveHorz(currentPath, center)
                time.sleep(0.5)
                moveVert(currentPath, center)
                PressKey('left', 0.1)
                PressKey('shift', 0.1)
                time.sleep(1)
                PressKey('right', 0.1)
                PressKey('shift', 0.1)
                time.sleep(1)

                
def moveHorz(currentPath, center):
    x = currentPath[0] - center[0]
    while x > 3:
        x = currentPath[0] - center[0]
        if x < 3:
            time.sleep(1)
            x = currentPath[0] - center[0]
            if x < 3:
                break
        HoldKey('right')
        time.sleep(0.1)
        if x > 17:
            PressKey('alt', 0.1)
            PressKey('alt', 0.1)
        ReleaseKey('right')
    while x < -3:
        x = currentPath[0] - center[0]
        if x > -3:
            time.sleep(1)
            x = currentPath[0] - center[0]
            if x > -3:
                break
        HoldKey('left')
        time.sleep(0.1)
        if x < -17:
            PressKey('alt', 0.1)
            PressKey('alt', 0.1)
        ReleaseKey('left')

def moveVert(currentPath, center):
    y = currentPath[1] - center[1]
    while y < -3:
        y = currentPath[1] - center[1]
        if y > -3:
            time.sleep(0.5)
            y = currentPath[1] - center[1]
            if y > -3:
                break
        PressKey('alt', 0.1)
        if y < -5:
            PressKey('up', 0.1)
            PressKey('up', 0.1)
    while y > 3:
        y = currentPath[1] - center[1]
        if y < 3:
            time.sleep(1.25)
            y = currentPath[1] - center[1]
            if y < 3:
                break
        HoldKey('down')
        PressKey('alt', 0.1)
        ReleaseKey('down')            
        
def nothing():
    pass

def shortestPath(trainPath, path, track):
    if len(trainPath) > 0:
        path.append(trainPath[0])
        nodes = len(trainPath)
        visited = [trainPath[0]]
        current_node = trainPath[0]
        while len(visited) < nodes:
            min = float('inf')
            for i in range(nodes):
                if trainPath[i] not in visited:

                    if math.dist(current_node, trainPath[i]) < min:
                        min = math.dist(current_node, trainPath[i])
                        nearest_node = trainPath[i]
            
            if nearest_node not in path:
                path.append(nearest_node)
                visited.append(nearest_node)
                current_node = nearest_node
        
        path.append(trainPath[0])
        # print(path)
        track.append(0)
        track.pop(0)
    












# import cv2
# import numpy as np

# def nothing(x):
#     pass

# cv2.namedWindow("Trackbars")
# cv2.createTrackbar("L - H", "Trackbars", 153, 179, nothing)
# cv2.createTrackbar("L - S", "Trackbars", 96, 255, nothing)
# cv2.createTrackbar("L - V", "Trackbars", 175, 255, nothing)
# cv2.createTrackbar("U - H", "Trackbars", 156, 179, nothing)
# cv2.createTrackbar("U - S", "Trackbars", 255, 255, nothing)
# cv2.createTrackbar("U - V", "Trackbars", 255, 255, nothing)
# cv2.createTrackbar("Thresh1", "Trackbars", 190, 1000, nothing)
# cv2.createTrackbar("Thresh2", "Trackbars", 135, 1000, nothing)

# cv2.createTrackbar("hThresh", "Trackbars", 19, 400, nothing)
# cv2.createTrackbar("hMinLine", "Trackbars", 20, 100, nothing)
# cv2.createTrackbar("hMaxGap", "Trackbars", 1, 100, nothing)

# kernel = np.ones((3,3), np.uint8) 
# while True:
#     image = camera.get_latest_frame()
#     info = np.iinfo(image.dtype)
#     image = image.astype(np.float64) / info.max 
#     image = 255 * image 
#     image = image.astype(np.uint8)


#     l_h = cv2.getTrackbarPos("L - H", "Trackbars")
#     l_s = cv2.getTrackbarPos("L - S", "Trackbars")
#     l_v = cv2.getTrackbarPos("L - V", "Trackbars")
#     u_h = cv2.getTrackbarPos("U - H", "Trackbars")
#     u_s = cv2.getTrackbarPos("U - S", "Trackbars")
#     u_v = cv2.getTrackbarPos("U - V", "Trackbars")
#     Thresh1 = cv2.getTrackbarPos("Thresh1", "Trackbars")
#     Thresh2 = cv2.getTrackbarPos("Thresh2", "Trackbars")
#     hThresh = cv2.getTrackbarPos("hThresh", "Trackbars")
#     hMinLine = cv2.getTrackbarPos("hMinLine", "Trackbars")
#     hMaxGap = cv2.getTrackbarPos("hMaxGap", "Trackbars")

#     lower_blue = np.array([l_h, l_s, l_v])
#     upper_blue = np.array([u_h, u_s, u_v])
    
#     black = np.zeros((50,440))

#     black = np.zeros((50,440))

#     hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

#     mask = cv2.inRange(hsv, lower_blue, upper_blue)
#     #mask = 255 - mask
#     # No Mask
#     result = image

#     #use mask
#     #result = cv2.bitwise_and(img, img, mask=mask)
#     mask = cv2.dilate(mask, kernel, iterations=1)

#     lines = cv2.Canny(result, threshold1=Thresh1, threshold2=Thresh2)
#     img_dilation = cv2.dilate(lines, kernel, iterations=1) 
#     lines[mask>0]=0

#     #HoughLines = cv2.HoughLinesP(img_dilation, 1, np.pi/180, hThresh, hMinLine, hMaxGap
#     HoughLines = cv2.HoughLinesP(lines, 1, np.pi/180, threshold = hThresh, minLineLength = hMinLine, maxLineGap = hMaxGap)
#     if HoughLines is not None:
#         for line in HoughLines:
#             coords = line[0]
#             cv2.line(image, (coords[0], coords[1]), (coords[2], coords[3]), [0,0,255], 3)
#             cv2.line(black, (coords[0], coords[1]), (coords[2], coords[3]), [255,255,255], 3)

#     #cv2.imshow(f"Mask{i}", mask)
#     cv2.imshow('original', image)
#     #cv2.imshow(f"Result{i}", result)
#     cv2.imshow('lines', lines)
#     #cv2.imshow(f"Dilation{i}", img_dilation)
#     #cv2.imshow(f"blacknWhite{i}", black)
#     cv2.waitKey(1)


