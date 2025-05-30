import openai, os, re, textwrap, logging
openai.api_key = os.getenv("OPENAI_API_KEY")

_NUM_RE = re.compile(r"\b(\d{1,3})(?:\s*/\s*100)?\b")   # 0-100 or “85/100”

def score_pair(b1: dict, b2: dict) -> float:
    """
    Ask GPT for a 0-100 synergy score and return it as float.
    """
    prompt = textwrap.dedent(f"""
        You are a world-class spirits sommelier.
        Score the following two bottles as a gift bundle on a 0-100 scale.
        Respond with ONLY the number, no words or symbols.

        Bottle A: {b1['name']} – ${b1['price']:.2f}
        Bottle B: {b2['name']} – ${b2['price']:.2f}
    """).strip()

    try:
        resp = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            temperature=0.1,
            max_tokens=3,              # enough for “85”
            messages=[
                {"role": "system", "content": "Reply with just a number."},
                {"role": "user", "content": prompt}
            ]
        )
        text = resp.choices[0].message.content.strip()
        m = _NUM_RE.search(text)
        if m:
            val = int(m.group(1))
            # clamp to 0-100 just in case
            return max(0, min(val, 100))
        logging.warning(f"[AI-score] Could not parse → “{text}”")
    except Exception as e:
        logging.error(f"[AI-score] {e}")

    return 50.0   # neutral fallback
