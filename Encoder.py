import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials, storage

class EncoderDB():
    ''' The only method you need from this class is uploadFile() '''
    def __init__(self, name="Test Encoder DB"):
        self._cred = credentials.Certificate("serviceAccountKey.json")
        if not firebase_admin._apps:
            firebase_admin.initialize_app(self._cred, {
                'databaseURL': "https://spring-capstone-c5472-default-rtdb.firebaseio.com/",
                'storageBucket': 'spring-capstone-c5472.appspot.com'
            })
        self._name = name
        self._bucket = storage.bucket()
        self._blob = None

    def __str__(self):
        return self._name

    def uploadFile(self, local_path, remote_path):
        ''' 
        Upload file to Firebase Storage 
        '''
        self._blob = self._bucket.blob(remote_path)
        try:
            self._blob.upload_from_filename(local_path)
            print(f"Upload successful: {local_path} to {remote_path}")
        except Exception as e:
            print(f"Upload unsuccessful: {local_path} to {remote_path}", e)

# Importing student images
folderPath = "Images"
pathList = os.listdir(folderPath)

imageList = []
studentIds = []

# Initialize EncoderDB
testEncodeDB = EncoderDB()

for path in pathList:
    if path.endswith('.png'):  # Ensure we only process .png files
        img = cv2.imread(os.path.join(folderPath, path))
        if img is not None:
            imageList.append(img)
            studentId = path.split(".")[0]
            studentIds.append(studentId)

            # Upload the image to Firebase
            local_path = os.path.join(folderPath, path)
            remote_path = f"Images/{path}"
            testEncodeDB.uploadFile(local_path, remote_path)
        else:
            print(f"Error loading image: {path}")

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

file_path = "EncodeFile.p"
with open(file_path, 'wb') as file:
    pickle.dump(encodeListKnownIds, file)
print("File Saved")

# Upload EncodeFile.p to Firebase Storage in the Resources directory
testEncodeDB.uploadFile(file_path, "Resources/EncodeFile.p")

if __name__ == '__main__':
    # Usage
    testEncodeDB = EncoderDB()
    status = testEncodeDB.uploadFile(file_path, "Resources/EncodeFile.p")
