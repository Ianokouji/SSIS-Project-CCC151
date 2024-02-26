import csv


'''
Contents of this file:
1.Class that creates student object
2.Class that creates course object
3.Class that performs operations on students
4.Class that performs operations on course 
'''



# Class that creates the course object
class Course:
    def __init__(self,course_name,course_code) -> None:    # Each Course object contains:
        self.course_name = course_name                     # A Course Name
        self.course_code = course_code                     # A Course Code
        

# Class that contains the operations on all Courses
class CourseOperations:
    def __init__(self, courses_csv, students_csv) -> None:
        self.courses_csv = courses_csv                      # File path of student csv
        self.students_csv = students_csv                    # File path of course csv
        self.courses = self.load_courses()                  # All courses in the csv file

        
    # Takes all the courses inside the csv file and puts it inside a Dictionary
    def load_courses(self):
        courses = {}                                                                                # Dictionary where course list is to be contained
        with open(self.courses_csv, 'r') as Mycsv:                                                  # Command to read csv file
            reader = csv.DictReader(Mycsv)                                                          # Creates csv dictionary reader object
            for row in reader:                                                                      # Loops through all the contents of the csv file                    
                course_name = row['Course Name']                                                    # Extracts the course name using its corresponding collumn in the csv
                course_code = row['Course Code']                                                    # Extracts the course code using its corresponding collumn in the csv
                courses[course_name] = Course(course_name = course_name, course_code = course_code)    # Creates course object using the extracted info from the csv, puts the new course object in the dictionary by using its name as the key                                      
        return courses                                      # Returns the List of all courses 
    
    
    # Function that handles saving the course
    # Pro: This function is reusable everytime I make changes in my Course list
    # Con: Despite appending a single course, it rewrites everything from our list which may make program slower 
    def save_courses_to_csv(self):                                      
        with open(self.courses_csv, 'w', newline='') as Mycsv:         # Command to write on Course csv file     
            fieldnames = ['Course Name', 'Course Code']                # Specifies the fieldnames or the Header of each Columns inside the csv file
            writer = csv.DictWriter(Mycsv, fieldnames=fieldnames)      # Creates a dictionary writer object and recieves the Course csv file and Specified fieldnames as arguements

            writer.writeheader()                                            # Overwrites each Header of the csv file when this called
            for course_name in self.courses:                                # It loops through the dictionary using the course name as its keys 
                writer.writerow({                                           # and writes them all down to our csv file
                    'Course Name': course_name,                             # It takes the course name and code of each object
                    'Course Code': self.courses[course_name].course_code    # and places them into each of their respectives cells using the fieldnames as Keys since it is a Dictionary
                })


    # Function that adds courses to CSV file and Checks for Duplicate
    def add_course(self, course):
        justified_course = course.course_name.strip().lower()                # Converts course name to lowercase and strips whitespace for checking
        justified_course_code = course.course_code.strip().lower()           # Converts course code to lowercase and strips whitespace for checking

        # Checks if the course name and code is not already used 
        if justified_course not in self.courses and justified_course_code not in [c.course_code.strip().lower() for c in self.courses.values()]:                             # If input course does not exist, it does saves the changes to the csv
            self.courses[justified_course] = course                          # Adds thge course the dictionary if it is unique            
            self.save_courses_to_csv()                                       # Saves the changes to the course csv file to update it
            return True                                                      # Sends true to Controller for every successful action
        else:
            return False                                                     # Sends false to Controller for every unsuccessful action
    


    # Function that handles the deletion of a course and updates the students that is enrolled in that course
    def delete_course(self, course_name):
        
        self.student_operations = StudentOperations(self.students_csv)       # Creates StudentOperations object for student update
        if course_name in self.courses:                                      # If course name exists in the courses Dictionary, proceeds to do action
            
            deleted_course = self.courses.pop(course_name)                   # Saves a copy before poping the deleted course

            self.save_courses_to_csv()                                       # Saves the current changes to the courses csv
    
            for student in self.student_operations.students.values():        # Loops through all the students in the student Dictionary
                if student.Course_code == deleted_course.course_code:        # If that student contains the deleted course 
                    student.Course_code = "Not enrolled"                     # It automatically sets that student to be Not Enrolled

            self.student_operations.save_students_to_csv()                   # Saves the current changes to the students csv
           
            return True                                                      # Sends true to Controller for every successful action
        else:
            return False                                                     # Sends false to Controller for every unsuccessful action
        
    def ClearCourses(self):
        if not self.courses:                                                 # Checks if the course dictionary is already empty
            return False                                                     # Return False if courses dictionary is already empty

        self.courses.clear()                                                 # Clears the csv if it has contents
        self.save_courses_to_csv()                                           # Save the changes to the courses CSV file

        # Set all students' course codes to "Not enrolled"
        self.student_operations = StudentOperations(self.students_csv)       # Creates StudentOperations object to access students csv
        for student in self.student_operations.students.values():            # Loops through the values and finds the course code for each
            student.Course_code = "Not enrolled"                             # Sets each course code to be Not enrolled

        self.student_operations.save_students_to_csv()                       # Save the changes to the students CSV file

        return True                                                          # Returns True for every successful process

        
           



# Class that creates Student object
class Student:
    def __init__(self, Name, Age, Student_id, Year_level, Gender, Course_code) -> None:         # Each Student object Has:
        self.Name = Name                                                                        # Student's Name
        self.Age = Age                                                                          # Student's Age
        self.Student_id = Student_id                                                            # Student's id
        self.Year_level = Year_level                                                            # Student's Year level
        self.Gender = Gender                                                                    # Student's Gender
        self.Course_code = Course_code                                                          # Student's Course Code


# Class that contains the operations on all Courses
class StudentOperations:
    def __init__(self, students_csv) -> None:
        self.students_csv = students_csv
        self.students = self.load_Students()
    

    # Takes all the Students inside the csv file and puts it inside dictionary
    def load_Students(self):
        students = {}                                               # Dictionary where course list is to be contained
        with open(self.students_csv, 'r') as Mycsv:                 # Command to read csv file
            reader = csv.DictReader(Mycsv)                          # Creates csv dictionary reader object
            for row in reader:                                      # Loops through all the contents of the csv file 
                Name = row['Name']                                  # Extracts an Attribute using its corresponding collumn in the csv
                Age = row['Age']
                Student_id = row['Student_id']
                Year_level = row['Year_level']
                Gender = row['Gender']
                Course_code = row['Course_code']
                # Creates course object using the extracted info from the csv, puts the new course object in the dictionary by using its name as the key 
                students[Name] = Student(Name = Name, Age = Age, Student_id = Student_id, Year_level = Year_level, Gender = Gender, Course_code = Course_code) 
        return students

    # Writes the changes after editing students to their the csv file
    def save_students_to_csv(self):
        with open(self.students_csv, 'w', newline='') as Mycsv:                                # Open the CSV file for writing
            fieldnames = ['Name', 'Age', 'Student_id', 'Year_level', 'Gender', 'Course_code']  # Define the fieldnames
            writer = csv.DictWriter(Mycsv, fieldnames=fieldnames)                              # Create a DictWriter object

            writer.writeheader()                                                               # Write the header row

            # Iterate over each student and write their data to the CSV file
            for student_name, student in self.students.items():
                writer.writerow({
                    'Name': student_name,
                    'Age': student.Age,
                    'Student_id': student.Student_id,
                    'Year_level': student.Year_level,
                    'Gender': student.Gender,
                    'Course_code': student.Course_code
                })

    # Adds Student to the csv, also checks if their ID and name exits 
    def add_student(self,student):
        student_name = student.Name                                          # Gets the student name of the new Student
        student_Id = student.Student_id                                      # Gets the student id of the new Student
        justified_student_name = student_name.strip().lower()                # For checking convenience, students name is justified
        self.student_operations = StudentOperations(self.students_csv)       # Creates StudentOperations object for student update

        # Check if there is already a student with the same ID
        if any(existing_student.Student_id == student_Id for existing_student in self.students.values()):
            return False                                                     # Student with the same ID already exists, so return False
        
        if justified_student_name in self.students:
            return False                                                     # Student with the same name already exists, so return False

        self.students[justified_student_name] = student                      # Adds the student to the Dictionary
        self.save_students_to_csv()                                          # Save the changes in my csv
        return True                                                          # Returns True for every successful process
    

    # Deletes a single student in the list
    def deleteStudent(self,StudentName):

        if StudentName in self.students:                                     # Checks if the student you are about to delete is in the Dictionary           

            self.students.pop(StudentName)                                   # Pops that student
    
            self.save_students_to_csv()                                      # Saves the changes to students csv file

            return True                                                      # Returns True for every successful process
        
        else:
            
            return False                                                     # For every error encountered, returns false

    # Function that clears the entire students csv 
    def ClearStudents(self):
       
        if not self.students:                                                # Check if students dictionary is already empty
            return False                                                     # If it already empty return false as nothing can be cleared
        
        self.students.clear()                                                # Clears it if it has content
        self.save_students_to_csv()                                          # Save changes to the students csv file
        
        return True                                                          # Returns True for every successful process

    
    
        
                    