# chatbot.py

import os
import requests
import json
from dotenv import load_dotenv

import os
os.environ['GIT_PYTHON_GIT_EXECUTABLE'] = r'C:\Program Files\Git\cmd\git.exe'
load_dotenv()  # Load environment variables from .env

API_KEY = os.getenv("GROQ_API_KEY")


def chat_with_groq(prompt):
    try:
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json={
                "model": "meta-llama/llama-4-scout-17b-16e-instruct",  # or "llama3-70b-8192"
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            }
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]

    except requests.exceptions.RequestException as e:
        return f"Error connecting to Groq API: {str(e)}"
    except json.JSONDecodeError:
        return "Error parsing response"
