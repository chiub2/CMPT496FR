import cv2
import pickle
import face_recognition
import numpy as np
import os

def draw_rounded_rectangle(img, pt1, pt2, color, thickness, radius=20):
    """Draw a rectangle with rounded corners."""
    x1, y1 = pt1
    x2, y2 = pt2

    # Top line
    cv2.line(img, (x1 + radius, y1), (x2 - radius, y1), color, thickness)
    # Bottom line
    cv2.line(img, (x1 + radius, y2), (x2 - radius, y2), color, thickness)
    # Left line
    cv2.line(img, (x1, y1 + radius), (x1, y2 - radius), color, thickness)
    # Right line
    cv2.line(img, (x2, y1 + radius), (x2, y2 - radius), color, thickness)

    # Four corners
    cv2.ellipse(img, (x1 + radius, y1 + radius), (radius, radius), 180, 0, 90, color, thickness)
    cv2.ellipse(img, (x2 - radius, y1 + radius), (radius, radius), 270, 0, 90, color, thickness)
    cv2.ellipse(img, (x1 + radius, y2 - radius), (radius, radius), 90, 0, 90, color, thickness)
    cv2.ellipse(img, (x2 - radius, y2 - radius), (radius, radius), 0, 0, 90, color, thickness)

def draw_label(img, text, position, font=cv2.FONT_HERSHEY_DUPLEX, font_scale=0.5, font_thickness=1, bg_color=(0, 255, 0), text_color=(255, 255, 255)):
    """Draw label with background rectangle for better readability."""
    (text_width, text_height), baseline = cv2.getTextSize(text, font, font_scale, font_thickness)
    x, y = position

    # Draw background
    cv2.rectangle(img, (x, y - text_height - baseline), (x + text_width, y + baseline), bg_color, thickness=cv2.FILLED)

    # Draw text
    cv2.putText(img, text, (x, y - baseline), font, font_scale, text_color, font_thickness)

def launch():
    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Camera could not be accessed.")
            return
        
        cap.set(3, 640)
        cap.set(4, 480)

        background_path = "Resources/background.png"
        encodings_path = "Resources/EncodeFile.p"
        if not os.path.exists(background_path) or not os.path.exists(encodings_path):
            print("Error: File path(s) incorrect.")
            return
        
        imgBackground = cv2.imread(background_path)
        with open(encodings_path, 'rb') as file:
            encodeListKnownIds = pickle.load(file)
        encodeListKnown, studentIds = encodeListKnownIds

        frame_skip = 5
        frame_count = 0
        prev_box = None
        alpha = 0.2

        while True:
            success, img = cap.read()
            if not success:
                break

            frame_count += 1
            if frame_count % frame_skip == 0:
                imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
                imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
                faceCurFrame = face_recognition.face_locations(imgS)
                encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

                for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
                    matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
                    faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
                    matchIndex = np.argmin(faceDis)
                    if matches[matchIndex]:
                        current_box = [coord * 4 for coord in faceLoc]  # Scale coordinates up
                        if prev_box is not None:
                            current_box = [int(prev_box[i] * (1 - alpha) + current_box[i] * alpha) for i in range(4)]
                        prev_box = current_box
                        draw_rounded_rectangle(img, (current_box[3], current_box[0]), (current_box[1], current_box[2]), (0, 255, 0), 2)
                        draw_label(img, studentIds[matchIndex], (current_box[3], current_box[0] - 20))
            else:
                if prev_box is not None:
                    draw_rounded_rectangle(img, (prev_box[3], prev_box[0]), (prev_box[1], prev_box[2]), (0, 255, 0), 2)
                    draw_label(img, studentIds[matchIndex], (prev_box[3], prev_box[0] - 20))

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
