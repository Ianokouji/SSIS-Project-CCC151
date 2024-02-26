from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QStyleFactory, QTableWidgetItem, QInputDialog, QMessageBox
from SSIS_UI_reset import Ui_MainWindow  
from PyQt5 import QtCore 


import os


#Connects my files
from Course_Student import Course, CourseOperations, StudentOperations, Student



class Controller:
    def __init__(self):
        self.app = QApplication([])

        # Create the main window
        self.main_window = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.main_window)

        current_directory = os.path.dirname(os.path.realpath(__file__))         # Calculates the path of the directory of the Student and course csv so I don't need to hard code them     
        courses_csv = os.path.join(current_directory, 'course.csv')             # Initializes path of courses csv file using Current_Directory object
        students_csv = os.path.join(current_directory, 'student.csv')           # Initializes path of courses csv file using Current_Directory object
        self.course_operations = CourseOperations(courses_csv, students_csv)    # Creates CourseOperations object to perform operations
        self.student_operations = StudentOperations(students_csv)               # Creates StudentOperations object to perform operations
        
       

    # -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # Connecting Buttons 
        self.ui.SaveCourse.clicked.connect(self.SaveCourse)                     # Add Course
        self.ui.AddCourse.clicked.connect(lambda: self.ChangeWidget(3))         # Change Display to Add Course
        self.ui.CoursesB.clicked.connect(lambda: self.ChangeWidget(1))          # Change Display to View Course Table
        self.ui.AddStudent.clicked.connect(lambda: self.ChangeWidget(2))        # Change Display to Add Student
        self.ui.StudentB.clicked.connect(lambda: self.ChangeWidget(0))          # Change Display to View Student Table

        self.ui.BSearchName.clicked.connect(self.SearchStudent)
        self.ui.BSearchCourse.clicked.connect(self.SearchCourseCode)

        self.ui.TCourse.itemClicked.connect(self.edit_course_code)              # Single Click item in row [1] Course table after toggle edit mode to edit course code
        self.ui.TCourse.itemClicked.connect(self.edit_course_name)              # Single Click item in row [0] Course table after toggle edit mode to edit course name
        self.ui.TStudent.itemClicked.connect(self.EditStudentName)              # Single click student name cell to edit
        self.ui.TStudent.itemClicked.connect(self.EditStudentAge)               # Single click student age cell to edit
        self.ui.TStudent.itemClicked.connect(self.EditStudentId)                # Single click student id cell to edit
        self.ui.TStudent.itemClicked.connect(self.EditStudentYrlvl)             # Single click student year level cell to edit
        self.ui.TStudent.itemClicked.connect(self.EditStudentGender)            # Single click student gender cell to edit
        self.ui.TStudent.itemClicked.connect(self.EditStudentCourseCode)        # Single click student course code cell to edit
        self.ui.TCourse.verticalHeader().sectionDoubleClicked.connect(self.DeleteCourseRow)             # When the vertical header of a row is double clicked in courses table, it promts delete course warning
        self.ui.TStudent.verticalHeader().sectionDoubleClicked.connect(self.deleteStudentRow)           # When the vertical header of a row is double clicked in students table, it promts delete course warning
 
        self.edit_mode = False                                                  # Boolean that is used for course Table edit switch
        self.disable_table()                                                    # Course Table is tamperproof by default also includes the clear button

        self.ui.AddStudent.clicked.connect(self.disable_edit_Button)            # Disabling the edit button when Tables are not on display
        self.ui.AddCourse.clicked.connect(self.disable_edit_Button)             # 

        self.ui.StudentB.clicked.connect(self.enable_edit_Button)               # When Table is in display allowing edit button
        self.ui.CoursesB.clicked.connect(self.enable_edit_Button)

        self.ui.EditB.clicked.connect(self.enable_edit_mode)                    # EditButton for course
        self.ui.CoursesB.clicked.connect(self.disable_edit_mode)                # When you view courses table, it automatically locks
        self.ui.StudentB.clicked.connect(self.disable_edit_mode)                # When you view students table, it automatically locks

        self.ui.SaveStudent.clicked.connect(self.SaveStudent)                   # Add Student

        self.ui.ClearCourses.clicked.connect(self.ClearCourses)                 # Button for clearing courses
        self.ui.ClearStudents.clicked.connect(self.ClearStudents)               # Button for clearing students
        
    #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        




        
    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # Course Operations 
    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    # Functionality for changing Stacked Widgets
    def ChangeWidget(self, index):
        self.ui.MainDisplay.setCurrentIndex(index)

    #Functioanlity for Clearing LineEdit
    def ClearCourseName_LineEdit(self):
        self.ui.CourseName.clear()
    
    #Functioanlity for Clearing LineEdit
    def ClearCourseCode_LineEdit(self):
        self.ui.CourseCode.clear() 


    #Functionality for Course ComboBox used in Adding Students
    def UpdateComboBox(self):
        self.ui.Course.clear()                                                                      # Clears the comboBox first as it gets update everytime 

        self.ui.Course.addItem("Not Enrolled")                                                      # Sets Not Enrolled as its default item
        course_codes = [course.course_code for course in self.course_operations.courses.values()]   # Gets all available course codes
        
        for course_code in course_codes:                                                            # Adds the items from the list to the combo box 
            self.ui.Course.addItem(course_code)                                                     # Adds all the course code as an item in comboBox



    # Updates the course table everytime a change is made
    # The way course operations deal with courses include popping courses
    # Therefore a course's position in display changes everytime you edit it
    # Thus, sorting the table Based on the first letter of the name allows the user to perform any operations and edit and not change the position in the table
    # As long as it does not involve changing the students first letter of the name, its position should not move
    def UpdateCourseTable(self):
        self.ui.TCourse.clearContents()                                        # Clears the table contents

        # Collect course data in a list of tuples
        course_data = []                                                       # Creates a data structure to store the of the course tuples
        for course_name, course in self.course_operations.courses.items():     # Loops through the dictionary using course name as its keys to access the course code
            course_tuple = (                                                   # Creates course tuple for each course
                course_name,                                                   # The tuple includes course name
                course.course_code                                             # And course code
            )
            course_data.append(course_tuple)                                   # Appends the created tupple to the data structere for storing

        sorted_course_data = sorted(course_data, key=lambda x: x[0])           # Sort course data based on course name    

        total_rows = len(sorted_course_data)                                   # Gets the length or total number of courses
        self.ui.TCourse.setRowCount(total_rows)                                # Uses it to determine how many rows are to be created in the table
        self.ui.TCourse.setColumnCount(2)                                      # Column number is set to 2 as there are only course code and course name 

        # Populate the table with sorted data, uses count as iterator for each row
        for count, course_tuple in enumerate(sorted_course_data):
            course_name, course_code = course_tuple                            # Unpack tuple and puts them to their respective variables
            course_code_item = QTableWidgetItem(course_code)                   # Creates QTableWidgetItem for each 
            course_name_item = QTableWidgetItem(course_name)                   # 
            self.ui.TCourse.setItem(count, 1, course_code_item)                # Set course name in first column
            self.ui.TCourse.setItem(count, 0, course_name_item)                # Set course code in second column



    # Functionality for Button that creates course
    def SaveCourse(self):
        
        course_name = self.ui.CourseName.text()                                 # Retrieves course name from LineEdit
        course_code = self.ui.CourseCode.text()                                 # Retrieves course code from LineEdit
        if course_code and course_name:
            course = Course(course_name,course_code)                                # Creates Course object 

            self.ClearCourseCode_LineEdit()                                         # Clears course name upon clicking save 
            self.ClearCourseName_LineEdit()                                         # Clears course code upon clicking save 
            
        
            if  self.course_operations.add_course(course):                          # add_course function is boolen because it also serves a duplicated checker
                self.ui.AddCourseError.setText("")                                  # When an added course is a duplicate it executes and sends true
            else:
                self.ui.AddCourseError.setText("Error: Course already exists")      # When a duplicate is found it sends false causing for an error to pop up

            self.UpdateComboBox()                                                   # Update changes in the comboBox
            self.UpdateCourseTable()                                                # Update changes in the Table
        else:
            QMessageBox.information(self.main_window, "Insufficeint Arguements", "Please fill in all required items.")




    # Error MessageBox when user promts the same course code of the item thay try to edit
    def SameCourseCodeError(self):
        message = "Same Course code input"
        QMessageBox.information(None, "Course Code Error", message)
        

    # Error MessageBox when user promts existing course code
    def CourseCodeAlreadyExistsError(self):
        QMessageBox.information(None, "Course Code Error", "Course code already exists.")
        

    # Error MessageBox when user promts the same course name of the item they try to edit
    def SameCourseNameError(self):
        message = "Same Course name input"
        QMessageBox.information(None, "Course Name Error", message)
        
    
    # Error MessageBox when user promts existing course name
    def CourseNameAlreadyExistsError(self):
        QMessageBox.information(None, "Course Name Error", "Course Name already exists.")
        





    # Function that handles the change in course code and updates it
    # Also includes updating the students csv
    def edit_course_code(self, item):
        if item.column() == 1:  # Assuming course code column is at index 0
                                                                                                        
            current_course_code = item.text()                                                                                                             # Get the current course code
            
            
            new_course_code, ok = QInputDialog.getText(self.main_window, 'Edit Course Code', 'Enter new course code:', text=current_course_code)          # Create and initialize the input dialog where user promts new course code
            
           
            if new_course_code == current_course_code:                                                                                                    # If same course code is prompted, erorr messageBox is displayed
                self.SameCourseCodeError()
                return
                
            if new_course_code in [course.course_code for course in self.course_operations.courses.values()]:                                             # If existing course code is prompted, error messageBox is displayed
                self.CourseCodeAlreadyExistsError()
                return


            if ok and new_course_code:                                                                                                                    # If there seems to be no problem, proceeds to update the course code 
                
                row = item.row()                                                                                                                          # Get the row index of the edited item
                course_name = self.ui.TCourse.item(row, 0).text()                                                                                         # Using the row, get the corresponding course name from column 0
                
                if course_name in self.course_operations.courses:                                                                                         # Checks if course name is present in the courses dictionary
                    course = self.course_operations.courses[course_name]                                                                                  # If so, then using the course name as a key, we access it in the dictionary
                    course.course_code = new_course_code                                                                                                  # And update its course code
                    
                   
                    for student in self.student_operations.students.values():                                                                              # Handles the update for studnets, Goes through all items in students Dictionary
                        if student.Course_code == current_course_code:                                                                                    # If a student has that course code
                            student.Course_code = new_course_code                                                                                         # It gets updated with the new one

                    # Save changes to CSV
                    self.course_operations.save_courses_to_csv()                                                                                          # Calls the course operations to save changes after the update
                    self.student_operations.save_students_to_csv()                                                                                        # Calls the student operations to reflect changes after the update
                    self.UpdateComboBox()                                                                                                                 # Updates ComboBox in Student Creation UI
                
                    
                    item.setText(new_course_code)                                                                                           
                    self.UpdateStudentTableSorted()                                                                                                       # Updates student table UI for every process created                       
                    QMessageBox.information(None, "Course Updates", "Course Code Update successfully")                                                    # Signals complete course code edit
            
    


    # Function that handles the change in course name and updates it
    def edit_course_name(self,item):
        if item.column() == 0:                                                                                                                            # Checks if the item is from the course name column
            
            current_course_name = item.text()                                                                                                             # Gets the current course name
            

            new_course_name, ok = QInputDialog.getText(self.main_window, 'Edit Course Name', 'Enter new course name:', text=current_course_name)          # Creates and initializes inputDialog where user prompts the new course

            if new_course_name == current_course_name:                                                                                                    # If same course name is prompted, erorr messageBox is displayed
                self.SameCourseNameError()
                return
            
            if new_course_name in [course.course_name.strip().lower() for course in self.course_operations.courses.values()]:                             # If existing course name is prompted, error messageBox is displayed
                self.CourseNameAlreadyExistsError()
                return
    
            if ok and new_course_name:                                                                                                                    # If there seems to be no problem proceeds to update the course name
            
                Jnew_course_name = new_course_name.strip().lower()                                                                                        # For Uniformality, the new Course name is justified
                if current_course_name in self.course_operations.courses:                                                                                 # Checks if current_course code is in the dictionary 
                    course = self.course_operations.courses.pop(current_course_name)                                                                      # If so, it pops the current course name
                    course.course_name = Jnew_course_name                                                                                                 # Store the new course name


                    self.course_operations.courses[Jnew_course_name] = course                                                                             # Adds the created course object back to the dictionary using the new course name as its key
                    self.course_operations.save_courses_to_csv()                                                                                          # Calls the course operations to save changes after the update
                                                                                                                                                          # Updates ComboBox in Student Creation UI
                    
                    item.setText(Jnew_course_name)                                                                                                        # Update the Courses Display Table
                    self.UpdateCourseTable()                                                                                                              # Updates the student table display
                    QMessageBox.information(None, "Course Updates", "Course Name Update successfully")                                                    # Signals complete course name edit
   


    # Function that gets the course to be deleted
    # Also updates the Student and Course table UI for changes
    def deleteCourse(self, item):
        row = item.row()                                                                # Get the row of the item when a user clicks on that row
        course_name_item = self.ui.TCourse.item(row, 0)                                 # Get the name of the item (course name)
        course_code_item = self.ui.TCourse.item(row, 1)                                 # Gets the course code of the item; to be used in student table update
        
        if course_name_item:                                                            # If course_name_item is already filled-in proceeds to deletion
            course_name = course_name_item.text()                                       # Converts QwidgetItem to text so we could use it as argument for delete function
            course_code = course_code_item.text()                                       # Converts QwidfgetItem to text for condition making in student table
    
            # Find the students enrolled in the deleted course and update their enrollment status
            for i in range(self.ui.TStudent.rowCount()):
                course_code_item = self.ui.TStudent.item(i,5)                           # Get the course code item for the current student
                if course_code_item and course_code_item.text() == course_code:         # Checks if there are course codes in the student table that is equal to the course code of the course we want to delete
                    course_code_item.setText("Not Enrolled")                            # Update the course code to "Not Enrolled"
                    
            
            
            if self.course_operations.delete_course(course_name):                       # Course deletion function is also a boolean function that sends true every time successful process is done
                self.ui.TCourse.removeRow(row)                                          # Remove the row from the course table
                self.UpdateComboBox()                                                   # Update the course ComboBox in the student table UI
                
                QMessageBox.information(self.main_window, "Course Deletion", "Course deleted successfully.")  # Prompts a message when a course deleted properly
            else:
                QMessageBox.warning(self.main_window, "Error", "Course deletion Error Occured")                # Prompts a message when course deletion error occurs 
    


    # Event Handler that calls the delete function everytime a user double clicks row
    # Also prompts a confirmation for deletion incase of accidental double click
    def DeleteCourseRow(self, row):
        item = self.ui.TCourse.item(row, 0)                                                                     
        reply = QMessageBox.question(self.main_window, 'Delete Course',
                                     'Are you sure you want to delete this course?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.deleteCourse(item)
            


    # Handling the Table edit for Button pressed
    def enable_edit_mode(self):
        if not self.edit_mode:
            # Enable the table
            self.enable_table()
            self.edit_mode = True

    def disable_edit_mode(self):
        if self.edit_mode:
            # Disable the table
            self.disable_table()
            self.edit_mode = False


    # Disables edit button when Tables are not on display
    def disable_edit_Button(self):
        self.ui.EditB.setEnabled(False)
    
    def enable_edit_Button(self):
        self.ui.EditB.setEnabled(True)


    # Handling the table edit for default display
    # Also envolves the clear button
    def enable_table(self):
        self.ui.TCourse.setEnabled(True)
        self.ui.TStudent.setEnabled(True)
        self.ui.ClearCourses.setEnabled(True)
        self.ui.ClearStudents.setEnabled(True)
       

    def disable_table(self):
        self.ui.TCourse.setEnabled(False)
        self.ui.TStudent.setEnabled(False)
        self.ui.ClearCourses.setEnabled(False)
        self.ui.ClearStudents.setEnabled(False)


    # Function that handles the Searching of courses through course codes
    def SearchCourseCode(self):
        courseCode_to_search = self.ui.SearchCourse.text().strip()                                 # Retrieves course code from Search LineEdit

        for course in self.course_operations.courses.values():                                     # Loops through the values in the courses or the course codes
            if course.course_code == courseCode_to_search:                                         # If that course code exits
                QMessageBox.information(self.main_window, "Course Information",                    # Information of that course code is displayed in a MessageBox
                                        f"Course Name: {course.course_name}\n"                     #
                                        f"Course Code: {course.course_code}\n")                    #
                return
        QMessageBox.warning(self.main_window, "Course Not Found", "Course is not registered.")     # If it does not exist in the courses list, prompts error message


    # Function that handles the updates in UI and confirmation when all courses are cleared
    def ClearCourses(self):
        reply = QMessageBox.question(self.main_window, 'Clear Courses',                            # Display a confirmation message box
                                     'Are you sure you want to clear all courses?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        

        if reply == QMessageBox.Yes:                                                               # Checks if the user confirms clearing 
            if self.course_operations.ClearCourses():                                              # Call the ClearCourses method of CourseOperations to clear all courses
                self.UpdateCourseTable()                                                           # After clearing courses, update the course table to reflect the changes
                self.UpdateComboBox()                                                              # Update the ComboBox with available courses

                # Handles the update in the student table 
                course_code_column = 5                                                             # Get the index of the course code column in the student table

                for row in range(self.ui.TStudent.rowCount()):                                     # Iterate over each row in the student table
                    self.ui.TStudent.item(row, course_code_column).setText("Not enrolled")         # Set the value of the course code cell to "Not Enrolled"

                # Display a message box indicating successful deletion
                QMessageBox.information(self.main_window, "Course Deletion", "Courses all deleted successfully.")
            else:
                # Display a message box indicating course Dictionary is empty
                QMessageBox.information(self.main_window, "Course Deletion", "No courses to delete.")

       
    #-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # Students Operations
    #-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


    # Updates student table for every update made
    # Same logic in Updating course table is used in updating student table
    # Also bears the same reason why table must be sorted
    def UpdateStudentTableSorted(self):
        self.ui.TStudent.clearContents()                                        # Clear the table contents

        student_data = []                                                       # data structure to store student data

        # Collect student data in a list of tuples; The student name and its attributes
        for student_name, student in self.student_operations.students.items():  # Loops through the dictionary using the student name as key
            student_tuple = (                                                   # Creates a tuple of student name and attributes for each student
                student_name,
                student.Age,
                student.Student_id,
                student.Year_level,
                student.Gender,
                student.Course_code
            )
            student_data.append(student_tuple)                                  # Appends the created tuple to the data structure for storing 

        
        sorted_student_data = sorted(student_data, key=lambda x: x[0])          # Sort student data based on the first letter of student names

        total_rows = len(sorted_student_data)                                   # Set the row count based on the number of students
        self.ui.TStudent.setRowCount(total_rows)                                #

        # Populate the table with the sorted data
        for count, student_tuple in enumerate(sorted_student_data):             # Loops through each sorted student data
            for column, value in enumerate(student_tuple):                      # Unpacks the tuple: Student name and Attributes
                item = QTableWidgetItem(str(value))                             # Creates a QTableWidgetItem for every Attribute and name
                self.ui.TStudent.setItem(count, column, item)                   # Fills the table with the data
      



    #Clearing the LineEdits in Add Student UI
    def ClearFirstName(self):
        self.ui.FirstName.clear()

    def ClearLastName(self):
        self.ui.LastName.clear()
    
    def ClearMidInitial(self):
        self.ui.MiddleInitial.clear()

    def ClearIDNumber(self):
        self.ui.IDNumber.clear()

    def ClearAge(self):
        self.ui.Age.clear()

    def ClearGender(self):
        self.ui.Gender.clear()
    
    def ClearYearlevel(self):
        self.ui.YearLevel.clear()

    
    # Function that adds student in CSV 
    def SaveStudent(self):
        first_name = self.ui.FirstName.text()                       # Gets the name of the Student 
        Middle_initial = self.ui.MiddleInitial.text()               # ..
        Last_name = self.ui.LastName.text()                         # ..

        Id_Number = self.ui.IDNumber.text()                         # Gets the Id Number of the Student
        Age = self.ui.Age.text()                                    # Gets the Age of the Student
        Gender = self.ui.Gender.text()                              # Gets the Gender of the Student 
        Year_Level = self.ui.YearLevel.text()                       # Gets the Year level of the student
        Course_code = self.ui.Course.currentText()                  # Gets the Course Code of the Student from ComboBox
        
        # If all LineEdits are filled 
        if first_name and Middle_initial and Last_name and Id_Number and Age and Gender and Year_Level and Course_code:        # Condition that checks if all LineEdits are filled  
            full_name = first_name + " " + Middle_initial + " " + Last_name                                                    # Formats Students Name into one String
            student = Student(full_name,Age,Id_Number,Year_Level,Gender,Course_code)                                           # A student object is created using the attributes

            # Clears the LineEdits after Pressing Save Button
            self.ClearFirstName()
            self.ClearLastName()
            self.ClearMidInitial()
            self.ClearIDNumber()
            self.ClearAge()
            self.ClearGender()
            self.ClearYearlevel()



            if  self.student_operations.add_student(student):                                                           # Sends student in student operation for deletion
                QMessageBox.information(self.main_window, "Enrollment Successful", "Student Enrolled Successfully.")    # Prompts message for every student successfully enrolled 
            else:
                QMessageBox.information(self.main_window, "Enrollment Error", "Student Already Enrolled.")              # If there are errors in the Add Student operations, this error message will be shown

            self.UpdateStudentTableSorted()                                                                             # Updates Student Table when the process is finshed
        
        else:
            QMessageBox.information(self.main_window, "Insufficeint Arguements", "Please fill in all required items.")  # If LineEdits are not fully filled then this error message will display  

    
    '''
    def SameStudentNameError(self):
        message = "Same Student name input"
        QMessageBox.information(None, "Student Name Error", message)
    '''
    def StudentAlreadyEnrolledError(self):
        message = "Existing Student input"
        QMessageBox.information(None, "Student Already enrolled", message)
    


    # Function that edits student's name and updates the csv and UI
    def EditStudentName(self,item):
        if item.column() == 0:                                  # Retrieves the Item column of the clicked TableWidgetIem
            current_student_name = item.text()                  # Gets the name of the student 

            
            new_student_name, ok = QInputDialog.getText(self.main_window, 'Edit Student Name', 'Enter new student name:', text=current_student_name)        # Get the new student name from user input

            if not ok or new_student_name == current_student_name:                                                                                          # Check if the user canceled the input or entered the same name
                return
        
            Jnew_student_name = new_student_name.strip().lower()                                                                                            # Convert the new student name to lowercase for comparison

            
            if Jnew_student_name in [student.Name.strip().lower() for student in self.student_operations.students.values()]:                                # Check if the new name already exists
                self.StudentAlreadyEnrolledError()                                                                                                          # Calls function for error message
                return
            
            # Update the student's name in the dictionary and CSV file
            if ok and new_student_name:

                if current_student_name in self.student_operations.students:                        # Check if the current student name exists in the dictionary
                    student = self.student_operations.students.pop(current_student_name)            # Pop the student object using the current name
                    student.Name = Jnew_student_name                                                # Update the student's name
                    self.student_operations.students[Jnew_student_name] = student                   # Add the student back to the dictionary with the new name
                    self.student_operations.save_students_to_csv()                                  # Save the updated students dictionary to the CSV file
                    item.setText(Jnew_student_name)                                                 # Update the text of the item in the UI
                    self.UpdateStudentTableSorted()                                                 # Update the entire list to maintain sorted state


    # Function that Edits the students age and reflects changes to csv and UI
    def EditStudentAge(self,item):
        if item.column() == 1:
            row = item.row()                                                                        # Get the row of the item being edited
            student_name_item = self.ui.TStudent.item(row, 0)                                       # Get the name of the student using the item row
            current_age = item.text()                                                               # Get the current age entered in the table as string 

            new_student_age, ok = QInputDialog.getText(self.main_window, 'Edit Student Age', 'Enter new student Age:', text=current_age)               # Get the new student age from user input

            if student_name_item and ok:
                student_name = student_name_item.text()                                             # Converts the student name to string
                if student_name in self.student_operations.students:                                # Access the student in the Students dictionary using the student name
                    self.student_operations.students[student_name].Age = new_student_age            # Updates the age of the student
                    
                    self.ui.TStudent.setItem(row, 1, QTableWidgetItem(new_student_age))             # Reflect changes to the UI by updating the corresponding QTableWidgetItem
                    self.student_operations.save_students_to_csv()                                  # Save changes in the students csv file


    # Function that Edits the students Year level and reflects changes to csv and UI
    def EditStudentYrlvl(self,item):
        if item.column() == 3:
            row = item.row()                                                                        # Get the row of the item being edited
            student_name_item = self.ui.TStudent.item(row, 0)                                       # Get the name of the student using the item row
            current_Yrlvl = item.text()                                                             # Get the current Year level in the table as string 

            new_student_Yrlevel, ok = QInputDialog.getText(self.main_window, 'Edit Student Year_Level', 'Enter new Year_Level:', text=current_Yrlvl)    # Get the new student age from user input

            if student_name_item and ok:
                student_name = student_name_item.text()                                             # Get the name of the student
                if student_name in self.student_operations.students:                                # Access the student in the Students dictionary using the student name
                    self.student_operations.students[student_name].Year_level = new_student_Yrlevel # Updates the Year level of the student
                    self.ui.TStudent.setItem(row, 3, QTableWidgetItem(new_student_Yrlevel))         # Reflect changes to the UI by updating the corresponding QTableWidgetItem
                    self.student_operations.save_students_to_csv()                                  # Save the changes in the student csv file
                


    # Function that Edits the students Gender and reflects changes to csv and UI
    def EditStudentGender(self,item):
        if item.column() == 4:
            row = item.row()                                                                        # Get the row of the item being edited
            student_name_item = self.ui.TStudent.item(row, 0)                                       # Get the name of the student using the item row
            current_Gender = item.text()                                                            # Get the current gender in the table as string

            new_student_Gender, ok = QInputDialog.getText(self.main_window, 'Edit Student Gender', 'Enter new Gender:', text=current_Gender)            # Get the new student age from user input

            if student_name_item and ok:
                student_name = student_name_item.text()                                             # Get the name of the student
                if student_name in self.student_operations.students:                                # Access the student in the Students dictionary using the student name
                    self.student_operations.students[student_name].Gender = new_student_Gender      # Updates the gender of the student
                    self.ui.TStudent.setItem(row, 4, QTableWidgetItem(new_student_Gender))          # Reflect changes to the UI by updating the corresponding QTableWidgetItem
                    self.student_operations.save_students_to_csv()                                  # Updates the changes in the students csv file
                      
    
    # Function that edits student's Id and updates the csv and UI
    def EditStudentId(self, item):
        if item.column() == 2:                                                                     
            row = item.row()                                                                        # Get the row of the item being edited
            student_name_item = self.ui.TStudent.item(row, 0)                                       # Get the name of the student using the item row
            current_ID = item.text()                                                                # Get the current ID in the table as string
            new_student_ID, ok = QInputDialog.getText(self.main_window, 'Edit Student ID', 'Enter new student ID', text=current_ID)                     # Get the new student age from user input

            if student_name_item and ok:
                student_name = student_name_item.text()                                             # Get the name of the student as string 

                if new_student_ID.strip() not in [student.Student_id.strip() for student in self.student_operations.students.values()]:                 # Check if the new student ID is unique
                    if student_name in self.student_operations.students:                                    # Checks if that student name is in the students dictionary
                        self.student_operations.students[student_name].Student_id = new_student_ID          # Update the student's ID in the dictionary and CSV file
                        self.ui.TStudent.setItem(row, 2, QTableWidgetItem(new_student_ID))                  # Reflect changes to the UI by updating the corresponding QTableWidgetItem
                        self.student_operations.save_students_to_csv()                                      # Updates the changes in the students csv file 
                else:
                    QMessageBox.warning(self.main_window, "Error", "Student ID already exists.")            # Prompts error message if user enters existing student id


    
    # Function that edits student's Course-code and updates the csv and UI                
    def EditStudentCourseCode(self, item):
        if item.column() == 5:                                                                      # Assuming course code is in column 3
            row = item.row()                                                                        # Get the row of the item being edited
            student_name_item = self.ui.TStudent.item(row, 0)                                       # Get the name of the student using the item row
            student_name = student_name_item.text()                                                 # Get the name of the student as string       
            
            # Fetch all available courses and stores it in a data structure that is used as a course list 
            available_course_codes = [course.course_code for course in self.course_operations.courses.values()]     
            available_course_codes.append("Not enrolled")                                           # Appends Not enrolled to the option as it is a default option
            
            # Let the user select a course code from the list
            selected_course, ok = QInputDialog.getItem(self.main_window, 'Edit Course Code', 
                                                    'Select new course code for student:', 
                                                    available_course_codes, editable=False)
            
            if ok and student_name:
                if student_name in self.student_operations.students:                                # Checks if the student name is present in the students dictionary
                    self.student_operations.students[student_name].Course_code = selected_course    # Update the student's course code
                    self.ui.TStudent.setItem(row, 5, QTableWidgetItem(selected_course))             # Reflect changes to the UI by updating the corresponding QTableWidgetItem
                    self.student_operations.save_students_to_csv()                                  # Save changes to CSV
                
    
    # Fucntion that handles the searching of a student using their Id and displays it 
    def SearchStudent(self):
        student_id_to_search = self.ui.SearchName.text().strip()                                    # Retrieves the student id from the LineEdit

        for student in self.student_operations.students.values():                                   # Check if the entered student ID is present in the students dictionary
            if student.Student_id == student_id_to_search:                                          # Gets the student having the same student Id as the one being searched

                QMessageBox.information(self.main_window, "Student Information",                    # When the student is found, display a messageBox displays its information
                                        f"Name: {student.Name}\n"
                                        f"Age: {student.Age}\n"
                                        f"Year Level: {student.Year_level}\n"
                                        f"Gender: {student.Gender}\n"
                                        f"Student ID: {student.Student_id}\n"
                                        f"Course Code: {student.Course_code}")
                return                                                                              # Once this display is done, this function ends                                                               

       
        QMessageBox.warning(self.main_window, "Student Not Found", "Student is not enrolled.")      # If the student ID is not found, show a message indicating the student is not enrolled
    


    # Function that deletes a single student and reflect the changes in csv and ui
    def DeleteStudent(self,item):

        row = item.row()                                                                            # Get the row of the item being edited
        StudentName = self.ui.TStudent.item(row,0)                                                  # Get the name of the student using the item row
        StudentNametxt = StudentName.text()                                                         # Get the name of the student as string  

        if StudentNametxt:  
            if self.student_operations.deleteStudent(StudentNametxt):                               # Removes student using the deleteStudent function in the students operations
                self.ui.TStudent.removeRow(row)                                                     # Clears the row of the deleted student in the table

                QMessageBox.information(self.main_window, "Student Unenrollment", "Student Unenrolled successfully.")       # Prompts a message everytime a successful process is made
            else:
                QMessageBox.information(self.main_window, "Student Unenrollment", "Student unenrollment failed.")           # Otherwise, prompts an error message

    

    # Event Handler that calls the delete function everytime a user double clicks row
    # Also prompts a confirmation for deletion incase of accidental double click
    def deleteStudentRow(self,row):
        item = self.ui.TStudent.item(row, 0)                                                                     
        reply = QMessageBox.question(self.main_window, 'Unenroll Student',
                                     'Are you sure you want to Unenroll this student?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.DeleteStudent(item)
    

    # Function that handles the clearing of all students and reflects changes in csv and ui
    def ClearStudents(self):
        reply = QMessageBox.question(self.main_window, 'Clear Students',                             # Ask for confirmation before clearing all students
                                     'Are you sure you want to clear all students?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:                                                                # If confirmation is triggered, proceeds to the deletion process
            if self.student_operations.ClearStudents():                                             # Calls the student operations to access the clear students fucntion in the operations class
                self.UpdateStudentTableSorted()                                                     # Updates the students table after deletion
                
                QMessageBox.information(self.main_window, "Students Cleared",                       # Display a message box to indicate successful deletion
                                        "All students have been cleared.")
            else:
                QMessageBox.information(self.main_window, "No Students to Clear",                   # Display a message box indicating that the CSV file is already empty
                                        "There are no students to clear.")

    
    #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        
   



    # Default fucntions that need to run as the program starts
    def run(self):
        self.ui.AddCourseError.setText("")
        self.UpdateStudentTableSorted()
        self.UpdateCourseTable()
        self.UpdateComboBox()
        self.main_window.show()
        self.app.exec_()

# Main function
if __name__ == "__main__":
    QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    QApplication.setStyle(QStyleFactory.create("Fusion"))
    controller = Controller()
    controller.run()