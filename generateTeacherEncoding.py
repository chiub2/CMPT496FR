import cv2
import mediapipe as mp
import pickle
import os

def generate_teacher_encodings():
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True)
    teacher_encodings = []

    folder_path = "Teacher_Images"
    for filename in os.listdir(folder_path):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            img_path = os.path.join(folder_path, filename)
            img = cv2.imread(img_path)
            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(rgb_img)
            if results.multi_face_landmarks:
                face_landmarks = results.multi_face_landmarks[0]
                flattened_landmarks = [(landmark.x, landmark.y, landmark.z) for landmark in face_landmarks.landmark]
                flattened_landmarks = [coord for point in flattened_landmarks for coord in point]
                teacher_encodings.append(flattened_landmarks)

    with open("TeacherEncodeFile.p", "wb") as f:
        pickle.dump(teacher_encodings, f)

if __name__ == "__main__":
    generate_teacher_encodings()
    print("Teacher face encodings generated and saved successfully.")
