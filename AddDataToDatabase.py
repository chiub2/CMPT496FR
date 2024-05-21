import firebase_admin
from firebase_admin import credentials, db, storage



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
    def __str__(self):
        return self._name
           
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
    
    def getAllStudents(self):
        '''
        Get all students in database
        '''
        return db.reference("Students").get()
    
    def getAllInstructors(self):
        '''
        Get all instructors in database
        '''
        return db.reference("Instructors").get()
    
    def updateStudentData(self, studentID:str, newStudentData:dict):
        '''
        StudentID: string
        newStudentData: dictionary in the ff format: 
            {
            "name": ...,
            "major": ...
            }
        '''
        student_info = self.getStudentDB(studentID)

        for key in newStudentData.keys():
            try:
                student_info[key] = newStudentData[key] #update field to be changed in firebase
                ref = db.reference(f"Students/{studentID}") # get reference to the field
                ref.child(key).set(student_info[key]) # set it to the new value
            except Exception as e:
                #field not yet in db for that key ... do something (key not found error?)
                pass
        print(student_info)

    
    def updateInstructorData(self, instructorID:str, newInstructorData:dict, fields:list):
        '''
        InstructorID: string
        newInstructorData: dictionary in the ff format
            {
            "First name": ...,
            "department": ...
            }
        '''
        instructor_info = self.getInstructorDB(instructorID)

        for key in newInstructorData.keys():
            try:
                instructor_info[key] = newInstructorData[key] # update field to be changed in firebase
            
                ref = db.reference(f"Instructors/{instructorID}") # get reference to the field
                ref.child(key).set(instructor_info[key]) # set it to the new value
            except Exception as e:
                #field not yet in db for that key ... do something (key not found error?)
                pass

    def getImgFromStorage(self, studentID:str):
        try: 
            self._blob = self._bucket.get_blob(f"Images/{studentID}.png")   
            self.img_array = np.frombuffer(self._blob.download_as_string(), np.uint8)
            print("Download succesful")
        except Exception as e:
            print("Upload unsuccesful: ",e)



if __name__ == '__main__':
    print("Testing database")

    testDB = FaceRecognitionFirebaseDB("testDB")

    #sample student data
    student_data = {
            "3101002": {
                "name": "Olasubomi Badiru",
                "major": "Computer Science",
                "minor": "Mathematics",
                "total_attendance": 0
            }
        }
    
    # sample instructor data
    instructor_data = {
            "9101001": {
                "first_name": "Mohammed",
                "last_name": "El-hajj",
                "department": "Computer Science",
                "email": "elhajjm@macewan.ca",
                "password": "barcelona"
            }
        }
    testDB.addStudent(student_data)
    testDB.addStudent({
        "3101003":{
            "name": "Will Smith"
        }
    })
    testDB.addStudent({
        "3101004":{
            "name": "Cardi Bee"
        }
    })
    testDB.updateStudentData("3101003", {"major": "Music", "minor": "Rap studies"})
    cardiTest = testDB.getStudentDB("3101003")
    print(cardiTest)

    
    testDB.addInstructor(instructor_data)