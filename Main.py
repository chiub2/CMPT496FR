import os
import cv2
import pickle
import face_recognition
import numpy as np
import cvzone

cap = cv2.VideoCapture(0)
cap.set(3, 640) # 3 is the width
cap.set(4, 480) # 4 is the height


imgBackground = cv2.imread("Resources/background.png")


# Import Resources into a list
folderPathForModes = "Resources/Modes/"
modePath = os.listdir(folderPathForModes)
imageModeList = []
for path in modePath:
    imageModeList.append(cv2.imread(os.path.join(folderPathForModes, path)))

# Import the encoding file
file = open("EncodeFile.p", 'rb')
encodeListKnownIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListKnownIds
print(studentIds)

while True:
    success, img = cap.read()

    imgS = cv2.resize(img, (0,0), None, 0.25, 0.25)    
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    imgBackground[162:162+480, 55:55+640] = img
    imgBackground[44:44+633, 808:808+414] = imageModeList[3]


    for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        #print(faceDis)
        matchIndex = np.argmin(faceDis)
        if True in matches:
            print('known face detected')
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
            bbox = 55+x1, 162+y1, x2-x1, y2-y1
            imgBackground = cvzone.cornerRect(imgBackground,bbox, rt = 0)
            

    # cv2.imshow("Camera", img)
    cv2.imshow("Background", imgBackground)
    cv2.waitKey(1)

