
import streamlit as st
import pandas as pd

from supabase_client import get_supabase_client
from misconception_engine import analyze_misconception
from diagnostic_engine import generate_diagnostic_question
from reasoning_engine import analyze_reasoning


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="AI Misconception Analyzer",
    page_icon="🧠",
    layout="wide"
)


# ==========================================
# SESSION STORAGE
# ==========================================

if "assessments" not in st.session_state:
    st.session_state.assessments = []

if "reasoning_records" not in st.session_state:
    st.session_state.reasoning_records = {}

if "latest_assessment" not in st.session_state:
    st.session_state.latest_assessment = None


# ==========================================
# SUPABASE CONNECTION
# ==========================================

supabase = None

try:
    supabase = get_supabase_client()

    supabase.table("student_assessments") \
        .select("id") \
        .limit(1) \
        .execute()

    st.success("Supabase database connected successfully!")

except Exception as e:
    st.error(
        "Database connection failed. "
        "Check your Streamlit Secrets and Supabase setup."
    )
    st.caption(str(e))


# ==========================================
# DATABASE TO DISPLAY FORMAT
# ==========================================

def convert_database_record(row):

    return {
        "Student": row["student_name"],
        "Subject": row["subject"],
        "Question": row["question"],
        "Correct Answer": row["correct_answer"] or "",
        "Student Answer": row["student_answer"] or "",
        "Correct": bool(row["is_correct"]),
        "Misconception": row["misconception"] or "",
        "Explanation": row["explanation"] or "",
        "Intervention": row["intervention"] or "",
        "_database_id": row["id"]
    }


# ==========================================
# LOAD PERMANENT ASSESSMENT HISTORY
# ==========================================

if supabase:

    try:
        response = supabase.table(
            "student_assessments"
        ).select("*").order(
            "created_at",
            desc=True
        ).execute()

        st.session_state.assessments = [
            convert_database_record(row)
            for row in response.data
        ]

    except Exception as e:
        st.warning("Could not load database history.")
        st.caption(str(e))


# ==========================================
# HEADER
# ==========================================

st.title("🧠 AI Misconception Analyzer")

st.subheader(
    "Student Learning Intelligence Platform"
)

st.write(
    "Analyze student answers, identify possible "
    "misconceptions, investigate reasoning, and "
    "recommend personalized interventions."
)

st.divider()


# ==========================================
# STUDENT ASSESSMENT
# ==========================================

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


# ==========================================
# ANSWER ANALYSIS AND DATABASE STORAGE
# ==========================================

if submitted:

    if all([
        student_name.strip(),
        question.strip(),
        correct_answer.strip(),
        student_answer.strip()
    ]):

        try:

            result = analyze_misconception(
                question,
                student_answer
            )

            is_correct = (
                student_answer.strip().lower()
                == correct_answer.strip().lower()
            )

            diagnostic = generate_diagnostic_question(
                result["type"]
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
                "Intervention": result["intervention"],
                "_database_id": None
            }

            # Save assessment permanently

            if supabase:

                database_record = {
                    "student_name": student_name.strip(),
                    "subject": subject,
                    "question": question,
                    "correct_answer": correct_answer,
                    "student_answer": student_answer,
                    "is_correct": is_correct,
                    "misconception": result["type"],
                    "explanation": result["explanation"],
                    "intervention": result["intervention"],
                    "diagnostic_question": diagnostic["question"]
                }

                response = supabase.table(
                    "student_assessments"
                ).insert(database_record).execute()

                if response.data:
                    record["_database_id"] = response.data[0]["id"]

                    st.success(
                        "Assessment saved permanently in Supabase!"
                    )
                else:
                    st.warning(
                        "Assessment analyzed, but database confirmation was not received."
                    )

            else:

                st.warning(
                    "Assessment is available in this session only. "
                    "Supabase is not connected."
                )

            st.session_state.latest_assessment = record

            # Keep session history when database is unavailable
            if not supabase:
                st.session_state.assessments.append(record)

            st.success("Assessment completed!")

        except Exception as e:

            st.error("Assessment analysis failed.")
            st.caption(str(e))

    else:

        st.warning(
            "Please complete all assessment fields."
        )


# ==========================================
# LATEST STUDENT ANALYSIS
# ==========================================

if st.session_state.latest_assessment:

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


    # ======================================
    # DIAGNOSTIC QUESTIONING
    # ======================================

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


    # ======================================
    # STUDENT REASONING ANALYSIS
    # ======================================

    st.subheader("Student Reasoning")

    reasoning_key = (
        str(latest.get("_database_id"))
        if latest.get("_database_id")
        else latest["Student"] + "|" + latest["Question"]
    )

    reasoning = st.text_area(
        "Enter the student's explanation",
        value=st.session_state.reasoning_records.get(
            reasoning_key, ""
        ),
        placeholder=(
            "Record the student's explanation "
            "and calculation steps..."
        ),
        key="reasoning_input"
    )

    if st.button("Analyze Student Reasoning"):

        if reasoning.strip():

            try:

                reasoning_result = analyze_reasoning(
                    reasoning
                )

                st.session_state.reasoning_records[
                    reasoning_key
                ] = reasoning

                st.subheader("Reasoning Analysis Report")

                st.write(
                    "Understanding Level:",
                    reasoning_result["understanding"]
                )

                st.write(
                    "Evidence:",
                    reasoning_result["evidence"]
                )

                st.info(
                    reasoning_result["recommendation"]
                )

                # Update permanent database record

                database_id = latest.get("_database_id")

                if supabase and database_id:

                    supabase.table(
                        "student_assessments"
                    ).update({
                        "student_reasoning": reasoning,
                        "reasoning_result": reasoning_result["understanding"],
                        "reasoning_evidence": reasoning_result["evidence"],
                        "reasoning_recommendation": reasoning_result["recommendation"]
                    }).eq(
                        "id",
                        database_id
                    ).execute()

                    st.success(
                        "Student reasoning saved to Supabase!"
                    )

            except Exception as e:

                st.error("Reasoning analysis failed.")
                st.caption(str(e))

        else:

            st.warning(
                "Please enter the student's explanation."
            )


# ==========================================
# LEARNING ANALYTICS DASHBOARD
# ==========================================

if st.session_state.assessments:

    st.divider()

    st.header("📊 Learning Analytics Dashboard")

    df = pd.DataFrame(
        st.session_state.assessments
    )

    # Remove internal database identifier from display
    display_df = df.drop(
        columns=["_database_id"],
        errors="ignore"
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


    # ======================================
    # ASSESSMENT HISTORY
    # ======================================

    st.subheader("Student Assessment History")

    st.dataframe(
        display_df,
        use_container_width=True
    )


    # ======================================
    # MISCONCEPTION FREQUENCY
    # ======================================

    st.subheader("Misconception Frequency")

    excluded = [
        "No misconception detected",
        "Unknown or unclassified response"
    ]

    mistakes = df[
        ~df["Misconception"].isin(excluded)
    ]

    if not mistakes.empty:

        frequency = (
            mistakes["Misconception"].value_counts()
        )

        st.bar_chart(frequency)

    else:

        st.info(
            "No classified misconceptions detected."
        )


    # ======================================
    # STUDENT PERFORMANCE
    # ======================================

    st.subheader("Student Performance")

    performance = (
        df.groupby("Student")["Correct"].mean()
        * 100
    )

    st.bar_chart(performance)


    # ======================================
    # DOWNLOAD REPORT
    # ======================================

    st.divider()

    st.subheader("📥 Download Student Report")

    csv_data = display_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="Download Assessment Report",
        data=csv_data,
        file_name="student_misconception_report.csv",
        mime="text/csv"
    )

else:

    st.info(
        "Submit your first student assessment "
        "to generate learning analytics."
    )


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    "AI Misconception Analyzer | "
    "Educational Data Intelligence Portfolio"
)
