import cv2
import mediapipe as mp
import time
import os
import handtracker as htm
import subprocess
from sudo import run_as_sudo

wCam, hCam = 640, 480
successions = 5;

cap = cv2.VideoCapture(0)

folderPath = "thumbs_up"
myList = os.listdir(folderPath)
print(myList)
overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    #print(f'{folderPath}/{imPath}')
    overlayList.append(image)

print(len(overlayList))

pTime = 0
thumbdetector = 2

detector = htm.HandDetector(detectionCon=0.77)

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw = False)
    #print(lmList)

    if len(lmList) != 0:
        for j in range(3,5):
            for i in range(0,2):
                if lmList[i][2] < lmList[j][2]:
                    thumbdetector = 0


        for j in range(3,5):
            for i in range(5,20):
                if lmList[i][2] < lmList[j][2]:
                    thumbdetector = 0

        if thumbdetector == 2:
            thumbdetector = 1

        if thumbdetector == 1:
            print("Thumb up")
            print(successions)
            successions = successions+1
            if successions == 5:
                print("Shutdown now")
                subprocess.run("sudo shutdown -h now", shell=True)
                #run_as_sudo("root","sudo shutdown -h now",shell=True)
                #subprocess.call(['osascript', '-e', 'tell app "loginwindow" to «event aevtrsdn»'])

        if thumbdetector == 0:
            print("Thumb down")
            successions = 0
        thumbdetector = 2

    h, w, c = overlayList[0].shape
    img[0:209, 0:241] = overlayList[0]

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (500, 70), cv2.FONT_ITALIC, 3, (128, 0, 128), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)