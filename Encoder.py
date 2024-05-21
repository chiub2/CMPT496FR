import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials, storage

class EncoderDB:

    storage_bucket_url = 'spring-capstone-c5472.appspot.com'

    def __init__(self, storage_bucket_url, credentials_path="serviceAccountKey.json"):
        if not firebase_admin._apps:
            self.cred = credentials.Certificate(credentials_path)
            self.app = firebase_admin.initialize_app(self.cred, {
                'storageBucket': storage_bucket_url
        })
        else:
            self.bucket = storage.bucket(app=self.app)
            self.encodings_path = "EncodeFile.p"

    def upload_file(self, file_path):
        ''' Upload a file to Firebase storage '''
        blob = self.bucket.blob(os.path.basename(file_path))
        try:
            blob.upload_from_filename(file_path)
            print("Upload successful")
        except Exception as e:
            print("Upload unsuccessful: ", e)

    def encode_and_save(self, image_path, student_id):
        ''' Encode face from a given image and link it to a student_id, then save the encoding '''
        image = face_recognition.load_image_file(image_path)
        encodings = face_recognition.face_encodings(image)
        if encodings:
            # Save encoding to a local file or a database
            self.save_encodings(encodings[0], student_id)
            print(f"Encoding successful for {student_id}")
        else:
            print("No face found in the image.")

    def save_encodings(self, encoding, student_id):
        ''' Append the encoding to a pickle file along with student_id '''
        # Try to load existing encodings if the file exists
        if os.path.exists(self.encodings_path):
            with open(self.encodings_path, 'rb') as file:
                try:
                    encode_list = pickle.load(file)  # Load existing encodings
                except EOFError:
                    encode_list = []  # If file is empty, start with an empty list
        else:
            encode_list = []  # Start with an empty list if file does not exist

        # Append the new encoding and student ID as a tuple
        encode_list.append((encoding, student_id))

        # Write the updated list back to the file
        with open(self.encodings_path, 'wb') as file:
            pickle.dump(encode_list, file)

        print(f"New encoding for student ID {student_id} added to {self.encodings_path}.")


if __name__ == '__main__':
    encoder = EncoderDB('https://spring-capstone-c5472-default-rtdb.firebaseio.com/')
    encoder.encode_and_save("path_to_student_image.jpg", "student_id")
    encoder.upload_file("path_to_student_image.jpg")





# import cv2
# import dlib
# import face_recognition
# import pickle
# import os
# import firebase_admin
# from firebase_admin import  storage, credentials




# class EncoderDB():
#     ''' The only mehod you need from this class is uploadFile() '''
#     def __init__(self, name = "Test Encoder DB"):
#         self._cred = credentials.Certificate("serviceAccountKey.json")
#         firebase_admin.initialize_app(self._cred, {
#             'databaseURL': "https://spring-capstone-c5472-default-rtdb.firebaseio.com/",
#             'storageBucket': 'spring-capstone-c5472.appspot.com'
#         })
#         self._name = name
#         self._bucket = storage.bucket()
#         self._blob = None
    
#     def __str__(self):
#         return self._name
    
#     def uploadFile(self, fName):
#         ''' 
#         no need to specify path before calling, this 
#         function finds the path using global variable - folderPath
#         '''
#         fileName = self.getFname(fName)
#         self._blob = self._bucket.blob(fileName)
#         try:    
#             self._blob.upload_from_filename(fileName)
#             print("Upload succesful")
#         except Exception as e:
#             print("Upload unsuccesful: ",e)

#     def getFname(self, path):
#         return f"{folderPath}/{path}" #os.path.join(folderPath, path)
    

# # Importing student images
# folderPath = "Images"
# pathList = os.listdir(folderPath)

# imageList = []
# studentIds = []

# for path in pathList:
#     imageList.append(cv2.imread(os.path.join(folderPath, path)))
#     path = path.split(".")[0]
#     studentIds.append(path)


# def findEncodings(imageList):
#     encodeList = []
#     for img in imageList:
#         img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#         encode = face_recognition.face_encodings(img)[0]
#         encodeList.append(encode)
#     return encodeList

# print("Encoding in Progress")
# encodeListKnown = findEncodings(imageList)
# encodeListKnownIds = [encodeListKnown, studentIds]
# print("Encoding Complete")

# file = open("EncodeFile.p", 'wb')
# pickle.dump(encodeListKnownIds, file)
# file.close
# print("File Saved")

    


# if __name__ == '__main__':

#     # Usage
#     testEncodeDB = EncoderDB()
#     status = testEncodeDB.uploadFile("3080126.png")