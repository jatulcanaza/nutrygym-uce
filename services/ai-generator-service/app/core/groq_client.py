import json
import re
import requests
from app.core.config import settings

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

def _extract_json(text: str) -> dict:
    # intenta encontrar el primer objeto JSON {...}
    m = re.search(r"\{[\s\S]*\}", text)
    if not m:
        raise ValueError("No JSON object found in model output")
    return json.loads(m.group(0))

def generate_meal_plan(prompt: str) -> dict:
    headers = {
        "Authorization": f"Bearer {settings.GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": settings.GROQ_MODEL,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a professional nutritionist. "
                    "Return ONLY valid JSON. Do not use markdown or code fences."
                )
            },
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.2,
        "max_tokens": 2500,
    }

    response = requests.post(GROQ_URL, headers=headers, json=payload, timeout=30)
    response.raise_for_status()

    content = response.json()["choices"][0]["message"]["content"]
    # Asegurar dict
    if isinstance(content, dict):
        return content

    return _extract_json(content)
