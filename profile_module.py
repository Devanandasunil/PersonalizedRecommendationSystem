def create_profile(user_data):
    """
    Create a structured user profile.
    """

    profile = {
        "Name": user_data["name"],
        "Age": user_data["age"],
        "Background": user_data["background"],
        "Interests": user_data["interests"],
        "Skill Level": user_data["skill_level"],
        "Preferred Category": user_data["preferred_category"],
        "Goal": user_data["goal"],
        "Preferences": user_data["preferences"],
        "Number of Items": user_data["number_of_items"]
    }

    return profile