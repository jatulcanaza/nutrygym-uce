import requests
from app.core.config import settings

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

def generate_meal_plan(prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {settings.GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": settings.GROQ_MODEL,
        "messages": [
            {"role": "system", "content": "You are a professional nutritionist."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    response = requests.post(GROQ_URL, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]
