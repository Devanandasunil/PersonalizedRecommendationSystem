def detect_intent(feedback):
    """
    Detect the user's intent from feedback.
    """

    text = feedback.lower().strip()

    if not text:
        return "No feedback provided"

    # Remove unwanted recommendations
    removal_phrases = [
        "remove",
        "avoid",
        "don't want",
        "do not want",
        "not interested",
        "less"
    ]

    if any(phrase in text for phrase in removal_phrases):
        return "Request to remove unwanted recommendations"

    # Practical learning and projects
    practical_phrases = [
        "practical",
        "project",
        "projects",
        "hands-on",
        "hands on",
        "real world",
        "real-world"
    ]

    if any(phrase in text for phrase in practical_phrases):
        return "Preference for practical learning and projects"

    # Beginner-friendly recommendations
    if any(
        phrase in text
        for phrase in [
            "beginner",
            "beginner friendly",
            "beginner-friendly",
            "easy",
            "simple"
        ]
    ):
        return "Preference for beginner-friendly recommendations"

    # Advanced recommendations
    if any(
        phrase in text
        for phrase in [
            "advanced",
            "expert",
            "hard",
            "difficult",
            "challenging"
        ]
    ):
        return "Preference for advanced recommendations"

    # AI / Machine Learning
    if any(
        phrase in text
        for phrase in [
            "ai",
            "artificial intelligence",
            "machine learning",
            "deep learning"
        ]
    ):
        return "Increased interest in Artificial Intelligence"

    # Python preference
    if "python" in text:
        return "Increased preference for Python-based recommendations"

    # More recommendations
    if any(
        phrase in text
        for phrase in [
            "more recommendations",
            "more suggestions",
            "more options",
            "give me more",
            "want more",
            "additional recommendations",
            "another recommendation"
        ]
    ):
        return "Request for more relevant recommendations"

    return "General recommendation refinement"