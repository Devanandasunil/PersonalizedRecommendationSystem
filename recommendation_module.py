import requests
import re


OLLAMA_URL = "http://localhost:11434/api/generate"

MODEL_NAME = "llama3.2:3b"


def generate_recommendations(prompt):
    """
    Send the generated prompt to Ollama
    and receive personalized recommendations.
    """

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.7
        }
    }

    try:

        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=120
        )

        response.raise_for_status()

        data = response.json()

        result = data.get("response", "")

        if not result:
            return {
                "success": False,
                "error": "Ollama returned an empty response.",
                "raw_response": ""
            }

        return {
            "success": True,
            "recommendations": parse_recommendations(result),
            "raw_response": result
        }

    except requests.exceptions.ConnectionError:

        return {
            "success": False,
            "error": (
                "Could not connect to Ollama. "
                "Make sure Ollama is running."
            ),
            "raw_response": ""
        }

    except requests.exceptions.Timeout:

        return {
            "success": False,
            "error": "Ollama request timed out.",
            "raw_response": ""
        }

    except Exception as error:

        return {
            "success": False,
            "error": str(error),
            "raw_response": ""
        }


def parse_recommendations(text):
    """
    Convert Ollama's response into structured recommendations.
    """

    recommendations = []

    pattern = re.compile(
        r"(?:^|\n)\s*(\d+)[\.\)]\s*(.+?)\n"
        r"(?:Description:\s*(.+?))?\n?"
        r"(?:Score:\s*(\d+))?\%?\s*\n?"
        r"(?:Reason:\s*(.+?))?"
        r"(?=\n\s*\d+[\.\)]|\Z)",
        re.IGNORECASE | re.DOTALL
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

    # Fallback if the model formatting is slightly different
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

        if re.match(r"^\d+[\.\)]", line):

            if current:
                recommendations.append(current)

            name = re.sub(
                r"^\d+[\.\)]\s*",
                "",
                line
            )

            current = {
                "number": len(recommendations) + 1,
                "name": name,
                "description": "",
                "score": 0,
                "reason": ""
            }

        elif current:

            if line.lower().startswith("description:"):

                current["description"] = line.split(
                    ":",
                    1
                )[1].strip()

            elif line.lower().startswith("score:"):

                score_text = line.split(
                    ":",
                    1
                )[1]

                numbers = re.findall(
                    r"\d+",
                    score_text
                )

                if numbers:
                    current["score"] = int(numbers[0])

            elif line.lower().startswith("reason:"):

                current["reason"] = line.split(
                    ":",
                    1
                )[1].strip()

    if current:
        recommendations.append(current)

    return recommendations