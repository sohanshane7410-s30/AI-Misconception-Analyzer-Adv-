
import streamlit as st

st.set_page_config(
    page_title="AI Misconception Analyzer",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 AI Misconception Analyzer")
st.subheader("Understand how students think and learn.")

st.write(
    "Identify student misconceptions, "
    "understand learning gaps, and recommend "
    "personalized interventions."
)

st.divider()

st.header("Student Assessment")

student_name = st.text_input("Student Name")

question = st.text_input(
    "Question",
    placeholder="Example: What is 1/2 + 1/4?"
)

correct_answer = st.text_input("Correct Answer")

student_answer = st.text_input("Student's Answer")

if st.button("Analyze Answer"):
    if student_name and question and correct_answer and student_answer:
        if student_answer.strip() == correct_answer.strip():
            st.success("Correct answer!")
            st.write("The student answered correctly.")
        else:
            st.error("Incorrect answer!")
            st.write("Further investigation is needed.")
            st.info(
                "Possible misconception: "
                "The student may have misunderstood "
                "the underlying concept."
            )
    else:
        st.warning("Please complete all fields.")

st.divider()

st.caption("AI Misconception Analyzer | Portfolio Project")
