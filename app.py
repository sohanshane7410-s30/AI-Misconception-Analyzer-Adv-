
import streamlit as st
import pandas as pd

from misconception_engine import analyze_misconception
from diagnostic_engine import generate_diagnostic_question


# =====================================
# PAGE CONFIGURATION
# =====================================

st.set_page_config(
    page_title="AI Misconception Analyzer",
    page_icon="🧠",
    layout="wide"
)


# =====================================
# SESSION STORAGE
# =====================================

if "assessments" not in st.session_state:
    st.session_state.assessments = []

if "student_reasoning" not in st.session_state:
    st.session_state.student_reasoning = {}


# =====================================
# HEADER
# =====================================

st.title("🧠 AI Misconception Analyzer")

st.subheader(
    "Student Learning Intelligence Platform"
)

st.write(
    "Identify possible student misconceptions, "
    "investigate their reasoning, and recommend "
    "personalized learning interventions."
)

st.divider()


# =====================================
# STUDENT ASSESSMENT
# =====================================

st.header("📝 Student Assessment")

with st.form("assessment_form"):

    student_name = st.text_input(
        "Student Name"
    )

    subject = st.selectbox(
        "Subject",
        ["Mathematics", "Science", "English"]
    )

    question = st.text_input(
        "Assessment Question",
        value="What is 1/2 + 1/4?"
    )

    correct_answer = st.text_input(
        "Correct Answer",
        value="3/4"
    )

    student_answer = st.text_input(
        "Student's Answer"
    )

    submitted = st.form_submit_button(
        "Analyze Student Answer"
    )


# =====================================
# ANALYZE ANSWER
# =====================================

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

        record = {
            "Student": student_name.strip(),
            "Subject": subject,
            "Question": question,
            "Correct Answer": correct_answer,
            "Student Answer": student_answer,
            "Correct": is_correct,
            "Misconception": result["type"],
            "Explanation": result["explanation"],
            "Intervention": result["intervention"]
        }

        st.session_state.assessments.append(record)

        st.session_state.latest_assessment = record

        st.success("Assessment completed!")

    else:

        st.warning(
            "Please complete all assessment fields."
        )


# =====================================
# LATEST ANALYSIS
# =====================================

if "latest_assessment" in st.session_state:

    latest = st.session_state.latest_assessment

    st.divider()

    st.header("🔍 Student Analysis Report")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Student",
            latest["Student"]
        )

    with col2:

        if latest["Correct"]:
            st.success("Correct Answer")
        else:
            st.error("Incorrect Answer")

    st.subheader("Detected Misconception")

    st.warning(latest["Misconception"])

    st.subheader("Explanation")

    st.write(latest["Explanation"])

    st.subheader("🎯 Recommended Intervention")

    st.info(latest["Intervention"])


    # =================================
    # DIAGNOSTIC QUESTIONING
    # =================================

    st.divider()

    st.header("🧠 Diagnostic Investigation")

    diagnostic = generate_diagnostic_question(
        latest["Misconception"]
    )

    st.write("Question to ask the student:")

    st.info(diagnostic["question"])

    st.caption(
        "Purpose: " + diagnostic["purpose"]
    )

    reasoning = st.text_area(
        "Student's explanation",
        value=st.session_state.student_reasoning.get(
            latest["Student"], ""
        ),
        placeholder=(
            "Record the student's explanation "
            "and problem-solving steps..."
        ),
        key="reasoning_input"
    )

    if st.button("Save Student Reasoning"):

        st.session_state.student_reasoning[
            latest["Student"]
        ] = reasoning

        st.success(
            "Student reasoning saved for this session."
        )


# =====================================
# ANALYTICS DASHBOARD
# =====================================

if st.session_state.assessments:

    st.divider()

    st.header("📊 Learning Analytics Dashboard")

    df = pd.DataFrame(
        st.session_state.assessments
    )

    total = len(df)

    correct = int(df["Correct"].sum())

    incorrect = total - correct

    accuracy = (correct / total) * 100

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Assessments",
        total
    )

    col2.metric(
        "Correct Answers",
        correct
    )

    col3.metric(
        "Incorrect Answers",
        incorrect
    )

    col4.metric(
        "Accuracy",
        f"{accuracy:.1f}%"
    )


    # =================================
    # ASSESSMENT HISTORY
    # =================================

    st.subheader("Student Assessment History")

    st.dataframe(
        df,
        use_container_width=True
    )


    # =================================
    # MISCONCEPTION FREQUENCY
    # =================================

    st.subheader("Misconception Frequency")

    excluded = [
        "No misconception detected",
        "Unknown or unclassified response"
    ]

    mistakes = df[
        ~df["Misconception"].isin(excluded)
    ]

    if not mistakes.empty:

        frequency = mistakes[
            "Misconception"
        ].value_counts()

        st.bar_chart(frequency)

    else:

        st.info(
            "No classified misconceptions detected."
        )


    # =================================
    # STUDENT PERFORMANCE
    # =================================

    st.subheader("Student Performance")

    performance = (
        df.groupby("Student")["Correct"]
        .mean() * 100
    )

    st.bar_chart(performance)


    # =================================
    # DOWNLOAD REPORT
    # =================================

    st.divider()

    st.subheader("📥 Download Student Report")

    csv_data = df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="Download Assessment Report",
        data=csv_data,
        file_name="student_misconception_report.csv",
        mime="text/csv"
    )


# =====================================
# FOOTER
# =====================================

else:

    st.info(
        "Submit your first student assessment "
        "to generate learning analytics."
    )


st.divider()

st.caption(
    "AI Misconception Analyzer | "
    "Educational Data Intelligence Portfolio Project"
)
