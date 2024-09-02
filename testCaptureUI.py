from datetime import datetime
import os
import time
import cv2
import face_recognition
import pickle
import numpy as np
import logging
import firebase_admin
from firebase_admin import credentials, db, storage, initialize_app
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QLabel
import threading
from scipy.spatial import distance as dist
from imutils import face_utils
from FireBaseDB import FaceRecognitionFirebaseDB
import dlib
import threading
import asyncio
import concurrent.futures




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

# Blink detection functions
def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

def is_blinking(eye):
    EAR_THRESHOLD = 0.25
    return eye_aspect_ratio(eye) < EAR_THRESHOLD

# Path to the shape predictor file
shape_predictor_path = "shape_predictor_68_face_landmarks.dat"

# Check if the shape predictor file exists
if not os.path.exists(shape_predictor_path):
    raise FileNotFoundError(f"shape_predictor_68_face_landmarks.dat file not found. Please ensure it is in the directory: {os.getcwd()}")

# Initialize dlib's face detector and facial landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(shape_predictor_path)

class FaceDetectionThread(threading.Thread):
    def __init__(self, cap, encodeListKnown, studentIds, update_present_students, label, face_recognition_db, course_name, section_id, selected_date):
        super().__init__()
        self.cap = cap
        self.encodeListKnown = encodeListKnown
        self.studentIds = studentIds
        self.update_present_students = update_present_students
        self.label = label
        self.face_recognition_db = face_recognition_db
        self.course_name = course_name
        self.section_id = section_id
        self.running = True
        self.last_update_times = {}
        self.attendance_cache = {}
        self.selected_date = selected_date
        self.detected_faces = {}  # Track detected faces with IDs and bounding boxes
        print(f"FaceDetectionThread initialized with date: {self.selected_date}")

    def run(self):
        print("FaceDetectionThread started running with date: ", self.selected_date)
        frame_skip = 5
        frame_count = 0
        blinking_count = {}

        while self.running:
            success, img = self.cap.read()
            if not success:
                logging.error("Failed to capture image from camera.")
                break

            frame_count += 1
            if frame_count % frame_skip == 0:
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = detector(gray, 0)

                detected_students = []

                for face in faces:
                    shape = predictor(gray, face)
                    shape = face_utils.shape_to_np(shape)

                    left_eye = shape[36:42]
                    right_eye = shape[42:48]

                    if is_blinking(left_eye) or is_blinking(right_eye):
                        (x, y, w, h) = (face.left(), face.top(), face.width(), face.height())
                        face_loc = (y, x + w, y + h, x)

                        encode_face = face_recognition.face_encodings(img, [face_loc])[0]

                        matches = face_recognition.compare_faces(self.encodeListKnown, encode_face)
                        face_dis = face_recognition.face_distance(self.encodeListKnown, encode_face)
                        match_index = np.argmin(face_dis)

                        if matches[match_index]:
                            student_id = self.studentIds[match_index]
                            if student_id not in blinking_count:
                                blinking_count[student_id] = 0
                            blinking_count[student_id] += 1

                            if blinking_count[student_id] >= 2:  # Require at least 2 blinks
                                current_box = [coord for coord in face_loc]
                                self.detected_faces[student_id] = (current_box, 0)  # Update detected faces
                                self.update_present_students([student_id])
                                print(f"Liveliness check passed for {student_id}")

                        else:
                            print("No matching student found or failed liveliness check.")
                    else:
                        print("No blink detected.")

                for student_id in list(self.detected_faces.keys()):
                    box, frames_since_last_seen = self.detected_faces[student_id]
                    if frames_since_last_seen < 5:
                        self.detected_faces[student_id] = (box, frames_since_last_seen + 1)
                        detected_students.append(student_id)
                    else:
                        del self.detected_faces[student_id]

                self.update_present_students(detected_students)

            # Drawing green boxes and student IDs
            for student_id, (box, _) in self.detected_faces.items():
                cv2.rectangle(img, (box[3], box[0]), (box[1], box[2]), (0, 255, 0), 2)
                cv2.putText(img, student_id, (box[3], box[0] - 10), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)

            frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            qt_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qt_image)
            self.label.setPixmap(pixmap)
            self.label.update()

        print("FaceDetectionThread stopped running...")

    def stop(self):
        self.running = False
        print("FaceDetectionThread stopped.")

    def should_update_attendance(self, student_id):
        current_time = time.time()
        last_update_time = self.last_update_times.get(student_id, 0)
        if current_time - last_update_time > 5:
            self.last_update_times[student_id] = current_time
            return True
        return False

    def update_attendance(self, student_id, face_recognition_db, course_name, section_id):
        try:
            enrolled_students_path = f"Courses/{course_name}-{section_id}/students"
            enrolled_students_ref = face_recognition_db.db.reference(enrolled_students_path)
            enrolled_students = enrolled_students_ref.get()
            
            if not enrolled_students or student_id not in enrolled_students:
                logging.info(f"Student {student_id} is not enrolled in course {course_name}, section {section_id}. Attendance not updated.")
                return False

            logging.info(f"Updating attendance for student {student_id} in course {course_name}, section {section_id} on {self.selected_date}")

            attendance_path = f"Attendance/{course_name}-{section_id}/{self.selected_date}"
            attendance_ref = face_recognition_db.db.reference(attendance_path)
            current_attendance = attendance_ref.get() or []

            if student_id not in current_attendance:
                current_attendance.append(student_id)
                attendance_ref.set(current_attendance)
                logging.info(f"Attendance for {student_id} in class {course_name}-{section_id} recorded for {self.selected_date}.")

                student_data = db.reference(f'Students/{student_id}').get()
                if student_data:
                    total_attendance = student_data.get("total_attendance", 0)
                    attendance_dates = student_data.get("attendance_dates", [])
                    if self.selected_date not in attendance_dates:
                        new_attendance = total_attendance + 1
                        attendance_dates.append(self.selected_date)
                        db.reference(f'Students/{student_id}').update({
                            "total_attendance": new_attendance,
                            "attendance_dates": attendance_dates
                        })
                        logging.info(f"Updated total attendance for {student_id}: {new_attendance}")
                    else:
                        logging.info(f"Attendance for {student_id} already recorded today.")
                else:
                    logging.warning(f"Student {student_id} not found in database.")
            else:
                logging.info(f"Attendance for {student_id} in class {course_name}-{section_id} already recorded for {self.selected_date}.")
                return False
        except Exception as e:
            logging.error(f"Error updating attendance for {student_id}: {e}")
            return False
        return True

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

def launch(label, face_recognition_db, course_name, section_id, update_present_students, selected_date):
    global cap, running
    running = True

    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            logging.error("Error: Camera could not be accessed.")
            return

        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        cap.set(cv2.CAP_PROP_FPS, 120)

        encodeListKnownIds = read_encode_file_from_storage()
        if encodeListKnownIds is None:
            return

        encodeListKnown, studentIds = encodeListKnownIds
        logging.info(f"Loaded student IDs: {studentIds}")

        print("Launching FaceDetectionThread with date: ", selected_date)
        face_detection_thread = FaceDetectionThread(
            cap, encodeListKnown, studentIds, update_present_students,
            label, face_recognition_db, course_name, section_id, selected_date
        )
        face_detection_thread.start()

        return face_detection_thread

    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        if not running and cap:
            cap.release()
            clear_label(label)

def stop(face_detection_thread):
    global running
    running = False
    if face_detection_thread:
        face_detection_thread.stop()
        face_detection_thread.join()
    if cap:
        cap.release()

def clear_label(label):
    black_image = QImage(640, 480, QImage.Format_RGB888)
    black_image.fill(Qt.black)
    pixmap = QPixmap.fromImage(black_image)
    label.setPixmap(pixmap)
    label.update()

if __name__ == "__main__":
    app = QApplication([])
    label = QLabel()
    label.show()

    selected_date = datetime.now().strftime('%Y-%m-%d')  # Default to today's date

    face_detection_thread = launch(label, FaceRecognitionFirebaseDB(), "course_name", "section_id", lambda x: print(x), selected_date)

    app.exec_()

    stop(face_detection_thread)

##########################################################

# # Set up logging
# logging.basicConfig(level=logging.DEBUG)

# # Initialize Firebase Admin SDK
# cred = credentials.Certificate("serviceAccountKey.json")
# if not firebase_admin._apps:
#     initialize_app(cred, {
#         'databaseURL': "https://spring-capstone-c5472-default-rtdb.firebaseio.com/",
#         'storageBucket': 'spring-capstone-c5472.appspot.com'
#     })

# # Fetch database reference
# student_ref = db.reference('Students')
# bucket = storage.bucket()

# # Blink detection functions
# def eye_aspect_ratio(eye):
#     A = dist.euclidean(eye[1], eye[5])
#     B = dist.euclidean(eye[2], eye[4])
#     C = dist.euclidean(eye[0], eye[3])
#     ear = (A + B) / (2.0 * C)
#     return ear

# def is_blinking(eye):
#     EAR_THRESHOLD = 0.25
#     return eye_aspect_ratio(eye) < EAR_THRESHOLD

# # Path to the shape predictor file
# shape_predictor_path = "shape_predictor_68_face_landmarks.dat"

# # Check if the shape predictor file exists
# if not os.path.exists(shape_predictor_path):
#     raise FileNotFoundError(f"shape_predictor_68_face_landmarks.dat file not found. Please ensure it is in the directory: {os.getcwd()}")

# # Initialize dlib's face detector and facial landmark predictor
# detector = dlib.get_frontal_face_detector()
# predictor = dlib.shape_predictor(shape_predictor_path)

# class FaceDetectionThread(threading.Thread):
#     def __init__(self, cap, encodeListKnown, studentIds, update_present_students, label, face_recognition_db, course_name, section_id, selected_date):
#         super().__init__()
#         self.cap = cap
#         self.encodeListKnown = encodeListKnown
#         self.studentIds = studentIds
#         self.update_present_students = update_present_students
#         self.label = label
#         self.face_recognition_db = face_recognition_db
#         self.course_name = course_name
#         self.section_id = section_id
#         self.running = True
#         self.last_update_times = {}
#         self.attendance_cache = {}
#         self.selected_date = selected_date
#         print(f"FaceDetectionThread initialized with date: {self.selected_date}")

#     def run(self):
#         print("FaceDetectionThread started running with date: ", self.selected_date)
#         frame_skip = 5
#         frame_count = 0
#         detected_faces = {}
#         blinking_count = {}

#         while self.running:
#             success, img = self.cap.read()
#             if not success:
#                 logging.error("Failed to capture image from camera.")
#                 break

#             frame_count += 1
#             if frame_count % frame_skip == 0:
#                 gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#                 faces = detector(gray, 0)

#                 detected_students = []

#                 for face in faces:
#                     shape = predictor(gray, face)
#                     shape = face_utils.shape_to_np(shape)

#                     left_eye = shape[36:42]
#                     right_eye = shape[42:48]

#                     if is_blinking(left_eye) or is_blinking(right_eye):
#                         (x, y, w, h) = (face.left(), face.top(), face.width(), face.height())
#                         face_loc = (y, x + w, y + h, x)

#                         encode_face = face_recognition.face_encodings(img, [face_loc])[0]

#                         matches = face_recognition.compare_faces(self.encodeListKnown, encode_face)
#                         face_dis = face_recognition.face_distance(self.encodeListKnown, encode_face)
#                         match_index = np.argmin(face_dis)

#                         if matches[match_index]:
#                             student_id = self.studentIds[match_index]
#                             if student_id not in blinking_count:
#                                 blinking_count[student_id] = 0
#                             blinking_count[student_id] += 1

#                             if blinking_count[student_id] >= 2:  # Require at least 2 blinks
#                                 current_box = [coord * 4 for coord in face_loc]
#                                 detected_faces[student_id] = (current_box, 0)
#                                 self.update_present_students([student_id])
#                                 print(f"Liveliness check passed for {student_id}")
#                                 cv2.rectangle(img, (current_box[3], current_box[0]), (current_box[1], current_box[2]), (0, 255, 0), 2)
#                                 cv2.putText(img, student_id, (current_box[3], current_box[0] - 10), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)
#                         else:
#                             print("No matching student found or failed liveliness check.")
#                     else:
#                         print("No blink detected.")

#                 for student_id in list(detected_faces.keys()):
#                     box, frames_since_last_seen = detected_faces[student_id]
#                     if frames_since_last_seen < 5:
#                         detected_faces[student_id] = (box, frames_since_last_seen + 1)
#                         detected_students.append(student_id)
#                     else:
#                         del detected_faces[student_id]

#                 self.update_present_students(detected_students)

#             frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#             h, w, ch = frame.shape
#             bytes_per_line = ch * w
#             qt_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
#             pixmap = QPixmap.fromImage(qt_image)
#             self.label.setPixmap(pixmap)
#             self.label.update()

#         print("FaceDetectionThread stopped running...")

#     def stop(self):
#         self.running = False
#         print("FaceDetectionThread stopped.")

#     def should_update_attendance(self, student_id):
#         current_time = time.time()
#         last_update_time = self.last_update_times.get(student_id, 0)
#         if current_time - last_update_time > 5:
#             self.last_update_times[student_id] = current_time
#             return True
#         return False

#     def update_attendance(self, student_id, face_recognition_db, course_name, section_id):
#         try:
#             enrolled_students_path = f"Courses/{course_name}-{section_id}/students"
#             enrolled_students_ref = face_recognition_db.db.reference(enrolled_students_path)
#             enrolled_students = enrolled_students_ref.get()
            
#             if not enrolled_students or student_id not in enrolled_students:
#                 logging.info(f"Student {student_id} is not enrolled in course {course_name}, section {section_id}. Attendance not updated.")
#                 return False

#             logging.info(f"Updating attendance for student {student_id} in course {course_name}, section {section_id} on {self.selected_date}")

#             attendance_path = f"Attendance/{course_name}-{section_id}/{self.selected_date}"
#             attendance_ref = face_recognition_db.db.reference(attendance_path)
#             current_attendance = attendance_ref.get() or []

#             if student_id not in current_attendance:
#                 current_attendance.append(student_id)
#                 attendance_ref.set(current_attendance)
#                 logging.info(f"Attendance for {student_id} in class {course_name}-{section_id} recorded for {self.selected_date}.")

#                 student_data = db.reference(f'Students/{student_id}').get()
#                 if student_data:
#                     total_attendance = student_data.get("total_attendance", 0)
#                     attendance_dates = student_data.get("attendance_dates", [])
#                     if self.selected_date not in attendance_dates:
#                         new_attendance = total_attendance + 1
#                         attendance_dates.append(self.selected_date)
#                         db.reference(f'Students/{student_id}').update({
#                             "total_attendance": new_attendance,
#                             "attendance_dates": attendance_dates
#                         })
#                         logging.info(f"Updated total attendance for {student_id}: {new_attendance}")
#                     else:
#                         logging.info(f"Attendance for {student_id} already recorded today.")
#                 else:
#                     logging.warning(f"Student {student_id} not found in database.")
#             else:
#                 logging.info(f"Attendance for {student_id} in class {course_name}-{section_id} already recorded for {self.selected_date}.")
#                 return False
#         except Exception as e:
#             logging.error(f"Error updating attendance for {student_id}: {e}")
#             return False
#         return True

# def read_encode_file_from_storage():
#     blob = bucket.blob('Resources/EncodeFile.p')
#     try:
#         content = blob.download_as_string()
#         encodeListKnownIds = pickle.loads(content)
#         logging.info("Read successful")
#         return encodeListKnownIds
#     except Exception as e:
#         logging.error(f"Read unsuccessful: {e}")
#         return None

# def launch(label, face_recognition_db, course_name, section_id, update_present_students, selected_date):
#     global cap, running
#     running = True

#     try:
#         cap = cv2.VideoCapture(0)
#         if not cap.isOpened():
#             logging.error("Error: Camera could not be accessed.")
#             return

#         cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
#         cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
#         cap.set(cv2.CAP_PROP_FPS, 120)

#         encodeListKnownIds = read_encode_file_from_storage()
#         if encodeListKnownIds is None:
#             return

#         encodeListKnown, studentIds = encodeListKnownIds
#         logging.info(f"Loaded student IDs: {studentIds}")

#         print("Launching FaceDetectionThread with date: ", selected_date)
#         face_detection_thread = FaceDetectionThread(
#             cap, encodeListKnown, studentIds, update_present_students,
#             label, face_recognition_db, course_name, section_id, selected_date
#         )
#         face_detection_thread.start()

#         return face_detection_thread

#     except Exception as e:
#         logging.error(f"An error occurred: {e}")
#     finally:
#         if not running and cap:
#             cap.release()
#             clear_label(label)

# def stop(face_detection_thread):
#     global running
#     running = False
#     if face_detection_thread:
#         face_detection_thread.stop()
#         face_detection_thread.join()
#     if cap:
#         cap.release()

# def clear_label(label):
#     black_image = QImage(640, 480, QImage.Format_RGB888)
#     black_image.fill(Qt.black)
#     pixmap = QPixmap.fromImage(black_image)
#     label.setPixmap(pixmap)
#     label.update()

# if __name__ == "__main__":
#     app = QApplication([])
#     label = QLabel()
#     label.show()

#     selected_date = datetime.now().strftime('%Y-%m-%d')  # Default to today's date

#     face_detection_thread = launch(label, FaceRecognitionFirebaseDB(), "course_name", "section_id", lambda x: print(x), selected_date)

#     app.exec_()

#     stop(face_detection_thread)