def rank_recommendations(recommendations):
    """
    Rank recommendations according to suitability score.
    """

    if not recommendations:
        return []

    # Sort by score
    ranked = sorted(
        recommendations,
        key=lambda item: item.get("score", 0),
        reverse=True
    )

    # Assign ranking positions
    for position, item in enumerate(ranked, start=1):

        item["rank"] = position

    return ranked