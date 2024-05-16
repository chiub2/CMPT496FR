import cv2
import pickle
import face_recognition
import numpy as np
import os

def launch():
    try:
        # Check for camera access
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Camera could not be accessed.")
            return
        
        # Set camera resolution
        cap.set(3, 640)
        cap.set(4, 480)

        # Check for necessary files
        background_path = "Resources/background.png"
        encodings_path = "Resources/EncodeFile.p"
        if not os.path.exists(background_path) or not os.path.exists(encodings_path):
            print("Error: File path(s) incorrect.")
            return
        
        # Load background and encodings
        imgBackground = cv2.imread(background_path)
        with open(encodings_path, 'rb') as file:
            encodeListKnownIds = pickle.load(file)
        encodeListKnown, studentIds = encodeListKnownIds
        print("Loaded student IDs:", studentIds)

        frame_skip = 5
        frame_count = 0
        prev_box = None  # Previous bounding box for smoothing
        alpha = 0.2  # Smoothing factor for box transitions

        while True:
            success, img = cap.read()
            if not success:
                print("Failed to capture image from camera.")
                break

            frame_count += 1
            if frame_count % frame_skip == 0:
                # Process face recognition every `frame_skip` frames
                imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
                imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
                faceCurFrame = face_recognition.face_locations(imgS)
                encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

                for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
                    matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
                    faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
                    matchIndex = np.argmin(faceDis)
                    if matches[matchIndex]:
                        current_box = [coord * 4 for coord in faceLoc]  # Adjust coordinates
                        if prev_box is not None:
                            # Smooth transitions for bounding box
                            current_box = [int(prev_box[i] * (1 - alpha) + current_box[i] * alpha) for i in range(4)]
                        prev_box = current_box
                        cv2.rectangle(img, (current_box[3], current_box[0]), (current_box[1], current_box[2]), (0, 255, 0), 2)
                        cv2.putText(img, studentIds[matchIndex], (current_box[3], current_box[0] - 10), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)
                        print('Detected:', studentIds[matchIndex])
            else:
                # Display last known box and label between detections
                if prev_box is not None:
                    cv2.rectangle(img, (prev_box[3], prev_box[0]), (prev_box[1], prev_box[2]), (0, 255, 0), 2)
                    cv2.putText(img, studentIds[matchIndex], (prev_box[3], prev_box[0] - 10), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)

            # Show updated image with background
            imgBackground[162:162+480, 55:55+640] = img
            cv2.imshow("Face Attendance", imgBackground)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except Exception as e:
        print("An error occurred:", e)

    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    launch()
