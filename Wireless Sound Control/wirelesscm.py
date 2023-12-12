# Import necessary libraries
import cv2
import mediapipe as mp
import math
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Initialize webcam capture
cap = cv2.VideoCapture(0)

# Initialize time variables for frame rate calculation (currently commented out)
pTime = 0
cTime = 0

# Set up hand tracking using Mediapipe
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraws = mp.solutions.drawing_utils

# Set up audio devices and interface for volume control
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# Get the range of volume levels supported by the system
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]

# Infinite loop for capturing and processing webcam frames
while True:
    # Capture a frame from the webcam
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Process the frame to detect hands
    results = hands.process(imgRGB)

    # If hands are detected, loop through each detected hand
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            lmList = []

            # Loop through each landmark of the hand
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])

                # Draw landmarks and connections on the image
                mpDraws.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

            # If landmarks are present, calculate distance between specific points
            if lmList:
                x1, y1 = lmList[4][1], lmList[4][2]
                x2, y2 = lmList[8][1], lmList[8][2]
                cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
                cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
                cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

                z1 = (x1 + x2) // 2
                z2 = (y1 + y2) // 2

                cv2.circle(img, (z1, z2), 15, (255, 0, 0), cv2.FILLED)
                length = math.hypot(x2 - x1, y2 - y1)

                # If distance is less than 50 pixels, draw a filled white circle
                if length < 50:
                    cv2.circle(img, (z1, z2), 15, (255, 255, 255), cv2.FILLED)

            # Map the distance to volume range and update system volume
            vol = np.interp(length, [50, 300], [minVol, maxVol])
            volBar = np.interp(length, [50, 300], [400, 150])
            volPer = np.interp(length, [50, 300], [0, 100])
            volume.SetMasterVolumeLevel(vol, None)

            # Draw volume level indicators on the image
            cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
            cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, f'{int(volPer)}%', (40, 450), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 255), 3)

    # Display the annotated image and wait for a key press
    cv2.imshow("Image", img)
    cv2.waitKey(1)