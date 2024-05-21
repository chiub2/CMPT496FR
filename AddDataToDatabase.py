import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("path/to/serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': 'whatever you name it'
})


ref = db.reference('######')


data = {
    "1234567":
        {
            "name": "Will Smith",
            "major": "Acting",
            "starting year": "2023",
            "total_attendance": "0",
            "standing": "G",
            "email": "will_smith@gmail.com",
            "year:": "1",
            "last_attedance:": "2023-09-01 12:00:00",
        },
    "3080126":
        {
            "name": "Brandon Chiu",
            "major": "Computer Science",
            "starting year": "2018",
            "total_attendance": "8",
            "standing": "G",
            "email": "chiub2@mymacewan.ca",
            "year:": "4",
            "last_attedance:": "2023-09-01 12:00:00",
        },
    "3101002":
        {
            "name": "Subomi Oluwalana",
            "major": "Computer Science",
            "starting year": "2018",
            "total_attendance": "6",
            "standing": "G",
            "email": "badiruo@mymacewan.ca",
            "year:": "4",
            "last_attedance:": "2023-09-01 12:00:00",
        }
}

for key,value in data.items():
    ref.child(key).set(value)