import logging
import firebase_admin
from firebase_admin import credentials, db, storage
import numpy as np
import csv


class FaceRecognitionFirebaseDB():
    def __init__(self, name="TestDB"):
        self._cred = credentials.Certificate("serviceAccountKey.json")
        if not firebase_admin._apps:
            firebase_admin.initialize_app(self._cred, {
                'databaseURL': "https://spring-capstone-c5472-default-rtdb.firebaseio.com/",
                'storageBucket': 'spring-capstone-c5472.appspot.com'
            })
        self._name = name
        self._student_ref = db.reference('Students')
        self._bucket = storage.bucket()
        self._blob = None
        
        self._instructor_ref = db.reference('Instructors')
        self._course_ref = db.reference('Courses')
        self._attendance_ref = db.reference('Attendance')



        self.current_course_name = None
        self.current_section_id = None

    def __str__(self):
        return self._name

    # def addAttendance(self, attendanceDict):
    #     for key, value in attendanceDict.items():
    #         self._attendance_ref.child(key).set(value)


    def set_course_context(self, course_name, section_id):
        self.current_course_name = course_name
        self.current_section_id = section_id

    def get_course_context(self):
        return self.current_course_name, self.current_section_id

    def addAttendance(self, course_name, section_id, date, student_id):
        attendance_ref = self._attendance_ref.child(f"{course_name}-{section_id}/{date}")
        current_attendance = attendance_ref.get()

        if current_attendance is None or isinstance(current_attendance, dict):
            current_attendance = []

        if student_id not in current_attendance:
            current_attendance.append(student_id)
            attendance_ref.set(current_attendance)

    def getEnrolledStudents(self, course_name, section_id):
        try:
            enrolled_students_ref = self._course_ref.child(f"{course_name}-{section_id}/students")
            enrolled_students = enrolled_students_ref.get()
            return enrolled_students
        except Exception as e:
            logging.error(f"Error occurred while retrieving enrolled students: {str(e)}")
            raise


    def addCourse(self, courseDict):
        for key, value in courseDict.items():
            self._course_ref.child(key).set(value)

    def addStudent(self, studentDict):
        for key, value in studentDict.items():
            self._student_ref.child(key).set(value)

    def addInstructor(self, instructorDict):
        for key, value in instructorDict.items():
            self._instructor_ref.child(key).set(value)

    def getStudent(self, studentID: str):
        return db.reference(f"Students/{studentID}").get()

    def getInstructor(self, instructorID: str):
        return db.reference(f"Instructors/{instructorID}").get()

    def getCourse(self, course_name: str, section_id: str):
        return db.reference(f"Courses/{course_name}-{section_id}").get()

    def getAttendance(self, course_name: str, section_id: str, date: str):
        return db.reference(f"Attendance/{course_name}-{section_id}/{date}").get()

    def deleteStudent(self, student_id):
        try:
            logging.debug(f"Deleting student with ID: {student_id}")

            # Remove the student from all enrolled courses
            all_courses = self.getAllCourses()
            for course_name, course_info in all_courses.items():
                if student_id in course_info.get("students", []):
                    course_info["students"].remove(student_id)
                    self.updateCourseData(course_info["course_name"], course_info["section_id"], course_info["course_name"], course_info["section_id"], course_info)

            # Delete the student record from the database
            student_ref = self._student_ref.child(student_id)
            student_ref.delete()
            logging.info(f"Student with ID {student_id} deleted successfully.")
        except Exception as e:
            logging.error(f"Error during delete: {str(e)}")
            raise

    def deleteCourse(self, course_name, section_id):
        try:
            logging.debug(f"Deleting Course with ID: {course_name}-{section_id}")
            course_ref = self._course_ref.child(f"{course_name}-{section_id}")
            course_ref.delete()
            logging.info(f"Course with ID {course_name}-{section_id} deleted successfully.")
        except Exception as e:
            logging.error(f"Error during delete: {str(e)}")
            raise
    
    def setEnrolledStudents(self, course_name, section_id, students :list):
        try:
            course_ref = self._course_ref.child(f"{course_name}-{section_id}/students")
            course_ref.set(students)
        except Exception as e:
            logging.error(f"Error during delete: {str(e)}")
            raise

    def getEnrolledStudents(self, course_name, section_id):
        try:
            enrolled_students_ref = self._course_ref.child(f"{course_name}-{section_id}/students")
            enrolled_students = enrolled_students_ref.get()
            return enrolled_students
        except Exception as e:
            logging.error(f"Error occured while retrieving enrolled students: {str(e)}")
            raise
    
    def getStudentinfofromList(self, student_ids):
        if student_ids == None:
            return {}
        try:
            studentInfo = {}
            for id in student_ids:
                studentInfo.update({id:self.getStudent(id)})
            return studentInfo
        except Exception as e:
            logging.error(f"Error occured while retrieving student info from IDs: {str(e)}")
            raise

    def getAllStudents(self):
        return self._student_ref.get()

    def getAllCourses(self):
        return self._course_ref.get()

    def updateCourseData(self, course_name: str, section_id: str, oldCourseID: str, old_section_id: str, newCourseData: dict):
        try:
            if course_name != oldCourseID or section_id != old_section_id:
                values = self.getCourse(oldCourseID, old_section_id)
                self.deleteCourse(values["course_name"], values["section_id"])
                for key in newCourseData.keys():
                    values[key] = newCourseData[key]
                self.addCourse({f"{course_name}-{section_id}": values})
            else:
                ref = db.reference(f"Courses/{course_name}-{section_id}")
                for key in newCourseData.keys():
                    try:
                        ref.child(key).set(newCourseData[key])
                    except Exception as e:
                        logging.error(f"Error updating student data: {str(e)}")
                        pass
        except Exception as e:
            print("An error occurred during deletion: ", e)

    def updateStudent(self, studentID: str, oldID: int, newStudentData: dict):
        student_info = self.getStudent(studentID)
        if studentID != oldID:
            values = self.getStudent(oldID)
            self.deleteStudent(values["student_id"])
            values["student_id"] = newStudentData["student_id"]
            for key in newStudentData.keys():
                values[key] = newStudentData[key]
            self.addStudent({values["student_id"]: values})
        else:
            ref = db.reference(f"Students/{studentID}")
            for key in newStudentData.keys():
                try:
                    ref.child(key).set(newStudentData[key])
                except Exception as e:
                    logging.error(f"Error updating student data: {str(e)}")
                    pass


    def updateStudentImage(self, student_id, image_url):
        try:
            # Update the student's record with the new image URL
            student_ref = db.reference(f"Students/{student_id}")
            student_ref.update({"image_url": image_url})
            print(f"Updated student {student_id} with image URL {image_url}")
        except Exception as e:
            print(f"Failed to update student image URL: {e}")


    def updateInstructorData(self, instructorID: str, newInstructorData: dict, fields: list):
        instructor_info = self.getInstructor(instructorID)
        for key, value in newInstructorData.items():
            try:
                instructor_info[key] = value
                ref = db.reference(f"Instructors/{instructorID}")
                ref.child(key).set(value)
            except Exception as e:
                logging.error(f"Error updating instructor data: {str(e)}")
                pass

    def getImgFromStorage(self, studentID: str):
        try:
            self._blob = self._bucket.get_blob(f"Images/{studentID}.png")
            self.img_array = np.frombuffer(self._blob.download_as_string(), np.uint8)
            print("Download successful")
        except Exception as e:
            logging.error(f"Download unsuccessful: {str(e)}")

    # Function to read the CSV file and create a dictionary
    def csv_to_dict(self, filename):
        student_dict = {}
        
        with open(filename, newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                student_id = row['student_id']
                student_dict[student_id] = {
                    'student_id': row['student_id'],
                    'full_name': row['fullname'],
                    'major': row['academic_major'],
                    'minor': row['academic_minor'],
                    'total_attendance': int(row['total_attendance'])
                }
        
        return student_dict

    def batchUploadStudents(self, fileName):
        student_dict = self.csv_to_dict(fileName)
        # Print the dictionary to verify
        print(student_dict)
        for student_id, details in student_dict.items():
            self.addStudent({student_id:details})

    def updateAttendanceStatus(self, course_name, section_id, student_id, date, is_present):
        attendance_ref = self._attendance_ref.child(f"{course_name}-{section_id}/{date}")
        current_attendance = attendance_ref.get()

        if current_attendance is None or isinstance(current_attendance, dict):
            current_attendance = []

        if is_present:
            if student_id not in current_attendance:
                current_attendance.append(student_id)
        else:
            if student_id in current_attendance:
                current_attendance.remove(student_id)

        attendance_ref.set(current_attendance)



    def getAttendance(self, course_name, section_id, date):
        try:
            attendance_ref = self._attendance_ref.child(f"{course_name}-{section_id}/{date}")
            return attendance_ref.get()
        except Exception as e:
            logging.error(f"Error retrieving attendance data: {str(e)}")
            raise
        

        

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    print("Testing database")

    testDB = FaceRecognitionFirebaseDB("testDB")
    # testDB.batchUploadStudents('students.csv')

    # course_data = {
    #     "CMPT101-AS01": {
    #         "course_name": "CMPT101",
    #         "section_id": "AS01",
    #         "meeting_days": ["Monday", "Tuesday"],
    #         "capacity": 30
    #     }
    # }
    # testDB.addCourse(course_data)
    # testPull = testDB.getCourse("CMPT101", "AS01")
    
    # print(testPull)

    # attendance_data = {
    #     "CMPT101-AS01/2024-05-30": [1, 2, 3, 4, 5, 6, 7, 8, 9]
    # }
    # testDB.addAttendance(attendance_data)
    # testPull = testDB.getAttendance("CMPT101", "AS01", "2024-05-30")
    
    # print(testPull)
