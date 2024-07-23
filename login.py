# import logging
# import cv2
# import mediapipe as mp
# import pickle
# import numpy as np
# import time
# from PyQt5 import QtWidgets, uic
# from PyQt5.QtCore import pyqtSignal
# from PyQt5.QtWidgets import QMessageBox

# class LoginForm(QtWidgets.QWidget):
#     login_successful = pyqtSignal()

#     def __init__(self):
#         super(LoginForm, self).__init__()
#         uic.loadUi('login.ui', self)
#         self.loginButton.clicked.connect(self.login)
#         self.faceRecognitionButton.clicked.connect(self.face_recognition_login)
#         self.forgotPasswordButton.clicked.connect(self.forgot_password)
#         self.needHelpButton.clicked.connect(self.need_help)

#     def login(self):
#         username = self.usernameLineEdit.text()
#         password = self.passwordLineEdit.text()
#         if self.validate_login(username, password):
#             QMessageBox.information(self, "Login Successful", "You have logged in successfully!")
#             self.login_successful.emit()
#             self.close()
#         else:
#             QMessageBox.warning(self, "Login Failed", "Invalid username or password!")

#     def face_recognition_login(self):
#         if self.validate_face_recognition():
#             QMessageBox.information(self, "Login Successful", "Face recognition successful!")
#             self.login_successful.emit()
#             self.close()
#         else:
#             QMessageBox.warning(self, "Login Failed", "Face recognition failed!")

#     def capture_face_encoding_from_camera(self):
#         logging.debug("Capturing face from the camera.")
#         video_capture = cv2.VideoCapture(0)
#         if not video_capture.isOpened():
#             logging.error("Unable to open camera.")
#             return None
        
#         logging.debug("Waiting for 5 seconds to allow the user to position their face.")
#         time.sleep(5)
#         ret, frame = video_capture.read()
#         video_capture.release()
#         if not ret:
#             logging.error("Failed to capture image from camera.")
#             return None

#         rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         face_mesh = mp.solutions.face_mesh.FaceMesh(static_image_mode=True)
#         results = face_mesh.process(rgb_frame)
#         if results.multi_face_landmarks:
#             face_landmarks = results.multi_face_landmarks[0]
#             flattened_landmarks = [(landmark.x, landmark.y, landmark.z) for landmark in face_landmarks.landmark]
#             flattened_landmarks = [coord for point in flattened_landmarks for coord in point]
#             return np.array(flattened_landmarks)
#         else:
#             logging.debug("No faces found in the captured image.")
#             return None

#     def validate_face_recognition(self):
#         logging.debug("Validating face recognition.")
#         captured_face_encoding = self.capture_face_encoding_from_camera()
#         if captured_face_encoding is None:
#             logging.debug("No face encoding captured.")
#             return False

#         logging.debug("Reading teacher encodings from file.")
#         with open("TeacherEncodeFile.p", "rb") as f:
#             teacher_encodings = pickle.load(f)
        
#         tolerance = 2.5 # Increase the tolerance level
#         for idx, teacher_encoding in enumerate(teacher_encodings):
#             distance = np.linalg.norm(np.array(teacher_encoding) - captured_face_encoding)
#             logging.debug(f"Distance to teacher encoding {idx}: {distance}")
#             if distance < tolerance:
#                 logging.debug(f"Face recognized with distance: {distance}")
#                 return True

#         logging.debug("Face not recognized.")
#         return False
    
#     def validate_login(self, username, password):
#             # Replace with your actual username and password validation logic
#             # Example: Simple hardcoded check
#             if username == 'admin' and password == 'password':
#                 return True
#             return False
#     def forgot_password(self):
#         QMessageBox.information(self, "Forgot Password", "Password recovery instructions sent to your email.")

#     def need_help(self):
#         QMessageBox.information(self, "Need Help?", "Please contact support for assistance.")

# if __name__ == "__main__":
#     app = QtWidgets.QApplication([])
#     window = LoginForm()
#     window.show()
#     app.exec_()



import logging
import cv2
import mediapipe as mp
import pickle
import numpy as np
import time
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import pyqtSignal, QTimer, QThread, pyqtSlot, Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMessageBox, QLabel, QPushButton

class CameraThread(QThread):
    frame_captured = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self.cap = cv2.VideoCapture(0)
        self.running = True
        self.face_mesh = mp.solutions.face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, min_detection_confidence=0.5)
        self.drawing_utils = mp.solutions.drawing_utils
        self.drawing_spec = mp.solutions.drawing_styles.get_default_face_mesh_tesselation_style()

    def run(self):
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                # Convert the frame to RGB
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = self.face_mesh.process(rgb_frame)
                if results.multi_face_landmarks:
                    for face_landmarks in results.multi_face_landmarks:
                        self.drawing_utils.draw_landmarks(
                            image=frame,
                            landmark_list=face_landmarks,
                            connections=mp.solutions.face_mesh.FACEMESH_TESSELATION,
                            landmark_drawing_spec=None,
                            connection_drawing_spec=self.drawing_spec
                        )
                self.frame_captured.emit(frame)

    def stop(self):
        self.running = False
        self.cap.release()

class LoginForm(QtWidgets.QWidget):
    login_successful = pyqtSignal()

    def __init__(self):
        super(LoginForm, self).__init__()
        uic.loadUi('login.ui', self)
        self.loginButton.clicked.connect(self.login)
        self.faceRecognitionButton.clicked.connect(self.face_recognition_login)
        self.forgotPasswordButton.clicked.connect(self.forgot_password)
        self.needHelpButton.clicked.connect(self.need_help)

        # Add a label to show the camera feed
        self.videoLabel = QLabel(self)
        self.videoLabel.setGeometry(140, 300, 320, 240) #setGeometry(x, y, width, height)

        # Add a retry button for face recognition
        self.retryButton = QPushButton("Retry Face Recognition", self)
        self.retryButton.setGeometry(340, 460, 200, 40)
        self.retryButton.setVisible(False)
        self.retryButton.clicked.connect(self.face_recognition_login)

        # Start the camera thread
        self.camera_thread = CameraThread()
        self.camera_thread.frame_captured.connect(self.update_video_label)
        self.camera_thread.start()

        self.setFixedSize(600, 600)  # Set fixed size of the window
        self.center()

    def center(self):
        frameGm = self.frameGeometry()
        screen = QtWidgets.QApplication.desktop().screenNumber(QtWidgets.QApplication.desktop().cursor().pos())
        centerPoint = QtWidgets.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    @pyqtSlot(np.ndarray)
    def update_video_label(self, frame):
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        p = convert_to_qt_format.scaled(320, 240, aspectRatioMode=1)
        self.videoLabel.setPixmap(QPixmap.fromImage(p))

    def login(self):
        username = self.usernameLineEdit.text()
        password = self.passwordLineEdit.text()
        if self.validate_login(username, password):
            QMessageBox.information(self, "Login Successful", "You have logged in successfully!")
            self.login_successful.emit()
            self.camera_thread.stop()
            self.close()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password!")

    def face_recognition_login(self):
        self.retryButton.setVisible(False)
        QMessageBox.information(self, "Face Recognition", "Look into the camera for 5 seconds.")
        QTimer.singleShot(5000, self.perform_face_recognition)

    def perform_face_recognition(self):
        if self.validate_face_recognition():
            msg_box = QMessageBox(QMessageBox.Information, "Login Successful", "Face recognition successful!")
            msg_box.show()
            QTimer.singleShot(3000, msg_box.close)
            QTimer.singleShot(3000, self.close_successfully)
        else:
            QMessageBox.warning(self, "Login Failed", "Face recognition failed!")
            self.retryButton.setVisible(True)

    def close_successfully(self):
        self.login_successful.emit()
        self.camera_thread.stop()
        self.close()

    def capture_face_encoding_from_camera(self):
        logging.debug("Capturing face from the camera.")
        ret, frame = self.camera_thread.cap.read()
        if not ret:
            logging.error("Failed to capture image from camera.")
            return None

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_mesh = mp.solutions.face_mesh.FaceMesh(static_image_mode=True)
        results = face_mesh.process(rgb_frame)
        if results.multi_face_landmarks:
            face_landmarks = results.multi_face_landmarks[0]
            flattened_landmarks = [(landmark.x, landmark.y, landmark.z) for landmark in face_landmarks.landmark]
            flattened_landmarks = [coord for point in flattened_landmarks for coord in point]
            return np.array(flattened_landmarks)
        else:
            logging.debug("No faces found in the captured image.")
            return None

    def validate_face_recognition(self):
        logging.debug("Validating face recognition.")
        captured_face_encoding = self.capture_face_encoding_from_camera()
        if captured_face_encoding is None:
            logging.debug("No face encoding captured.")
            return False

        logging.debug("Reading teacher encodings from file.")
        with open("TeacherEncodeFile.p", "rb") as f:
            teacher_encodings = pickle.load(f)
        
        tolerance = 2.5 # Increase the tolerance level
        for idx, teacher_encoding in enumerate(teacher_encodings):
            distance = np.linalg.norm(np.array(teacher_encoding) - captured_face_encoding)
            logging.debug(f"Distance to teacher encoding {idx}: {distance}")
            if distance < tolerance:
                logging.debug(f"Face recognized with distance: {distance}")
                return True

        logging.debug("Face not recognized.")
        return False

    def validate_login(self, username, password):
        # Replace with your actual username and password validation logic
        # Example: Simple hardcoded check
        if username == 'admin' and password == 'password':
            return True
        return False

    def forgot_password(self):
        QMessageBox.information(self, "Forgot Password", "Password recovery instructions sent to your email.")

    def need_help(self):
        QMessageBox.information(self, "Need Help?", "Please contact support for assistance.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    app = QtWidgets.QApplication([])
    window = LoginForm()
    window.show()
    app.exec_()
