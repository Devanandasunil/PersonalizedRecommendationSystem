from flask import Flask, render_template, request

from input_module import collect_user_input
from profile_module import create_profile
from preference_module import analyze_preferences
from prompt_module import generate_prompt
from recommendation_module import generate_recommendations
from ranking_module import rank_recommendations
from explanation_module import generate_explanations
from feedback_module import (
    collect_feedback,
    build_refinement_instruction
)
from intent_module import detect_intent
from save_module import save_recommendations


app = Flask(__name__)


# Store current session data
current_profile = None
current_recommendations = []


@app.route("/")
def home():

    return render_template(
        "index.html"
    )


@app.route(
    "/profile",
    methods=["POST"]
)
def profile():

    global current_profile
    global current_recommendations

    # --------------------------------
    # STEP 1: INPUT MODULE
    # --------------------------------

    user_data = collect_user_input(
        request.form
    )


    # --------------------------------
    # STEP 2: PROFILE MODULE
    # --------------------------------

    profile = create_profile(
        user_data
    )

    current_profile = profile


    # --------------------------------
    # STEP 3: PREFERENCE ANALYSIS
    # --------------------------------

    preference_analysis = (
        analyze_preferences(profile)
    )


    # --------------------------------
    # STEP 4: PROMPT GENERATION
    # --------------------------------

    prompt = generate_prompt(
        profile,
        preference_analysis
    )


    # --------------------------------
    # STEP 5: OLLAMA
    # --------------------------------

    ai_result = generate_recommendations(
        prompt
    )


    if not ai_result["success"]:

        return render_template(
            "index.html",
            profile=profile,
            profile_submitted=True,
            preference_analysis=preference_analysis,
            prompt=prompt,
            error=ai_result["error"]
        )


    # --------------------------------
    # STEP 6: RANKING
    # --------------------------------

    recommendations = (
        rank_recommendations(
            ai_result["recommendations"]
        )
    )


    # --------------------------------
    # STEP 7: EXPLANATIONS
    # --------------------------------

    recommendations = (
        generate_explanations(
            recommendations,
            profile
        )
    )


    current_recommendations = recommendations


    return render_template(
        "index.html",

        profile=profile,

        profile_submitted=True,

        preference_analysis=preference_analysis,

        prompt=prompt,

        recommendations=recommendations,

        recommendation_generated=True
    )


@app.route(
    "/feedback",
    methods=["POST"]
)
def feedback():

    global current_profile
    global current_recommendations


    if current_profile is None:

        return render_template(
            "index.html",
            error="Please create a profile first."
        )


    # --------------------------------
    # FEEDBACK
    # --------------------------------

    feedback = collect_feedback(
        request.form.get(
            "feedback",
            ""
        )
    )


    # --------------------------------
    # INTENT DETECTION
    # --------------------------------

    intent = detect_intent(
        feedback
    )


    # --------------------------------
    # REFINEMENT INSTRUCTION
    # --------------------------------

    instruction = (
        build_refinement_instruction(
            feedback,
            intent
        )
    )


    # --------------------------------
    # CREATE REFINEMENT PROMPT
    # --------------------------------

    previous = ""

    for item in current_recommendations:

        previous += f"""
{item.get("rank", "")}. {item.get("name", "")}
Score: {item.get("score", "")}
Reason: {item.get("reason", "")}
"""


    refinement_prompt = f"""
You are a personalized recommendation assistant.

USER PROFILE
============

Name: {current_profile["Name"]}
Age: {current_profile["Age"]}
Background: {current_profile["Background"]}
Interests: {current_profile["Interests"]}
Skill Level: {current_profile["Skill Level"]}
Preferred Category: {current_profile["Preferred Category"]}
Goal: {current_profile["Goal"]}
Preferences: {current_profile["Preferences"]}

PREVIOUS RECOMMENDATIONS
========================

{previous}

{instruction}

Use the user feedback as a NEW preference, not as a request to
rephrase the previous list. Replace previous items with genuinely
different recommendations whenever they do not satisfy the updated
preferences. The refined list must be specifically aligned with the
detected intent and feedback.

Generate exactly
{current_profile["Number of Items"]}
refined personalized recommendations.

Use exactly this format:

1. Recommendation Name
Description: Short description
Score: 95
Reason: Explanation

2. Recommendation Name
Description: Short description
Score: 90
Reason: Explanation

Do not add unnecessary text.
"""


    # --------------------------------
    # OLLAMA REFINEMENT
    # --------------------------------

    ai_result = generate_recommendations(
        refinement_prompt
    )


    if not ai_result["success"]:

        return render_template(
            "index.html",
            profile=current_profile,
            recommendations=current_recommendations,
            feedback=feedback,
            intent=intent,
            error=ai_result["error"]
        )


    # --------------------------------
    # RANK REFINED RESULTS
    # --------------------------------

    refined = rank_recommendations(
        ai_result["recommendations"]
    )


    refined = generate_explanations(
        refined,
        current_profile
    )


    current_recommendations = refined


    # --------------------------------
    # SAVE
    # --------------------------------

    save_recommendations(
        current_profile,
        refined,
        feedback,
        intent
    )


    return render_template(
        "index.html",

        profile=current_profile,

        recommendations=refined,

        recommendation_generated=True,

        feedback=feedback,

        intent=intent,

        refined_recommendations=True,

        saved=True
    )


if __name__ == "__main__":

    app.run(
        debug=True
    )