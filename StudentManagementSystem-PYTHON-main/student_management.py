import json
import os

DATA_FILE = "students.txt"


def load_students():
    """Load student data from the JSON file."""
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

            if isinstance(data, list):
                return data

            return []

    except (json.JSONDecodeError, OSError):
        return []


def save_students():
    """Save all student data to the JSON file."""
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(students, file, indent=4)

        return True

    except OSError as error:
        print(f"Error saving student data: {error}")
        return False


students = load_students()


def add_student():
    roll = input("Enter Roll Number: ").strip()

    if not roll:
        print("Roll Number cannot be empty!")
        return

    # Prevent duplicate roll numbers
    for student in students:
        if student["roll"] == roll:
            print("A student with this Roll Number already exists!")
            return

    name = input("Enter Name: ").strip()

    if not name:
        print("Name cannot be empty!")
        return

    course = input("Enter Course: ").strip()

    if not course:
        print("Course cannot be empty!")
        return

    student = {
        "roll": roll,
        "name": name,
        "course": course
    }

    students.append(student)

    if save_students():
        print("Student Added Successfully!")


def view_students():
    if not students:
        print("No Students Found!")
        return

    print("\n===== Student List =====")

    for student in students:
        print(
            f"Roll: {student['roll']} | "
            f"Name: {student['name']} | "
            f"Course: {student['course']}"
        )


def search_student():
    roll = input("Enter Roll Number: ").strip()

    for student in students:
        if student["roll"] == roll:
            print("\nStudent Found!")
            print(f"Roll: {student['roll']}")
            print(f"Name: {student['name']}")
            print(f"Course: {student['course']}")
            return

    print("Student Not Found!")


def update_student():
    roll = input("Enter Roll Number to Update: ").strip()

    for student in students:
        if student["roll"] == roll:
            name = input("New Name: ").strip()

            if not name:
                print("Name cannot be empty!")
                return

            course = input("New Course: ").strip()

            if not course:
                print("Course cannot be empty!")
                return

            student["name"] = name
            student["course"] = course

            if save_students():
                print("Student Updated Successfully!")

            return

    print("Student Not Found!")


def delete_student():
    roll = input("Enter Roll Number to Delete: ").strip()

    for student in students:
        if student["roll"] == roll:
            students.remove(student)

            if save_students():
                print("Student Deleted Successfully!")

            return

    print("Student Not Found!")


def main():
    while True:
        print("\n===== Student Management System =====")
        print("1. Add Student")
        print("2. View Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Exit")

        choice = input("Enter Choice: ").strip()

        if choice == "1":
            add_student()

        elif choice == "2":
            view_students()

        elif choice == "3":
            search_student()

        elif choice == "4":
            update_student()

        elif choice == "5":
            delete_student()

        elif choice == "6":
            print("Thank you for using Student Management System!")
            break

        else:
            print("Invalid Choice! Please enter a number from 1 to 6.")


if __name__ == "__main__":
    main()