
import streamlit as st
from misconception_engine import analyze_misconception

st.set_page_config(
    page_title="AI Misconception Analyzer",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 AI Misconception Analyzer")
st.subheader("Understand how students think and learn.")

st.markdown(
    "Detect learning misconceptions and generate "
    "personalized teaching interventions."
)

st.divider()

st.header("Student Assessment")

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
    "Student's Answer",
    placeholder="Enter the student's answer"
)

if st.button("Analyze Student Answer"):

    if student_name and question and correct_answer and student_answer:

        result = analyze_misconception(
            question,
            student_answer
        )

        st.divider()

        st.subheader("Analysis Report")

        st.write("Student:", student_name)

        if student_answer.strip() == correct_answer.strip():
            st.success("Correct Answer")
        else:
            st.error("Incorrect Answer")

        st.subheader("Detected Misconception")
        st.warning(result["type"])

        st.subheader("Explanation")
        st.write(result["explanation"])

        st.subheader("Recommended Intervention")
        st.info(result["intervention"])

    else:
        st.warning("Please complete all fields.")

st.divider()

st.caption(
    "AI Misconception Analyzer | Learning Intelligence Project"
)
