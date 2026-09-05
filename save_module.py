import os
import pandas as pd
from datetime import datetime


DATA_FOLDER = "data"

FILE_PATH = os.path.join(
    DATA_FOLDER,
    "saved_recommendations.csv"
)


def save_recommendations(
    profile,
    recommendations,
    feedback="",
    intent=""
):
    """
    Save recommendation results into CSV.
    """

    os.makedirs(
        DATA_FOLDER,
        exist_ok=True
    )

    rows = []

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    for item in recommendations:

        rows.append({

            "Timestamp": timestamp,

            "Name": profile.get(
                "Name",
                ""
            ),

            "Age": profile.get(
                "Age",
                ""
            ),

            "Background": profile.get(
                "Background",
                ""
            ),

            "Interests": profile.get(
                "Interests",
                ""
            ),

            "Skill Level": profile.get(
                "Skill Level",
                ""
            ),

            "Preferred Category": profile.get(
                "Preferred Category",
                ""
            ),

            "Goal": profile.get(
                "Goal",
                ""
            ),

            "Preferences": profile.get(
                "Preferences",
                ""
            ),

            "Rank": item.get(
                "rank",
                ""
            ),

            "Recommendation": item.get(
                "name",
                ""
            ),

            "Score": item.get(
                "score",
                ""
            ),

            "Reason": item.get(
                "reason",
                ""
            ),

            "Feedback": feedback,

            "Intent": intent

        })

    new_data = pd.DataFrame(rows)

    if os.path.exists(FILE_PATH):

        old_data = pd.read_csv(
            FILE_PATH
        )

        final_data = pd.concat(
            [
                old_data,
                new_data
            ],
            ignore_index=True
        )

    else:

        final_data = new_data

    final_data.to_csv(
        FILE_PATH,
        index=False
    )

    return FILE_PATH