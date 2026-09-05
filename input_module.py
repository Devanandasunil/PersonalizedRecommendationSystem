def collect_user_input(form_data):
    """
    Collect user information from the submitted form.
    """

    profile = {
        "name": form_data.get("name", "").strip(),
        "age": form_data.get("age", "").strip(),
        "background": form_data.get("background", "").strip(),
        "interests": form_data.get("interests", "").strip(),
        "skill_level": form_data.get("skill", "").strip(),
        "preferred_category": form_data.get("category", "").strip(),
        "goal": form_data.get("goal", "").strip(),
        "preferences": form_data.get("preferences", "").strip(),
        "number_of_items": form_data.get("number", "5").strip()
    }

    return profile