import cv2
import dlib
import face_recognition
import pickle
import os

# Importing student images
folderPath = "Images"
pathList = os.listdir(folderPath)

imageList = []
studentIds = []

for path in pathList:
    imageList.append(cv2.imread(os.path.join(folderPath, path)))
    path = path.split(".")[0]
    studentIds.append(path)


def findEncodings(imageList):
    encodeList = []
    for img in imageList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

print("Encoding in Progress")
encodeListKnown = findEncodings(imageList)
encodeListKnownIds = [encodeListKnown, studentIds]
print("Encoding Complete")

file = open("EncodeFile.p", 'wb')
pickle.dump(encodeListKnownIds, file)
file.close
print("File Saved")

