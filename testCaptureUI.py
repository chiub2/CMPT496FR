# import datetime
# from datetime import datetime
# import cv2
# import pickle
# import face_recognition
# import numpy as np
# import os
# import firebase_admin
# from firebase_admin import credentials, db, storage

# # Initialize Firebase
# cred = credentials.Certificate("serviceAccountKey.json")
# if not firebase_admin._apps:
#     firebase_admin.initialize_app(cred, {
#         'databaseURL': "https://spring-capstone-c5472-default-rtdb.firebaseio.com/",
#         'storageBucket': 'spring-capstone-c5472.appspot.com'
#     })

# # Fetch database reference
# student_ref = db.reference('Students')
# bucket = storage.bucket()
# #Testing for the Face Recognition to update the attendance 
# # def update_attendance(student_id):
# #     # Fetch the student's current attendance data
# #     student_data = student_ref.child(student_id).get()
# #     if student_data:
# #         current_attendance = student_data.get("total_attendance", 0)
# #         new_attendance = current_attendance + 1
# #         student_ref.child(student_id).update({"total_attendance": new_attendance})
# #         print(f"Updated attendance for {student_id}: {new_attendance}")
# #     else:
# #         print(f"Student {student_id} not found in database.")

# def update_attendance(student_id):
#     try:
#         # Fetch the student's current attendance data
#         student_data = student_ref.child(student_id).get()
#         if student_data:
#             current_attendance = student_data.get("total_attendance", 0)
#             attendance_dates = student_data.get("attendance_dates", [])
#             now = datetime.now().strftime('%Y-%m-%d')  # Add Time later because it will keep incrementing %H:%M:%S
#             if now not in attendance_dates:
#                 new_attendance = current_attendance + 1
#                 attendance_dates.append(now)
#                 student_ref.child(student_id).update({
#                     "total_attendance": new_attendance,
#                     "attendance_dates": attendance_dates
#                 })
#                 print(f"Updated attendance for {student_id}: {new_attendance}")
#             else:
#                 print(f"Attendance for {student_id} already recorded today.")
#         else:
#             print(f"Student {student_id} not found in database.")
#     except Exception as e:
#         print(f"Error updating attendance for {student_id}: {e}")

# def read_encode_file_from_storage():
#     blob = bucket.blob('Resources/EncodeFile.p')
#     try:
#         content = blob.download_as_string()
#         encodeListKnownIds = pickle.loads(content)
#         print("Read successful")
#         return encodeListKnownIds
#     except Exception as e:
#         print("Read unsuccessful: ", e)
#         return None


# def launch():
#     try:
#         # Check for camera access
#         cap = cv2.VideoCapture(0)
#         if not cap.isOpened():
#             print("Error: Camera could not be accessed.")
#             return
        
#         # Set camera resolution
#         cap.set(3, 640)
#         cap.set(4, 480)

#         # Check for necessary files
#         background_path = "Resources/background.png"
#         if not os.path.exists(background_path):
#             print("Error: Background path incorrect.")
#             return
        
#         # Load background
#         imgBackground = cv2.imread(background_path)
        
#         # Load encodings from Firebase Storage
#         encodeListKnownIds = read_encode_file_from_storage()
#         if encodeListKnownIds is None:
#             return

#         encodeListKnown, studentIds = encodeListKnownIds
#         print("Loaded student IDs:", studentIds)

#         frame_skip = 5
#         frame_count = 0
#         prev_box = None  # Previous bounding box for smoothing
#         alpha = 0.2  # Smoothing factor for box transitions

#         while True:
#             success, img = cap.read()
#             if not success:
#                 print("Failed to capture image from camera.")
#                 break

#             frame_count += 1
#             if frame_count % frame_skip == 0:
#                 # Process face recognition every `frame_skip` frames
#                 imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
#                 imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
#                 faceCurFrame = face_recognition.face_locations(imgS)
#                 encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

#                 for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
#                     matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
#                     faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
#                     matchIndex = np.argmin(faceDis)
#                     if matches[matchIndex]:
#                         student_id = studentIds[matchIndex]
#                         current_box = [coord * 4 for coord in faceLoc]  # Adjust coordinates
#                         if prev_box is not None:
#                             # Smooth transitions for bounding box
#                             current_box = [int(prev_box[i] * (1 - alpha) + current_box[i] * alpha) for i in range(4)]
#                         prev_box = current_box
#                         cv2.rectangle(img, (current_box[3], current_box[0]), (current_box[1], current_box[2]), (0, 255, 0), 2)
#                         cv2.putText(img, student_id, (current_box[3], current_box[0] - 10), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)
#                         print('Detected:', student_id)

#                         # Update attendance in the database
#                         update_attendance(student_id)
#             else:
#                 # Display last known box and label between detections
#                 if prev_box is not None:
#                     cv2.rectangle(img, (prev_box[3], prev_box[0]), (prev_box[1], prev_box[2]), (0, 255, 0), 2)
#                     cv2.putText(img, student_id, (prev_box[3], prev_box[0] - 10), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)

#             # Show updated image with background
#             imgBackground[162:162+480, 55:55+640] = img
#             cv2.imshow("Face Attendance", imgBackground)

#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break

#     except Exception as e:
#         print("An error occurred:", e)

#     finally:
#         cap.release()
#         cv2.destroyAllWindows()

# if __name__ == "__main__":
#     launch()

# testCaptureUI.py
from datetime import datetime
import cv2
import face_recognition
import pickle
import numpy as np
import logging
import firebase_admin
from firebase_admin import credentials, db, storage, initialize_app
from PyQt5.QtGui import QImage, QPixmap
import os
from PyQt5.QtCore import Qt

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Initialize Firebase Admin SDK
cred = credentials.Certificate("serviceAccountKey.json")
if not firebase_admin._apps:
    initialize_app(cred, {
        'databaseURL': "https://spring-capstone-c5472-default-rtdb.firebaseio.com/",
        'storageBucket': 'spring-capstone-c5472.appspot.com'
    })

# Fetch database reference
student_ref = db.reference('Students')
bucket = storage.bucket()

# Global flag to control camera running state
running = True

def update_attendance(student_id):
    try:
        student_data = student_ref.child(student_id).get()
        if student_data:
            current_attendance = student_data.get("total_attendance", 0)
            attendance_dates = student_data.get("attendance_dates", [])
            now = datetime.now().strftime('%Y-%m-%d')
            if now not in attendance_dates:
                new_attendance = current_attendance + 1
                attendance_dates.append(now)
                student_ref.child(student_id).update({
                    "total_attendance": new_attendance,
                    "attendance_dates": attendance_dates
                })
                logging.info(f"Updated attendance for {student_id}: {new_attendance}")
            else:
                logging.info(f"Attendance for {student_id} already recorded today.")
        else:
            logging.warning(f"Student {student_id} not found in database.")
    except Exception as e:
        logging.error(f"Error updating attendance for {student_id}: {e}")

def read_encode_file_from_storage():
    blob = bucket.blob('Resources/EncodeFile.p')
    try:
        content = blob.download_as_string()
        encodeListKnownIds = pickle.loads(content)
        logging.info("Read successful")
        return encodeListKnownIds
    except Exception as e:
        logging.error(f"Read unsuccessful: {e}")
        return None

def launch(label):
    global running
    running = True
    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Camera could not be accessed.")
            return
        
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        cap.set(cv2.CAP_PROP_FPS, 30)  # Set the frame rate to 30 FPS

        encodeListKnownIds = read_encode_file_from_storage()
        if encodeListKnownIds is None:
            return

        encodeListKnown, studentIds = encodeListKnownIds
        print("Loaded student IDs:", studentIds)

        prev_box = None
        alpha = 0.2

        while running:
            success, img = cap.read()
            if not success:
                print("Failed to capture image from camera.")
                break

            imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
            imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
            faceCurFrame = face_recognition.face_locations(imgS)
            encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

            for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
                matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
                faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
                matchIndex = np.argmin(faceDis)
                if matches[matchIndex]:
                    student_id = studentIds[matchIndex]
                    current_box = [coord * 4 for coord in faceLoc]
                    if prev_box is not None:
                        current_box = [int(prev_box[i] * (1 - alpha) + current_box[i] * alpha) for i in range(4)]
                    prev_box = current_box
                    cv2.rectangle(img, (current_box[3], current_box[0]), (current_box[1], current_box[2]), (0, 255, 0), 2)
                    cv2.putText(img, student_id, (current_box[3], current_box[0] - 10), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)
                    print('Detected:', student_id)
                    update_attendance(student_id)

            frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            qt_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qt_image)
            label.setPixmap(pixmap)
            label.update()

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except Exception as e:
        print("An error occurred:", e)
    finally:
        cap.release()
        cv2.destroyAllWindows()
        clear_label(label)


def stop():
    global running
    running = False

def clear_label(label):
    # Create a black QPixmap to clear the label
    black_image = QImage(640, 480, QImage.Format_RGB888)
    black_image.fill(Qt.black)
    pixmap = QPixmap.fromImage(black_image)
    label.setPixmap(pixmap)
    label.update()