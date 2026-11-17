
def analyze_misconception(question, student_answer):

    question = question.strip().lower()
    answer = student_answer.strip().lower()

    if "1/2 + 1/4" in question:

        if answer == "2/6":
            return {
                "type": "Adding Numerators and Denominators",
                "explanation": (
                    "The student may be adding the "
                    "numerators and denominators directly."
                ),
                "intervention": (
                    "Teach common denominators using "
                    "visual fraction models."
                )
            }

        elif answer == "3/8":
            return {
                "type": "Denominator Multiplication Error",
                "explanation": (
                    "The student may be multiplying "
                    "the denominators without correctly "
                    "converting the fractions."
                ),
                "intervention": (
                    "Teach equivalent fractions and "
                    "common denominators step by step."
                )
            }

        elif answer == "5/4":
            return {
                "type": "Incorrect Fraction Addition",
                "explanation": (
                    "The student may have incorrectly "
                    "combined the fraction values."
                ),
                "intervention": (
                    "Use fraction strips to demonstrate "
                    "how 1/2 and 1/4 combine."
                )
            }

        elif answer == "3/4":
            return {
                "type": "No misconception detected",
                "explanation": (
                    "The student provided the correct answer."
                ),
                "intervention": (
                    "Introduce a more challenging "
                    "fraction addition problem."
                )
            }

    return {
        "type": "Unknown or unclassified response",
        "explanation": (
            "The system cannot confidently identify "
            "the student's misconception."
        ),
        "intervention": (
            "Ask the student to explain their reasoning "
            "and review their working."
        )
    }
