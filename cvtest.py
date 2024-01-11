import cv2
import numpy as np
import dxcam
import time
import math
from keyevent import PressKey, ReleaseKey, HoldKey, CheckKey

def capture(center, startBot, direction, bounds):
    camera = dxcam.create(output_idx = 0, output_color = "BGRA")
    player_img = cv2.imread('player.png', cv2.IMREAD_UNCHANGED)

    camera.start(target_fps = 60, region=(0, 35, 250, 225))

    cv2.namedWindow('record', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('record', 600, 350)  
    cv2.createTrackbar('start', 'record', 0, 1, nothing) 
    cv2.createTrackbar('topbound', 'record', 0, 189, nothing) 
    cv2.createTrackbar('lefthorz', 'record', 0, 249, nothing) 
    cv2.createTrackbar('righthorz', 'record', 0, 249, nothing) 
    cv2.createTrackbar('cw/ccw', 'record', 0, 1, nothing)
    cv2.createTrackbar('h', 'record', 0, 100, nothing) 
    cv2.createTrackbar('w', 'record', 0, 100, nothing)

    while True:
        image = camera.get_latest_frame()
        info = np.iinfo(image.dtype)
        image = image.astype(np.float64) / info.max 
        image = 255 * image 
        image = image.astype(np.uint8)
        imgcopy = image.copy()

        result = cv2.matchTemplate(image, player_img, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        w = player_img.shape[1]

        center[0] = max_loc[0] + int(w/2)
        center[1] = max_loc[1] + int(w/2)

        tb = cv2.getTrackbarPos('topbound', 'record')
        lhb = cv2.getTrackbarPos('lefthorz', 'record')
        rhb = 249 - cv2.getTrackbarPos('righthorz', 'record')
        changeH = cv2.getTrackbarPos('h', 'record')
        changeW = cv2.getTrackbarPos('w', 'record')

        if (rhb < lhb) or (lhb > rhb):
            rhb = lhb
        
        alpha = 0.5

        
        cv2.rectangle(imgcopy, (249, tb), (rhb, 189), (100,149,237), -1)
        cv2.rectangle(imgcopy, (0, tb), (lhb, 189), (240,128,128), -1)
        cv2.line(image, (0, tb), (249, tb), (255,165,0), 1)
        cv2.line(image, (0, tb + 10), (249, tb + 10), (255,165,0), 1)
        
        image = cv2.addWeighted(imgcopy, alpha, image, 1 - alpha, 0)

        cv2.circle(image, center, int(w/2), (0, 0, 255), 1)
        cv2.circle(image, center, 27, (0, 0, 255), 1)
        cv2.circle(image, center, 1, (25,25,112), 1)

        startBot.append(cv2.getTrackbarPos('start', 'record'))
        startBot.remove(startBot[0])

        direction.append(cv2.getTrackbarPos('cw/ccw', 'record'))
        direction.remove(direction[0])

        
        bounds.append(tb) 
        bounds.append(lhb) 
        bounds.append(rhb) 
        del bounds[:3]

        imgW = int(image.shape[1] * (1 + (changeW/100)))
        imgH = int(image.shape[0] * (1 + (changeH/100)))
        newImg = (imgW, imgH)
        resized = cv2.resize(image, newImg, interpolation=cv2.INTER_CUBIC)

        crop_img = resized[0: 150, 0:200]

        cv2.namedWindow('gaming', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('gaming', 500, 370) 

        cv2.imshow('gaming', crop_img)

        if (cv2.waitKey(1) & 0xFF) == ord('q'):
            cv2.destroyAllWindows()
            break

def movement(center, startBot, direction, bounds):
    checkStartY = 0
    startY = 0
    while True:
        # print(center)
        x = center[0]
        y = center[1]

        if startBot[0] == 1 and checkStartY == 0:
            startY = y
            checkStartY = 1
        if startBot[0] == 0:
            checkStartY = 0
        
        if startBot[0] == 1:
            if direction[0] == 0:
                direct = 0
                while direct == 0:
                    if startBot[0] == 0:
                        break
                    x = center[0]
                    y = center[1]
                    print(center)
                    print(bounds)
                    while x < bounds[1] and y > (bounds[0] + 10):
                        # print('bye')
                        # time.sleep(0.3)
                        PressKey('alt', 0.1)
                        PressKey('up', 0.1)
                        PressKey('up', 0.1)
                        time.sleep(0.6)
                        x = center[0]
                        y = center[1]
                        if y < bounds[0]:
                            HoldKey('down')
                            PressKey('alt', 0.1)
                            ReleaseKey('down') 
                            time.sleep(0.6)
                            x = center[0]
                            y = center[1]
                        if y < (bounds[0] + 10):
                            direct = 1
                            break
                    if direct == 1:
                        break
                    HoldKey('left')
                    PressKey('alt', 0.1)
                    PressKey('alt', 0.1)
                    ReleaseKey('left')
                    time.sleep(0.1)
                    PressKey('shift', 0.1)
                    print('hi')
                    time.sleep(0.6)
                    
                while direct == 1:
                    x = center[0]
                    y = center[1]
                    print(center)
                    print(bounds)
                    while x > bounds[2]:
                        print('bye')
                        HoldKey('down')
                        PressKey('alt', 0.1)
                        ReleaseKey('down')  
                        # time.sleep(0.6)
                        x = center[0]
                        y = center[1]
                        if y > (startY - 5):
                            PressKey('delete', 0.1)
                            direct = 0
                            break
                    if direct == 0:
                        break
                    HoldKey('right')
                    PressKey('alt', 0.1)
                    PressKey('alt', 0.1)
                    ReleaseKey('right')
                    time.sleep(0.1)
                    PressKey('shift', 0.1)
                    print('hi')
                    time.sleep(0.6)

                        
            # if direction[0] == 1:
            #     direct = 1
            #     while direct == 1:
            #         HoldKey('right')
            #         time.sleep(0.1)
            #         PressKey('alt', 0.1)
            #         PressKey('alt', 0.1)
            #         ReleaseKey('right')
            #         if x > bounds[2] and y < (bounds[1] + bounds[2]):
            #             time.sleep(1)
            #             PressKey('alt', 0.1)
            #             PressKey('up', 0.1)
            #             PressKey('up', 0.1)
            #             direct = 0

            
            
            


                
# def moveHorz(currentPath, center):
#     x = currentPath[0] - center[0]
#     while x > 3:
#         x = currentPath[0] - center[0]
#         if x < 3:
#             time.sleep(1)
#             x = currentPath[0] - center[0]
#             if x < 3:
#                 break
#         HoldKey('right')
#         time.sleep(0.1)
#         if x > 17:
#             PressKey('alt', 0.1)
#             PressKey('alt', 0.1)
#         ReleaseKey('right')
#     while x < -3:
#         x = currentPath[0] - center[0]
#         if x > -3:
#             time.sleep(1)
#             x = currentPath[0] - center[0]
#             if x > -3:
#                 break
#         HoldKey('left')
#         time.sleep(0.1)
#         if x < -17:
#             PressKey('alt', 0.1)
#             PressKey('alt', 0.1)
#         ReleaseKey('left')

# def moveVert(currentPath, center):
#     y = currentPath[1] - center[1]
#     while y < -3:
#         y = currentPath[1] - center[1]
#         if y > -3:
#             time.sleep(0.5)
#             y = currentPath[1] - center[1]
#             if y > -3:
#                 break
#         PressKey('alt', 0.1)
#         if y < -5:
#             PressKey('up', 0.1)
#             PressKey('up', 0.1)
#     while y > 3:
#         y = currentPath[1] - center[1]
#         if y < 3:
#             time.sleep(1.25)
#             y = currentPath[1] - center[1]
#             if y < 3:
#                 break
#         HoldKey('down')
#         PressKey('alt', 0.1)
#         ReleaseKey('down')            
        
def nothing():
    pass
    












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


