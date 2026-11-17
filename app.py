
import streamlit as st
import pandas as pd
from misconception_engine import analyze_misconception

st.set_page_config(
    page_title="AI Misconception Analyzer",
    page_icon="🧠",
    layout="wide"
)

if "assessments" not in st.session_state:
    st.session_state.assessments = []

st.title("🧠 AI Misconception Analyzer")
st.write("Student Learning Intelligence Platform")

st.divider()

# ASSESSMENT INPUT
st.header("Student Assessment")

with st.form("assessment_form"):
    student_name = st.text_input("Student Name")

    question = st.text_input(
        "Question",
        value="What is 1/2 + 1/4?"
    )

    correct_answer = st.text_input(
        "Correct Answer",
        value="3/4"
    )

    student_answer = st.text_input(
        "Student's Answer"
    )

    submitted = st.form_submit_button("Analyze Answer")

if submitted:
    if all([
        student_name.strip(),
        question.strip(),
        correct_answer.strip(),
        student_answer.strip()
    ]):
        result = analyze_misconception(
            question,
            student_answer
        )

        is_correct = (
            student_answer.strip().lower()
            == correct_answer.strip().lower()
        )

        st.session_state.assessments.append({
            "Student": student_name,
            "Question": question,
            "Student Answer": student_answer,
            "Correct": is_correct,
            "Misconception": result["type"],
            "Intervention": result["intervention"]
        })

        st.success("Assessment completed!")

    else:
        st.warning("Please complete all fields.")

# LATEST ANALYSIS
if st.session_state.assessments:

    latest = st.session_state.assessments[-1]

    st.header("Latest Analysis")

    if latest["Correct"]:
        st.success("Correct Answer")
    else:
        st.error("Incorrect Answer")

    st.write("Student:", latest["Student"])

    st.subheader("Detected Misconception")
    st.warning(latest["Misconception"])

    st.subheader("Recommended Intervention")
    st.info(latest["Intervention"])

    st.divider()

    # ANALYTICS DASHBOARD
    st.header("📊 Learning Analytics Dashboard")

    df = pd.DataFrame(st.session_state.assessments)

    total = len(df)
    correct = int(df["Correct"].sum())
    incorrect = total - correct

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Assessments", total)
    col2.metric("Correct Answers", correct)
    col3.metric("Incorrect Answers", incorrect)

    st.subheader("Student Assessment History")
    st.dataframe(df, use_container_width=True)

    st.subheader("Misconception Frequency")

    mistakes = df[
        df["Misconception"]
        != "No misconception detected"
    ]

    mistakes = mistakes[
        mistakes["Misconception"]
        != "Unknown or unclassified response"
    ]

    if not mistakes.empty:
        frequency = (
            mistakes["Misconception"]
            .value_counts()
        )

        st.bar_chart(frequency)
    else:
        st.info("No classified misconceptions detected yet.")

    st.subheader("Student Performance")

    performance = (
        df.groupby("Student")["Correct"]
        .mean() * 100
    )

    st.bar_chart(performance)

else:
    st.info("Submit your first student assessment to see analytics.")

st.divider()

st.caption(
    "AI Misconception Analyzer | Student Learning Intelligence"
)
