import cv2
import mediapipe as mp
import time
import os
import handtracker as htm
import subprocess
from sudo import run_as_sudo

wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)


folderPath = "middlefinger"
myList = os.listdir(folderPath)
print(myList)
overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    #print(f'{folderPath}/{imPath}')
    overlayList.append(image)

print(len(overlayList))

pTime = 0
middlefingerdetector = 2

detector = htm.HandDetector(detectionCon=0.77)

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw = False)
    #print(lmList)

    if len(lmList) != 0:
        for j in range(11,13):
            for i in range(0,9):
                if lmList[i][2] < lmList[j][2]:
                    middlefingerdetector = 0


        for j in range(11,13):
            for i in range(13,20):
                if lmList[i][2] < lmList[j][2]:
                    middlefingerdetector = 0

        if middlefingerdetector == 2:
            middlefingerdetector = 1

        if middlefingerdetector == 1:
            print("Va te faire enculer")
            #subprocess.run("sudo shutdown -h now", shell=True)
            #run_as_sudo("root","sudo shutdown -h now",shell=True)
            subprocess.call(['osascript', '-e', 'tell app "loginwindow" to «event aevtrsdn»'])

        if middlefingerdetector == 0:
            print("je t'aime")
        middlefingerdetector = 2
    h, w, c = overlayList[0].shape
    img[0:198, 0:200] = overlayList[0]

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (500, 70), cv2.FONT_ITALIC, 3, (128, 0, 128), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)