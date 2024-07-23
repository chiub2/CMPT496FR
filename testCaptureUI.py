from datetime import datetime
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
import asyncio
import qasync
from FireBaseDB import FaceRecognitionFirebaseDB
import threading

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

class FaceDetectionThread(threading.Thread):
    def __init__(self, cap, encodeListKnown, studentIds, update_present_students, label, face_recognition_db, course_name, section_id):
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

    def run(self):
        frame_skip = 5
        frame_count = 0
        detected_faces = {}

        while self.running:
            success, img = self.cap.read()
            if not success:
                logging.error("Failed to capture image from camera.")
                break

            frame_count += 1
            if frame_count % frame_skip == 0:
                imgS = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
                imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
                faceCurFrame = face_recognition.face_locations(imgS)
                encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

                detected_students = []

                for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
                    matches = face_recognition.compare_faces(self.encodeListKnown, encodeFace)
                    faceDis = face_recognition.face_distance(self.encodeListKnown, encodeFace)
                    matchIndex = np.argmin(faceDis)
                    if matches[matchIndex]:
                        student_id = self.studentIds[matchIndex]
                        logging.info(f"Matched student ID: {student_id}")
                        current_box = [coord * 4 for coord in faceLoc]
                        detected_faces[student_id] = (current_box, 0)  # Reset frame count for the detected face
                        detected_students.append(student_id)
                        logging.info(f"Detected: {student_id}")
                        logging.info(f"Calling update_attendance with student_id: {student_id}")
                        self.update_attendance(student_id, self.face_recognition_db, self.course_name, self.section_id)
                    else:
                        logging.info("No matching student found.")

                # Increment the frame count for faces that were not detected in the current frame
                for student_id in list(detected_faces.keys()):
                    box, frames_since_last_seen = detected_faces[student_id]
                    if frames_since_last_seen < 5:  # Keep the box for up to 5 frames
                        detected_faces[student_id] = (box, frames_since_last_seen + 1)
                        detected_students.append(student_id)
                    else:
                        del detected_faces[student_id]

                self.update_present_students(detected_students)  # Call the callback function with all detected student IDs

            # Draw all detected faces
            for student_id, (box, _) in detected_faces.items():
                cv2.rectangle(img, (box[3], box[0]), (box[1], box[2]), (0, 255, 0), 2)
                cv2.putText(img, student_id, (box[3], box[0] - 10), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)

            frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            qt_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qt_image)
            self.label.setPixmap(pixmap)
            self.label.update()

    def stop(self):
        self.running = False

    @staticmethod
    def update_attendance(student_id, face_recognition_db, course_name, section_id):
        try:
            # Check if the student is enrolled in the course and section
            enrolled_students_path = f"Courses/{course_name}-{section_id}/students"
            enrolled_students_ref = face_recognition_db.db.reference(enrolled_students_path)
            enrolled_students = enrolled_students_ref.get()
            
            if not enrolled_students or student_id not in enrolled_students:
                logging.info(f"Student {student_id} is not enrolled in course {course_name}, section {section_id}. Attendance not updated.")
                return

            now = datetime.now().strftime('%Y-%m-%d')
            logging.info(f"Updating attendance for student {student_id} in course {course_name}, section {section_id} on {now}")

            attendance_path = f"Attendance/{course_name}-{section_id}/{now}"
            attendance_ref = face_recognition_db.db.reference(attendance_path)
            current_attendance = attendance_ref.get()
            if current_attendance is None:
                current_attendance = []

            if student_id not in current_attendance:
                current_attendance.append(student_id)
                attendance_ref.set(current_attendance)
                logging.info(f"Attendance for {student_id} in class {course_name}-{section_id} recorded for {now}.")

                # Increment total attendance for the student
                FaceDetectionThread.increment_student_attendance(student_id)
            else:
                logging.info(f"Attendance for {student_id} in class {course_name}-{section_id} already recorded for {now}.")
        except Exception as e:
            logging.error(f"Error updating attendance for {student_id}: {e}")

    @staticmethod
    def increment_student_attendance(student_id):
        try:
            student_data = db.reference(f'Students/{student_id}').get()
            if student_data:
                current_attendance = student_data.get("total_attendance", 0)
                attendance_dates = student_data.get("attendance_dates", [])
                now = datetime.now().strftime('%Y-%m-%d')
                if now not in attendance_dates:
                    new_attendance = current_attendance + 1
                    attendance_dates.append(now)
                    db.reference(f'Students/{student_id}').update({
                        "total_attendance": new_attendance,
                        "attendance_dates": attendance_dates
                    })
                    logging.info(f"Updated total attendance for {student_id}: {new_attendance}")
                else:
                    logging.info(f"Attendance for {student_id} already recorded today.")
            else:
                logging.warning(f"Student {student_id} not found in database.")
        except Exception as e:
            logging.error(f"Error updating total attendance for {student_id}: {e}")

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

def launch(label, face_recognition_db, course_name, section_id, update_present_students):
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

        face_detection_thread = FaceDetectionThread(
            cap, encodeListKnown, studentIds, update_present_students,
            label, face_recognition_db, course_name, section_id
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

    face_detection_thread = launch(label, FaceRecognitionFirebaseDB(), "course_name", "section_id", lambda x: print(x))

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

# cap = None  # Global variable to access camera
# running = False

# face_recognition_db = FaceRecognitionFirebaseDB()

# def update_attendance(student_id, face_recognition_db, course_name, section_id):
#     try:
#         now = datetime.now().strftime('%Y-%m-%d')
#         logging.info(f"Updating attendance for student {student_id} in course {course_name}, section {section_id} on {now}")

#         attendance_ref = face_recognition_db._attendance_ref.child(f"{course_name}-{section_id}/{now}")
#         current_attendance = attendance_ref.get()
#         if not current_attendance:
#             current_attendance = []
#         if student_id not in current_attendance:
#             current_attendance.append(student_id)
#             attendance_ref.set(current_attendance)
#             logging.info(f"Attendance for {student_id} in class {course_name}-{section_id} recorded for {now}.")
#         else:
#             logging.info(f"Attendance for {student_id} in class {course_name}-{section_id} already recorded for {now}.")
#     except Exception as e:
#         logging.error(f"Error updating attendance for {student_id}: {e}")

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

# async def process_frame_async(img, encodeListKnown, studentIds, face_recognition_db, course_name, section_id, update_present_students):
#     imgS = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
#     imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
#     faceCurFrame = face_recognition.face_locations(imgS)
#     encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

#     detected_students = []

#     for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
#         matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
#         faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
#         matchIndex = np.argmin(faceDis)
#         if matches[matchIndex]:
#             student_id = studentIds[matchIndex]
#             logging.info(f"Matched student ID: {student_id}")
#             current_box = [coord * 4 for coord in faceLoc]
#             detected_students.append((student_id, current_box))
#             logging.info(f"Detected: {student_id}")
#             update_attendance(student_id, face_recognition_db, course_name, section_id)
#         else:
#             logging.info("No matching student found.")

#     return img, detected_students

# async def update_frame(label, encodeListKnown, studentIds, face_recognition_db, course_name, section_id, update_present_students, alpha, frame_skip):
#     global cap, running
#     frame_count = 0
#     detected_faces = {}

#     while running:
#         success, img = cap.read()
#         if not success:
#             logging.error("Failed to capture image from camera.")
#             break

#         frame_count += 1
#         if frame_count % frame_skip == 0:
#             img, detected_faces = await process_frame_async(img, encodeListKnown, studentIds, face_recognition_db, course_name, section_id, update_present_students)

#         detected_students = []
#         for student_id, current_box in detected_faces:
#             detected_students.append(student_id)
#             cv2.rectangle(img, (current_box[3], current_box[0]), (current_box[1], current_box[2]), (0, 255, 0), 2)
#             cv2.putText(img, student_id, (current_box[3], current_box[0] - 10), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)

#         update_present_students(detected_students)  # Call the callback function with all detected student IDs

#         frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#         h, w, ch = frame.shape
#         bytes_per_line = ch * w
#         qt_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
#         pixmap = QPixmap.fromImage(qt_image)
#         label.setPixmap(pixmap)
#         label.update()

#         await asyncio.sleep(0)  # Yield control to the event loop

# async def launch(label, face_recognition_db, course_name, section_id, update_present_students):
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

#         alpha = 0.2
#         frame_skip = 5

#         await update_frame(label, encodeListKnown, studentIds, face_recognition_db, course_name, section_id, update_present_students, alpha, frame_skip)

#     except Exception as e:
#         logging.error(f"An error occurred: {e}")
#     finally:
#         if cap:
#             cap.release()
#         cv2.destroyAllWindows()
#         clear_label(label)

# def stop():
#     global running
#     running = False
#     if cap:
#         cap.release()

# def face_distance(face_encodings):
#     return np.linalg.norm(face_encodings)

# def clear_label(label):
#     black_image = QImage(640, 480, QImage.Format_RGB888)
#     black_image.fill(Qt.black)
#     pixmap = QPixmap.fromImage(black_image)
#     label.setPixmap(pixmap)
#     label.update()

# if __name__ == "__main__":
#     app = qasync.QApplication([])
#     label = QLabel()
#     label.show()

#     loop = qasync.QEventLoop(app)
#     asyncio.set_event_loop(loop)

#     asyncio.ensure_future(launch(label, face_recognition_db, "course_name", "section_id", lambda x: print(x)))

#     with loop:
#         loop.run_forever()





# New code for trying with mediapipe Library
# from datetime import datetime
# import cv2
# import mediapipe as mp
# import pickle
# import numpy as np
# import logging
# import firebase_admin
# from firebase_admin import credentials, db, storage
# from PyQt5.QtGui import QImage, QPixmap
# from PyQt5.QtCore import Qt
# import os
# from FireBaseDB import FaceRecognitionFirebaseDB

# logging.basicConfig(level=logging.DEBUG)

# cred = credentials.Certificate("serviceAccountKey.json")
# if not firebase_admin._apps:
#     firebase_admin.initialize_app(cred, {
#         'databaseURL': "https://spring-capstone-c5472-default-rtdb.firebaseio.com/",
#         'storageBucket': 'spring-capstone-c5472.appspot.com'
#     })

# student_ref = db.reference('Students')
# bucket = storage.bucket()

# cap = None
# running = False

# face_recognition_db = FaceRecognitionFirebaseDB()

# def update_attendance(student_id, face_recognition_db, course_name, section_id):
#     try:
#         now = datetime.now().strftime('%Y-%m-%d')
#         logging.info(f"Attempting to update attendance for student {student_id} in course {course_name}, section {section_id} on {now}")

#         attendance_ref = face_recognition_db._attendance_ref.child(f"{course_name}-{section_id}/{now}")
#         current_attendance = attendance_ref.get()
#         if not current_attendance:
#             current_attendance = []

#         enrolled_students_ref = face_recognition_db._attendance_ref.child(f"{course_name}-{section_id}/enrolled_students")
#         enrolled_students = enrolled_students_ref.get() or []

#         if student_id in enrolled_students:
#             if student_id not in current_attendance:
#                 current_attendance.append(student_id)
#                 attendance_ref.set(current_attendance)
#                 logging.info(f"Attendance for {student_id} in class {course_name}-{section_id} recorded for {now}.")
#             else:
#                 logging.info(f"Attendance for {student_id} in class {course_name}-{section_id} already recorded for {now}.")
#         else:
#             logging.info(f"Student {student_id} is not enrolled in course {course_name}, section {section_id}. Attendance not updated.")
#     except Exception as e:
#         logging.error(f"Error updating attendance for {student_id}: {e}")

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

# def launch(label, face_recognition_db, course_name, section_id, update_present_students):
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

#         frame_skip = 5
#         frame_count = 0

#         mp_face_mesh = mp.solutions.face_mesh
#         face_mesh = mp_face_mesh.FaceMesh(
#             static_image_mode=False,
#             max_num_faces=1,
#             refine_landmarks=True,
#             min_detection_confidence=0.5,
#             min_tracking_confidence=0.5
#         )
#         mp_drawing = mp.solutions.drawing_utils
#         mp_drawing_styles = mp.solutions.drawing_styles

#         while running:
#             success, img = cap.read()
#             if not success:
#                 logging.error("Failed to capture image from camera.")
#                 break

#             frame_count += 1
#             if frame_count % frame_skip == 0:
#                 imgS = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
#                 rgb_img = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
#                 results = face_mesh.process(rgb_img)

#                 if results.multi_face_landmarks:
#                     face_landmarks = results.multi_face_landmarks[0]
#                     flattened_landmarks = [(landmark.x, landmark.y, landmark.z) for landmark in face_landmarks.landmark]
#                     flattened_landmarks = [coord for point in flattened_landmarks for coord in point]

#                     if len(flattened_landmarks) != 468 * 3:
#                         if len(flattened_landmarks) > 468 * 3:
#                             flattened_landmarks = flattened_landmarks[:468 * 3]
#                         else:
#                             flattened_landmarks.extend([0] * (468 * 3 - len(flattened_landmarks)))

#                     distances = [np.linalg.norm(np.array(flattened_landmarks) - np.array(known)) for known in encodeListKnown]
#                     min_distance = min(distances)
#                     min_index = distances.index(min_distance)

#                     logging.info(f"Calculated distances: {distances}")
#                     logging.info(f"Minimum distance: {min_distance}, Index: {min_index}")

#                     if min_distance < 2.5:  # Adjust threshold as needed
#                         student_id = studentIds[min_index]
#                         logging.info(f"Matched student ID: {student_id}")
#                         update_attendance(student_id, face_recognition_db, course_name, section_id)
#                         update_present_students([student_id])
#                     else:
#                         logging.info("No matching student found.")

#                     for face_landmarks in results.multi_face_landmarks:
#                         mp_drawing.draw_landmarks(
#                             image=img,
#                             landmark_list=face_landmarks,
#                             connections=mp_face_mesh.FACEMESH_TESSELATION,
#                             landmark_drawing_spec=None,
#                             connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style()
#                         )
#                         mp_drawing.draw_landmarks(
#                             image=img,
#                             landmark_list=face_landmarks,
#                             connections=mp_face_mesh.FACEMESH_CONTOURS,
#                             landmark_drawing_spec=None,
#                             connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_contours_style()
#                         )
#                         mp_drawing.draw_landmarks(
#                             image=img,
#                             landmark_list=face_landmarks,
#                             connections=mp_face_mesh.FACEMESH_IRISES,
#                             landmark_drawing_spec=None,
#                             connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_iris_connections_style()
#                         )

#             frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#             h, w, ch = frame.shape
#             bytes_per_line = ch * w
#             qt_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
#             pixmap = QPixmap.fromImage(qt_image)
#             label.setPixmap(pixmap)
#             label.update()

#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break

#     except Exception as e:
#         logging.error(f"An error occurred: {e}")
#     finally:
#         if cap:
#             cap.release()
#         cv2.destroyAllWindows()
#         clear_label(label)

# def stop():
#     global running
#     running = False
#     if cap:
#         cap.release()

# def clear_label(label):
#     black_image = QImage(640, 480, QImage.Format_RGB888)
#     black_image.fill(Qt.black)
#     pixmap = QPixmap.fromImage(black_image)
#     label.setPixmap(pixmap)
#     label.update()
