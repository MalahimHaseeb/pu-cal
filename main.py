import streamlit as st

st.set_page_config(page_title="PU GPA Calculator", page_icon="🎓", layout="centered")

GRADE_TABLE = [
    (85, 100, "A", 4.00),
    (80, 84.99, "A-", 3.70),
    (75, 79.99, "B+", 3.30),
    (70, 74.99, "B", 3.00),
    (65, 69.99, "B-", 2.70),
    (61, 64.99, "C+", 2.30),
    (58, 60.99, "C", 2.00),
    (55, 57.99, "C-", 1.70),
    (50, 54.99, "D", 1.00),
    (0, 49.99, "F", 0.00),
]


def marks_to_grade(marks):
    for low, high, letter, points in GRADE_TABLE:
        if low <= marks <= high:
            return letter, points
    return "F", 0.00


st.title("🎓 PU GPA / CGPA Calculator")
st.caption("Based on the official University of the Punjab grading scale")

with st.expander("Grading scale reference"):
    st.table(
        {
            "Marks %": [f"{low}-{high}" if high < 100 else f"{low} & above" for low, high, _, _ in GRADE_TABLE],
            "Grade": [g[2] for g in GRADE_TABLE],
            "Points": [g[3] for g in GRADE_TABLE],
        }
    )

tab1, tab2 = st.tabs(["Semester GPA", "Cumulative CGPA"])

with tab1:
    st.subheader("Previous record (optional)")
    st.write("If you've completed semesters before, enter your CGPA so far and total credit hours to get an updated CGPA after this semester.")
    prev_cols = st.columns(2)
    previous_credits = prev_cols[0].number_input(
        "Total credit hours completed so far", min_value=0.0, value=0.0, step=0.5, key="previous_credits"
    )
    previous_cgpa = prev_cols[1].number_input(
        "CGPA so far", min_value=0.0, max_value=4.0, value=0.0, step=0.01, key="previous_cgpa"
    )

    st.divider()
    st.subheader("This semester's subjects")
    st.write("Add each course with its credit hours and either marks % or a letter grade.")

    if "courses" not in st.session_state:
        st.session_state.courses = [{"name": "Course 1", "credits": 3.0, "marks": 80.0}]

    def add_course():
        st.session_state.courses.append(
            {"name": f"Course {len(st.session_state.courses) + 1}", "credits": 3.0, "marks": 80.0}
        )

    def remove_course(index):
        st.session_state.courses.pop(index)

    for i, course in enumerate(st.session_state.courses):
        cols = st.columns([3, 2, 2, 2, 1])
        course["name"] = cols[0].text_input("Course name", value=course["name"], key=f"name_{i}")
        course["credits"] = cols[1].number_input(
            "Credit hrs", min_value=0.0, max_value=10.0, value=course["credits"], step=0.5, key=f"credits_{i}"
        )
        course["marks"] = cols[2].number_input(
            "Marks %", min_value=0.0, max_value=100.0, value=course["marks"], step=1.0, key=f"marks_{i}"
        )
        letter, points = marks_to_grade(course["marks"])
        cols[3].markdown(f"**{letter}** ({points:.2f})")
        if len(st.session_state.courses) > 1:
            if cols[4].button("✕", key=f"remove_{i}"):
                remove_course(i)
                st.rerun()

    st.button("+ Add course", on_click=add_course)

    total_credits = sum(c["credits"] for c in st.session_state.courses)
    total_quality_points = sum(c["credits"] * marks_to_grade(c["marks"])[1] for c in st.session_state.courses)

    if total_credits > 0:
        gpa = total_quality_points / total_credits
        st.divider()
        st.metric("Semester GPA", f"{gpa:.2f}", help=f"{total_quality_points:.2f} quality points / {total_credits:.1f} credit hours")
    else:
        st.info("Add at least one course with credit hours to calculate GPA.")

with tab2:
    st.subheader("Cumulative CGPA")
    st.write("Enter each completed semester's GPA and total credit hours for that semester.")

    if "semesters" not in st.session_state:
        st.session_state.semesters = [{"label": "Semester 1", "gpa": 3.0, "credits": 15.0}]

    def add_semester():
        st.session_state.semesters.append(
            {"label": f"Semester {len(st.session_state.semesters) + 1}", "gpa": 3.0, "credits": 15.0}
        )

    def remove_semester(index):
        st.session_state.semesters.pop(index)

    for i, sem in enumerate(st.session_state.semesters):
        cols = st.columns([3, 2, 2, 1])
        sem["label"] = cols[0].text_input("Semester", value=sem["label"], key=f"sem_label_{i}")
        sem["gpa"] = cols[1].number_input(
            "GPA", min_value=0.0, max_value=4.0, value=sem["gpa"], step=0.01, key=f"sem_gpa_{i}"
        )
        sem["credits"] = cols[2].number_input(
            "Credit hrs", min_value=0.0, max_value=50.0, value=sem["credits"], step=0.5, key=f"sem_credits_{i}"
        )
        if len(st.session_state.semesters) > 1:
            if cols[3].button("✕", key=f"remove_sem_{i}"):
                remove_semester(i)
                st.rerun()

    st.button("+ Add semester", on_click=add_semester)

    total_sem_credits = sum(s["credits"] for s in st.session_state.semesters)
    total_sem_points = sum(s["gpa"] * s["credits"] for s in st.session_state.semesters)

    if total_sem_credits > 0:
        cgpa = total_sem_points / total_sem_credits
        st.divider()
        st.metric("CGPA", f"{cgpa:.2f}", help=f"{total_sem_points:.2f} points / {total_sem_credits:.1f} credit hours")
        if cgpa < 2.00:
            st.warning("Below the minimum 2.00 CGPA required for BS degree completion at PU.")
    else:
        st.info("Add at least one semester with credit hours to calculate CGPA.")