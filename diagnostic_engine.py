
def generate_diagnostic_question(misconception):

    questions = {
        "Adding Numerators and Denominators": {
            "question": (
                "When adding 1/2 and 1/4, "
                "why did you add both numerators "
                "and denominators?"
            ),
            "purpose": (
                "Investigate whether the student "
                "understands equivalent fractions."
            )
        },

        "Denominator Multiplication Error": {
            "question": (
                "Can you explain how you decided "
                "what denominator to use?"
            ),
            "purpose": (
                "Check the student's understanding "
                "of common denominators."
            )
        },

        "Incorrect Fraction Addition": {
            "question": (
                "Can you show how you combined "
                "one half and one fourth?"
            ),
            "purpose": (
                "Investigate the student's fraction "
                "addition strategy."
            )
        }
    }

    return questions.get(
        misconception,
        {
            "question": (
                "Can you explain your steps "
                "for solving this problem?"
            ),
            "purpose": (
                "Gather more evidence about "
                "the student's reasoning."
            )
        }
    )
