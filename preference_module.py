from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# Load the sentence transformer model
model = SentenceTransformer("all-MiniLM-L6-v2")


def analyze_preferences(profile):
    """
    Analyze the user's interests, goals and preferences.
    Uses Sentence Transformers to calculate similarity
    between the user's profile and recommendation categories.
    """

    interests = profile["Interests"]
    goal = profile["Goal"]
    preferences = profile["Preferences"]

    user_text = f"""
    Interests: {interests}
    Goal: {goal}
    Preferences: {preferences}
    """

    # Convert user profile into an embedding
    user_embedding = model.encode([user_text])

    categories = [
        "Programming and Software Development",
        "Artificial Intelligence and Machine Learning",
        "Data Science and Analytics",
        "Web Development",
        "Cybersecurity and Networking",
        "Cloud Computing and DevOps",
        "Database and Backend Development",
        "Mobile Application Development"
    ]

    # Convert categories into embeddings
    category_embeddings = model.encode(categories)

    # Calculate similarity
    similarities = cosine_similarity(
        user_embedding,
        category_embeddings
    )[0]

    preference_scores = []

    for category, score in zip(
        categories,
        similarities
    ):

        preference_scores.append({
            "category": category,
            "score": round(
                float(score) * 100,
                2
            )
        })

    # Highest similarity first
    preference_scores.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return {
        "user_text": user_text.strip(),
        "top_preferences": preference_scores[:5]
    }