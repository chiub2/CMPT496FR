import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials, storage
import datetime
import logging
import requests
import numpy as np

logging.basicConfig(level=logging.DEBUG)

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
            logging.info(f"Upload successful: {local_path} to {remote_path}")
        except Exception as e:
            logging.error(f"Upload unsuccessful: {local_path} to {remote_path}", e)

    def get_file_url(self, remote_path):
        ''' 
        Get public URL of the uploaded file 
        '''
        blob = self._bucket.blob(remote_path)
        return blob.generate_signed_url(expiration=datetime.timedelta(minutes=15))

def read_images_from_firebase():
    image_list = []
    student_ids = []

    blobs = storage.bucket().list_blobs(prefix="Images/")
    for blob in blobs:
        if blob.name.endswith('.png'):
            url = blob.generate_signed_url(expiration=datetime.timedelta(minutes=15))
            response = requests.get(url)
            img = cv2.imdecode(np.frombuffer(response.content, np.uint8), -1)
            if img is not None:
                image_list.append(img)
                student_id = os.path.basename(blob.name).split(".")[0]
                student_ids.append(student_id)
                logging.info(f"Read image for student ID: {student_id}")
            else:
                logging.error(f"Error loading image from URL: {url}")
    
    return image_list, student_ids

def findEncodings(imageList):
    encodeList = []
    for img in imageList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

def main():
    # Initialize EncoderDB
    testEncodeDB = EncoderDB()

    # Read local images
    local_folder_path = "Images"
    local_image_list = []
    local_student_ids = []

    for path in os.listdir(local_folder_path):
        if path.endswith('.png'):  # Ensure we only process .png files
            img = cv2.imread(os.path.join(local_folder_path, path))
            if img is not None:
                local_image_list.append(img)
                student_id = path.split(".")[0]
                local_student_ids.append(student_id)

                # Upload the image to Firebase
                local_path = os.path.join(local_folder_path, path)
                remote_path = f"Images/{path}"
                testEncodeDB.uploadFile(local_path, remote_path)
            else:
                logging.error(f"Error loading image: {path}")

    # Read Firebase images
    firebase_image_list, firebase_student_ids = read_images_from_firebase()

    # Combine local and Firebase images
    combined_image_list = local_image_list + firebase_image_list
    combined_student_ids = local_student_ids + firebase_student_ids

    logging.info("Encoding in Progress")
    encodeListKnown = findEncodings(combined_image_list)
    encodeListKnownIds = [encodeListKnown, combined_student_ids]
    logging.info("Encoding Complete")

    file_path = "EncodeFile.p"
    with open(file_path, 'wb') as file:
        pickle.dump(encodeListKnownIds, file)
    logging.info("File Saved")

    # Upload StudentEncodeFile.p to Firebase Storage in the Resources directory
    testEncodeDB.uploadFile(file_path, "Resources/EncodeFile.p")

if __name__ == '__main__':
    main()

############################################################################################################
#New code for mediapipe library
############################################################################################################
# import cv2
# import mediapipe as mp
# import pickle
# import os
# import firebase_admin
# from firebase_admin import credentials, storage
# import datetime
# import logging
# import requests
# import numpy as np

# logging.basicConfig(level=logging.DEBUG)

# class EncoderDB():
#     def __init__(self, name="Test Encoder DB"):
#         self._cred = credentials.Certificate("serviceAccountKey.json")
#         if not firebase_admin._apps:
#             firebase_admin.initialize_app(self._cred, {
#                 'databaseURL': "https://spring-capstone-c5472-default-rtdb.firebaseio.com/",
#                 'storageBucket': 'spring-capstone-c5472.appspot.com'
#             })
#         self._name = name
#         self._bucket = storage.bucket()
#         self._blob = None

#     def uploadFile(self, local_path, remote_path):
#         self._blob = self._bucket.blob(remote_path)
#         try:
#             self._blob.upload_from_filename(local_path)
#             logging.info(f"Upload successful: {local_path} to {remote_path}")
#         except Exception as e:
#             logging.error(f"Upload unsuccessful: {local_path} to {remote_path}", e)

#     def get_file_url(self, remote_path):
#         blob = self._bucket.blob(remote_path)
#         return blob.generate_signed_url(expiration=datetime.timedelta(minutes=15))

# def read_images_from_firebase():
#     image_list = []
#     student_ids = []

#     blobs = storage.bucket().list_blobs(prefix="Images/")
#     for blob in blobs:
#         if blob.name.endswith('.png'):
#             url = blob.generate_signed_url(expiration=datetime.timedelta(minutes=15))
#             response = requests.get(url)
#             img = cv2.imdecode(np.frombuffer(response.content, np.uint8), -1)
#             if img is not None:
#                 image_list.append(img)
#                 student_id = os.path.basename(blob.name).split(".")[0]
#                 student_ids.append(student_id)
#                 logging.info(f"Read image for student ID: {student_id}")
#             else:
#                 logging.error(f"Error loading image from URL: {url}")
    
#     return image_list, student_ids

# def findEncodings(imageList):
#     mp_face_mesh = mp.solutions.face_mesh
#     face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True)
#     encodeList = []
#     for img in imageList:
#         rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#         results = face_mesh.process(rgb_img)
#         if results.multi_face_landmarks:
#             face_landmarks = results.multi_face_landmarks[0]
#             flattened_landmarks = [(landmark.x, landmark.y, landmark.z) for landmark in face_landmarks.landmark]
#             flattened_landmarks = [coord for point in flattened_landmarks for coord in point]
#             encodeList.append(flattened_landmarks)
#         else:
#             logging.error("No face landmarks found for image.")
#     return encodeList

# def main():
#     local_folder_path = "Images"
#     local_image_list = []
#     local_student_ids = []

#     for path in os.listdir(local_folder_path):
#         if path.endswith('.png'):
#             img = cv2.imread(os.path.join(local_folder_path, path))
#             if img is not None:
#                 local_image_list.append(img)
#                 student_id = path.split(".")[0]
#                 local_student_ids.append(student_id)

#     firebase_image_list, firebase_student_ids = read_images_from_firebase()
#     combined_image_list = local_image_list + firebase_image_list
#     combined_student_ids = local_student_ids + firebase_student_ids

#     logging.info("Encoding in Progress")
#     encodeListKnown = findEncodings(combined_image_list)
#     encodeListKnownIds = [encodeListKnown, combined_student_ids]
#     logging.info("Encoding Complete")

#     file_path = "EncodeFile.p"
#     with open(file_path, 'wb') as file:
#         pickle.dump(encodeListKnownIds, file)
#     logging.info("File Saved")

#     testEncodeDB = EncoderDB()
#     testEncodeDB.uploadFile(file_path, "Resources/EncodeFile.p")

# if __name__ == '__main__':
#     main()
    
