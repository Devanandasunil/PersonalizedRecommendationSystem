def generate_prompt(profile, preference_analysis):
    """
    Generate the prompt that will be sent to Ollama.
    """

    number_of_items = profile["Number of Items"]

    top_preferences = preference_analysis["top_preferences"]

    preference_text = "\n".join(
        [
            f"- {item['category']}: {item['score']}%"
            for item in top_preferences
        ]
    )

    prompt = f"""
You are an intelligent personalized recommendation assistant.

Analyze the following user profile and generate personalized recommendations.

USER PROFILE
------------

Name: {profile["Name"]}
Age: {profile["Age"]}
Background: {profile["Background"]}
Interests: {profile["Interests"]}
Skill Level: {profile["Skill Level"]}
Preferred Category: {profile["Preferred Category"]}
Goal: {profile["Goal"]}
Preferences: {profile["Preferences"]}

NUMBER OF RECOMMENDATIONS
-------------------------
{number_of_items}

PREFERENCE ANALYSIS
-------------------
{preference_text}

TASK
----

Generate exactly {number_of_items} personalized recommendations.

For every recommendation provide:

1. Recommendation name
2. Short description
3. Suitability score from 0 to 100
4. Reason why it matches the user

Consider:

- User interests
- Skill level
- Preferred category
- Career or learning goal
- Personal preferences
- Background

Return the answer in this format:

1. Recommendation Name
Description: ...
Score: ...
Reason: ...

2. Recommendation Name
Description: ...
Score: ...
Reason: ...

Do not include unnecessary introductory text.
"""

    return prompt.strip()