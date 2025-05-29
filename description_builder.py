# description_builder.py

import openai

# Make sure you've set openai.api_key = "YOUR_KEY" before usage

def generate_description(bundle_name: str) -> str:
    """
    For a simple example, we'll do minimal prompt to GPT.
    In reality, you can pass brand, flavor notes, etc.
    """
    prompt = (
        f"Write a short HTML description for the liquor bundle: '{bundle_name}'. "
        "Use bold headings and highlight the unique qualities of each bottle. "
        "Include a note about being over 21 to purchase."
    )

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
        temperature=0.7,
    )

    return response.choices[0].message.content.strip()
