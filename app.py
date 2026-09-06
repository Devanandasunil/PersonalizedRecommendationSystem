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


# ============================================================
# STORE CURRENT SESSION DATA
# ============================================================

current_profile = None
current_recommendations = []


# ============================================================
# HOME PAGE
# ============================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# ============================================================
# PROFILE + INITIAL RECOMMENDATIONS
# ============================================================

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
        analyze_preferences(
            profile
        )
    )


    # --------------------------------
    # STEP 4: PROMPT GENERATION
    # --------------------------------

    prompt = generate_prompt(
        profile,
        preference_analysis
    )


    # --------------------------------
    # STEP 5: KAGGLE DATASET + OLLAMA
    # --------------------------------

    ai_result = generate_recommendations(
        prompt,
        profile=profile
    )


    # --------------------------------
    # CHECK AI RESULT
    # --------------------------------

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
    # STEP 6: RANKING MODULE
    # --------------------------------

    recommendations = (
        rank_recommendations(
            ai_result["recommendations"]
        )
    )


    # --------------------------------
    # STEP 7: EXPLANATION MODULE
    # --------------------------------

    recommendations = (
        generate_explanations(
            recommendations,
            profile
        )
    )


    # Store recommendations
    current_recommendations = (
        recommendations
    )


    # --------------------------------
    # DISPLAY RESULTS
    # --------------------------------

    return render_template(
        "index.html",

        profile=profile,

        profile_submitted=True,

        preference_analysis=preference_analysis,

        prompt=prompt,

        recommendations=recommendations,

        recommendation_generated=True
    )


# ============================================================
# FEEDBACK + REFINEMENT
# ============================================================

@app.route(
    "/feedback",
    methods=["POST"]
)
def feedback():

    global current_profile
    global current_recommendations


    # --------------------------------
    # CHECK PROFILE
    # --------------------------------

    if current_profile is None:

        return render_template(
            "index.html",

            error=(
                "Please create a profile first."
            )
        )


    # --------------------------------
    # STEP 8: FEEDBACK MODULE
    # --------------------------------

    feedback = collect_feedback(
        request.form.get(
            "feedback",
            ""
        )
    )


    # --------------------------------
    # STEP 9: INTENT DETECTION
    # --------------------------------

    intent = detect_intent(
        feedback
    )


    # --------------------------------
    # STEP 10: REFINEMENT INSTRUCTION
    # --------------------------------

    instruction = (
        build_refinement_instruction(
            feedback,
            intent
        )
    )


    # --------------------------------
    # PREVIOUS RECOMMENDATIONS
    # --------------------------------

    previous = ""

    for item in current_recommendations:

        previous += f"""
{item.get("rank", "")}. {item.get("name", "")}
Score: {item.get("score", "")}
Reason: {item.get("reason", "")}
"""


    # --------------------------------
    # REFINEMENT PROMPT
    # --------------------------------

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


USER FEEDBACK
=============

{feedback}


DETECTED INTENT
===============

{intent}


REFINEMENT INSTRUCTION
======================

{instruction}


IMPORTANT REFINEMENT RULES
==========================

Use the user feedback as a NEW preference.

Do not simply rephrase the previous recommendations.

Replace previous items with genuinely different
recommendations whenever they do not satisfy the
updated preferences.

The refined recommendations must be specifically
aligned with the detected intent and feedback.

Use the Kaggle dataset courses provided by the
recommendation system.

Do not invent course names.

Generate exactly
{current_profile["Number of Items"]}
refined personalized recommendations.


OUTPUT FORMAT
=============

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
    # STEP 11: KAGGLE DATASET +
    #          OLLAMA REFINEMENT
    # --------------------------------

    # Names of previous recommendations
    # are excluded from the new dataset search.

    previous_names = [
        item.get("name", "")
        for item in current_recommendations
    ]


    ai_result = generate_recommendations(
        refinement_prompt,

        profile=current_profile,

        feedback=feedback,

        exclude_names=previous_names
    )


    # --------------------------------
    # CHECK REFINEMENT RESULT
    # --------------------------------

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
    # STEP 12: RANK REFINED RESULTS
    # --------------------------------

    refined = rank_recommendations(
        ai_result["recommendations"]
    )


    # --------------------------------
    # STEP 13: EXPLANATIONS
    # --------------------------------

    refined = generate_explanations(
        refined,
        current_profile
    )


    # Store refined recommendations
    current_recommendations = refined


    # --------------------------------
    # STEP 14: SAVE MODULE
    # --------------------------------

    save_recommendations(
        current_profile,

        refined,

        feedback,

        intent
    )


    # --------------------------------
    # DISPLAY REFINED RESULTS
    # --------------------------------

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


# ============================================================
# RUN FLASK APPLICATION
# ============================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )