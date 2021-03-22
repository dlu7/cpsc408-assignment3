import sqlite3
import pandas as pd
import re

# setting options to show full dataframe
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# Question 2
# --- a) Import .csv file into Student table
# establish connection to db
conn = sqlite3.connect('./StudentDB')
cursor = conn.cursor()

# import data from csv
students = pd.read_csv('./students.csv')
# appending data from csv into empty table in database
students.to_sql('Student', conn, if_exists='append', index=False)
conn.commit()


# --- b) Display all students and their attributes
def displayStudents():
    cursor.execute("SELECT * FROM Student WHERE ifnull(isDeleted, 0) != 1;")
    studentrecords = cursor.fetchall()
    df = pd.DataFrame(studentrecords, columns = ['StudentID', 'FirstName', 'LastName', 'GPA', 'Major',
                                                     'FacultyAdvisor', 'Address', 'City', 'State', 'ZipCode',
                                                     'MobilePhoneNumber', 'isDeleted'])
    print("\nAll Student Records: \n")
    print(df)


# --- c) Add new students
def addStudent():
    # retrieving and validating user input for:
    # First Name
    first = input("Enter the student's first name: ")
    while True:
        if first.isalpha():
            break
        else:
            print("Invalid: please enter A-Z characters only.")
            first = input("Enter the student's first name: ")

    # Last Name
    last = input("Enter the student's last name: ")
    while True:
        if last.isalpha():
            break
        else:
            print("Invalid: please enter A-Z characters only.")
            last = input("Enter the student's last name: ")

    # GPA
    gpa = input("Enter the student's GPA: ")
    while True:
        try:
            gpa = float(gpa)
        except ValueError:
            print("Invalid: please enter numbers only.")
        else:
            if gpa > 5.0 or gpa < 0.0:
                print("Invalid: GPA is reported on a 5.0 scale.")
                gpa = input("Enter the student's GPA: ")
            else:
                break

    # Major
    major = input("Enter the student's major: ")
    while True:
        if " " in major or major.isalpha():
            break
        else:
            print("Invalid: please enter A-Z characters only.")
            major = input("Enter the student's major: ")

    # Faculty Advisor
    advisor = input("Enter the student's faculty advisor: ")
    while True:
        if (" " or "-" in advisor) or advisor.isalpha():
            break
        else:
            print("Invalid: please enter A-Z characters only.")
            advisor = input("Enter the student's faculty advisor: ")

    # Address
    address = input("Enter the student's street address (and apartment if applicable)"
                    "\n[ex. 123 Maple Street Apt. 45]: ")
    while True:
        format = "^\d+( \w+)( \w+)?( Apt. \d+)?$"
        isaddress = re.match(format, address)

        if isaddress:
            break
        else:
            address = input("Invalid: please enter the address (and apartment if applicable)"
                           "\nin the format - 123 Maple Street Apt. 45: ")

    # City
    city = input("Enter which city the student resides in: ")
    while True:
        if city.isalpha():
            break
        else:
            print("Invalid: please enter A-Z characters only.")
            city = input("Enter which city the student resides in: ")

    # State
    state = input("Enter which state the student resides in (ex. California): ")
    while True:
        if len(state) > 3 and state.isalpha():
            break
        else:
            print("Invalid: please enter the full name of the state using A-Z characters only (ex. California).")
            state = input("Enter which state the student resides in: ")

    # ZIP Code
    zipcode = input("Enter the student's ZIP code: ")
    while True:
        if len(zipcode) == 5 and zipcode.isdigit():
            break
        else:
            print("Invalid: ZIP code should be 5 digits.")
            zipcode = input("Enter the student's ZIP code: ")

    # Phone Number
    number = input("Enter the student's phone number"
                   "\n[ex. (123) 456-7890 x000] (x for optional extension): ")
    while True:
        pattern = "^\((\d{3})\) (\d{3})-(\d{4})( x\d+)?$"
        isphone = re.match(pattern, number)

        if isphone:
            break
        else:
            number = input("Invalid: please enter the phone number "
                           "\nin the format (123) 456-7890 x000 (x for optional extension): ")

    # isDeleted default value is 0 (false)
    cursor.execute("INSERT INTO Student('FirstName', 'LastName', 'GPA', 'Major', 'FacultyAdvisor', 'Address', 'City', 'State', 'ZipCode', 'MobilePhoneNumber', 'isDeleted')"
                   "VALUES (?,?,?,?,?,?,?,?,?,?,?)", (first, last, gpa, major, advisor, address, city, state, zipcode, number, 0))
    conn.commit()
    print("Added student into record.")


# --- d) Update students by Major, Advisor, and/or MobilePhoneNumber
def updateStudent():
    # using StudentID to update specific student record
    while True:
        studentID = input("Enter the student's ID to continue the update process: ")
        if studentID.isdigit():
            break
        else:
            print("Invalid: Student ID should be numeric.")

    # user inputs what they want to update -- by Major, Advisor, or Phone Number
    while True:
        update = input("What would you like to update?\n"
                       "Type 'major' to update major\n"
                       "     'advisor' to update faculty advisor\n"
                       "  or 'number' to update mobile phone number: ")

        if update == 'major' or 'advisor' or 'number':
            break
        else:
            print("Invalid: please try again.")
            update = input("What would you like to update?\n"
                          "Type 'major' to update major\n"
                          "     'advisor' to update faculty advisor\n"
                          "  or 'number' to update mobile phone number: ")


    # updating major
    if update == 'major' or update == 'Major':
        update = "Major"
        while True:
            user_input = input("Enter the student's new major: ")
            if " " in user_input or user_input.isalpha():
                break
            else:
                print("Invalid: please enter A-Z characters only.")

    # updating advisor
    elif update == 'advisor' or update == 'Advisor':
        update = "FacultyAdvisor"
        while True:
            user_input = input("Enter the student's new faculty advisor: ")
            if " " in user_input or user_input.isalpha():
                break
            else:
                print("Invalid: please enter A-Z characters only.")

    # updating mobile phone number
    elif update == 'number' or update == 'Number':
        update = "MobilePhoneNumber"
        user_input = input("Enter the student's new phone number"
                           "\n[ex. (123) 456-7890 x000] (x for optional extension): ")
        while True:
            pattern = "^\((\d{3})\) (\d{3})-(\d{4})( x\d+)?$"
            isphone = re.match(pattern, user_input)

            if isphone:
                break
            else:
                user_input = input("Invalid: please enter the new phone number "
                                       "\nin the format (123) 456-7890 x000 (x for optional extension): ")
    else:
        print("Invalid: please try again.")
        update = input("What would you like to update?: ")


    # updating in database
    cursor.executescript("UPDATE Student SET {0} = '{1}' WHERE StudentID = {2};".format(update, user_input, studentID))
    conn.commit()
    print("Updated " + update + " in student record.")


# --- e) Delete students by StudentID
def deleteStudent():
    # using StudentID to soft delete specific student record
    studentID = input("Enter the student's ID: ")
    while True:
        if studentID.isdigit():
            break
        else:
            print("Invalid: Student ID should be numeric.")
            studentID = input("Enter the student's ID: ")

    # soft delete sets isDeleted = 1
    cursor.execute("UPDATE Student SET isDeleted = 1 WHERE StudentID = ?", (studentID, ))
    conn.commit()
    print("Deleted student with ID #" + studentID + ".")


# --- f) Search/display students by Major, GPA, City, State, and Advisor
def searchStudent():
    while True:
        search = input("Type any one word below to search by:\n"
                       "    major\n"
                       "    GPA\n"
                       "    city\n"
                       "    state\n"
                       "    advisor\n"
                       "What would you like to search by?: ")

        if search == 'major' or search == 'Major':
            break
        elif search == 'gpa' or search == 'GPA':
            break
        elif search == 'city' or search == 'City':
            break
        elif search == 'state' or search == 'State':
            break
        elif search == 'advisor' or search == 'Advisor':
            break
        else:
            print("Invalid: please try again.")

    # search by Major
    if search == 'major' or search == 'Major':
        search = "Major"
        while True:
            user_input = input("Which major are you searching by? [ex. Computer Science]: ")
            if " " in user_input or user_input.isalpha():
                cursor.execute("SELECT * FROM Student WHERE Major = ? AND ifnull(isDeleted, 0) != 1;", (user_input,))
                output = cursor.fetchall()
                if len(output) > 0:
                    df = pd.DataFrame(output, columns=['StudentID', 'FirstName', 'LastName', 'GPA', 'Major',
                                                           'FacultyAdvisor', 'Address', 'City', 'State', 'ZipCode',
                                                           'MobilePhoneNumber', 'isDeleted'])
                    print("\nSearching by Major in " + user_input + "\n")
                    print(df)
                    break
                else:
                    print("No records were found.")
                    break
            else:
                print("Invalid: please try again.")

    # search by GPA
    elif search == 'gpa' or search == 'GPA':
        search = "GPA"
        while True:
            user_input = input("What GPA are you searching by? [ex. 2, 3.5]: ")
            try:
                user_input = float(user_input)
            except ValueError:
                print("Invalid: please try again.")
            else:
                if user_input > 5.0 or user_input < 0.0:
                    print("Invalid: GPA is reported on a 5.0 scale.")
                    user_input = input("Enter the student's GPA: ")
                else:
                    cursor.execute("SELECT * FROM Student WHERE GPA = ? AND ifnull(isDeleted, 0) != 1", (user_input,))
                    output = cursor.fetchall()
                    if len(output) > 0:
                        df = pd.DataFrame(output, columns=['StudentID', 'FirstName', 'LastName', 'GPA', 'Major',
                                                           'FacultyAdvisor', 'Address', 'City', 'State', 'ZipCode',
                                                           'MobilePhoneNumber', 'isDeleted'])
                        user_input = str(user_input)
                        print("\nSearching by GPA of" + user_input + "\n")
                        print(df)
                        break
                    else:
                        print("No records were found.")
                        break


    # search by City
    elif search == 'city' or search == 'City':
        search = "City"
        while True:
            user_input = input("Which city are you searching by? [ex. Anaheim]: ")
            if user_input.isalpha():
                cursor.execute("SELECT * FROM Student WHERE City = ? AND ifnull(isDeleted, 0) != 1;", (user_input, ))
                output = cursor.fetchall()
                if len(output) > 0:
                    df = pd.DataFrame(output, columns=['StudentID', 'FirstName', 'LastName', 'GPA', 'Major',
                                                       'FacultyAdvisor', 'Address', 'City', 'State', 'ZipCode',
                                                       'MobilePhoneNumber', 'isDeleted'])
                    print("\nSearching by the City of " + user_input + "\n")
                    print(df)
                    break
                else:
                    print("No records were found.")
                    break
            else:
                print("Invalid: please try again.")

    # search by State
    elif search == 'state' or search == 'State':
        search = "State"
        while True:
            user_input = input("Which state are you searching by? [ex. California]: ")
            if len(user_input) > 3 and user_input.isalpha():
                cursor.execute("SELECT * FROM Student WHERE State = ? AND ifnull(isDeleted, 0) != 1;", (user_input,))
                output = cursor.fetchall()
                if len(output) > 0:
                    df = pd.DataFrame(output, columns=['StudentID', 'FirstName', 'LastName', 'GPA', 'Major',
                                                           'FacultyAdvisor', 'Address', 'City', 'State', 'ZipCode',
                                                           'MobilePhoneNumber', 'isDeleted'])
                    print("\nSearching by the State of " + user_input + "\n")
                    print(df)
                    break
                else:
                    print("No records were found.")
                    break
            else:
                print("Invalid: please enter the full name of the state using A-Z characters only (ex. California).")

    # search by Advisor
    elif search == 'advisor' or search == 'Advisor':
        search = "FacultyAdvisor"
        while True:
            user_input = input("Which advisor are you searching by? [ex. Rene German]: ")
            if (" " or "-" in user_input) or user_input.isalpha():
                cursor.execute("SELECT * FROM Student WHERE FacultyAdvisor = ? AND ifnull(isDeleted, 0) != 1;", (user_input,))
                output = cursor.fetchall()
                if len(output) > 0:
                    df = pd.DataFrame(output, columns=['StudentID', 'FirstName', 'LastName', 'GPA', 'Major',
                                                       'FacultyAdvisor', 'Address', 'City', 'State', 'ZipCode',
                                                       'MobilePhoneNumber', 'isDeleted'])
                    print("\nSearching by Faculty Advisor: " + user_input + "\n")
                    print(df)
                    break
                else:
                    print("No records were found.")
                    break
            else:
                print("Invalid: please try again.")
    else:
        print("Invalid: please try again.")
        search = input("What would you like to search by?: ")


# menu options
def menu():
    print("\n                Menu                ")
    print("----------------------------------------")
    print("1. Display all student records")
    print("2. Add new student record")
    print("3. Update student record")
    print("4. Delete student record")
    print("5. Search and display student records")
    print("6. Exit program")
    print("----------------------------------------")
    return input("Choose a corresponding number: ")


# user is able to execute commands and reprompt menu until they exit
user_input = ""
while user_input != "6":
    user_input = menu()

    if user_input == '1':
        displayStudents()
    elif user_input == '2':
        addStudent()
    elif user_input == '3':
        updateStudent()
    elif user_input == '4':
        deleteStudent()
    elif user_input == '5':
        searchStudent()
    elif user_input == '6':
        print("Goodbye!")
        quit()
    else:
        print("Invalid option: please try again.")


conn.close()