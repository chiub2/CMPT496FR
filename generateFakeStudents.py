import csv
import random
import faker

# Initialize faker generator
fake = faker.Faker()

# List of possible academic majors and minors
majors = [
    "Computer Science", "Mathematics", "Physics", "Chemistry", "Biology",
    "English", "History", "Economics", "Psychology", "Sociology"
]

minors = [
    "Philosophy", "Art", "Statistics", "Geography", "Music",
    "Political Science", "Linguistics", "Anthropology", "Environmental Science", "Business"
]

# Function to generate a random student ID starting with '3'
def generate_student_id():
    return f"3{random.randint(1000000, 9999999)}"

# Generate data
data = []
for _ in range(100):
    fullname = fake.name()
    academic_major = random.choice(majors)
    academic_minor = random.choice(minors)
    student_id = generate_student_id()
    total_attendance = random.randint(0, 100)
    
    data.append([fullname, academic_major, academic_minor, student_id, total_attendance])

# Write data to CSV
with open("students.csv", "w", newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["fullname", "academic_major", "academic_minor", "student_id", "total_attendance"])
    writer.writerows(data)

print("CSV file 'students.csv' generated successfully.")
