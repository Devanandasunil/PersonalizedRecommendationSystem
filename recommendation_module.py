import os
import re
import requests
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:3b"

DATASET_PATH = os.path.join(
    os.path.dirname(__file__),
    "dataset",
    "courses.csv"
)

# Load the sentence transformer model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


def load_dataset():
    """
    Load the Kaggle course dataset.
    """
    if not os.path.exists(DATASET_PATH):
        return None

    return pd.read_csv(DATASET_PATH)


def get_dataset_candidates(profile, feedback="", exclude_names=None, top_k=15):
    """
    Find the most relevant courses from the Kaggle dataset
    using semantic similarity.
    """

    df = load_dataset()

    if df is None or df.empty:
        return []

    exclude_names = exclude_names or []

    # Create a combined user preference text
    user_text = f"""
    Interests: {profile.get("Interests", "")}
    Skill Level: {profile.get("Skill Level", "")}
    Preferred Category: {profile.get("Preferred Category", "")}
    Goal: {profile.get("Goal", "")}
    Preferences: {profile.get("Preferences", "")}
    Feedback: {feedback}
    """

    # Create course text from important dataset fields
    df["course_text"] = (
        df["course_title"].fillna("").astype(str)
        + " "
        + df["subject"].fillna("").astype(str)
        + " "
        + df["level"].fillna("").astype(str)
    )

    # Generate embeddings
    user_embedding = embedding_model.encode(
        [user_text],
        convert_to_numpy=True
    )

    course_embeddings = embedding_model.encode(
        df["course_text"].tolist(),
        convert_to_numpy=True,
        show_progress_bar=False
    )

    similarities = cosine_similarity(
        user_embedding,
        course_embeddings
    )[0]

    df["similarity"] = similarities

    # Remove previously recommended courses during refinement
    if exclude_names:
        df = df[
            ~df["course_title"].isin(exclude_names)
        ]

    # Sort by semantic relevance
    df = df.sort_values(
        "similarity",
        ascending=False
    ).head(top_k)

    candidates = []

    for _, row in df.iterrows():

        candidates.append({
            "course_id": row.get("course_id", ""),
            "title": row.get("course_title", ""),
            "subject": row.get("subject", ""),
            "level": row.get("level", ""),
            "price": row.get("price", ""),
            "is_paid": row.get("is_paid", ""),
            "reviews": row.get("num_reviews", ""),
            "subscribers": row.get("num_subscribers", ""),
            "url": row.get("url", ""),
            "similarity": round(
                float(row.get("similarity", 0)) * 100,
                2
            )
        })

    return candidates


def build_dataset_context(candidates):
    """
    Convert dataset candidates into a compact prompt section.
    """

    if not candidates:
        return "No dataset courses were found."

    context = ""

    for index, course in enumerate(candidates, start=1):

        context += f"""
CANDIDATE {index}
Course ID: {course["course_id"]}
Course Title: {course["title"]}
Subject: {course["subject"]}
Level: {course["level"]}
Price: {course["price"]}
Paid: {course["is_paid"]}
Reviews: {course["reviews"]}
Subscribers: {course["subscribers"]}
URL: {course["url"]}
Dataset Relevance: {course["similarity"]}%
"""

    return context.strip()


def generate_recommendations(
    prompt,
    profile=None,
    feedback="",
    exclude_names=None
):
    """
    Retrieve relevant courses from the Kaggle dataset
    and ask Ollama to generate personalized recommendations.
    """

    # If a profile is provided, retrieve actual dataset courses
    candidates = []

    if profile:
        candidates = get_dataset_candidates(
            profile,
            feedback=feedback,
            exclude_names=exclude_names,
            top_k=15
        )

    dataset_context = build_dataset_context(candidates)

    # Add dataset information to the original prompt
    if candidates:

        final_prompt = f"""
{prompt}

DATASET INSTRUCTION
===================

Use ONLY courses from the Kaggle course dataset provided below.

Do NOT invent course names.

Use the EXACT course title from the dataset.

Select the courses that best match the user's:
- interests
- skill level
- goal
- preferred category
- preferences
- feedback

Rank the selected courses by suitability.

KAGGLE DATASET COURSES
======================

{dataset_context}

IMPORTANT:
- Do not create fictional courses.
- Do not modify course titles.
- Use only the candidate courses listed above.
- Generate exactly the requested number of recommendations.
- Keep the requested output format.
"""

    else:
        final_prompt = prompt

    payload = {
        "model": MODEL_NAME,
        "prompt": final_prompt,
        "stream": False,
        "options": {
            "temperature": 0.7
        }
    }

    try:

        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=180
        )

        response.raise_for_status()

        data = response.json()

        result = data.get(
            "response",
            ""
        ).strip()

        if not result:

            return {
                "success": False,
                "error": "Ollama returned an empty response.",
                "recommendations": [],
                "raw_response": ""
            }

        recommendations = parse_recommendations(
            result
        )

        return {
            "success": True,
            "recommendations": recommendations,
            "raw_response": result,
            "dataset_candidates": candidates
        }

    except requests.exceptions.ConnectionError:

        return {
            "success": False,
            "error": (
                "Could not connect to Ollama. "
                "Make sure Ollama is running."
            ),
            "recommendations": [],
            "raw_response": ""
        }

    except requests.exceptions.Timeout:

        return {
            "success": False,
            "error": "Ollama request timed out.",
            "recommendations": [],
            "raw_response": ""
        }

    except Exception as error:

        return {
            "success": False,
            "error": str(error),
            "recommendations": [],
            "raw_response": ""
        }


def parse_recommendations(text):
    """
    Convert Ollama response into structured recommendations.
    """

    recommendations = []

    pattern = re.compile(
        r"""
        (?:^|\n)
        \s*
        (\d+)[\.\)]
        \s*
        (.+?)
        \n
        Description:
        \s*
        (.+?)
        \n
        Score:
        \s*
        (\d+)
        \s*%?
        \s*
        \n
        Reason:
        \s*
        (.+?)
        (?=
            \n\s*\d+[\.\)]
            |
            $
        )
        """,
        re.IGNORECASE |
        re.DOTALL |
        re.VERBOSE
    )

    matches = pattern.findall(text)

    for match in matches:

        number = match[0].strip()
        name = match[1].strip()
        description = match[2].strip()
        score = match[3].strip()
        reason = match[4].strip()

        try:
            score_value = int(score)
        except ValueError:
            score_value = 0

        recommendations.append({
            "number": int(number),
            "name": name,
            "description": description,
            "score": score_value,
            "reason": reason
        })

    # Fallback parser
    if not recommendations:
        recommendations = parse_fallback(text)

    return recommendations


def parse_fallback(text):
    """
    Simple fallback parser for LLM responses.
    """

    recommendations = []

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    current = None

    for line in lines:

        if re.match(
            r"^\d+[\.\)]",
            line
        ):

            if current:
                recommendations.append(
                    current
                )

            name = re.sub(
                r"^\d+[\.\)]\s*",
                "",
                line
            )

            current = {
                "number": len(
                    recommendations
                ) + 1,
                "name": name,
                "description": "",
                "score": 0,
                "reason": ""
            }

        elif current:

            if line.lower().startswith(
                "description:"
            ):

                current["description"] = (
                    line.split(
                        ":",
                        1
                    )[1].strip()
                )

            elif line.lower().startswith(
                "score:"
            ):

                score_text = line.split(
                    ":",
                    1
                )[1]

                numbers = re.findall(
                    r"\d+",
                    score_text
                )

                if numbers:
                    current["score"] = int(
                        numbers[0]
                    )

            elif line.lower().startswith(
                "reason:"
            ):

                current["reason"] = (
                    line.split(
                        ":",
                        1
                    )[1].strip()
                )

    if current:
        recommendations.append(
            current
        )

    return recommendations