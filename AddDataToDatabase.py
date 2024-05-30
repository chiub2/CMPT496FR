import logging
import firebase_admin
from firebase_admin import credentials, db, storage
import numpy as np



class FaceRecognitionFirebaseDB():
    def __init__(self, name = "TestDB"):
        self._cred = credentials.Certificate("serviceAccountKey.json")
        firebase_admin.initialize_app(self._cred, {
            'databaseURL': "https://spring-capstone-c5472-default-rtdb.firebaseio.com/",
            'storageBucket': 'spring-capstone-c5472.appspot.com'
        
        })
        self._name = name
        self._student_ref = db.reference('Students')
        self._bucket = storage.bucket()
        self._blob = None
        ''' Student Data format
        {
            StudentID: {
                "full_name": 
                "major:
                "minor":
                "total_attendance": 
            }

        }
        '''
        self._instructor_ref = db.reference('Instructors')
        ''' Instructor Data format
        {
            InstructorID: {
                "first_name": 
                "last_name": 
                "department": 
                "email": 
                "password": 
            }

        }
        '''
        self._course_ref = db.reference('Courses')
        ''' Course Data format
        {
            CourseName-sectionID: {
                "course_name": 
                "section_id:
                "meeting_days": ["day1", "day2"]
                "capacity": 
                "enrolled":
                "students_enrolled": [1, 2 ... n]
            }

        }
        '''
        self._attendance_ref = db.reference('Attendance')
        ''' Course Data format
        {
            "CourseName-sectionID/Date": [studentID1, studentID2, studentID3 ... studentIDn]
            }

        }
        '''
    def __str__(self):
        return self._name

    def addAttendance(self, attendanceDict):

        for key, value in attendanceDict.items():
            self._attendance_ref.child(key).set(value)

    def addCourse(self, courseDict):
        print(courseDict)
        for key, value in courseDict.items():
            self._course_ref.child(key).set(value)

    def addStudent(self, studentDict):
        for key, value in studentDict.items():
            self._student_ref.child(key).set(value)

    def addInstructor(self, instructorDict):
        for key, value in instructorDict.items():
            self._instructor_ref.child(key).set(value)

    def getStudentDB(self, studentID: str):
        ''' Make API call to get ONE student from firebase'''
        return db.reference(f"Students/{studentID}").get()

    def getInstructorDB(self, instructorID: str):
        ''' Make API call to get ONE instructor from firebase'''
        return db.reference(f"Instructors/{instructorID}").get()
    
    def getCourseDB(self, course_name: str, section_id: str):
        ''' Make API call to get ONE student from firebase'''
        return db.reference(f"Courses/{course_name}-{section_id}").get()
    
    def getAttendanceDB(self, course_name: str, section_id: str, date:str):
        ''' Make API call to get ONE student from firebase'''
        return db.reference(f"Attendance/{course_name}-{section_id}/{date}").get()

    def deleteStudent(self, student_id):
        try:
            logging.debug(f"Deleting student with ID: {student_id}")
            student_ref = self._student_ref.child(student_id)
            student_ref.remove()  # Correct method to delete a node in Firebase Realtime Database
            logging.info(f"Student with ID {student_id} deleted successfully.")
        except Exception as e:
            logging.error(f"Error during delete: {str(e)}")
            raise

    def getAllStudents(self):
        return self._student_ref.get()
    
    def getAllCourses(self):
        return self._course_ref.get()

    def updateStudentData(self, studentID: str, newStudentData: dict):
        student_info = self.getStudentDB(studentID)
        for key in newStudentData.keys():
            try:
                student_info[key] = newStudentData[key]
                ref = db.reference(f"Students/{studentID}")
                ref.child(key).set(student_info[key])
            except Exception as e:
                logging.error(f"Error updating student data: {str(e)}")
                pass

    def updateInstructorData(self, instructorID: str, newInstructorData: dict, fields: list):
        instructor_info = self.getInstructorDB(instructorID)
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




if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    print("Testing database")

    testDB = FaceRecognitionFirebaseDB("testDB")

    course_data = {
        "CMPT101-AS01": {
            "course_name": "CMPT101",
            "section_id": "AS01",
            "meeting_days": ["Monday", "Tuesday"],
            "capacity": 30
        }
    }
    testDB.addCourse(courseDict=course_data)
    testPull = testDB.getCourseDB("CMPT101", "AS01")
    
    print(testPull)

    attendance_data = {
        "CMPT101-AS01/2024-05-30": [1,2,3,4,5,6,7,8,9]
    }
    testDB.addAttendance(attendance_data)
    testPull = testDB.getAttendanceDB("CMPT101", "AS01", "2024-05-30")
    
    print(testPull)
    # student_data = {
    #     "3101002": {
    #         "name": "Olasubomi Badiru",
    #         "major": "Computer Science",
    #         "minor": "Mathematics",
    #         "total_attendance": 0
    #     }
    # }

    # instructor_data = {
    #     "9101001": {
    #         "first_name": "Mohammed",
    #         "last_name": "El-hajj",
    #         "department": "Computer Science",
    #         "email": "elhajjm@macewan.ca",
    #         "password": "barcelona"
    #     }
    # }
    # testDB.addStudent(student_data)
    # testDB.addStudent({
    #     "3101003": {
    #         "name": "Will Smith"
    #     }
    # })
    # testDB.addStudent({
    #     "3101004": {
    #         "name": "Cardi Bee"
    #     }
    # })
    # testDB.updateStudentData("3101003", {"major": "Music", "minor": "Rap studies"})
    # cardiTest = testDB.getStudentDB("3101003")
    # print(cardiTest)

    # testDB.addInstructor(instructor_data)