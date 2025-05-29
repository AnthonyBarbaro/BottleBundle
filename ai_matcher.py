# ai_matcher.py
import openai, os, re

openai.api_key = os.getenv("OPENAI_API_KEY")

def score_pair(b1: dict, b2: dict) -> float:
    """
    Returns a float synergy score 0-100 from GPT.
    """
    prompt = (
        "You are a spirits expert. Rate the following two bottles as a gift bundle. "
        "Give ONE number 0-100 (higher = better pairing). "
        f"Bottle A: {b1['name']} – ${b1['price']}\n"
        f"Bottle B: {b2['name']} – ${b2['price']}\n"
        "Consider brand prestige, style compatibility, and perceived customer value."
    )

    resp = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=4
    )

    # Extract the first number you see
    text = resp.choices[0].message.content
    try:
        return float(re.search(r'\d+', text).group())
    except Exception:
        return 50.0  # neutral fallback
