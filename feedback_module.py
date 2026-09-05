def collect_feedback(feedback):
    """
    Clean and store user feedback.
    """

    if feedback is None:
        return ""

    return feedback.strip()


def build_refinement_instruction(feedback, intent="General recommendation refinement"):
    """
    Convert feedback into instructions for the AI.
    """

    if not feedback:
        return ""

    instruction = f"""
USER FEEDBACK:
{feedback}

DETECTED INTENT:
{intent}

REFINEMENT INSTRUCTIONS:
Use the detected intent and user feedback as additional preferences.
Generate new recommendations that strongly reflect these preferences.
Do not simply repeat the previous recommendations.
Avoid recommendations that do not match the updated preferences.
Prefer practical, hands-on, beginner-friendly Python and AI projects
when requested by the user.
"""

    return instruction.strip()