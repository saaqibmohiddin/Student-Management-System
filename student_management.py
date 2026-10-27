
import json
from pathlib import Path

import streamlit as st

# -------------------------------
# PAGE CONFIGURATION
# -------------------------------

st.set_page_config(
    page_title="EduTrack - Student Management",
    page_icon="🎓",
    layout="wide"
)

DATA_FILE = Path(__file__).resolve().parent / "students.txt"


# -------------------------------
# DATA MANAGEMENT
# -------------------------------

def load_students():
    if not DATA_FILE.exists():
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, list):
            return [
                student for student in data
                if isinstance(student, dict)
                and all(key in student for key in ("roll", "name", "course"))
            ]

        return []

    except (json.JSONDecodeError, OSError):
        return []


def save_students():
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(st.session_state.students, file, indent=4)
        return True
    except OSError:
        st.error("Unable to save student data.")
        return False


if "students" not in st.session_state:
    st.session_state.students = load_students()


# -------------------------------
# APPLICATION HEADER
# -------------------------------

st.title("🎓 EduTrack")
st.subheader("Student Management System")
st.caption("Manage student records easily")


students = st.session_state.students

# -------------------------------
# DASHBOARD
# -------------------------------

col1, col2 = st.columns(2)

with col1:
    st.metric("Total Students", len(students))

with col2:
    st.metric(
        "Total Courses",
        len(set(s["course"] for s in students))
    )

st.divider()


# -------------------------------
# ADD STUDENT
# -------------------------------

st.header("➕ Add Student")

with st.form("add_student_form", clear_on_submit=True):
    roll = st.text_input("Roll Number")
    name = st.text_input("Student Name")
    course = st.text_input("Course")

    add_button = st.form_submit_button("Add Student")

    if add_button:
        roll = roll.strip()
        name = name.strip()
        course = course.strip()

        if not roll or not name or not course:
            st.error("Please fill in all fields.")

        elif any(s["roll"] == roll for s in students):
            st.error("This Roll Number already exists.")

        else:
            students.append({
                "roll": roll,
                "name": name,
                "course": course
            })

            if save_students():
                st.success("Student added successfully!")
                st.rerun()


st.divider()


# -------------------------------
# VIEW STUDENTS
# -------------------------------

st.header("📋 View Students")

if students:
    st.dataframe(
        students,
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("No students found. Add your first student above.")


st.divider()


# -------------------------------
# SEARCH STUDENT
# -------------------------------

st.header("🔍 Search Student")

search_roll = st.text_input(
    "Enter Roll Number to Search",
    key="search_roll"
)

if st.button("Search Student"):
    result = next(
        (s for s in students if s["roll"] == search_roll.strip()),
        None
    )

    if result:
        st.success("Student found!")

        st.write("**Roll Number:**", result["roll"])
        st.write("**Name:**", result["name"])
        st.write("**Course:**", result["course"])
    else:
        st.warning("Student not found.")


st.divider()


# -------------------------------
# UPDATE STUDENT
# -------------------------------

st.header("✏️ Update Student")

if students:
    selected_roll = st.selectbox(
        "Select Roll Number",
        [s["roll"] for s in students],
        key="update_roll"
    )

    selected_student = next(
        s for s in students if s["roll"] == selected_roll
    )

    with st.form("update_student_form"):
        new_name = st.text_input(
            "New Name",
            value=selected_student["name"]
        )

        new_course = st.text_input(
            "New Course",
            value=selected_student["course"]
        )

        update_button = st.form_submit_button("Update Student")

        if update_button:
            new_name = new_name.strip()
            new_course = new_course.strip()

            if not new_name or not new_course:
                st.error("Name and course cannot be empty.")
            else:
                selected_student["name"] = new_name
                selected_student["course"] = new_course

                if save_students():
                    st.success("Student updated successfully!")
                    st.rerun()
else:
    st.info("Add a student before updating records.")


st.divider()


# -------------------------------
# DELETE STUDENT
# -------------------------------

st.header("🗑️ Delete Student")

if students:
    delete_roll = st.selectbox(
        "Select Student to Delete",
        [s["roll"] for s in students],
        key="delete_roll"
    )

    if st.button("Delete Student", type="primary"):
        st.session_state.students = [
            s for s in students if s["roll"] != delete_roll
        ]

        if save_students():
            st.success("Student deleted successfully!")
            st.rerun()
else:
    st.info("No student records available to delete.")


# -------------------------------
# FOOTER
# -------------------------------

st.divider()
st.caption("EduTrack | Student Management System")
