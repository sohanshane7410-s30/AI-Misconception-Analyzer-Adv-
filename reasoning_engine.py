
def analyze_reasoning(student_reasoning):

    reasoning = student_reasoning.strip().lower()

    if not reasoning:
        return {
            "understanding": "Not Assessed",
            "evidence": "No student explanation provided.",
            "recommendation": "Ask the student to explain their steps."
        }

    # Direct numerator and denominator addition
    if (
        "add" in reasoning
        and ("numerator" in reasoning or "denominator" in reasoning)
    ) or "added the top" in reasoning:

        return {
            "understanding": "Misconception Identified",
            "evidence": (
                "The explanation suggests the student "
                "adds numerators and denominators directly."
            ),
            "recommendation": (
                "Teach equivalent fractions and common "
                "denominators using visual fraction models."
            )
        }

    # Common denominator understanding
    if (
        "common denominator" in reasoning
        or "same denominator" in reasoning
    ):

        return {
            "understanding": "Possible Understanding",
            "evidence": (
                "The student refers to using a common denominator."
            ),
            "recommendation": (
                "Ask the student to demonstrate the "
                "method using another fraction problem."
            )
        }

    # Unclear explanation
    return {
        "understanding": "Partial or Unclear Understanding",
        "evidence": (
            "The explanation does not provide enough "
            "evidence to identify the student's strategy."
        ),
        "recommendation": (
            "Ask the student to show each calculation "
            "step and explain their reasoning."
        )
    }
