
def analyze_misconception(question, student_answer):

    question = question.strip().lower()
    answer = student_answer.strip().lower()

    # Fraction addition misconception
    if "1/2 + 1/4" in question:

        if answer == "2/6":
            return {
                "type": "Adding Numerators and Denominators",
                "explanation": (
                    "The student added both numerators "
                    "and denominators directly."
                ),
                "intervention": (
                    "Teach students to find a common "
                    "denominator before adding fractions."
                )
            }

        elif answer == "3/4":
            return {
                "type": "No misconception detected",
                "explanation": "The student understands this calculation.",
                "intervention": "Provide a slightly more challenging problem."
            }

    return {
        "type": "Unknown or unclassified response",
        "explanation": (
            "The system cannot confidently identify "
            "the student's misconception yet."
        ),
        "intervention": (
            "Ask the student to explain their reasoning "
            "and review their working."
        )
    }
