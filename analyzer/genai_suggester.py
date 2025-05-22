import os
import requests
from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def suggest_stronger_password(password: str) -> str:
    prompt = f"""
Improve this password while keeping it memorable. Avoid names or dates. 
Password: "{password}"
Strong Alternatives:"""

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": "You are a helpful AI security assistant that suggests strong but memorable passwords."},
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)

    if response.status_code == 200:
        suggestion = response.json()['choices'][0]['message']['content']
        return suggestion.strip()
    else:
        return "⚠️ Failed to get suggestions. Check API key or network."
