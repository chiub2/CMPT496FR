import cv2
import dlib
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import  storage, credentials




class EncoderDB():
    ''' The only mehod you need from this class is uploadFile() '''
    def __init__(self, name = "Test Encoder DB"):
        self._cred = credentials.Certificate("serviceAccountKey.json")
        firebase_admin.initialize_app(self._cred, {
            'databaseURL': "https://spring-capstone-c5472-default-rtdb.firebaseio.com/",
            'storageBucket': 'spring-capstone-c5472.appspot.com'
        })
        self._name = name
        self._bucket = storage.bucket()
        self._blob = None
    
    def __str__(self):
        return self._name
    
    def uploadFile(self, fName):
        ''' 
        no need to specify path before calling, this 
        function finds the path using global variable - folderPath
        '''
        fileName = self.getFname(fName)
        self._blob = self._bucket.blob(fileName)
        try:    
            self._blob.upload_from_filename(fileName)
            print("Upload succesful")
        except Exception as e:
            print("Upload unsuccesful: ",e)

    def getFname(self, path):
        return f"{folderPath}/{path}" #os.path.join(folderPath, path)
    

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

    


if __name__ == '__main__':

    # Usage
    testEncodeDB = EncoderDB()
    status = testEncodeDB.uploadFile("3080126.png")