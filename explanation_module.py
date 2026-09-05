def generate_explanations(recommendations, profile):
    """
    Generate structured explanations for recommendations.
    """

    for recommendation in recommendations:

        if not recommendation.get("reason"):

            recommendation["reason"] = (
                f"This recommendation matches your "
                f"{profile['Interests']} interests and "
                f"your goal of {profile['Goal']}."
            )

    return recommendations