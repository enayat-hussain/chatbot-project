import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
API_URL = os.getenv("GROQ_API_URL")

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def get_payload(prompt, model="meta-llama/llama-4-scout-17b-16e-instruct"):
    return {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
